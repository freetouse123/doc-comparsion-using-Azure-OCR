"""
Main function for the implemeting the both SOP and BMR 
"""
from src.data_cleaning import DataCleaning
from src.data_extraction import DataExtraction
from src.data_splitter import SOPDocumentChunking
from utils.converter import convert_word_to_pdf_bytes
from utils.helper import time_decorator
from config.config import DefaultConfig


from pathlib import Path

logger = DefaultConfig().logger


class Pipeline:

    def __init__(self, sop_file_path, bmr_file_path):
        self.sop_file_path = sop_file_path
        self.bmr_file_path = bmr_file_path
        self.data_cleaning = DataCleaning()
        self.data_extraction = DataExtraction()
        self.sop_splitter = SOPDocumentChunking()
    
        if not self.sop_file_path.lower().endswith(".pdf"):
            logger.warning("Warning: SOP Files does not have a .pdf extension.")
            self.sop_file_path_bytes = convert_word_to_pdf_bytes(self.sop_file_path)

        else:

            logger.info("Pdf files founded......")
            with open(sop_file_path, "rb") as f:
                self.sop_file_path_bytes = f.read()
        

        if not self.bmr_file_path.lower().endswith(".pdf"):
            logger.warning("Warning: BMR Files does not have a .pdf extension.")
            self.bmr_file_path_bytes = convert_word_to_pdf_bytes(self.bmr_file_path)

        else:
            logger.info("Pdf files founded......")
            with open(self.bmr_file_path, "rb") as f:
                self.bmr_file_path_bytes = f.read()
    

    def sop_doc_pipeline(self):
        """
        Docstring for sop_doc_pipeline
        
        :param self: Description
        """
        try:
            sop_page_wise_data, data,  sop_data_md  = self.data_extraction.main(
                file_bytes=self.sop_file_path_bytes, 
                OCR= True
            )

            ## extracting the contian from the json
            allowed_parent_sop = data.get("list_of_process_steps")
            
            ## data cleaning:
            cleaned_text_ocr = [
                self.data_cleaning.data_cleaning_for_sop_manufauturing(text=text )
                for text in sop_page_wise_data
                ]
            
            clean_data = "\n\n".join(cleaned_text_ocr)
            
            ## chunking the doc:
            parent_chunk = self.sop_splitter.sop_doc_parent_chunk(
                Parent_chunk= allowed_parent_sop,
                text= clean_data
            )

            ## child chunking documents;
            child_chunk = self.sop_splitter.child_chunking_for_sop_doc(parent_chunk=parent_chunk)


        except Exception as e:
            logger.error(f"error in BMR document processing pipeline: {e}")
            raise

    def bmr_doc_pipeline(self):
        try:
            bmr_page_wise_data, data_bmr,  bmr_data_md = self.data_extraction.main(
                file_bytes=self.bmr_file_path_bytes, 
                OCR= True
            )

            cleaned_text_bmr = [
                self.data_cleaning.extract_and_clean_bmr(text=text )
                for text in bmr_page_wise_data
            ]
        
            cleaned_text_bmr_text = "\n\n".join(cleaned_text_bmr)

        except Exception as e:
            logger.error(f"error in BMR document processing pipeline: {e}")
            raise


    



