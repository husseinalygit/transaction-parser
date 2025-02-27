from flask import Blueprint
from app.api.endpoints import chat, classification, ner

api_bp = Blueprint('api', __name__)

# Register routes
api_bp.add_url_rule('/chat', view_func=chat.chat_endpoint, methods=['POST'])
api_bp.add_url_rule('/classify', view_func=classification.classify_endpoint, methods=['POST'])
api_bp.add_url_rule('/ner', view_func=ner.ner_endpoint, methods=['POST'])

def health_check():
    return {"status": "healthy"}, 200 