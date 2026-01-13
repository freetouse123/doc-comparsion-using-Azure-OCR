from utils.logger import Logger
import tomllib
import os

LOG_FILE_PATH = os.path.join("logs", "app.logs")
PARENT_CHUNK_DIR = r"Backend\artifact\parent_chunks"

os.makedirs(PARENT_CHUNK_DIR, exist_ok=True)  

class DefaultConfig:
    PROMPTS = tomllib.load(open(os.path.join(os.path.dirname(__file__), "prompts.toml"), "rb"))
    logger = Logger(name= "data_extraction", log_file=LOG_FILE_PATH, log_to_file=True) 
    FILE_PATH_FOR_SOP_PARENT_CHUNK = os.path.join(PARENT_CHUNK_DIR, "parent_chunks_for_sop.json")
    FILE_PATH_FOR_BMR_PARENT_CHUNK = os.path.join(PARENT_CHUNK_DIR, "parent_chunks_for_bmr.json")
