from utils.logger import Logger
import tomllib
import os

backend_dir = os.path.dirname(os.path.dirname(__file__))
LOG_FILE_PATH = os.path.join(backend_dir, "logs", "app.logs")
PARENT_CHUNK_DIR = os.path.join(backend_dir, "artifact", "parent_chunks")
CHILD_CHUNK_DIR = os.path.join(backend_dir, "artifact", "child_chunks")

os.makedirs(PARENT_CHUNK_DIR, exist_ok=True)
os.makedirs(CHILD_CHUNK_DIR, exist_ok=True)
os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)

class DefaultConfig:
    PROMPTS = tomllib.load(open(os.path.join(os.path.dirname(__file__), "prompts.toml"), "rb"))
    logger = Logger(name="doument_comparator", log_file=LOG_FILE_PATH, log_to_file=True)
    FILE_PATH_FOR_SOP_PARENT_CHUNK = os.path.join(PARENT_CHUNK_DIR, "parent_chunks_for_sop.json")
    FILE_PATH_FOR_BMR_PARENT_CHUNK = os.path.join(PARENT_CHUNK_DIR, "parent_chunks_for_bmr.json")
    FILE_PATH_FOR_SOP_CHILD_CHUNK = os.path.join(CHILD_CHUNK_DIR, "child_chunks_for_sop.json")
