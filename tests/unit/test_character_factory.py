import unittest
from unittest.mock import patch, MagicMock
from src.political_debate.domain.character_factory import CharacterFactory
from src.political_debate.domain.models import Participant, CharacterType


class TestCharacterFactory(unittest.TestCase):
    """Test the CharacterFactory class"""
    
    def setUp(self):
        self.factory = CharacterFactory()
    
    def test_create_democrat(self):
        """Test creating a Democratic participant"""
        democrat = self.factory.create_democrat()
        
        self.assertIsInstance(democrat, Participant)
        self.assertEqual(democrat.name, "Market Liberal Democrat")
        self.assertEqual(democrat.character_type, CharacterType.DEMOCRAT)
        self.assertIn("progressive", democrat.personality.lower())
        self.assertIn("social justice", democrat.personality.lower())
    
    def test_create_republican(self):
        """Test creating a Republican participant"""
        republican = self.factory.create_republican()
        
        self.assertIsInstance(republican, Participant)
        self.assertEqual(republican.name, "MAGA Nationalist")
        self.assertEqual(republican.character_type, CharacterType.REPUBLICAN)
        self.assertIn("traditional", republican.personality.lower())
        self.assertIn("america first", republican.personality.lower())
    
    @patch('random.choice')
    def test_create_random_american(self, mock_choice):
        """Test creating a random American participant"""
        # Mock random selections
        mock_choice.side_effect = [
            "male",  # gender
            "John",  # name
            "boomer",  # generation
            "New York"  # city
        ]
        
        # Mock age generation
        with patch('random.randint', return_value=65):
            american = self.factory.create_random_american()
        
        self.assertIsInstance(american, Participant)
        self.assertEqual(american.character_type, CharacterType.RANDOM_AMERICAN)
        self.assertEqual(american.gender, "male")
        self.assertEqual(american.age, 65)
        self.assertEqual(american.city, "New York")
        self.assertIn("John from New York", american.name)
    
    @patch('random.choice')
    def test_create_random_redditor(self, mock_choice):
        """Test creating a random Redditor participant"""
        # Mock random selections
        mock_choice.side_effect = [
            "throwaway12345",  # username
            "politics"  # subreddit
        ]
        
        redditor = self.factory.create_random_redditor()
        
        self.assertIsInstance(redditor, Participant)
        self.assertEqual(redditor.character_type, CharacterType.RANDOM_REDDITOR)
        self.assertEqual(redditor.subreddit, "politics")
        self.assertEqual(redditor.username, "throwaway12345")
        self.assertIn("u/throwaway12345 from r/politics", redditor.name)
    
    def test_create_additional_character_marxist(self):
        """Test creating a Marxist character"""
        marxist = self.factory.create_additional_character("marxist_leninist")
        
        self.assertIsInstance(marxist, Participant)
        self.assertEqual(marxist.name, "Marxist-Leninist")
        self.assertEqual(marxist.character_type, CharacterType.MARXIST)
        self.assertIn("revolutionary", marxist.personality.lower())
    
    def test_create_additional_character_invalid(self):
        """Test creating character with invalid key raises error"""
        with self.assertRaises(ValueError):
            self.factory.create_additional_character("invalid_character")
    
    def test_generate_city_personality(self):
        """Test city personality generation"""
        # Test known city
        ny_personality = self.factory._generate_city_personality_for_city("New York City")
        self.assertIn("fast-paced", ny_personality)
        
        # Test unknown city  
        unknown_personality = self.factory._generate_city_personality_for_city("Unknown City")
        self.assertIn("friendly", unknown_personality)
    
    def test_generate_subreddit_personality(self):
        """Test subreddit personality generation"""
        # Test known subreddit
        politics_personality = self.factory._generate_subreddit_personality_for_subreddit("politics")
        self.assertIn("politically engaged", politics_personality)
        
        # Test unknown subreddit
        unknown_personality = self.factory._generate_subreddit_personality_for_subreddit("unknown")
        self.assertIn("online community", unknown_personality)
    
    def test_data_access(self):
        """Test that factory has access to character data"""
        self.assertIsNotNone(self.factory.data)
        self.assertTrue(len(self.factory.data.male_names) > 0)
        self.assertTrue(len(self.factory.data.female_names) > 0)
        self.assertTrue(len(self.factory.data.us_cities) > 0)


if __name__ == "__main__":
    unittest.main()