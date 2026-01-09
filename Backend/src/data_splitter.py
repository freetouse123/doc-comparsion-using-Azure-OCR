"""
Data Splitter Module is used for splitting text into different chunks using the parents and child chunck
Based on the different pattern it will split the chunks.
"""
from typing import List, Dict
from config.config import DefaultConfig
import os
import json
import re

config = DefaultConfig()
logger = config.logger

class ParentChunk:
    def __init__(self):
        logger.info("Chunking initalization")
        pass

    def parent_chunk(self, text: str) -> Dict:
        """
        Split the input text into "parent chunks" based on the word 'Detailed BO' 
        and save them as a JSON file.
        """
        try:
            logger.info("Parent chunking started...")

            # Split the text by 'Detailed BO' (case-insensitive)
            parts = re.split(r'\s*Detailed\s+BO\s*', text, flags=re.IGNORECASE)
            parts = [chunk.strip() for chunk in parts if chunk.strip()]

            logger.info(f"Total parent chunks created: {len(parts)}")

            # Convert to dictionary {0: chunk0, 1: chunk1, ...}
            chunks_dict = {i: chunk for i, chunk in enumerate(parts)}

            # Write to JSON file
            with open(config.PARENT_CHUNK_FILE_PATH, "w", encoding="utf-8") as f:
                json.dump(chunks_dict, f, ensure_ascii=False, indent=4)

            logger.success(f"Parent chunks saved to {config.PARENT_CHUNK_FILE_PATH}")

            return chunks_dict

        except Exception as e:
            logger.error(f"Error in splitting the text into parent chunks: {e}")
            raise
    

    def child_chunk(self, text:str)-> List[str]:
        try:
            pass
        except Exception as e:
            logger.error(f"Error in child chunk:{e}")


class ChildChunking:
    def __init__(self):
        pass

    def extracting_entity(self, json_payload:dict):
        try:
            pass
        
        except Exception as e:
            logger.error(f"Error in extracting data from the json payload")