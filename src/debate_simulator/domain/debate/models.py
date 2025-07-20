from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum


class DebateStatus(Enum):
    """Status of a debate session."""
    NOT_STARTED = "not_started"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"
    COMPLETED = "completed"


@dataclass
class DebateMessage:
    """A single message in a debate conversation."""
    round_number: int
    speaker_name: str
    message: str
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "round": self.round_number,
            "speaker": self.speaker_name,
            "message": self.message,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DebateMessage':
        """Create from dictionary."""
        return cls(
            round_number=data["round"],
            speaker_name=data["speaker"],
            message=data["message"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            metadata=data.get("metadata", {})
        )


@dataclass
class DebateRound:
    """A complete round of debate with all participant responses."""
    round_number: int
    messages: List[DebateMessage] = field(default_factory=list)
    judge_feedback: Optional[Dict[str, Any]] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    
    def add_message(self, message: DebateMessage) -> None:
        """Add a message to this round."""
        self.messages.append(message)
    
    def get_messages_by_speaker(self, speaker_name: str) -> List[DebateMessage]:
        """Get all messages from a specific speaker in this round."""
        return [msg for msg in self.messages if msg.speaker_name == speaker_name]
    
    def is_complete(self, expected_participants: int) -> bool:
        """Check if round is complete (all participants have responded)."""
        return len(self.messages) >= expected_participants
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "round_number": self.round_number,
            "messages": [msg.to_dict() for msg in self.messages],
            "judge_feedback": self.judge_feedback,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DebateRound':
        """Create from dictionary."""
        return cls(
            round_number=data["round_number"],
            messages=[DebateMessage.from_dict(msg) for msg in data.get("messages", [])],
            judge_feedback=data.get("judge_feedback"),
            start_time=datetime.fromisoformat(data["start_time"]) if data.get("start_time") else None,
            end_time=datetime.fromisoformat(data["end_time"]) if data.get("end_time") else None
        )


@dataclass
class DebateConversation:
    """Complete conversation history for a debate."""
    topic: str
    rounds: List[DebateRound] = field(default_factory=list)
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    
    def add_round(self, round_obj: DebateRound) -> None:
        """Add a new round to the conversation."""
        self.rounds.append(round_obj)
    
    def get_current_round(self) -> Optional[DebateRound]:
        """Get the current (last) round."""
        return self.rounds[-1] if self.rounds else None
    
    def get_all_messages(self) -> List[DebateMessage]:
        """Get all messages from all rounds."""
        messages = []
        for round_obj in self.rounds:
            messages.extend(round_obj.messages)
        return messages
    
    def get_messages_for_context(self, last_n: int = 6) -> List[DebateMessage]:
        """Get the last N messages for context."""
        all_messages = self.get_all_messages()
        return all_messages[-last_n:] if len(all_messages) > last_n else all_messages
    
    def get_participant_message_count(self, speaker_name: str) -> int:
        """Get total message count for a participant."""
        return sum(1 for msg in self.get_all_messages() if msg.speaker_name == speaker_name)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "topic": self.topic,
            "rounds": [round_obj.to_dict() for round_obj in self.rounds],
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DebateConversation':
        """Create from dictionary."""
        return cls(
            topic=data["topic"],
            rounds=[DebateRound.from_dict(r) for r in data.get("rounds", [])],
            start_time=datetime.fromisoformat(data["start_time"]),
            end_time=datetime.fromisoformat(data["end_time"]) if data.get("end_time") else None
        )


@dataclass
class DebateSettings:
    """Configuration settings for a debate."""
    total_rounds: int = 5
    response_delay: float = 1.0
    competitive_mode: bool = False
    auto_judge: bool = True
    max_response_length: int = 100
    timeout_per_response: int = 30
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "total_rounds": self.total_rounds,
            "response_delay": self.response_delay,
            "competitive_mode": self.competitive_mode,
            "auto_judge": self.auto_judge,
            "max_response_length": self.max_response_length,
            "timeout_per_response": self.timeout_per_response
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DebateSettings':
        """Create from dictionary."""
        return cls(
            total_rounds=data.get("total_rounds", 5),
            response_delay=data.get("response_delay", 1.0),
            competitive_mode=data.get("competitive_mode", False),
            auto_judge=data.get("auto_judge", True),
            max_response_length=data.get("max_response_length", 100),
            timeout_per_response=data.get("timeout_per_response", 30)
        )


@dataclass
class DebateSession:
    """Complete debate session including all metadata."""
    session_id: str
    topic: str
    participants: List[str]  # Character names
    settings: DebateSettings
    conversation: DebateConversation
    status: DebateStatus = DebateStatus.NOT_STARTED
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def start(self) -> None:
        """Mark the debate as started."""
        self.status = DebateStatus.RUNNING
    
    def pause(self) -> None:
        """Pause the debate."""
        if self.status == DebateStatus.RUNNING:
            self.status = DebateStatus.PAUSED
    
    def resume(self) -> None:
        """Resume a paused debate."""
        if self.status == DebateStatus.PAUSED:
            self.status = DebateStatus.RUNNING
    
    def stop(self) -> None:
        """Stop the debate."""
        if self.status in [DebateStatus.RUNNING, DebateStatus.PAUSED]:
            self.status = DebateStatus.STOPPED
            self.conversation.end_time = datetime.now()
    
    def complete(self) -> None:
        """Mark the debate as completed."""
        self.status = DebateStatus.COMPLETED
        self.conversation.end_time = datetime.now()
    
    def is_running(self) -> bool:
        """Check if debate is currently running."""
        return self.status == DebateStatus.RUNNING
    
    def is_finished(self) -> bool:
        """Check if debate is finished (stopped or completed)."""
        return self.status in [DebateStatus.STOPPED, DebateStatus.COMPLETED]
    
    def get_progress(self) -> float:
        """Get debate progress as percentage (0.0 to 1.0)."""
        if self.status == DebateStatus.NOT_STARTED:
            return 0.0
        elif self.status in [DebateStatus.STOPPED, DebateStatus.COMPLETED]:
            return 1.0
        else:
            completed_rounds = len(self.conversation.rounds)
            return min(completed_rounds / self.settings.total_rounds, 1.0)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "session_id": self.session_id,
            "topic": self.topic,
            "participants": self.participants,
            "settings": self.settings.to_dict(),
            "conversation": self.conversation.to_dict(),
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DebateSession':
        """Create from dictionary."""
        return cls(
            session_id=data["session_id"],
            topic=data["topic"],
            participants=data["participants"],
            settings=DebateSettings.from_dict(data["settings"]),
            conversation=DebateConversation.from_dict(data["conversation"]),
            status=DebateStatus(data["status"]),
            created_at=datetime.fromisoformat(data["created_at"]),
            metadata=data.get("metadata", {})
        )


# Utility functions
def create_debate_session(
    session_id: str,
    topic: str,
    participants: List[str],
    settings: DebateSettings = None
) -> DebateSession:
    """Create a new debate session."""
    if settings is None:
        settings = DebateSettings()
    
    conversation = DebateConversation(topic=topic)
    
    return DebateSession(
        session_id=session_id,
        topic=topic,
        participants=participants,
        settings=settings,
        conversation=conversation
    )


def generate_session_id() -> str:
    """Generate a unique session ID."""
    import uuid
    return str(uuid.uuid4())[:8]