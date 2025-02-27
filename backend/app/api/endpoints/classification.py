from flask import request, jsonify
from app.services.classification_service import ClassificationService

classification_service = ClassificationService()

def classify_endpoint():
    try:
        data = request.get_json()
        if not data or "transaction" not in data:
            return jsonify({"error": "Missing required keys in request data"}), 400

        result = classification_service.classify_transaction(data["transaction"])
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "error": "Failed to process classification",
            "details": str(e)
        }), 500 