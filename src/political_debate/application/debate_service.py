import logging
import random
from typing import List, Dict, Any
from datetime import datetime

from ..domain.models import (
    Participant, Message, DebateSession, CharacterStats, 
    Position, JudgeAdjustment
)
from ..domain.character_factory import CharacterFactory
from ..infrastructure.openai_client import OpenAIService


class DebateService:
    """Application service for managing political debates"""
    
    def __init__(self, openai_api_key: str = None):
        self.character_factory = CharacterFactory()
        self.openai_service = OpenAIService(openai_api_key)
        self.logger = logging.getLogger(__name__)
    
    def create_debate_session(
        self, 
        topic: str, 
        selected_characters: List[str],
        rounds: int = 5,
        competitive_mode: bool = False
    ) -> DebateSession:
        """Create a new debate session with selected characters"""
        
        participants = []
        
        for char_key in selected_characters:
            try:
                if char_key == "democrat":
                    participant = self.character_factory.create_democrat()
                elif char_key == "republican":
                    participant = self.character_factory.create_republican()
                elif char_key == "random_american":
                    participant = self.character_factory.create_random_american()
                elif char_key == "random_redditor":
                    participant = self.character_factory.create_random_redditor()
                else:
                    participant = self.character_factory.create_additional_character(char_key)
                
                participants.append(participant)
                
            except Exception as e:
                self.logger.error(f"Failed to create character {char_key}: {str(e)}")
                continue
        
        if not participants:
            raise ValueError("No valid participants could be created")
        
        # Assign positions randomly
        self._assign_positions(participants)
        
        session = DebateSession(
            topic=topic,
            participants=participants,
            rounds=rounds,
            competitive_mode=competitive_mode
        )
        
        self.logger.info(f"Created debate session: {topic} with {len(participants)} participants")
        return session
    
    def conduct_round(
        self, 
        session: DebateSession, 
        round_number: int,
        current_message: str = None
    ) -> List[Message]:
        """Conduct a single round of debate"""
        
        if current_message is None:
            current_message = f"Let's discuss {session.topic}. What are your thoughts on this issue?"
        
        round_messages = []
        conversation_context = [msg.to_dict() for msg in session.messages]
        
        for participant in session.participants:
            try:
                # Update style for competitive mode
                if session.competitive_mode:
                    participant.style = self._get_dynamic_style(participant)
                
                # Generate response
                response = self.openai_service.generate_debate_response(
                    participant_name=participant.name,
                    participant_role=participant.role,
                    personality=participant.personality,
                    style=participant.style,
                    current_message=current_message,
                    conversation_context=conversation_context
                )
                
                # Create message
                message = Message(
                    speaker_name=participant.name,
                    content=response,
                    round_number=round_number
                )
                
                # Add to session and round
                session.add_message(message)
                round_messages.append(message)
                
                # Update current message for next participant
                current_message = response
                
                self.logger.debug(f"Generated response for {participant.name} in round {round_number}")
                
            except Exception as e:
                self.logger.error(f"Error generating response for {participant.name}: {str(e)}")
                continue
        
        # Judge the round if in competitive mode
        if session.competitive_mode and round_messages:
            self._judge_round(session, round_messages)
        
        self.logger.info(f"Completed round {round_number} with {len(round_messages)} messages")
        return round_messages
    
    def get_available_topics(self) -> List[str]:
        """Get list of available debate topics"""
        return self.character_factory.data.debate_topics
    
    def _assign_positions(self, participants: List[Participant]) -> None:
        """Randomly assign left/right positions to participants"""
        random.shuffle(participants)
        
        mid_point = len(participants) // 2
        left_speakers = participants[:mid_point]
        right_speakers = participants[mid_point:]
        
        # If odd number, assign extra to right
        if len(participants) % 2 == 1 and len(left_speakers) < len(right_speakers):
            left_speakers.append(right_speakers.pop())
        
        # Set positions
        for participant in left_speakers:
            participant.position = Position.LEFT
        for participant in right_speakers:
            participant.position = Position.RIGHT
    
    def _get_dynamic_style(self, participant: Participant) -> str:
        """Generate dynamic style based on current stats"""
        base_style = participant.style
        
        # Modify style based on anger level
        if participant.stats.anger > 70:
            base_style += ", EXTREMELY ANGRY and hostile"
        elif participant.stats.anger > 50:
            base_style += ", noticeably heated and aggressive"
        elif participant.stats.anger < 30:
            base_style += ", remarkably calm and composed"
        
        # Modify based on patience level  
        if participant.stats.patience < 30:
            base_style += ", impatient and quick to interrupt"
        elif participant.stats.patience > 70:
            base_style += ", very patient and thoughtful"
        
        # Modify based on uniqueness
        if participant.stats.uniqueness > 70:
            base_style += ", highly creative and original in arguments"
        elif participant.stats.uniqueness < 30:
            base_style += ", tends to repeat common talking points"
        
        return base_style
    
    def _judge_round(self, session: DebateSession, round_messages: List[Message]) -> None:
        """Judge a round and adjust participant stats"""
        
        try:
            # Convert messages to format expected by OpenAI service
            round_msg_data = [
                {"speaker": msg.speaker_name, "message": msg.content}
                for msg in round_messages
            ]
            
            # Get judge feedback
            adjustments = self.openai_service.generate_judge_feedback(
                round_msg_data, session.participants
            )
            
            # Apply adjustments
            for participant in session.participants:
                if participant.name in adjustments:
                    adjustment_data = adjustments[participant.name]
                    participant.stats.adjust(adjustment_data)
                    self.logger.debug(f"Applied stats adjustment to {participant.name}: {adjustment_data}")
            
        except Exception as e:
            self.logger.error(f"Error judging round: {str(e)}")


class ParticipantManager:
    """Service for managing debate participants"""
    
    def __init__(self):
        self.character_factory = CharacterFactory()
    
    def get_available_characters(self) -> Dict[str, Dict[str, Any]]:
        """Get available character types with metadata"""
        return {
            "main": {
                "democrat": {
                    "name": "Market Liberal Democrat",
                    "description": "Progressive economic policy expert",
                    "emoji": "🔵"
                },
                "republican": {
                    "name": "MAGA Nationalist", 
                    "description": "America First conservative",
                    "emoji": "🔴"
                }
            },
            "additional": {
                key: {
                    "name": data["name"],
                    "description": data["role"],
                    "emoji": self._get_character_emoji(key)
                }
                for key, data in self.character_factory.data.get_additional_characters().items()
            }
        }
    
    def _get_character_emoji(self, character_key: str) -> str:
        """Get emoji for character type"""
        emoji_map = {
            "random_american": "🗽",
            "random_redditor": "🤖", 
            "marxist_leninist": "☭",
            "anarcho_capitalist": "$",
            "catholic_theocrat": "⛪",
            "absolute_monarchist": "👑",
            "islamic_extremist": "☪️",
            "evangelist_preacher": "✝️",
            "master_baiter": "💪",
            "chinese_communist": "🇨🇳"
        }
        return emoji_map.get(character_key, "⚫")