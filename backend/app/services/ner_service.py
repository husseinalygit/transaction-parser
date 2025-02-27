import requests
from app.core.config import Config
import json

class NERService:
    def __init__(self):
        self.server_url = Config.OLLAMA_URL
        self.llm_name = Config.LLM_NAME

    def extract_entities(self, message):
        try:
            # Prepare NER request
            request_body = {
                "model": self.llm_name,
                "prompt": self._build_prompt(message),
                "stream": False,
                "format": {"type": "object",},
                "properties": {
                        "amount": {"type": "str"},
                        "balance": {"type": "str"},
                        "store": {"type": "str"},
                        "date": {"type": "str"},
                        "time": {"type": "str"}, 
                        "required": [
                                     "amount", 
                                    "balance", 
                                    "store", 
                                    "date", 
                                    "time"]}, 
                "options": {
                    "temperature": 0.0, 
                    "seed": 0
                }
            }

            # Make request to Ollama
            response = requests.post(self.server_url, json=request_body)
            results = response.json()
            results['response_json'] = json.loads(results['response'])
            results['llm'] = self.llm_name
            return results
        except Exception as e:
            print(f"NER error: {str(e)}")
            raise

    def _build_prompt(self, message):
        return f"""Extract the following entities from this message:
        - amount (transaction amount)
        - balance (remaining balance)
        - store (merchant or store name)
        - date (transaction date)
        - time (transaction time)

        Message: {message}

        Return the extracted entities in JSON format.""" 