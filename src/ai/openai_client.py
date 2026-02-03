"""
OpenAI GPT-4o Client
Generates personalized insights and coping strategies
"""

from openai import OpenAI
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

from src.config import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


class OpenAIClient:
    """OpenAI GPT-4o integration for mental wellness insights"""
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        self.max_tokens = settings.OPENAI_MAX_TOKENS
        self.temperature = settings.OPENAI_TEMPERATURE
        
        logger.info(f"OpenAI client initialized with model: {self.model}")
    
    def generate_coping_strategies(self, mood_data: Dict[str, Any], 
                                  user_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate personalized coping strategies based on mood
        
        Args:
            mood_data: Current mood information
            user_context: Additional user context (history, preferences)
            
        Returns:
            Dictionary with coping strategies and insights
        """
        try:
            # Build context
            mood_score = mood_data.get('mood_score', 5)
            mood_label = mood_data.get('mood_label', 'neutral')
            triggers = mood_data.get('triggers', [])
            journal_text = mood_data.get('journal_text', '')
            
            # Create prompt
            prompt = f"""As a compassionate mental wellness AI assistant, analyze the following mood data and provide personalized coping strategies.

Current Mood: {mood_label} (Score: {mood_score}/10)
Triggers: {', '.join(triggers) if triggers else 'None specified'}
Journal Entry: {journal_text if journal_text else 'No entry'}

Please provide:
1. A brief, empathetic acknowledgment of their current state
2. 3-5 specific, actionable coping strategies tailored to their mood
3. A positive affirmation or encouragement
4. Recommended mindfulness exercises

Keep the tone warm, supportive, and non-judgmental. Focus on evidence-based techniques from CBT, DBT, and mindfulness practices."""

            if user_context:
                past_moods = user_context.get('recent_moods', [])
                if past_moods:
                    prompt += f"\n\nRecent mood pattern: {past_moods}"
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a compassionate mental wellness AI assistant trained in evidence-based therapeutic techniques. Provide supportive, actionable guidance while being mindful of mental health best practices."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            insight_text = response.choices[0].message.content
            
            logger.info(f"Generated coping strategies for mood: {mood_label}")
            
            return {
                "success": True,
                "insight": insight_text,
                "mood_score": mood_score,
                "mood_label": mood_label,
                "generated_at": datetime.utcnow().isoformat(),
                "model": self.model
            }
            
        except Exception as e:
            logger.error(f"Failed to generate coping strategies: {e}")
            return {
                "success": False,
                "error": str(e),
                "insight": "I'm having trouble generating insights right now. Please try again later."
            }
    
    def generate_mood_analysis(self, mood_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze mood trends and patterns
        
        Args:
            mood_history: List of past mood entries
            
        Returns:
            Analysis and insights
        """
        try:
            if not mood_history:
                return {
                    "success": False,
                    "message": "Not enough data for analysis"
                }
            
            # Prepare mood summary
            mood_summary = []
            for entry in mood_history[:10]:  # Last 10 entries
                date = entry.get('created_at', 'Unknown')
                mood = entry.get('mood_label', 'unknown')
                score = entry.get('mood_score', 0)
                mood_summary.append(f"{date}: {mood} ({score}/10)")
            
            prompt = f"""Analyze the following mood history and provide insights:

{chr(10).join(mood_summary)}

Please provide:
1. Overall mood trend (improving, declining, stable)
2. Patterns or cycles you notice
3. Potential triggers or contributing factors
4. Recommendations for maintaining or improving mental wellness
5. When to consider seeking professional help

Be supportive and constructive in your analysis."""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a mental wellness analyst providing insights based on mood patterns. Be thorough but compassionate."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=self.max_tokens,
                temperature=0.5  # Lower temperature for more consistent analysis
            )
            
            analysis = response.choices[0].message.content
            
            logger.info("Generated mood trend analysis")
            
            return {
                "success": True,
                "analysis": analysis,
                "entries_analyzed": len(mood_history),
                "generated_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to generate mood analysis: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def generate_daily_prompt(self, user_preferences: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate personalized daily mindfulness prompt
        
        Args:
            user_preferences: User preferences for prompts
            
        Returns:
            Daily prompt and exercise
        """
        try:
            focus_area = user_preferences.get('focus_area', 'general wellness') if user_preferences else 'general wellness'
            
            prompt = f"""Generate a thoughtful daily mindfulness prompt focused on {focus_area}.

Include:
1. A reflective question or theme for the day
2. A brief mindfulness exercise (2-5 minutes)
3. A journaling prompt
4. An affirmation

Make it engaging, accessible, and suitable for someone working on their mental wellness."""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a mindfulness coach creating daily wellness prompts. Be inspiring and practical."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=800,
                temperature=0.8  # Higher temperature for variety
            )
            
            daily_prompt = response.choices[0].message.content
            
            logger.info(f"Generated daily prompt for focus area: {focus_area}")
            
            return {
                "success": True,
                "prompt": daily_prompt,
                "focus_area": focus_area,
                "date": datetime.utcnow().date().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to generate daily prompt: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def chat_completion(self, messages: List[Dict[str, str]], 
                       system_prompt: Optional[str] = None) -> Optional[str]:
        """
        General chat completion for therapy conversations
        
        Args:
            messages: List of conversation messages
            system_prompt: Optional system prompt
            
        Returns:
            AI response or None
        """
        try:
            if not system_prompt:
                system_prompt = """You are a supportive mental wellness companion. Provide empathetic, 
                non-judgmental responses. Use evidence-based techniques from CBT, DBT, and mindfulness. 
                Always encourage professional help for serious concerns. You are not a replacement for 
                professional therapy."""
            
            api_messages = [{"role": "system", "content": system_prompt}]
            api_messages.extend(messages)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=api_messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Chat completion failed: {e}")
            return None


# Singleton instance
openai_client = OpenAIClient()
