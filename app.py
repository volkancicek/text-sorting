import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from config.config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Validate and load configuration
Config.validate()

# Configure Gemini
genai.configure(api_key=Config.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

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
        prompt = (
            "You are an issue classification expert. "
            "Give a category for each comment with an adjective. "
            "Try to create groups for the categories you created. "
            "In the output, first write your groups and the number of the comments in each group. "
            f"Then, write each comment with the category and group you assign in this format user_name-comment-category-group: {text}"
        )
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logger.error(f"Error classifying text: {str(e)}")
        raise

@app.route('/api/classify', methods=['POST'])
def classify_text_api():
    """API endpoint for text classification"""
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({
                'error': 'Missing required field: text'
            }), 400
            
        text = data['text']
        if not isinstance(text, str) or not text.strip():
            return jsonify({
                'error': 'Invalid text: must be a non-empty string'
            }), 400
            
        result = classify_text(text)
        return jsonify({'result': result})
        
    except Exception as e:
        logger.error(f"API error: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    logger.info(f"Starting Flask server on {Config.HOST}:{Config.PORT}")
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    ) 