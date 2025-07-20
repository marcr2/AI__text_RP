from typing import List, Dict, Any, Optional, Callable
from datetime import datetime
import random
import time

from .models import (
    DebateSession, DebateRound, DebateMessage, DebateSettings, 
    DebateStatus, create_debate_session, generate_session_id
)
from .judge import DebateJudge
from ..characters.base import Character
from ..topics import create_topic_prompt


class DebateOrchestrator:
    """Orchestrates the flow of a political debate between AI characters."""
    
    def __init__(self, ai_client, judge: Optional[DebateJudge] = None):
        """Initialize the orchestrator with required dependencies."""
        self.ai_client = ai_client
        self.judge = judge
        self.current_session: Optional[DebateSession] = None
        
        # Callbacks for UI updates
        self.on_message_generated: Optional[Callable] = None
        self.on_round_completed: Optional[Callable] = None
        self.on_judge_feedback: Optional[Callable] = None
        self.on_session_completed: Optional[Callable] = None
        self.on_progress_update: Optional[Callable] = None
    
    def create_debate(
        self,
        topic: str,
        participants: List[Character],
        settings: DebateSettings = None
    ) -> DebateSession:
        """Create a new debate session."""
        if settings is None:
            settings = DebateSettings()
        
        session_id = generate_session_id()
        participant_names = [p.name for p in participants]
        
        self.current_session = create_debate_session(
            session_id=session_id,
            topic=topic,
            participants=participant_names,
            settings=settings
        )
        
        # Assign positions to participants (left/right sides)
        self._assign_positions(participants)
        
        return self.current_session
    
    def start_debate(self, participants: List[Character]) -> None:
        """Start the debate session."""
        if not self.current_session:
            raise ValueError("No active debate session")
        
        self.current_session.start()
        self._conduct_debate(participants)
    
    def stop_debate(self) -> None:
        """Stop the current debate."""
        if self.current_session:
            self.current_session.stop()
    
    def pause_debate(self) -> None:
        """Pause the current debate."""
        if self.current_session:
            self.current_session.pause()
    
    def resume_debate(self, participants: List[Character]) -> None:
        """Resume a paused debate."""
        if self.current_session and self.current_session.status.value == "paused":
            self.current_session.resume()
            self._conduct_debate(participants, resume=True)
    
    def _assign_positions(self, participants: List[Character]) -> None:
        """Assign left/right positions to participants."""
        # Shuffle for randomness
        shuffled = participants.copy()
        random.shuffle(shuffled)
        
        # Split into left and right sides
        mid_point = len(shuffled) // 2
        
        for i, participant in enumerate(shuffled):
            if i < mid_point or (len(shuffled) % 2 == 1 and i == len(shuffled) - 1 and mid_point > len(shuffled) // 2):
                participant.position = "left"
            else:
                participant.position = "right"
    
    def _conduct_debate(self, participants: List[Character], resume: bool = False) -> None:
        """Main debate loop."""
        if not self.current_session:
            return
        
        settings = self.current_session.settings
        conversation = self.current_session.conversation
        
        # Starting round number for resume functionality
        start_round = len(conversation.rounds) if resume else 0
        
        # Create initial prompt
        current_message = create_topic_prompt(self.current_session.topic)
        
        for round_num in range(start_round, settings.total_rounds):
            if not self.current_session.is_running():
                break
            
            # Create new round
            debate_round = DebateRound(
                round_number=round_num + 1,
                start_time=datetime.now()
            )
            
            # Collect messages for this round
            round_messages = []
            
            # Each participant responds in this round
            for participant_index, participant in enumerate(participants):
                if not self.current_session.is_running():
                    break
                
                # Update progress
                total_responses = settings.total_rounds * len(participants)
                current_response = round_num * len(participants) + participant_index
                progress = current_response / total_responses
                
                if self.on_progress_update:
                    self.on_progress_update(progress, round_num + 1, participant.name)
                
                # Update character style for competitive mode
                if settings.competitive_mode:
                    participant.style = participant.get_dynamic_style()
                
                # Generate response
                try:
                    response = self._generate_character_response(
                        participant, current_message, conversation.get_messages_for_context()
                    )
                    
                    # Create debate message
                    message = DebateMessage(
                        round_number=round_num + 1,
                        speaker_name=participant.name,
                        message=response,
                        timestamp=datetime.now()
                    )
                    
                    # Add to round and conversation
                    debate_round.add_message(message)
                    round_messages.append(message)
                    
                    # Callback for UI update
                    if self.on_message_generated:
                        self.on_message_generated(message, participant)
                    
                    current_message = response
                    
                    # Delay between responses
                    if settings.response_delay > 0:
                        time.sleep(settings.response_delay)
                        
                except Exception as e:
                    # Handle AI generation errors gracefully
                    error_message = f"Error generating response: {str(e)}"
                    message = DebateMessage(
                        round_number=round_num + 1,
                        speaker_name=participant.name,
                        message=error_message,
                        timestamp=datetime.now(),
                        metadata={"error": True}
                    )
                    debate_round.add_message(message)
                    round_messages.append(message)
            
            # Finish the round
            debate_round.end_time = datetime.now()
            conversation.add_round(debate_round)
            
            # Judge the round in competitive mode
            if settings.competitive_mode and self.judge and round_messages:
                try:
                    judge_adjustments = self.judge.judge_round(round_messages, participants)
                    debate_round.judge_feedback = judge_adjustments
                    
                    # Apply adjustments to participants
                    for participant in participants:
                        if participant.name in judge_adjustments:
                            participant.adjust_stats(judge_adjustments[participant.name])
                    
                    if self.on_judge_feedback:
                        self.on_judge_feedback(judge_adjustments, round_num + 1)
                        
                except Exception as e:
                    # Handle judge errors gracefully
                    pass
            
            # Round completed callback
            if self.on_round_completed:
                self.on_round_completed(debate_round, round_num + 1)
            
            # Check if we should stop
            if not self.current_session.is_running():
                break
        
        # Complete the debate
        if self.current_session.is_running():
            self.current_session.complete()
            
            # Final performance evaluation
            if settings.competitive_mode and self.judge:
                try:
                    overall_performance = self.judge.judge_overall_performance(
                        participants, conversation.get_all_messages()
                    )
                    self.current_session.metadata["final_performance"] = overall_performance
                except Exception as e:
                    pass
            
            if self.on_session_completed:
                self.on_session_completed(self.current_session)
    
    def _generate_character_response(
        self, 
        character: Character, 
        current_message: str, 
        context_messages: List[DebateMessage]
    ) -> str:
        """Generate a response for a character."""
        # Build conversation context for AI
        context_for_ai = []
        
        # Add system message
        system_prompt = f"""
You are {character.name}, a {character.role}.
Personality: {character.personality}
Communication Style: {character.style}

**Instructions:**
- Stay in character and respond as this political analyst would.
- Be direct and critical.
- Use specific statistics, economic data, and theoretical frameworks.
- Cite empirical evidence and policy outcomes.
- Avoid unnecessary pleasantries, apologies, or gratitude.
- Focus on analytical critique and data-driven arguments.

**Critical Rules:**
1. Keep your response to a MAXIMUM of 50 words. Count carefully and stop before reaching the limit.
2. Use complete sentences as if you are speaking out loud.
3. You may use common texting abbreviations (e.g., lol, omg, tbh, fr, ngl, imo, btw, idk, smh, yk, etc.).
4. Make your response sound natural and conversational.
5. ALWAYS finish your response with a complete sentence—never cut off mid-thought.
6. DO NOT start your response with 'lol'—be expressive and in-character from the first word.
7. Get angry, passionate, and emotional as needed to fit your caricature—don't hold back on expressing strong opinions and reactions.

**Output Requirements:**
- Output plain text only.
- Do NOT use HTML, Markdown, or code fences.
"""
        
        context_for_ai.append({
            "role": "system",
            "content": system_prompt
        })
        
        # Add conversation history
        for msg in context_messages[-6:]:  # Last 6 messages for context
            role = "user" if msg.speaker_name != character.name else "assistant"
            context_for_ai.append({
                "role": role,
                "content": msg.message
            })
        
        # Add current message
        context_for_ai.append({
            "role": "user",
            "content": current_message
        })
        
        # Generate response using AI client
        response = self.ai_client.generate_response(context_for_ai)
        
        return response
    
    def get_session_summary(self) -> Optional[Dict[str, Any]]:
        """Get a summary of the current session."""
        if not self.current_session:
            return None
        
        conversation = self.current_session.conversation
        all_messages = conversation.get_all_messages()
        
        # Calculate statistics
        participant_stats = {}
        for participant_name in self.current_session.participants:
            participant_messages = [msg for msg in all_messages if msg.speaker_name == participant_name]
            participant_stats[participant_name] = {
                "message_count": len(participant_messages),
                "total_words": sum(len(msg.message.split()) for msg in participant_messages),
                "avg_words_per_message": sum(len(msg.message.split()) for msg in participant_messages) / max(len(participant_messages), 1)
            }
        
        return {
            "session_id": self.current_session.session_id,
            "topic": self.current_session.topic,
            "status": self.current_session.status.value,
            "total_rounds": len(conversation.rounds),
            "total_messages": len(all_messages),
            "duration": (conversation.end_time - conversation.start_time).total_seconds() if conversation.end_time else None,
            "participant_stats": participant_stats,
            "competitive_mode": self.current_session.settings.competitive_mode,
            "progress": self.current_session.get_progress()
        }
    
    def export_session(self) -> Optional[Dict[str, Any]]:
        """Export the current session for saving/sharing."""
        if not self.current_session:
            return None
        
        return self.current_session.to_dict()
    
    def import_session(self, session_data: Dict[str, Any]) -> DebateSession:
        """Import a session from exported data."""
        self.current_session = DebateSession.from_dict(session_data)
        return self.current_session