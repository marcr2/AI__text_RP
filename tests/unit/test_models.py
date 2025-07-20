import unittest
from datetime import datetime
from src.political_debate.domain.models import (
    CharacterStats, Participant, Message, DebateSession, 
    CharacterType, Position, JudgeAdjustment
)


class TestCharacterStats(unittest.TestCase):
    """Test the CharacterStats model"""
    
    def setUp(self):
        self.stats = CharacterStats(anger=50, patience=60, uniqueness=70)
    
    def test_initialization(self):
        """Test stats initialization with custom values"""
        self.assertEqual(self.stats.anger, 50)
        self.assertEqual(self.stats.patience, 60)
        self.assertEqual(self.stats.uniqueness, 70)
    
    def test_default_initialization(self):
        """Test stats initialization with default values"""
        default_stats = CharacterStats()
        self.assertEqual(default_stats.anger, 50)
        self.assertEqual(default_stats.patience, 50)
        self.assertEqual(default_stats.uniqueness, 50)
    
    def test_adjust_stats(self):
        """Test adjusting stats within bounds"""
        self.stats.adjust({"anger": 10, "patience": -20, "uniqueness": 5})
        
        self.assertEqual(self.stats.anger, 60)
        self.assertEqual(self.stats.patience, 40)
        self.assertEqual(self.stats.uniqueness, 75)
    
    def test_adjust_stats_bounds(self):
        """Test that stats stay within 0-100 bounds"""
        self.stats.adjust({"anger": 100, "patience": -100, "uniqueness": 50})
        
        self.assertEqual(self.stats.anger, 100)  # Max 100
        self.assertEqual(self.stats.patience, 0)  # Min 0
        self.assertEqual(self.stats.uniqueness, 100)  # Max 100
    
    def test_total_score(self):
        """Test total score calculation"""
        self.assertEqual(self.stats.total_score, 180)  # 50 + 60 + 70
    
    def test_performance_rating(self):
        """Test performance rating calculation"""
        # Test EXCELLENT (240+)
        excellent_stats = CharacterStats(80, 80, 80)  # 240 total
        self.assertEqual(excellent_stats.performance_rating, "🌟 EXCELLENT")
        
        # Test GOOD (180-239)
        good_stats = CharacterStats(60, 60, 60)  # 180 total
        self.assertEqual(good_stats.performance_rating, "👍 GOOD")
        
        # Test AVERAGE (120-179)
        average_stats = CharacterStats(40, 40, 40)  # 120 total
        self.assertEqual(average_stats.performance_rating, "😐 AVERAGE")
        
        # Test POOR (<120)
        poor_stats = CharacterStats(20, 20, 20)  # 60 total
        self.assertEqual(poor_stats.performance_rating, "😞 POOR")


class TestParticipant(unittest.TestCase):
    """Test the Participant model"""
    
    def setUp(self):
        self.participant = Participant(
            name="Test Participant",
            role="Test Role",
            personality="Test personality",
            style="Test style",
            character_type=CharacterType.DEMOCRAT,
            position=Position.LEFT
        )
    
    def test_initialization(self):
        """Test participant initialization"""
        self.assertEqual(self.participant.name, "Test Participant")
        self.assertEqual(self.participant.role, "Test Role")
        self.assertEqual(self.participant.character_type, CharacterType.DEMOCRAT)
        self.assertEqual(self.participant.position, Position.LEFT)
        self.assertIsInstance(self.participant.stats, CharacterStats)
    
    def test_display_name_normal(self):
        """Test display name for normal participants"""
        self.assertEqual(self.participant.display_name, "Test Participant")
    
    def test_display_name_random_american(self):
        """Test display name for random American participants"""
        american = Participant(
            name="John from Chicago",
            role="American",
            personality="Test",
            style="Test",
            character_type=CharacterType.RANDOM_AMERICAN,
            city="Chicago",
            age=35
        )
        self.assertEqual(american.display_name, "John from Chicago (35yo)")
    
    def test_emoji_property(self):
        """Test emoji property for different character types"""
        self.assertEqual(self.participant.emoji, "🔵")  # Democrat
        
        republican = Participant(
            name="GOP", role="Test", personality="Test", style="Test",
            character_type=CharacterType.REPUBLICAN
        )
        self.assertEqual(republican.emoji, "🔴")
    
    def test_message_class_property(self):
        """Test message class property for styling"""
        self.assertEqual(self.participant.message_class, "democrat-message")


class TestMessage(unittest.TestCase):
    """Test the Message model"""
    
    def setUp(self):
        self.message = Message(
            speaker_name="Test Speaker",
            content="Test message content",
            round_number=1
        )
    
    def test_initialization(self):
        """Test message initialization"""
        self.assertEqual(self.message.speaker_name, "Test Speaker")
        self.assertEqual(self.message.content, "Test message content")
        self.assertEqual(self.message.round_number, 1)
        self.assertIsInstance(self.message.timestamp, datetime)
    
    def test_to_dict(self):
        """Test message serialization to dictionary"""
        msg_dict = self.message.to_dict()
        
        self.assertEqual(msg_dict["speaker"], "Test Speaker")
        self.assertEqual(msg_dict["message"], "Test message content")
        self.assertEqual(msg_dict["round"], 1)
        self.assertIn("timestamp", msg_dict)


class TestDebateSession(unittest.TestCase):
    """Test the DebateSession model"""
    
    def setUp(self):
        self.participant1 = Participant(
            name="Participant 1", role="Role 1", personality="P1", style="S1",
            character_type=CharacterType.DEMOCRAT
        )
        self.participant2 = Participant(
            name="Participant 2", role="Role 2", personality="P2", style="S2",
            character_type=CharacterType.REPUBLICAN
        )
        
        self.session = DebateSession(
            topic="Test Topic",
            participants=[self.participant1, self.participant2],
            rounds=3,
            competitive_mode=True
        )
    
    def test_initialization(self):
        """Test session initialization"""
        self.assertEqual(self.session.topic, "Test Topic")
        self.assertEqual(len(self.session.participants), 2)
        self.assertEqual(self.session.rounds, 3)
        self.assertTrue(self.session.competitive_mode)
        self.assertEqual(len(self.session.messages), 0)
    
    def test_add_message(self):
        """Test adding messages to session"""
        message = Message("Speaker", "Content", 1)
        self.session.add_message(message)
        
        self.assertEqual(len(self.session.messages), 1)
        self.assertEqual(self.session.messages[0], message)
    
    def test_get_messages_for_round(self):
        """Test getting messages for specific round"""
        msg1 = Message("Speaker 1", "Round 1 Content", 1)
        msg2 = Message("Speaker 2", "Round 2 Content", 2)
        msg3 = Message("Speaker 1", "Round 1 Content 2", 1)
        
        self.session.add_message(msg1)
        self.session.add_message(msg2)
        self.session.add_message(msg3)
        
        round1_messages = self.session.get_messages_for_round(1)
        round2_messages = self.session.get_messages_for_round(2)
        
        self.assertEqual(len(round1_messages), 2)
        self.assertEqual(len(round2_messages), 1)
        self.assertEqual(round2_messages[0], msg2)
    
    def test_to_dict(self):
        """Test session serialization to dictionary"""
        session_dict = self.session.to_dict()
        
        self.assertEqual(session_dict["topic"], "Test Topic")
        self.assertEqual(session_dict["rounds"], 3)
        self.assertTrue(session_dict["competitive_mode"])
        self.assertIn("session_start", session_dict)
        self.assertIn("participants", session_dict)
        self.assertEqual(len(session_dict["participants"]), 2)


class TestJudgeAdjustment(unittest.TestCase):
    """Test the JudgeAdjustment model"""
    
    def setUp(self):
        self.adjustment = JudgeAdjustment(
            participant_name="Test Participant",
            anger_adjustment=5,
            patience_adjustment=-3,
            uniqueness_adjustment=2
        )
    
    def test_initialization(self):
        """Test adjustment initialization"""
        self.assertEqual(self.adjustment.participant_name, "Test Participant")
        self.assertEqual(self.adjustment.anger_adjustment, 5)
        self.assertEqual(self.adjustment.patience_adjustment, -3)
        self.assertEqual(self.adjustment.uniqueness_adjustment, 2)
    
    def test_to_dict(self):
        """Test adjustment serialization to dictionary"""
        adj_dict = self.adjustment.to_dict()
        
        expected = {
            "anger": 5,
            "patience": -3,
            "uniqueness": 2
        }
        self.assertEqual(adj_dict, expected)


if __name__ == "__main__":
    unittest.main()