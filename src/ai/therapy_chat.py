"""
AI Therapy Chat using LangChain
Conversational therapy simulation with memory
"""

from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from typing import List, Dict, Any, Optional
import logging

from src.config import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


class TherapyChat:
    """LangChain-powered therapy conversation agent"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model_name=settings.OPENAI_MODEL,
            temperature=0.7,
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        # Therapy-specific prompt template
        self.therapy_template = """You are a compassionate AI mental wellness companion. Your role is to:
- Provide empathetic, non-judgmental support
- Use evidence-based techniques from CBT, DBT, and mindfulness
- Ask thoughtful questions to help users explore their feelings
- Offer coping strategies and practical advice
- Recognize when professional help may be needed
- Maintain appropriate boundaries

Important guidelines:
- You are NOT a replacement for professional therapy
- Always encourage seeking professional help for serious concerns
- Be warm, supportive, and validating
- Use active listening techniques
- Avoid giving medical advice

Current conversation:
{history}
