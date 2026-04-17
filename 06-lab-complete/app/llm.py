import google.generativeai as genai
import logging
from .config import settings

logger = logging.getLogger(__name__)

def ask_gemini(question: str) -> tuple[str, str]:
    """Gọi thực tế tới Gemini API với cơ chế Fallback."""
    if not settings.gemini_api_key:
        return "⚠️ Gemini API Key not set. Please configure GEMINI_API_KEY.", "none"

    genai.configure(api_key=settings.gemini_api_key)
    
    # Danh sách model thử nghiệm theo thứ tự ưu tiên
    models_to_try = [settings.llm_model] + settings.fallback_models
    last_error = ""

    for model_name in models_to_try:
        if not model_name: continue
        
        try:
            logger.info(f"Attempting Gemini call with model: {model_name}")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(question)
            
            if response and response.text:
                return response.text, model_name
                
        except Exception as e:
            error_msg = str(e)
            last_error = error_msg
            # Nếu là lỗi Quota (429), tiếp tục thử model tiếp theo
            if "429" in error_msg or "quota" in error_msg.lower():
                logger.warning(f"Model {model_name} hit quota limit. Trying next fallback...")
                continue
            
            # Nếu là lỗi khác (ví dụ: Invalid Model Name), log và thử tiếp
            logger.error(f"Error with model {model_name}: {error_msg}")
            continue

    # Nếu tất cả đều thất bại
    if "429" in last_error or "quota" in last_error.lower():
        return "⚠️ Tất cả các model đều đang quá tải hoặc hết hạn mức (Quota). Vui lòng thử lại sau.", "none"
    
    return f"Error calling Gemini after trying all models. Last error: {last_error}", "none"

def ask_mock(question: str) -> tuple[str, str]:
    """Mock LLM fallback."""
    return f"This is a mock response to: '{question}'", "mock-v1"

def ask(question: str) -> tuple[str, str]:
    """Router cho LLM calls dựa trên config."""
    if settings.gemini_api_key:
        return ask_gemini(question)
    return ask_mock(question)
