from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any, Optional
from datetime import datetime


@dataclass
class CharacterStats:
    """Character statistics for competitive mode."""
    anger: int = 50
    patience: int = 50
    uniqueness: int = 50
    
    def adjust(self, adjustments: Dict[str, int]) -> None:
        """Adjust stats with bounds checking (0-100)."""
        self.anger = max(0, min(100, self.anger + adjustments.get("anger", 0)))
        self.patience = max(0, min(100, self.patience + adjustments.get("patience", 0)))
        self.uniqueness = max(0, min(100, self.uniqueness + adjustments.get("uniqueness", 0)))
    
    def to_dict(self) -> Dict[str, int]:
        """Convert to dictionary."""
        return {
            "anger": self.anger,
            "patience": self.patience,
            "uniqueness": self.uniqueness
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, int]) -> 'CharacterStats':
        """Create from dictionary."""
        return cls(
            anger=data.get("anger", 50),
            patience=data.get("patience", 50),
            uniqueness=data.get("uniqueness", 50)
        )


@dataclass
class Character:
    """Base character model for the debate simulator."""
    name: str
    role: str
    personality: str
    style: str
    stats: CharacterStats
    position: Optional[str] = None  # 'left' or 'right'
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
    
    def get_dynamic_style(self) -> str:
        """Get dynamic style based on current stats."""
        base_style = self.style
        anger = self.stats.anger
        patience = self.stats.patience
        
        # Anger modifiers
        if anger >= 80:
            anger_modifier = "EXTREMELY ENRAGED, FURIOUS, SCREAMING with CAPS, uses EXCLAMATION MARKS CONSTANTLY!!!"
        elif anger >= 60:
            anger_modifier = "VERY ANGRY, HOSTILE, uses CAPS frequently, aggressive tone"
        elif anger >= 40:
            anger_modifier = "moderately frustrated, some CAPS usage"
        else:
            anger_modifier = "calm, measured tone"
        
        # Patience modifiers
        if patience <= 20:
            patience_modifier = "EXTREMELY IMPATIENT, INTERRUPTS, RUSHES through points, agitated"
        elif patience <= 40:
            patience_modifier = "impatient, short responses, wants to move on quickly"
        elif patience <= 60:
            patience_modifier = "moderately patient, normal pacing"
        else:
            patience_modifier = "very patient, takes time to explain, calm demeanor"
        
        return f"{base_style}, {anger_modifier}, {patience_modifier}"
    
    def adjust_stats(self, adjustments: Dict[str, int]) -> None:
        """Adjust character stats."""
        self.stats.adjust(adjustments)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert character to dictionary."""
        return {
            "name": self.name,
            "role": self.role,
            "personality": self.personality,
            "style": self.style,
            "stats": self.stats.to_dict(),
            "position": self.position,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Character':
        """Create character from dictionary."""
        return cls(
            name=data["name"],
            role=data["role"],
            personality=data["personality"],
            style=data["style"],
            stats=CharacterStats.from_dict(data.get("stats", {})),
            position=data.get("position"),
            metadata=data.get("metadata", {})
        )


class CharacterFactory(ABC):
    """Abstract factory for creating characters."""
    
    @abstractmethod
    def create_character(self, character_type: str, **kwargs) -> Character:
        """Create a character of the specified type."""
        pass
    
    @abstractmethod
    def get_available_types(self) -> list[str]:
        """Get list of available character types."""
        pass


class CharacterRepository(ABC):
    """Abstract repository for character persistence."""
    
    @abstractmethod
    def save(self, character: Character) -> None:
        """Save a character."""
        pass
    
    @abstractmethod
    def get_by_name(self, name: str) -> Optional[Character]:
        """Get character by name."""
        pass
    
    @abstractmethod
    def get_all(self) -> list[Character]:
        """Get all characters."""
        pass