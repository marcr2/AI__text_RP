from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from .models import DebateMessage, DebateRound
from ..characters.base import Character
import json


class DebateJudge(ABC):
    """Abstract base class for debate judges."""
    
    @abstractmethod
    def judge_round(self, round_messages: List[DebateMessage], participants: List[Character]) -> Dict[str, Dict[str, int]]:
        """Judge a round and return stat adjustments for each participant."""
        pass
    
    @abstractmethod
    def judge_overall_performance(self, participants: List[Character], conversation_history: List[DebateMessage]) -> Dict[str, Any]:
        """Judge overall performance across all rounds."""
        pass


class AIDebateJudge(DebateJudge):
    """AI-powered debate judge using external AI service."""
    
    def __init__(self, ai_client):
        """Initialize with AI client for making judgment calls."""
        self.ai_client = ai_client
    
    def judge_round(self, round_messages: List[DebateMessage], participants: List[Character]) -> Dict[str, Dict[str, int]]:
        """Judge a round using AI evaluation."""
        if not round_messages:
            return {p.name: {"anger": 0, "patience": 0, "uniqueness": 0} for p in participants}
        
        try:
            # Build context for the judge
            round_context = "\n".join([f"{msg.speaker_name}: {msg.message}" for msg in round_messages])
            
            judge_prompt = f"""You are an impartial debate judge evaluating a political debate round. Analyze the following responses and rate each participant on three metrics:

ROUND CONTEXT:
{round_context}

PARTICIPANTS: {[p.name for p in participants]}

For each participant, rate them on a scale of -10 to +10 for each category:

1. ANGER: How much their anger increased/decreased this round
   - Negative = they became calmer/more patient
   - Positive = they became more enraged/frustrated

2. PATIENCE: How much their patience changed this round  
   - Negative = they became more impatient/agitated
   - Positive = they became more patient/calm

3. UNIQUENESS: How unique/creative their argument was compared to others
   - Negative = repetitive or unoriginal points
   - Positive = fresh perspective or unique insights

Respond ONLY with a JSON object like this:
{{
  "Participant Name 1": {{"anger": 5, "patience": -3, "uniqueness": 2}},
  "Participant Name 2": {{"anger": -2, "patience": 4, "uniqueness": -1}}
}}

Be fair and consistent. Consider emotional escalation, argument quality, and originality."""

            # Make the AI call
            response = self.ai_client.generate_judge_response(judge_prompt)
            
            # Parse the JSON response
            try:
                adjustments = json.loads(response)
                return adjustments
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                return {p.name: {"anger": 0, "patience": 0, "uniqueness": 0} for p in participants}
                
        except Exception as e:
            # Return neutral adjustments if any error occurs
            return {p.name: {"anger": 0, "patience": 0, "uniqueness": 0} for p in participants}
    
    def judge_overall_performance(self, participants: List[Character], conversation_history: List[DebateMessage]) -> Dict[str, Any]:
        """Judge overall performance across the entire debate."""
        results = {}
        
        for participant in participants:
            participant_messages = [msg for msg in conversation_history if msg.speaker_name == participant.name]
            
            # Calculate basic metrics
            total_messages = len(participant_messages)
            avg_message_length = sum(len(msg.message) for msg in participant_messages) / max(total_messages, 1)
            
            # Get final stats
            final_stats = participant.stats.to_dict()
            
            # Calculate performance rating
            total_score = sum(final_stats.values())
            if total_score >= 240:
                performance = "EXCELLENT"
                rating = 5
            elif total_score >= 180:
                performance = "GOOD"
                rating = 4
            elif total_score >= 120:
                performance = "AVERAGE"
                rating = 3
            elif total_score >= 60:
                performance = "POOR"
                rating = 2
            else:
                performance = "VERY POOR"
                rating = 1
            
            results[participant.name] = {
                "final_stats": final_stats,
                "total_messages": total_messages,
                "avg_message_length": avg_message_length,
                "performance": performance,
                "rating": rating,
                "total_score": total_score
            }
        
        return results


class MockDebateJudge(DebateJudge):
    """Mock judge for testing purposes."""
    
    def __init__(self, fixed_adjustments: Optional[Dict[str, Dict[str, int]]] = None):
        """Initialize with optional fixed adjustments for predictable testing."""
        self.fixed_adjustments = fixed_adjustments
    
    def judge_round(self, round_messages: List[DebateMessage], participants: List[Character]) -> Dict[str, Dict[str, int]]:
        """Return fixed or random adjustments."""
        if self.fixed_adjustments:
            return self.fixed_adjustments.copy()
        
        # Return small random adjustments for testing
        import random
        adjustments = {}
        for participant in participants:
            adjustments[participant.name] = {
                "anger": random.randint(-3, 3),
                "patience": random.randint(-3, 3),
                "uniqueness": random.randint(-3, 3)
            }
        return adjustments
    
    def judge_overall_performance(self, participants: List[Character], conversation_history: List[DebateMessage]) -> Dict[str, Any]:
        """Return mock performance results."""
        results = {}
        for participant in participants:
            results[participant.name] = {
                "final_stats": participant.stats.to_dict(),
                "total_messages": len([msg for msg in conversation_history if msg.speaker_name == participant.name]),
                "avg_message_length": 50,  # Mock value
                "performance": "AVERAGE",
                "rating": 3,
                "total_score": 150
            }
        return results


class RuleBasedJudge(DebateJudge):
    """Rule-based judge that evaluates based on predefined criteria."""
    
    def __init__(self):
        """Initialize with rule-based criteria."""
        self.criteria = {
            "anger_triggers": ["CAPS", "!!!", "OUTRAGED", "FURIOUS", "ENRAGED"],
            "patience_indicators": ["calm", "measured", "thoughtful", "consider"],
            "uniqueness_indicators": ["innovative", "unique", "different approach", "fresh perspective"]
        }
    
    def judge_round(self, round_messages: List[DebateMessage], participants: List[Character]) -> Dict[str, Dict[str, int]]:
        """Judge based on text analysis rules."""
        adjustments = {}
        
        for participant in participants:
            participant_messages = [msg for msg in round_messages if msg.speaker_name == participant.name]
            
            anger_adjustment = 0
            patience_adjustment = 0
            uniqueness_adjustment = 0
            
            for message in participant_messages:
                text = message.message.upper()
                
                # Anger assessment
                anger_indicators = sum(1 for trigger in self.criteria["anger_triggers"] if trigger in text)
                if anger_indicators > 0:
                    anger_adjustment += min(anger_indicators * 2, 5)
                
                # Patience assessment
                patience_indicators = sum(1 for indicator in self.criteria["patience_indicators"] if indicator.upper() in text)
                if patience_indicators > 0:
                    patience_adjustment += min(patience_indicators, 3)
                
                # Uniqueness assessment
                uniqueness_indicators = sum(1 for indicator in self.criteria["uniqueness_indicators"] if indicator.upper() in text)
                if uniqueness_indicators > 0:
                    uniqueness_adjustment += min(uniqueness_indicators, 3)
                
                # Message length factor
                if len(message.message) > 100:
                    patience_adjustment -= 1  # Long messages indicate impatience
                
            adjustments[participant.name] = {
                "anger": anger_adjustment,
                "patience": patience_adjustment,
                "uniqueness": uniqueness_adjustment
            }
        
        return adjustments
    
    def judge_overall_performance(self, participants: List[Character], conversation_history: List[DebateMessage]) -> Dict[str, Any]:
        """Judge overall performance using rule-based criteria."""
        results = {}
        
        for participant in participants:
            participant_messages = [msg for msg in conversation_history if msg.speaker_name == participant.name]
            
            # Calculate metrics
            total_messages = len(participant_messages)
            total_words = sum(len(msg.message.split()) for msg in participant_messages)
            avg_words_per_message = total_words / max(total_messages, 1)
            
            # Analyze consistency
            message_lengths = [len(msg.message) for msg in participant_messages]
            length_variance = max(message_lengths) - min(message_lengths) if message_lengths else 0
            
            # Rate performance
            final_stats = participant.stats.to_dict()
            total_score = sum(final_stats.values())
            
            if total_score >= 200:
                performance = "EXCELLENT"
                rating = 5
            elif total_score >= 150:
                performance = "GOOD"
                rating = 4
            elif total_score >= 100:
                performance = "AVERAGE"
                rating = 3
            elif total_score >= 50:
                performance = "POOR"
                rating = 2
            else:
                performance = "VERY POOR"
                rating = 1
            
            results[participant.name] = {
                "final_stats": final_stats,
                "total_messages": total_messages,
                "avg_words_per_message": avg_words_per_message,
                "length_variance": length_variance,
                "performance": performance,
                "rating": rating,
                "total_score": total_score
            }
        
        return results


def create_judge(judge_type: str = "ai", **kwargs) -> DebateJudge:
    """Factory function to create different types of judges."""
    if judge_type == "ai":
        ai_client = kwargs.get("ai_client")
        if not ai_client:
            raise ValueError("AI client required for AI judge")
        return AIDebateJudge(ai_client)
    elif judge_type == "mock":
        return MockDebateJudge(kwargs.get("fixed_adjustments"))
    elif judge_type == "rule_based":
        return RuleBasedJudge()
    else:
        raise ValueError(f"Unknown judge type: {judge_type}")