import requests
from app.core.config import Config
from app.core.constants import CATEGORIES
from duckduckgo_search import DDGS
import json

def dict_to_string(d):
    return "\n".join([f"{k} : {v}" for k, v in d.items()])

class ClassificationService:
    def __init__(self):
        self.server_url = Config.OLLAMA_URL
        self.llm_name = Config.LLM_NAME

    def _search_store(self, store_name):
        if not store_name:
            return []
        try:
            results = DDGS().text(store_name, max_results=5)
            return [{
                "name": item.get("title", ""),
                "snippet": item.get("body", ""),
                "url": item.get("link", "")
            } for item in results]
        except Exception as e:
            print(f"Search error: {str(e)}")
            return []

    def classify_transaction(self, transaction, model = None):
        # Add store search results to transaction
        store_search = self._search_store(transaction.get("store"))
        transaction["store_search"] = store_search

        # Prepare classification request
        request_body = {
            "model": self.llm_name,
            "prompt": self._build_prompt(transaction),
            "stream": False,
            "format": {"type": "object"},
            "properties": {
                "code": {"type": "int"},
                "label": {"type": "str"},
                "reason": {"type": "str"},
                "required": ["code", "label", "reason"]
            },
            "options": {
                "temperature": 0.0,
                "seed": 0
            }
        }

        # Make request to Ollama
        response = requests.post(self.server_url, json=request_body)
        json_response = response.json()
        json_response['response_json'] = json.loads(json_response['response'])
        json_response['llm'] = self.llm_name
        json_response['transaction'] = transaction
        
        return json_response

    def _build_prompt(self, transaction):
        return f""" Given the following categories, their description and code : 
        {dict_to_string(CATEGORIES)}
        And the following transcation infomration including the amount, sotre name, and the top5 web search results for the store name:
        {dict_to_string(dict(transaction))}
        *TASK* : Classify the transaction into the correct category (choose from the provided ones), and provide the category label, transaction code, and why it was classified as such. Send the in following format :
        Label : transaction category
        Code : transaction code
        Reason : why it was classified as such"""