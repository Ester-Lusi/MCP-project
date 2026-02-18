import os
from dotenv import load_dotenv

load_dotenv()

def build_settings():
    return {
        "file_storage_path": os.getenv("FILE_STORAGE_PATH", "/path/to/storage"),
        "log_level": os.getenv("LOG_LEVEL", "INFO")
    }

def get_default_env_path():
    return os.getenv("ENV_PATH", ".env")
