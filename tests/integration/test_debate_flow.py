import unittest
from unittest.mock import Mock, patch
import json
from datetime import datetime

from src.debate_simulator.domain.characters.base import Character, CharacterStats
from src.debate_simulator.domain.debate.models import DebateSettings, DebateStatus
from src.debate_simulator.application.character_service import CharacterService
from src.debate_simulator.application.debate_service import DebateService
from src.debate_simulator.infrastructure.ai_client import MockAIClient
from src.debate_simulator.infrastructure.config import AppConfig, ConfigManager


class TestDebateFlowIntegration(unittest.TestCase):
    """Integration tests for the complete debate flow."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create mock AI client with predictable responses
        self.ai_client = MockAIClient(
            fixed_response="Mock debate response",
            fixed_judge_response='{"Test Character 1": {"anger": 2, "patience": -1, "uniqueness": 1}, "Test Character 2": {"anger": -1, "patience": 2, "uniqueness": 0}}'
        )
        
        # Create services
        self.character_service = CharacterService()
        self.debate_service = DebateService(self.ai_client, self.character_service)
        
        # Test data
        self.test_topic = "Test political debate topic"
        self.test_character_types = ["democratic_commentator", "republican_commentator"]
        self.test_settings = DebateSettings(
            total_rounds=2,
            response_delay=0.0,  # No delay for tests
            competitive_mode=True
        )
    
    def test_complete_debate_flow(self):
        """Test the complete debate flow from creation to completion."""
        # Step 1: Create debate session
        session_result = self.debate_service.create_debate_session(
            topic=self.test_topic,
            selected_character_types=self.test_character_types,
            settings=self.test_settings
        )
        
        self.assertTrue(session_result["success"])
        self.assertIsNotNone(session_result["session"])
        self.assertEqual(len(session_result["participants"]), 2)
        
        session = session_result["session"]
        participants = session_result["participants"]
        
        # Verify session creation
        self.assertEqual(session.topic, self.test_topic)
        self.assertEqual(session.status, DebateStatus.NOT_STARTED)
        self.assertTrue(session.settings.competitive_mode)
        
        # Step 2: Start debate
        start_result = self.debate_service.start_debate(participants)
        self.assertTrue(start_result["success"])
        
        # Step 3: Verify debate completion
        # The mock AI client should have been called multiple times
        expected_calls = self.test_settings.total_rounds * len(participants)
        self.assertEqual(self.ai_client.call_count, expected_calls)
        
        # In competitive mode, judge should have been called
        if self.test_settings.competitive_mode:
            self.assertEqual(self.ai_client.judge_call_count, self.test_settings.total_rounds)
        
        # Step 4: Check final session state
        session_status = self.debate_service.get_session_status()
        self.assertIn(session_status["status"], ["completed", "stopped"])
        self.assertEqual(session_status["topic"], self.test_topic)
    
    def test_character_creation_and_assignment(self):
        """Test character creation and position assignment."""
        # Create characters
        characters = self.character_service.create_characters_from_selection(
            ["democratic_commentator", "republican_commentator", "marxist_leninist"]
        )
        
        self.assertEqual(len(characters), 3)
        
        # Verify character properties
        character_names = [char.name for char in characters]
        self.assertIn("Market Liberal Democrat", character_names)
        self.assertIn("MAGA Nationalist", character_names)
        self.assertIn("Marxist-Leninist", character_names)
        
        # Test position assignment
        self.character_service.assign_positions(characters)
        
        # Verify positions are assigned
        positions = [char.position for char in characters]
        self.assertIn("left", positions)
        self.assertIn("right", positions)
        
        # Verify all characters have positions
        for char in characters:
            self.assertIn(char.position, ["left", "right"])
    
    def test_competitive_mode_stats_tracking(self):
        """Test that competitive mode properly tracks and updates character stats."""
        # Create debate with competitive mode
        session_result = self.debate_service.create_debate_session(
            topic=self.test_topic,
            selected_character_types=self.test_character_types,
            settings=DebateSettings(total_rounds=1, competitive_mode=True, response_delay=0.0)
        )
        
        participants = session_result["participants"]
        initial_stats = {char.name: char.stats.to_dict() for char in participants}
        
        # Start debate
        self.debate_service.start_debate(participants)
        
        # Check that stats have been updated
        final_stats = {char.name: char.stats.to_dict() for char in participants}
        
        # At least one character should have different stats
        stats_changed = False
        for char_name in initial_stats:
            if initial_stats[char_name] != final_stats[char_name]:
                stats_changed = True
                break
        
        self.assertTrue(stats_changed, "Character stats should have changed in competitive mode")
    
    def test_session_export_and_import(self):
        """Test session export and import functionality."""
        # Create and run a short debate
        session_result = self.debate_service.create_debate_session(
            topic=self.test_topic,
            selected_character_types=self.test_character_types,
            settings=DebateSettings(total_rounds=1, response_delay=0.0)
        )
        
        participants = session_result["participants"]
        self.debate_service.start_debate(participants)
        
        # Export session
        exported_data = self.debate_service.export_session()
        self.assertIsNotNone(exported_data)
        self.assertIn("topic", exported_data)
        self.assertIn("conversation", exported_data)
        self.assertIn("exported_at", exported_data)
        
        # Create new service and import session
        new_service = DebateService(self.ai_client)
        import_result = new_service.import_session(exported_data)
        
        self.assertTrue(import_result["success"])
        self.assertEqual(import_result["session"].topic, self.test_topic)
    
    def test_debate_with_random_characters(self):
        """Test debate flow with random characters."""
        character_types = ["random_american", "random_redditor", "democratic_commentator"]
        
        session_result = self.debate_service.create_debate_session(
            topic=self.test_topic,
            selected_character_types=character_types,
            settings=DebateSettings(total_rounds=1, response_delay=0.0)
        )
        
        self.assertTrue(session_result["success"])
        participants = session_result["participants"]
        self.assertEqual(len(participants), 3)
        
        # Verify random characters were created properly
        random_american = None
        random_redditor = None
        
        for char in participants:
            if "from" in char.name and "u/" not in char.name:
                random_american = char
            elif "u/" in char.name:
                random_redditor = char
        
        self.assertIsNotNone(random_american)
        self.assertIsNotNone(random_redditor)
        
        # Verify metadata
        self.assertIn("gender", random_american.metadata)
        self.assertIn("age", random_american.metadata)
        self.assertIn("subreddit", random_redditor.metadata)
        self.assertIn("username", random_redditor.metadata)
    
    def test_error_handling_in_debate_flow(self):
        """Test error handling throughout the debate flow."""
        # Test with invalid topic
        result = self.debate_service.create_debate_session(
            topic="",  # Invalid topic
            selected_character_types=self.test_character_types,
            settings=self.test_settings
        )
        
        self.assertFalse(result["success"])
        self.assertIn("error", result)
        
        # Test with invalid character types
        result = self.debate_service.create_debate_session(
            topic=self.test_topic,
            selected_character_types=["nonexistent_character"],
            settings=self.test_settings
        )
        
        self.assertFalse(result["success"])
        
        # Test starting debate without session
        start_result = self.debate_service.start_debate([])
        self.assertFalse(start_result["success"])
        self.assertIn("No active debate session", start_result["error"])
    
    def test_debate_statistics_and_results(self):
        """Test debate statistics collection and competitive results."""
        # Run a competitive debate
        session_result = self.debate_service.create_debate_session(
            topic=self.test_topic,
            selected_character_types=self.test_character_types,
            settings=DebateSettings(total_rounds=2, competitive_mode=True, response_delay=0.0)
        )
        
        participants = session_result["participants"]
        self.debate_service.start_debate(participants)
        
        # Get debate statistics
        stats = self.debate_service.get_debate_statistics()
        self.assertIn("total_sessions", stats)
        self.assertIn("character_stats", stats)
        self.assertTrue(stats["current_session_active"])
        
        # Get competitive results
        results = self.debate_service.get_competitive_results()
        self.assertIsNotNone(results)
        self.assertTrue(results["competitive_mode"])
        self.assertEqual(results["total_participants"], 2)
        self.assertIn("participants", results)
        
        # Verify results structure
        for participant_result in results["participants"]:
            self.assertIn("name", participant_result)
            self.assertIn("stats", participant_result)
            self.assertIn("performance", participant_result)
            self.assertIn("rating", participant_result)


class TestServiceIntegration(unittest.TestCase):
    """Test integration between different services."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.ai_client = MockAIClient()
        self.character_service = CharacterService()
        self.debate_service = DebateService(self.ai_client, self.character_service)
    
    def test_character_service_integration(self):
        """Test integration between debate service and character service."""
        # Test character creation through debate service
        available_types = self.character_service.get_available_character_types()
        self.assertGreater(len(available_types), 0)
        
        # Test validation
        validation = self.character_service.validate_character_selection(
            ["democratic_commentator", "republican_commentator"]
        )
        self.assertTrue(validation["valid"])
        
        # Test character statistics
        stats = self.character_service.get_character_statistics()
        self.assertIn("total_available", stats)
        self.assertGreater(stats["total_available"], 0)
    
    def test_ai_client_integration(self):
        """Test integration with AI client."""
        # Test connection
        from src.debate_simulator.infrastructure.ai_client import test_ai_connection
        
        connection_test = test_ai_connection(self.ai_client)
        self.assertTrue(connection_test)
        
        # Test response generation
        messages = [{"role": "user", "content": "Test message"}]
        response = self.ai_client.generate_response(messages)
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)
    
    def test_configuration_integration(self):
        """Test integration with configuration system."""
        # Test configuration with mock AI enabled
        config = AppConfig(
            enable_mock_ai=True,
            default_rounds=3,
            enable_competitive_mode=True
        )
        
        config_manager = ConfigManager(config, load_dotenv_file=False)
        
        # Test configuration retrieval
        ai_config = config_manager.get_ai_config()
        self.assertTrue(ai_config["use_mock"])
        
        streamlit_config = config_manager.get_streamlit_config()
        self.assertIn("page_title", streamlit_config)
        
        # Test configuration validation
        missing_config = config_manager.check_required_config()
        # With mock AI enabled, should not require API key
        self.assertEqual(len(missing_config), 0)


class TestErrorRecoveryIntegration(unittest.TestCase):
    """Test error recovery and resilience in integrated systems."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.ai_client = MockAIClient()
        self.character_service = CharacterService()
        self.debate_service = DebateService(self.ai_client, self.character_service)
    
    def test_ai_client_failure_recovery(self):
        """Test system behavior when AI client fails."""
        # Create a failing AI client
        failing_client = MockAIClient()
        failing_client.generate_response = Mock(side_effect=Exception("AI failure"))
        
        debate_service = DebateService(failing_client, self.character_service)
        
        # Attempt to create and run debate
        session_result = debate_service.create_debate_session(
            topic="Test topic",
            selected_character_types=["democratic_commentator"],
            settings=DebateSettings(total_rounds=1, response_delay=0.0)
        )
        
        # Session creation should succeed
        self.assertTrue(session_result["success"])
        
        # Starting debate should handle AI failures gracefully
        participants = session_result["participants"]
        start_result = debate_service.start_debate(participants)
        
        # Should not crash the entire system
        self.assertTrue(start_result["success"])
    
    def test_partial_character_creation_failure(self):
        """Test behavior when some characters fail to create."""
        # Mock character service to fail on certain types
        original_create = self.character_service.create_character
        
        def failing_create(char_type, **kwargs):
            if char_type == "failing_character":
                raise Exception("Character creation failed")
            return original_create(char_type, **kwargs)
        
        self.character_service.create_character = failing_create
        
        # Attempt to create characters with some failures
        characters = self.character_service.create_characters_from_selection(
            ["democratic_commentator", "failing_character", "republican_commentator"]
        )
        
        # Should create the successful characters and skip failures
        self.assertEqual(len(characters), 2)
        character_names = [char.name for char in characters]
        self.assertIn("Market Liberal Democrat", character_names)
        self.assertIn("MAGA Nationalist", character_names)
    
    def test_session_state_consistency(self):
        """Test that session state remains consistent across operations."""
        # Create session
        session_result = self.debate_service.create_debate_session(
            topic="Consistency test",
            selected_character_types=["democratic_commentator", "republican_commentator"],
            settings=DebateSettings(total_rounds=1, response_delay=0.0)
        )
        
        session = session_result["session"]
        initial_status = session.status
        
        # Start debate
        participants = session_result["participants"]
        self.debate_service.start_debate(participants)
        
        # Check session status is updated
        final_status = self.debate_service.get_session_status()
        self.assertNotEqual(initial_status.value, final_status["status"])
        
        # Export and verify consistency
        exported = self.debate_service.export_session()
        self.assertEqual(exported["topic"], "Consistency test")
        self.assertIn("conversation", exported)


if __name__ == "__main__":
    unittest.main()