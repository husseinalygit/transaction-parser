import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from config.app_config import AppConfig

class Config(AppConfig):
    pass
