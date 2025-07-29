from typing import List, Dict, Any, Optional, Callable
from datetime import datetime
import json

from ..domain.debate.models import DebateSession, DebateSettings, DebateStatus
from ..domain.debate.orchestrator import DebateOrchestrator
from ..domain.debate.judge import DebateJudge, create_judge
from ..domain.characters.base import Character
from ..domain.topics import DebateTopics, create_topic_prompt
from ..infrastructure.ai_client import AIClient
from ..infrastructure.logging_config import get_debate_logger
from .character_service import CharacterService


class DebateService:
    """High-level service for managing debate sessions."""
    
    def __init__(self, ai_client: AIClient, character_service: CharacterService = None):
        """Initialize the debate service."""
        self.ai_client = ai_client
        self.character_service = character_service or CharacterService()
        self.logger = get_debate_logger()
        
        # Initialize components
        self.topics = DebateTopics()
        self.orchestrator: Optional[DebateOrchestrator] = None
        self.judge: Optional[DebateJudge] = None
        
        # Session management
        self.current_session: Optional[DebateSession] = None
        self.session_history: List[DebateSession] = []
        
        # UI callbacks
        self._ui_callbacks: Dict[str, Callable] = {}
    
    def register_ui_callback(self, event_name: str, callback: Callable) -> None:
        """Register a callback for UI updates."""
        self._ui_callbacks[event_name] = callback
        self.logger.debug(f"Registered UI callback for event: {event_name}")
    
    def _trigger_ui_callback(self, event_name: str, *args, **kwargs) -> None:
        """Trigger a UI callback if registered."""
        if event_name in self._ui_callbacks:
            try:
                self._ui_callbacks[event_name](*args, **kwargs)
            except Exception as e:
                self.logger.error(f"Error in UI callback {event_name}: {str(e)}")
    
    def get_available_topics(self) -> List[str]:
        """Get all available debate topics."""
        return self.topics.get_all_topics()
    
    def validate_topic(self, topic: str) -> bool:
        """Validate if a topic is suitable for debate."""
        return self.topics.validate_topic(topic)
    
    def create_debate_session(
        self,
        topic: str,
        selected_character_types: List[str],
        settings: DebateSettings = None
    ) -> Dict[str, Any]:
        """Create a new debate session."""
        try:
            # Validate inputs
            if not self.validate_topic(topic):
                return {"success": False, "error": "Invalid topic"}
            
            character_validation = self.character_service.validate_character_selection(selected_character_types)
            if not character_validation["valid"]:
                return {"success": False, "error": character_validation["errors"]}
            
            # Create characters
            participants = self.character_service.create_characters_from_selection(selected_character_types)
            if not participants:
                return {"success": False, "error": "Failed to create any characters"}
            
            # Assign positions
            self.character_service.assign_positions(participants)
            
            # Set up judge for competitive mode
            if settings and settings.competitive_mode:
                self.judge = create_judge("ai", ai_client=self.ai_client)
            
            # Create orchestrator
            self.orchestrator = DebateOrchestrator(self.ai_client, self.judge)
            
            # Set up orchestrator callbacks
            self.orchestrator.on_message_generated = lambda msg, char: self._trigger_ui_callback(
                "message_generated", msg, char
            )
            self.orchestrator.on_round_completed = lambda round_obj, round_num: self._trigger_ui_callback(
                "round_completed", round_obj, round_num
            )
            self.orchestrator.on_judge_feedback = lambda feedback, round_num: self._trigger_ui_callback(
                "judge_feedback", feedback, round_num
            )
            self.orchestrator.on_session_completed = lambda session: self._trigger_ui_callback(
                "session_completed", session
            )
            self.orchestrator.on_progress_update = lambda progress, round_num, speaker: self._trigger_ui_callback(
                "progress_update", progress, round_num, speaker
            )
            
            # Create debate session
            self.current_session = self.orchestrator.create_debate(topic, participants, settings)
            
            self.logger.info(f"Created debate session: {topic} with {len(participants)} participants")
            
            return {
                "success": True,
                "session": self.current_session,
                "participants": participants,
                "warnings": character_validation.get("warnings", [])
            }
            
        except Exception as e:
            self.logger.error(f"Failed to create debate session: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def start_debate(self, participants: List[Character]) -> Dict[str, Any]:
        """Start the current debate session."""
        try:
            if not self.orchestrator or not self.current_session:
                return {"success": False, "error": "No active debate session"}
            
            if self.current_session.status != DebateStatus.NOT_STARTED:
                return {"success": False, "error": "Debate already started"}
            
            self.logger.info(f"Starting debate: {self.current_session.topic}")
            
            # Start the orchestrator (this will run the debate)
            self.orchestrator.start_debate(participants)
            
            return {"success": True}
            
        except Exception as e:
            self.logger.error(f"Failed to start debate: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def stop_debate(self) -> Dict[str, Any]:
        """Stop the current debate session."""
        try:
            if not self.orchestrator or not self.current_session:
                return {"success": False, "error": "No active debate session"}
            
            self.orchestrator.stop_debate()
            self.logger.info(f"Stopped debate: {self.current_session.topic}")
            
            return {"success": True}
            
        except Exception as e:
            self.logger.error(f"Failed to stop debate: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def pause_debate(self) -> Dict[str, Any]:
        """Pause the current debate session."""
        try:
            if not self.orchestrator or not self.current_session:
                return {"success": False, "error": "No active debate session"}
            
            self.orchestrator.pause_debate()
            self.logger.info(f"Paused debate: {self.current_session.topic}")
            
            return {"success": True}
            
        except Exception as e:
            self.logger.error(f"Failed to pause debate: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def resume_debate(self, participants: List[Character]) -> Dict[str, Any]:
        """Resume a paused debate session."""
        try:
            if not self.orchestrator or not self.current_session:
                return {"success": False, "error": "No active debate session"}
            
            self.orchestrator.resume_debate(participants)
            self.logger.info(f"Resumed debate: {self.current_session.topic}")
            
            return {"success": True}
            
        except Exception as e:
            self.logger.error(f"Failed to resume debate: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def get_session_status(self) -> Dict[str, Any]:
        """Get the current session status."""
        if not self.current_session:
            return {"status": "no_session"}
        
        summary = self.orchestrator.get_session_summary() if self.orchestrator else None
        
        return {
            "status": self.current_session.status.value,
            "session_id": self.current_session.session_id,
            "topic": self.current_session.topic,
            "progress": self.current_session.get_progress(),
            "summary": summary
        }
    
    def export_session(self) -> Optional[Dict[str, Any]]:
        """Export the current session for saving."""
        if not self.orchestrator:
            return None
        
        session_data = self.orchestrator.export_session()
        if session_data:
            # Add metadata
            session_data["exported_at"] = datetime.now().isoformat()
            session_data["export_version"] = "1.0"
        
        return session_data
    
    def import_session(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Import a session from exported data."""
        try:
            if not self.orchestrator:
                self.orchestrator = DebateOrchestrator(self.ai_client)
            
            self.current_session = self.orchestrator.import_session(session_data)
            
            self.logger.info(f"Imported session: {self.current_session.topic}")
            
            return {"success": True, "session": self.current_session}
            
        except Exception as e:
            self.logger.error(f"Failed to import session: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def get_debate_statistics(self) -> Dict[str, Any]:
        """Get statistics about debates."""
        total_sessions = len(self.session_history)
        if self.current_session:
            total_sessions += 1
        
        stats = {
            "total_sessions": total_sessions,
            "current_session_active": self.current_session is not None,
            "character_stats": self.character_service.get_character_statistics()
        }
        
        if self.current_session:
            stats["current_session"] = {
                "topic": self.current_session.topic,
                "participants": self.current_session.participants,
                "status": self.current_session.status.value,
                "progress": self.current_session.get_progress()
            }
        
        return stats
    
    def cleanup_session(self) -> None:
        """Clean up the current session and move to history."""
        if self.current_session:
            # Move to history if completed
            if self.current_session.is_finished():
                self.session_history.append(self.current_session)
                self.logger.info(f"Moved session to history: {self.current_session.topic}")
            
            # Clear current session
            self.current_session = None
            self.orchestrator = None
            self.judge = None
    
    def get_competitive_results(self) -> Optional[Dict[str, Any]]:
        """Get competitive mode results for the current session."""
        if not self.current_session or not self.current_session.settings.competitive_mode:
            return None
        
        final_performance = self.current_session.metadata.get("final_performance")
        if not final_performance:
            return None
        
        # Format results for display
        results = []
        for participant_name, performance in final_performance.items():
            results.append({
                "name": participant_name,
                "stats": performance["final_stats"],
                "performance": performance["performance"],
                "rating": performance["rating"],
                "total_score": performance["total_score"],
                "total_messages": performance["total_messages"]
            })
        
        # Sort by total score descending
        results.sort(key=lambda x: x["total_score"], reverse=True)
        
        return {
            "participants": results,
            "total_participants": len(results),
            "competitive_mode": True
        }
    
    def add_custom_topic(self, topic: str) -> bool:
        """Add a custom topic to the available topics."""
        if self.validate_topic(topic):
            self.topics.add_topic(topic)
            self.logger.info(f"Added custom topic: {topic}")
            return True
        return False
    
    def search_topics(self, keyword: str) -> List[str]:
        """Search topics by keyword."""
        return self.topics.search_topics(keyword)


# Convenience functions
def create_debate_service(ai_client: AIClient) -> DebateService:
    """Create a new debate service instance."""
    return DebateService(ai_client)


def validate_debate_configuration(
    topic: str,
    character_types: List[str],
    settings: DebateSettings = None
) -> Dict[str, Any]:
    """Validate a complete debate configuration."""
    # Create temporary service for validation
    from ..infrastructure.ai_client import MockAIClient
    temp_service = DebateService(MockAIClient())
    
    validation_result = {
        "valid": True,
        "errors": [],
        "warnings": []
    }
    
    # Validate topic
    if not temp_service.validate_topic(topic):
        validation_result["valid"] = False
        validation_result["errors"].append("Invalid or empty topic")
    
    # Validate characters
    char_validation = temp_service.character_service.validate_character_selection(character_types)
    if not char_validation["valid"]:
        validation_result["valid"] = False
        validation_result["errors"].extend(char_validation["errors"])
    
    validation_result["warnings"].extend(char_validation.get("warnings", []))
    
    # Validate settings
    if settings:
        if settings.total_rounds < 1 or settings.total_rounds > 50:
            validation_result["valid"] = False
            validation_result["errors"].append("Total rounds must be between 1 and 50")
        
        if settings.response_delay < 0 or settings.response_delay > 10:
            validation_result["warnings"].append("Response delay should be between 0 and 10 seconds")
    
    return validation_result