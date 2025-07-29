import os
import logging
from typing import List, Dict, Any, Optional
from openai import OpenAI


class OpenAIService:
    """Service for handling OpenAI API communication"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY environment variable.")
        
        self.client = self._create_client()
        self.logger = logging.getLogger(__name__)
    
    def _create_client(self) -> OpenAI:
        """Create OpenAI client with clean environment"""
        # Create a clean environment for OpenAI client
        clean_env = os.environ.copy()
        
        # Remove all proxy-related environment variables
        proxy_vars = [
            "HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy", 
            "NO_PROXY", "no_proxy"
        ]
        for var in proxy_vars:
            if var in clean_env:
                del clean_env[var]
        
        # Set API key in environment
        clean_env["OPENAI_API_KEY"] = self.api_key
        
        return OpenAI(api_key=self.api_key)
    
    def generate_debate_response(
        self, 
        participant_name: str,
        participant_role: str,
        personality: str,
        style: str,
        current_message: str,
        conversation_context: List[Dict[str, Any]],
        max_words: int = 50
    ) -> str:
        """Generate a debate response for a participant"""
        
        try:
            # Build conversation context
            context_messages = self._build_context_messages(
                participant_name, participant_role, personality, style,
                current_message, conversation_context, max_words
            )
            
            self.logger.debug(f"Generating response for {participant_name}")
            self.logger.debug(f"Context messages: {context_messages}")
            
            # Make API call
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=context_messages,
                max_tokens=150,
                temperature=0.7
            )
            
            result = response.choices[0].message.content.strip()
            
            self.logger.debug(f"Generated response for {participant_name}: {result}")
            return result
            
        except Exception as e:
            self.logger.error(f"Error generating response for {participant_name}: {str(e)}")
            return f"Error: Failed to generate response - {str(e)}"
    
    def generate_judge_feedback(
        self, 
        round_messages: List[Dict[str, str]], 
        participants: List[Any]
    ) -> Dict[str, Dict[str, int]]:
        """Generate judge feedback for competitive mode"""
        
        try:
            # Build judge prompt
            judge_prompt = self._build_judge_prompt(round_messages, participants)
            
            self.logger.debug("Generating judge feedback")
            self.logger.debug(f"Judge prompt: {judge_prompt}")
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": """You are an impartial AI judge evaluating debate performance. 
                        For each participant, provide stat adjustments between -10 and +10 for:
                        - anger (how heated/emotional they became)
                        - patience (how calm/composed they remained)  
                        - uniqueness (how original/interesting their arguments were)
                        
                        Format your response EXACTLY as JSON:
                        {"ParticipantName": {"anger": X, "patience": Y, "uniqueness": Z}}"""
                    },
                    {"role": "user", "content": judge_prompt}
                ],
                max_tokens=500,
                temperature=0.3
            )
            
            judge_response = response.choices[0].message.content.strip()
            self.logger.debug(f"Judge response: {judge_response}")
            
            # Parse judge response
            import json
            try:
                adjustments = json.loads(judge_response)
                self.logger.debug(f"Parsed judge adjustments: {adjustments}")
                return adjustments
            except json.JSONDecodeError:
                self.logger.error(f"Failed to parse judge response as JSON: {judge_response}")
                return {}
            
        except Exception as e:
            self.logger.error(f"Error generating judge feedback: {str(e)}")
            return {}
    
    def _build_context_messages(
        self,
        participant_name: str,
        participant_role: str, 
        personality: str,
        style: str,
        current_message: str,
        conversation_context: List[Dict[str, Any]],
        max_words: int
    ) -> List[Dict[str, str]]:
        """Build context messages for API call"""
        
        context_messages = [
            {
                "role": "system",
                "content": f"""
You are {participant_name}, a {participant_role}.
Personality: {personality}
Communication Style: {style}

**Instructions:**
- Stay in character and respond as this political analyst would.
- Be direct and critical.
- Use specific statistics, economic data, and theoretical frameworks.
- Cite empirical evidence and policy outcomes.
- Avoid unnecessary pleasantries, apologies, or gratitude.
- Focus on analytical critique and data-driven arguments.

**Critical Rules:**
1. Keep your response to a MAXIMUM of {max_words} words. Count carefully and stop before reaching the limit.
2. Use complete sentences as if you are speaking out loud.
3. Never break character or mention being an AI.
4. Respond directly to the most recent message.
"""
            }
        ]
        
        # Add conversation history (last 5 messages to maintain context)
        recent_context = conversation_context[-5:] if len(conversation_context) > 5 else conversation_context
        for msg in recent_context:
            context_messages.append({
                "role": "user",
                "content": f"{msg['speaker']}: {msg['message']}"
            })
        
        # Add current message
        context_messages.append({
            "role": "user", 
            "content": f"Respond to this: {current_message}"
        })
        
        return context_messages
    
    def _build_judge_prompt(
        self, 
        round_messages: List[Dict[str, str]], 
        participants: List[Any]
    ) -> str:
        """Build prompt for judge evaluation"""
        
        prompt = "Evaluate this debate round:\n\n"
        
        for msg in round_messages:
            prompt += f"{msg['speaker']}: {msg['message']}\n\n"
        
        prompt += "\nParticipants:\n"
        for p in participants:
            name = getattr(p, 'name', p.get('name', 'Unknown'))
            prompt += f"- {name}\n"
        
        prompt += "\nProvide stat adjustments for each participant based on their performance."
        
        return prompt