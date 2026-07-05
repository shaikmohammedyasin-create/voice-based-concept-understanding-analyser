# VBCUA Settings Configuration
import os

APP_NAME = "Voice-Based Concept Understanding Analyser"
VERSION = "1.0.0"
MAX_AUDIO_SIZE_MB = 25
DEFAULT_HISTORY_LIMIT = 15
CONCEPTS_FILE_PATH = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "concepts.json"))
