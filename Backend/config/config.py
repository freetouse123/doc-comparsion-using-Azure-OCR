from utils.logger import Logger
import tomllib
import os

LOG_FILE_PATH = os.path.join("logs", "app.logs")
PARENT_CHUNK_DIR = "artifact"

os.makedirs(PARENT_CHUNK_DIR, exist_ok=True)  

class DefaultConfig:
    PROMPTS = tomllib.load(open(os.path.join(os.path.dirname(__file__), "prompts.toml"), "rb"))
    logger = Logger(name= "data_extraction", log_file=LOG_FILE_PATH, log_to_file=True) 
    PARENT_CHUNK_FILE_PATH = os.path.join(PARENT_CHUNK_DIR, "parent_chunk.json")
