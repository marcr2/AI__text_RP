from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class Position(Enum):
    """Debate position enum"""
    LEFT = "left"
    RIGHT = "right"


class CharacterType(Enum):
    """Character type classification"""
    DEMOCRAT = "democrat"
    REPUBLICAN = "republican"
    RANDOM_AMERICAN = "random_american"
    RANDOM_REDDITOR = "random_redditor"
    MARXIST = "marxist_leninist"
    ANARCHO = "anarcho_capitalist"
    CATHOLIC = "catholic_theocrat"
    MONARCHIST = "absolute_monarchist"
    ISLAMIC = "islamic_extremist"
    EVANGELIST = "evangelist_preacher"
    MASTER_BAITER = "master_baiter"
    CHINESE_COMMUNIST = "chinese_communist"


@dataclass
class CharacterStats:
    """Character performance stats"""
    anger: int = 50
    patience: int = 50
    uniqueness: int = 50

    def adjust(self, adjustments: Dict[str, int]) -> None:
        """Apply stat adjustments with bounds checking"""
        for stat, adjustment in adjustments.items():
            if hasattr(self, stat):
                current_value = getattr(self, stat)
                new_value = max(0, min(100, current_value + adjustment))
                setattr(self, stat, new_value)

    @property
    def total_score(self) -> int:
        """Calculate total performance score"""
        return self.anger + self.patience + self.uniqueness

    @property
    def performance_rating(self) -> str:
        """Get performance rating based on total score"""
        total = self.total_score
        if total >= 240:
            return "🌟 EXCELLENT"
        elif total >= 180:
            return "👍 GOOD"
        elif total >= 120:
            return "😐 AVERAGE"
        else:
            return "😞 POOR"


@dataclass
class Participant:
    """A debate participant with their characteristics"""
    name: str
    role: str
    personality: str
    style: str
    character_type: CharacterType
    position: Position = Position.LEFT
    stats: CharacterStats = field(default_factory=CharacterStats)
    
    # Optional fields for specific character types
    gender: Optional[str] = None
    generation: Optional[str] = None
    age: Optional[int] = None
    city: Optional[str] = None
    subreddit: Optional[str] = None
    username: Optional[str] = None
    
    @property
    def display_name(self) -> str:
        """Get formatted display name for UI"""
        if self.character_type == CharacterType.RANDOM_AMERICAN and self.city and self.age:
            name_part = self.name.split(" from ")[0] if " from " in self.name else self.name
            return f"{name_part} from {self.city} ({self.age}yo)"
        return self.name
    
    @property
    def emoji(self) -> str:
        """Get appropriate emoji for character type"""
        emoji_map = {
            CharacterType.DEMOCRAT: "🔵",
            CharacterType.REPUBLICAN: "🔴",
            CharacterType.RANDOM_REDDITOR: "🤖",
            CharacterType.MARXIST: "☭",
            CharacterType.ANARCHO: "$",
            CharacterType.CATHOLIC: "⛪",
            CharacterType.MONARCHIST: "👑",
            CharacterType.ISLAMIC: "☪️",
            CharacterType.EVANGELIST: "✝️",
            CharacterType.MASTER_BAITER: "💪",
            CharacterType.CHINESE_COMMUNIST: "🇨🇳",
            CharacterType.RANDOM_AMERICAN: "👩" if self.gender == "female" else "👨",
        }
        return emoji_map.get(self.character_type, "⚫")

    @property
    def message_class(self) -> str:
        """Get CSS class for message styling"""
        class_map = {
            CharacterType.DEMOCRAT: "democrat-message",
            CharacterType.REPUBLICAN: "republican-message",
            CharacterType.RANDOM_REDDITOR: "redditor-message",
            CharacterType.MARXIST: "marxist-message",
            CharacterType.ANARCHO: "anarcho-message",
            CharacterType.CATHOLIC: "catholic-message",
            CharacterType.MONARCHIST: "monarchist-message",
            CharacterType.ISLAMIC: "islamic-message",
            CharacterType.EVANGELIST: "evangelist-message",
            CharacterType.MASTER_BAITER: "master-baiter-message",
            CharacterType.CHINESE_COMMUNIST: "chinese-communist-message",
            CharacterType.RANDOM_AMERICAN: "random-american-message",
        }
        return class_map.get(self.character_type, "democrat-message")


@dataclass
class Message:
    """A single debate message"""
    speaker_name: str
    content: str
    round_number: int
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "round": self.round_number,
            "speaker": self.speaker_name,
            "message": self.content,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class DebateSession:
    """A complete debate session"""
    topic: str
    participants: List[Participant]
    messages: List[Message] = field(default_factory=list)
    rounds: int = 5
    competitive_mode: bool = False
    session_start: datetime = field(default_factory=datetime.now)
    
    def add_message(self, message: Message) -> None:
        """Add a message to the session"""
        self.messages.append(message)
    
    def get_messages_for_round(self, round_number: int) -> List[Message]:
        """Get all messages for a specific round"""
        return [msg for msg in self.messages if msg.round_number == round_number]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "session_start": self.session_start.isoformat(),
            "topic": self.topic,
            "rounds": self.rounds,
            "conversation": [msg.to_dict() for msg in self.messages],
            "competitive_mode": self.competitive_mode,
            "participants": [
                {"name": p.name, "stats": p.stats.__dict__}
                for p in self.participants
            ] if self.competitive_mode else []
        }


@dataclass
class JudgeAdjustment:
    """Judge adjustments for a participant"""
    participant_name: str
    anger_adjustment: int = 0
    patience_adjustment: int = 0
    uniqueness_adjustment: int = 0
    
    def to_dict(self) -> Dict[str, int]:
        """Convert to dictionary for stats adjustment"""
        return {
            "anger": self.anger_adjustment,
            "patience": self.patience_adjustment,
            "uniqueness": self.uniqueness_adjustment
        }