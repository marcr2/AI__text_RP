import unittest
from unittest.mock import patch, MagicMock
import os
from src.political_debate.application.debate_service import DebateService
from src.political_debate.domain.models import DebateSession


class TestDebateWorkflow(unittest.TestCase):
    """Integration tests for the complete debate workflow"""
    
    def setUp(self):
        """Set up test environment with mocked OpenAI service"""
        self.mock_api_key = "test_api_key"
        
        # Mock OpenAI responses
        self.mock_debate_response = "This is a test debate response from the AI."
        self.mock_judge_response = '{"Test Participant": {"anger": 5, "patience": -2, "uniqueness": 3}}'
        
    @patch('src.political_debate.infrastructure.openai_client.OpenAI')
    def test_complete_debate_workflow(self, mock_openai):
        """Test complete debate workflow from creation to completion"""
        
        # Setup mock OpenAI client
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        
        # Mock debate response
        mock_response = MagicMock()
        mock_response.choices[0].message.content = self.mock_debate_response
        mock_client.chat.completions.create.return_value = mock_response
        
        # Create debate service
        debate_service = DebateService(self.mock_api_key)
        
        # Create debate session
        session = debate_service.create_debate_session(
            topic="Test Topic",
            selected_characters=["democrat", "republican"],
            rounds=2,
            competitive_mode=False
        )
        
        # Verify session creation
        self.assertIsInstance(session, DebateSession)
        self.assertEqual(session.topic, "Test Topic")
        self.assertEqual(len(session.participants), 2)
        self.assertEqual(session.rounds, 2)
        self.assertFalse(session.competitive_mode)
        
        # Conduct first round
        round1_messages = debate_service.conduct_round(session, 1)
        
        # Verify round 1 results
        self.assertEqual(len(round1_messages), 2)  # One message per participant
        self.assertEqual(len(session.messages), 2)
        
        for message in round1_messages:
            self.assertEqual(message.content, self.mock_debate_response)
            self.assertEqual(message.round_number, 1)
        
        # Conduct second round
        round2_messages = debate_service.conduct_round(session, 2)
        
        # Verify round 2 results
        self.assertEqual(len(round2_messages), 2)
        self.assertEqual(len(session.messages), 4)  # Total messages
        
        # Verify OpenAI was called correct number of times
        self.assertEqual(mock_client.chat.completions.create.call_count, 4)
    
    @patch('src.political_debate.infrastructure.openai_client.OpenAI')
    def test_competitive_mode_workflow(self, mock_openai):
        """Test debate workflow with competitive mode enabled"""
        
        # Setup mock OpenAI client
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        
        # Mock responses
        debate_response = MagicMock()
        debate_response.choices[0].message.content = self.mock_debate_response
        
        judge_response = MagicMock()
        judge_response.choices[0].message.content = self.mock_judge_response
        
        # Alternate between debate and judge responses
        mock_client.chat.completions.create.side_effect = [
            debate_response,  # Participant 1
            debate_response,  # Participant 2
            judge_response,   # Judge evaluation
        ]
        
        # Create debate service
        debate_service = DebateService(self.mock_api_key)
        
        # Create competitive session
        session = debate_service.create_debate_session(
            topic="Competitive Test Topic", 
            selected_characters=["democrat", "republican"],
            rounds=1,
            competitive_mode=True
        )
        
        # Store original stats
        original_stats = {
            p.name: (p.stats.anger, p.stats.patience, p.stats.uniqueness)
            for p in session.participants
        }
        
        # Conduct round with judging
        round_messages = debate_service.conduct_round(session, 1)
        
        # Verify round completed
        self.assertEqual(len(round_messages), 2)
        
        # Verify judge was called
        self.assertEqual(mock_client.chat.completions.create.call_count, 3)
        
        # Verify stats were potentially adjusted (mock returns adjustments for "Test Participant")
        # Since our participants don't have that exact name, stats should remain unchanged
        for participant in session.participants:
            original = original_stats[participant.name]
            current = (participant.stats.anger, participant.stats.patience, participant.stats.uniqueness)
            # Stats should be unchanged since mock response doesn't match participant names
            self.assertEqual(original, current)
    
    @patch('src.political_debate.infrastructure.openai_client.OpenAI')
    def test_error_handling_in_debate(self, mock_openai):
        """Test error handling when OpenAI API fails"""
        
        # Setup mock OpenAI client that raises exception
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        
        # Create debate service
        debate_service = DebateService(self.mock_api_key)
        
        # Create session
        session = debate_service.create_debate_session(
            topic="Error Test Topic",
            selected_characters=["democrat"],
            rounds=1,
            competitive_mode=False
        )
        
        # Conduct round (should handle errors gracefully)
        round_messages = debate_service.conduct_round(session, 1)
        
        # Should return empty list due to errors
        self.assertEqual(len(round_messages), 0)
        self.assertEqual(len(session.messages), 0)
    
    @patch('src.political_debate.infrastructure.openai_client.OpenAI')
    def test_session_serialization(self, mock_openai):
        """Test session serialization after debate completion"""
        
        # Setup mock OpenAI client
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.choices[0].message.content = self.mock_debate_response
        mock_client.chat.completions.create.return_value = mock_response
        
        # Create debate service
        debate_service = DebateService(self.mock_api_key)
        
        # Create and run session
        session = debate_service.create_debate_session(
            topic="Serialization Test",
            selected_characters=["democrat", "republican"],
            rounds=1,
            competitive_mode=True
        )
        
        debate_service.conduct_round(session, 1)
        
        # Test serialization
        session_dict = session.to_dict()
        
        # Verify serialized data
        self.assertEqual(session_dict["topic"], "Serialization Test")
        self.assertEqual(session_dict["rounds"], 1)
        self.assertTrue(session_dict["competitive_mode"])
        self.assertEqual(len(session_dict["conversation"]), 2)
        self.assertEqual(len(session_dict["participants"]), 2)
        
        # Verify message structure
        for conv_msg in session_dict["conversation"]:
            self.assertIn("speaker", conv_msg)
            self.assertIn("message", conv_msg)
            self.assertIn("round", conv_msg)
            self.assertIn("timestamp", conv_msg)
    
    def test_invalid_character_selection(self):
        """Test handling of invalid character selections"""
        
        with patch('src.political_debate.infrastructure.openai_client.OpenAI'):
            debate_service = DebateService(self.mock_api_key)
            
            # Should raise error for no valid participants
            with self.assertRaises(ValueError):
                debate_service.create_debate_session(
                    topic="Invalid Test",
                    selected_characters=["invalid_character"],
                    rounds=1,
                    competitive_mode=False
                )
    
    @patch('src.political_debate.infrastructure.openai_client.OpenAI')
    def test_random_character_generation(self, mock_openai):
        """Test integration with random character generation"""
        
        # Setup mock OpenAI client
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.choices[0].message.content = self.mock_debate_response
        mock_client.chat.completions.create.return_value = mock_response
        
        # Create debate service
        debate_service = DebateService(self.mock_api_key)
        
        # Create session with random characters
        with patch('random.choice') as mock_choice, \
             patch('random.randint', return_value=35):
            
            mock_choice.side_effect = [
                "male", "John", "millennial", "Chicago",  # For random_american
                "reddit_user", "politics"  # For random_redditor
            ]
            
            session = debate_service.create_debate_session(
                topic="Random Character Test",
                selected_characters=["random_american", "random_redditor"],
                rounds=1,
                competitive_mode=False
            )
        
        # Verify characters were created
        self.assertEqual(len(session.participants), 2)
        
        # Check character types
        char_types = [p.character_type.value for p in session.participants]
        self.assertIn("random_american", char_types)
        self.assertIn("random_redditor", char_types)
        
        # Conduct debate
        round_messages = debate_service.conduct_round(session, 1)
        self.assertEqual(len(round_messages), 2)


if __name__ == "__main__":
    unittest.main()