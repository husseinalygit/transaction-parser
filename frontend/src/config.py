import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from config.app_config import AppConfig

class Config(AppConfig):
    pass

# For backward compatibility
NER_SERVICE_URL = Config.NER_ENDPOINT
CLASSIFICATION_SERVICE_URL = Config.CLASSIFICATION_ENDPOINT
CHAT_URL = Config.CHAT_ENDPOINT
CSV_FILENAME = Config.CSV_FILENAME
CSV_PATH = Config.DATA_PATH
CATEGORIES = Config.CATEGORIES
