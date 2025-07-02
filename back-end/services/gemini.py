import logging
import google.generativeai as genai
from config.config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def classify_text(text: str) -> str:
    """
    Classify text using Gemini AI model.
    Args:
        text (str): Input text to classify
    Returns:
        str: Classification result
    Raises:
        Exception: If there's an error in text classification
    """
    try:
        Config.validateGemini()
        genai.configure(api_key=Config.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = (
            "You are an issue classification expert. "
            "Give a category for each comment with an adjective. "
            "Try to create groups for the categories you created. "
            "Create output in csv format, first write your groups and the number of the comments in each group. "
            f"Then, write each comment with the category and group you assign: {text}"
        )

        tokenResponse = model.count_tokens(prompt)
        logger.info(f"Total tokens in the prompt: {tokenResponse.total_tokens}")

        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logger.error(f"Error classifying text: {str(e)}")
        raise
