from dotenv import load_dotenv
import os

load_dotenv()

class AppConfig:
    # Server Configuration
    SERVER_HOST = "backend"
    SERVER_PORT = 5000
    
    # LLM Configuration
    LLM_NAME = "qwen2.5-coder:1.5b"
    OLLAMA_URL = "http://ollama:11434/api/generate"
    OLLAMA_BASE_URL = "http://ollama:11434"
    # Data Storage
    DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data/")
    CSV_FILENAME = "app_data.csv"
    
    # API Endpoints
    API_BASE_URL = f"http://{SERVER_HOST}:{SERVER_PORT}"
    NER_ENDPOINT = f"{API_BASE_URL}/ner"
    CLASSIFICATION_ENDPOINT = f"{API_BASE_URL}/classify"
    CHAT_ENDPOINT = f"{API_BASE_URL}/chat"
    
    # Transaction Categories
    CATEGORIES = {
        "Restaurants": {"description": "Expenses from restaurants, and delivery apps", "code": 1},
        "Groceries": {"description": "Expenses from grocery stores, shoping centers, super markets and hypermarkets", "code": 2},
        "Transportation": {"description": "Expenses related to transportation, such as fuel, public transportation, and taxi services, car maintainince", "code": 3},
        "Donations and Gifts": {"description": "Expenses related to donations and charity", "code": 4},
        "Health and Fitness": {"description": "Expenses related to health, such as medical services, pharmacies, and health insurance, and gym", "code": 5},
        "Fees and Subscriptions": {"description": "Expenses related to subscription services, such as streaming platforms, software, and online services", "code": 6},
    } 