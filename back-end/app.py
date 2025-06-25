import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from config.config import Config
from services.gemini import classify_text as gemini_classify_text
from services.openai import classify_text as openai_classify_text

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Model handler registry for extensibility
MODEL_HANDLERS = {
    'gemini': gemini_classify_text,
    'openai': openai_classify_text,
}

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
        model = data.get('model', 'gemini')
        if not isinstance(text, str) or not text.strip():
            return jsonify({
                'error': 'Invalid text: must be a non-empty string'
            }), 400
        
        logger.info(f"/api/classify called | model: {model} | text preview: {text[:100]}")
        handler = MODEL_HANDLERS.get(model, MODEL_HANDLERS['gemini'])
        result = handler(text)
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
