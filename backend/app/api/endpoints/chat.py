from flask import request, jsonify
from app.services.chat_service import ChatService

chat_service = ChatService()

def chat_endpoint():
    try:
        data = request.get_json()
        if not data or "query" not in data:
            return jsonify({"error": "Missing message in request data"}), 400
        
        response = chat_service.process_query(data["query"])
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({
            "error": "Failed to process response",
            "details": str(e)
        }), 500 