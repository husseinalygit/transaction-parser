from flask import request, jsonify
from app.services.ner_service import NERService

ner_service = NERService()

def ner_endpoint():
    try:
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"error": "Missing message in request data"}), 400
            
        result = ner_service.extract_entities(data["message"])
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "error": "Failed to process NER",
            "details": str(e)
        }), 500 