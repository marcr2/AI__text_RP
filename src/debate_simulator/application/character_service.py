from typing import List, Dict, Any, Optional
from ..domain.characters.base import Character, CharacterFactory
from ..domain.characters.predefined import PredefinedCharacterFactory, CHARACTER_TYPE_DISPLAY_NAMES
from ..domain.characters.random_generators import RandomCharacterFactory
from ..infrastructure.logging_config import get_character_logger


class CharacterService:
    """Application service for managing characters."""
    
    def __init__(self):
        """Initialize the character service with factories."""
        self.predefined_factory = PredefinedCharacterFactory()
        self.random_factory = RandomCharacterFactory()
        self.logger = get_character_logger()
        
        # Cache for created characters
        self._character_cache: Dict[str, Character] = {}
    
    def get_available_character_types(self) -> Dict[str, str]:
        """Get all available character types with display names."""
        available_types = {}
        
        # Add predefined characters
        for char_type in self.predefined_factory.get_available_types():
            display_name = CHARACTER_TYPE_DISPLAY_NAMES.get(char_type, char_type)
            available_types[char_type] = display_name
        
        # Add random characters
        for char_type in self.random_factory.get_available_types():
            if char_type == "random_american":
                available_types[char_type] = "🗽 Random American"
            elif char_type == "random_redditor":
                available_types[char_type] = "🤖 Random Redditor"
        
        return available_types
    
    def create_character(self, character_type: str, **kwargs) -> Character:
        """Create a character of the specified type."""
        try:
            # Check if character already exists in cache
            cache_key = f"{character_type}_{hash(str(sorted(kwargs.items())))}"
            if cache_key in self._character_cache:
                self.logger.debug(f"Returning cached character: {character_type}")
                return self._character_cache[cache_key]
            
            # Create new character
            if character_type in self.predefined_factory.get_available_types():
                character = self.predefined_factory.create_character(character_type, **kwargs)
            elif character_type in self.random_factory.get_available_types():
                character = self.random_factory.create_character(character_type, **kwargs)
            else:
                raise ValueError(f"Unknown character type: {character_type}")
            
            # Cache the character
            self._character_cache[cache_key] = character
            
            self.logger.info(f"Character created: {character.name} ({character_type})")
            return character
            
        except Exception as e:
            self.logger.error(f"Failed to create character {character_type}: {str(e)}")
            raise
    
    def create_characters_from_selection(self, selected_types: List[str]) -> List[Character]:
        """Create multiple characters from a list of selected types."""
        characters = []
        
        for char_type in selected_types:
            try:
                character = self.create_character(char_type)
                characters.append(character)
            except Exception as e:
                self.logger.error(f"Failed to create character {char_type}: {str(e)}")
                # Continue with other characters instead of failing completely
                continue
        
        self.logger.info(f"Created {len(characters)} characters from {len(selected_types)} requested types")
        return characters
    
    def get_default_characters(self) -> List[Character]:
        """Get the default Democrat and Republican characters."""
        try:
            democrat = self.create_character("democratic_commentator")
            republican = self.create_character("republican_commentator")
            return [democrat, republican]
        except Exception as e:
            self.logger.error(f"Failed to create default characters: {str(e)}")
            raise
    
    def get_character_info(self, character_type: str) -> Dict[str, Any]:
        """Get information about a character type without creating an instance."""
        if character_type in self.predefined_factory.get_available_types():
            return self.predefined_factory.get_character_info(character_type)
        else:
            return {"error": f"Character type {character_type} not found"}
    
    def validate_character_selection(self, selected_types: List[str]) -> Dict[str, Any]:
        """Validate a character selection."""
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "character_count": len(selected_types)
        }
        
        if not selected_types:
            validation_result["valid"] = False
            validation_result["errors"].append("No characters selected")
            return validation_result
        
        if len(selected_types) < 2:
            validation_result["warnings"].append("At least 2 characters recommended for a good debate")
        
        if len(selected_types) > 10:
            validation_result["warnings"].append("Too many characters may make the debate hard to follow")
        
        # Check for unknown character types
        available_types = set(self.get_available_character_types().keys())
        for char_type in selected_types:
            if char_type not in available_types:
                validation_result["valid"] = False
                validation_result["errors"].append(f"Unknown character type: {char_type}")
        
        return validation_result
    
    def get_character_statistics(self) -> Dict[str, Any]:
        """Get statistics about character usage."""
        predefined_count = len(self.predefined_factory.get_available_types())
        random_count = len(self.random_factory.get_available_types())
        cached_count = len(self._character_cache)
        
        return {
            "total_available": predefined_count + random_count,
            "predefined_characters": predefined_count,
            "random_character_types": random_count,
            "cached_characters": cached_count,
            "available_types": list(self.get_available_character_types().keys())
        }
    
    def clear_character_cache(self) -> None:
        """Clear the character cache."""
        cache_size = len(self._character_cache)
        self._character_cache.clear()
        self.logger.info(f"Cleared character cache ({cache_size} characters)")
    
    def assign_positions(self, characters: List[Character]) -> None:
        """Assign left/right positions to characters for debate display."""
        import random
        
        # Shuffle for randomness
        shuffled_indices = list(range(len(characters)))
        random.shuffle(shuffled_indices)
        
        # Split into left and right sides
        mid_point = len(characters) // 2
        
        for i, char_index in enumerate(shuffled_indices):
            if i < mid_point or (len(characters) % 2 == 1 and i == len(characters) - 1 and mid_point > len(characters) // 2):
                characters[char_index].position = "left"
            else:
                characters[char_index].position = "right"
        
        self.logger.debug(f"Assigned positions to {len(characters)} characters")
    
    def update_character_stats(self, characters: List[Character], stat_adjustments: Dict[str, Dict[str, int]]) -> None:
        """Update character statistics based on judge feedback."""
        for character in characters:
            if character.name in stat_adjustments:
                character.adjust_stats(stat_adjustments[character.name])
                self.logger.debug(f"Updated stats for {character.name}: {stat_adjustments[character.name]}")
    
    def get_character_by_name(self, characters: List[Character], name: str) -> Optional[Character]:
        """Find a character by name from a list of characters."""
        for character in characters:
            if character.name == name:
                return character
        return None
    
    def export_characters(self, characters: List[Character]) -> List[Dict[str, Any]]:
        """Export characters to dictionary format for serialization."""
        return [character.to_dict() for character in characters]
    
    def import_characters(self, character_data: List[Dict[str, Any]]) -> List[Character]:
        """Import characters from dictionary format."""
        characters = []
        for data in character_data:
            try:
                character = Character.from_dict(data)
                characters.append(character)
            except Exception as e:
                self.logger.error(f"Failed to import character {data.get('name', 'unknown')}: {str(e)}")
        
        self.logger.info(f"Imported {len(characters)} characters")
        return characters


# Convenience functions for common operations
def create_character_service() -> CharacterService:
    """Create a new character service instance."""
    return CharacterService()


def get_available_characters() -> Dict[str, str]:
    """Get all available character types with display names."""
    service = CharacterService()
    return service.get_available_character_types()


def create_debate_participants(selected_types: List[str]) -> List[Character]:
    """Create characters for a debate from selected types."""
    service = CharacterService()
    return service.create_characters_from_selection(selected_types)