import google.generativeai as genai
import logging
from .config import settings

logger = logging.getLogger(__name__)

def ask_gemini(question: str) -> str:
    """Gọi thực tế tới Gemini API."""
    if not settings.gemini_api_key:
        return "⚠️ Gemini API Key not set. Please configure GEMINI_API_KEY."

    try:
        genai.configure(api_key=settings.gemini_api_key)
        model = genai.GenerativeModel(settings.llm_model)
        
        response = model.generate_content(question)
        
        if response and response.text:
            return response.text
        return "Empty response from Gemini."
        
    except Exception as e:
        logger.error(f"Gemini API Error: {str(e)}")
        return f"Error calling Gemini: {str(e)}"

def ask_mock(question: str) -> str:
    """Mock LLM fallback."""
    return f"This is a mock response to: '{question}'"

def ask(question: str) -> str:
    """Router cho LLM calls dựa trên config."""
    if settings.gemini_api_key:
        return ask_gemini(question)
    return ask_mock(question)
