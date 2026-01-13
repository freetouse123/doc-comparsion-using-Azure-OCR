"""
Data Splitter Module is used for splitting text into different chunks using the parents and child chunck
Based on the different pattern it will split the chunks.
"""
from collections import defaultdict
from typing import List, Dict
from config.config import DefaultConfig
from utils.utils import normalize_text, detect_parent
import os
import json
import re

config = DefaultConfig()
logger = config.logger


class SOPDocumentChunking:
    """
    Parent Chunking class.
    """

    def __init__(self):
        pass

    @staticmethod
    def sop_doc_parent_chunk(text: str, Parent_chunk:List[str]) -> Dict:
        try:
            logger.info(f"parent chunk initialze for the SOP Documents")
            ALLOWED_PARENTS = Parent_chunk
            PARENT_KEYWORD = "ID - BO Description"
            
            text = normalize_text(text)
            
            lines = text.split("\n")
            print(len(lines))
            
            parent_chunks = defaultdict(list)
            current_parent = "MISCELLANEOUS"

            for line in lines:
                line = line.strip()
                if not line:
                    continue

                # Detect BO Description
                if PARENT_KEYWORD in line:
                    detected = detect_parent(line, ALLOWED_PARENTS=ALLOWED_PARENTS)
                    if detected:
                        current_parent = detected
                    else:
                        current_parent = "MISCELLANEOUS"

                parent_chunks[current_parent].append(line)

            
            parent_chunk = []
            parent_id = 1

            for parent_name, content_lines in parent_chunks.items():
                merged_text = "\n".join(content_lines).strip()

                parent_chunk.append({
                    "parent_chunk_id": parent_id,
                    "parent_chunk_name": parent_name,
                    "number_of_child_chunks_possible": len(content_lines),
                    "chunk_data": merged_text
                })

                parent_id += 1
            
            ## store the extract chunk into json files
            with open(
                config.FILE_PATH_FOR_SOP_PARENT_CHUNK,
                "w",
                encoding= "utf-8"
            ) as f:
                json.dump(parent_chunk,  f, indent=2, ensure_ascii=False)

            return parent_chunk
             
        except Exception as e:
            logger.error(f"Error in Generating Parent chunks for the SOP documents: {e}")
    
    @staticmethod
    def child_chunking(text:str)->Dict:
        try:
            id_pattern = re.compile(r"(F1M\d+/(?:[A-Z]+/)+[A-Z]+)")
            matches = list(id_pattern.finditer(text))

            child_chunks = []

            for i, match in enumerate(matches):
                chunk_id = match.group(1)

                start = match.end()
                end = matches[i + 1].start() if i + 1 < len(matches) else len(text)

                section_text = text[start:end].strip()

                # 🔑 Split name and data using " Active:"
                if " Active:" in section_text:
                    name_part, data_part = section_text.split(" Active:", 1)
                    name_of_child_chunk = name_part.strip()
                    child_chunk_data = "Active:" + data_part.strip()
                else:
                    # fallback (rare)
                    name_of_child_chunk = section_text.split()[0]
                    child_chunk_data = section_text[len(name_of_child_chunk):].strip()

                child_chunks.append({
                    "chunk_id": chunk_id,
                    "name_of_child_chunk": name_of_child_chunk,
                    "child_chunk_data": child_chunk_data
                })

            return child_chunks

        except Exception as e:
            logger.error(f"Error in Child chunking:{e}")


    @staticmethod
    def child_chunking_for_sop_doc(parent_chunk:Dict)-> Dict:
        try:
            final_output = []

            for parent in parent_chunk:
                parent_entry = {
                    "name_of_parent_chunk": parent.get("parent_chunk_name"),
                    "parent_chunk": parent.get("chunk_data"),
                    "child_chunks": SOPDocumentChunking.child_chunking(parent.get("chunk_data", ""))
                }
                final_output.append(parent_entry)
            
            with open(
                config.FILE_PATH_FOR_SOP_CHILD_CHUNK,
                "w",
                encoding= "utf-8"
            ) as f:
                json.dump(final_output,  f, indent=2, ensure_ascii=False)
            
            return final_output
        except Exception as e:
            logger.error(f"Error in Child chunking for the SOP documents:{e}")







class BMRDocumentChunking:

    def __init__(self):
        pass

    def bmr_doc_parent_chunk():
        try:
            pass
        except Exception as e:
            raise


    