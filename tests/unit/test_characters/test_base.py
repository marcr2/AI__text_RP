import unittest
from datetime import datetime
from src.debate_simulator.domain.characters.base import (
    Character, CharacterStats, CharacterFactory, CharacterRepository
)


class TestCharacterStats(unittest.TestCase):
    """Test cases for CharacterStats class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.stats = CharacterStats()
    
    def test_default_initialization(self):
        """Test default stat values."""
        self.assertEqual(self.stats.anger, 50)
        self.assertEqual(self.stats.patience, 50)
        self.assertEqual(self.stats.uniqueness, 50)
    
    def test_custom_initialization(self):
        """Test custom stat values."""
        stats = CharacterStats(anger=80, patience=20, uniqueness=70)
        self.assertEqual(stats.anger, 80)
        self.assertEqual(stats.patience, 20)
        self.assertEqual(stats.uniqueness, 70)
    
    def test_adjust_stats_within_bounds(self):
        """Test stat adjustments within valid bounds."""
        adjustments = {"anger": 10, "patience": -15, "uniqueness": 5}
        self.stats.adjust(adjustments)
        
        self.assertEqual(self.stats.anger, 60)
        self.assertEqual(self.stats.patience, 35)
        self.assertEqual(self.stats.uniqueness, 55)
    
    def test_adjust_stats_with_upper_bound(self):
        """Test stat adjustments that exceed upper bound."""
        self.stats.anger = 95
        adjustments = {"anger": 20}
        self.stats.adjust(adjustments)
        
        self.assertEqual(self.stats.anger, 100)  # Clamped to max
    
    def test_adjust_stats_with_lower_bound(self):
        """Test stat adjustments that exceed lower bound."""
        self.stats.patience = 5
        adjustments = {"patience": -20}
        self.stats.adjust(adjustments)
        
        self.assertEqual(self.stats.patience, 0)  # Clamped to min
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        expected = {"anger": 50, "patience": 50, "uniqueness": 50}
        self.assertEqual(self.stats.to_dict(), expected)
    
    def test_from_dict(self):
        """Test creation from dictionary."""
        data = {"anger": 75, "patience": 25, "uniqueness": 90}
        stats = CharacterStats.from_dict(data)
        
        self.assertEqual(stats.anger, 75)
        self.assertEqual(stats.patience, 25)
        self.assertEqual(stats.uniqueness, 90)
    
    def test_from_dict_with_missing_values(self):
        """Test creation from dictionary with missing values."""
        data = {"anger": 80}
        stats = CharacterStats.from_dict(data)
        
        self.assertEqual(stats.anger, 80)
        self.assertEqual(stats.patience, 50)  # Default value
        self.assertEqual(stats.uniqueness, 50)  # Default value


class TestCharacter(unittest.TestCase):
    """Test cases for Character class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.stats = CharacterStats(anger=70, patience=30, uniqueness=85)
        self.character = Character(
            name="Test Character",
            role="test role",
            personality="test personality",
            style="test style",
            stats=self.stats,
            position="left",
            metadata={"test_key": "test_value"}
        )
    
    def test_initialization(self):
        """Test character initialization."""
        self.assertEqual(self.character.name, "Test Character")
        self.assertEqual(self.character.role, "test role")
        self.assertEqual(self.character.personality, "test personality")
        self.assertEqual(self.character.style, "test style")
        self.assertEqual(self.character.position, "left")
        self.assertEqual(self.character.metadata["test_key"], "test_value")
    
    def test_post_init_metadata(self):
        """Test that metadata is initialized if None."""
        character = Character(
            name="Test",
            role="test",
            personality="test",
            style="test",
            stats=self.stats
        )
        self.assertIsInstance(character.metadata, dict)
        self.assertEqual(len(character.metadata), 0)
    
    def test_get_dynamic_style_high_anger(self):
        """Test dynamic style with high anger."""
        self.character.stats.anger = 85
        style = self.character.get_dynamic_style()
        self.assertIn("EXTREMELY ENRAGED", style)
        self.assertIn("FURIOUS", style)
    
    def test_get_dynamic_style_low_patience(self):
        """Test dynamic style with low patience."""
        self.character.stats.patience = 15
        style = self.character.get_dynamic_style()
        self.assertIn("EXTREMELY IMPATIENT", style)
        self.assertIn("INTERRUPTS", style)
    
    def test_get_dynamic_style_moderate_stats(self):
        """Test dynamic style with moderate stats."""
        self.character.stats.anger = 45
        self.character.stats.patience = 55
        style = self.character.get_dynamic_style()
        self.assertIn("moderately frustrated", style)
        self.assertIn("moderately patient", style)
    
    def test_adjust_stats(self):
        """Test character stat adjustments."""
        adjustments = {"anger": -10, "patience": 15, "uniqueness": -5}
        self.character.adjust_stats(adjustments)
        
        self.assertEqual(self.character.stats.anger, 60)
        self.assertEqual(self.character.stats.patience, 45)
        self.assertEqual(self.character.stats.uniqueness, 80)
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        character_dict = self.character.to_dict()
        
        self.assertEqual(character_dict["name"], "Test Character")
        self.assertEqual(character_dict["role"], "test role")
        self.assertEqual(character_dict["position"], "left")
        self.assertIsInstance(character_dict["stats"], dict)
        self.assertEqual(character_dict["metadata"]["test_key"], "test_value")
    
    def test_from_dict(self):
        """Test creation from dictionary."""
        data = {
            "name": "Dict Character",
            "role": "dict role",
            "personality": "dict personality",
            "style": "dict style",
            "stats": {"anger": 80, "patience": 20, "uniqueness": 60},
            "position": "right",
            "metadata": {"key": "value"}
        }
        
        character = Character.from_dict(data)
        
        self.assertEqual(character.name, "Dict Character")
        self.assertEqual(character.role, "dict role")
        self.assertEqual(character.position, "right")
        self.assertEqual(character.stats.anger, 80)
        self.assertEqual(character.metadata["key"], "value")


class MockCharacterFactory(CharacterFactory):
    """Mock implementation of CharacterFactory for testing."""
    
    def create_character(self, character_type: str, **kwargs) -> Character:
        """Create a mock character."""
        stats = CharacterStats()
        return Character(
            name=f"Mock {character_type}",
            role="mock role",
            personality="mock personality",
            style="mock style",
            stats=stats,
            **kwargs
        )
    
    def get_available_types(self) -> list[str]:
        """Return mock character types."""
        return ["type1", "type2", "type3"]


class MockCharacterRepository(CharacterRepository):
    """Mock implementation of CharacterRepository for testing."""
    
    def __init__(self):
        self.characters = {}
    
    def save(self, character: Character) -> None:
        """Save character to mock storage."""
        self.characters[character.name] = character
    
    def get_by_name(self, name: str) -> Character:
        """Get character by name."""
        return self.characters.get(name)
    
    def get_all(self) -> list[Character]:
        """Get all characters."""
        return list(self.characters.values())


class TestCharacterFactory(unittest.TestCase):
    """Test cases for CharacterFactory interface."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.factory = MockCharacterFactory()
    
    def test_create_character(self):
        """Test character creation."""
        character = self.factory.create_character("type1")
        self.assertEqual(character.name, "Mock type1")
        self.assertEqual(character.role, "mock role")
    
    def test_create_character_with_kwargs(self):
        """Test character creation with additional arguments."""
        character = self.factory.create_character("type2", position="right")
        self.assertEqual(character.position, "right")
    
    def test_get_available_types(self):
        """Test getting available character types."""
        types = self.factory.get_available_types()
        self.assertEqual(types, ["type1", "type2", "type3"])


class TestCharacterRepository(unittest.TestCase):
    """Test cases for CharacterRepository interface."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.repository = MockCharacterRepository()
        self.character = Character(
            name="Repo Test",
            role="test role",
            personality="test personality",
            style="test style",
            stats=CharacterStats()
        )
    
    def test_save_and_get_character(self):
        """Test saving and retrieving character."""
        self.repository.save(self.character)
        retrieved = self.repository.get_by_name("Repo Test")
        
        self.assertEqual(retrieved.name, "Repo Test")
        self.assertEqual(retrieved.role, "test role")
    
    def test_get_nonexistent_character(self):
        """Test retrieving non-existent character."""
        result = self.repository.get_by_name("Nonexistent")
        self.assertIsNone(result)
    
    def test_get_all_characters(self):
        """Test getting all characters."""
        # Add multiple characters
        char1 = Character("Char1", "role1", "personality1", "style1", CharacterStats())
        char2 = Character("Char2", "role2", "personality2", "style2", CharacterStats())
        
        self.repository.save(char1)
        self.repository.save(char2)
        
        all_chars = self.repository.get_all()
        self.assertEqual(len(all_chars), 2)
        names = [char.name for char in all_chars]
        self.assertIn("Char1", names)
        self.assertIn("Char2", names)


if __name__ == "__main__":
    unittest.main()