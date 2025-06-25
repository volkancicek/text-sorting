import logging
from openai import OpenAI
from config.config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def classify_text(text: str) -> str:
    """
    Classify text using OpenAI GPT model.
    Args:
        text (str): Input text to classify
    Returns:
        str: Classification result
    Raises:
        Exception: If there's an error in text classification
    """
    try:
        Config.validateOpenAI()
        client = OpenAI(api_key=Config.OPENAI_API_KEY)
        prompt = (
            "Give a category for each comment with an adjective. "
            "Try to create groups for the categories you created. "
            "Create output in csv format, first write your groups and the number of the comments in each group. "
            f"Then, write each comment with the category and group you assign: {text}"
        )
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an issue classification expert."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        logger.error(f"Error classifying text: {str(e)}")
        raise
