import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration class"""
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    PORT = int(os.getenv('FLASK_PORT', '5000'))

    @staticmethod
    def validateGemini():
        """Validate required configuration variables"""
        if not Config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY environment variable is not set")

    @staticmethod
    def validateOpenAI():
        """Validate required configuration variables for OpenAI"""
        if not Config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is not set") 
