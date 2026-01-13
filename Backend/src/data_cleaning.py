import re
from config.config import DefaultConfig
from typing import List
logger = DefaultConfig().logger


class DataCleaning:
    
    def __init__(self):
        pass


    @staticmethod    
    def data_cleaning_for_sop_manufauturing(text:List[str])-> List[str]:
        """
        More flexible version that can handle variations in the header/footer.
        Handles multiple header formats found in MBR documents.
        """

        try:
            logger.info("Text cleaning Process initalize for the Maunfaturing SOP.....")

            # Flexible header patterns
            header_patterns = [
                # Main header pattern (page 1 style)
                r'Master Batch Record\s*30000773\s*[-–]\s*ARIPIPRAZOLE\s*5\s*MG\s*TAB\s*Effective\s*Alembic\s*Touching Lives over["\s]*100\s*years\s*ID/Version/Description\s*F1M00332/00000001/Aripiprazole Tab[\.\s]*USP 5mg',
                
                # Simpler catch-all for header
                r'Master Batch Record\s*30000773[^M]*?Aripiprazole Tab\.?USP 5mg',
                
                # NEW: Repeated header on subsequent pages (Material line)
                r'Master Batch Record\s*Material:\s*30000773\s*[-–]\s*ARIPIPRAZOLE\s*5\s*MG\s*TAB\s*BO',
                
                # NEW: Variation without "BO" at end
                r'Master Batch Record\s*Material:\s*30000773\s*[-–]\s*ARIPIPRAZOLE\s*5\s*MG\s*TAB(?=\s*BO|\s*$)',
                
                # NEW: Just the "Master Batch RecordMaterial:" line standalone
                r'Master Batch RecordMaterial:\s*30000773\s*[-–]\s*ARIPIPRAZOLE\s*5\s*MG\s*TABBO',
            ]
            
            # Flexible footer patterns
            footer_patterns = [
                # Standard footer: Page X of Y + Name + Date + Version
                r'Page\s*\d+\s*of\s*\d+\s*[A-Za-z\s]+\d{2}/\d{2}/\d{4}\s*\d{2}:\d{2}:\d{2}\s*V\d+',
                
                # Alternative: Version first
                r'V\d+\s*[A-Za-z\s]+\d{2}/\d{2}/\d{4}\s*\d{2}:\d{2}:\d{2}\s*Page\s*\d+\s*of\s*\d+',
                
                # Just page number pattern
                r'Page\s*\d+\s*of\s*\d+',
            ]
            
            cleaned_text = text
            
            # Remove all header patterns
            for pattern in header_patterns:
                cleaned_text = re.sub(pattern, '', cleaned_text, flags=re.IGNORECASE | re.DOTALL)
            
            # Remove all footer patterns
            for pattern in footer_patterns:
                cleaned_text = re.sub(pattern, '', cleaned_text, flags=re.IGNORECASE)
            
            # Clean up whitespace
            cleaned_text = re.sub(r'\n{3,}', '\n\n', cleaned_text)
            cleaned_text = re.sub(r'[ \t]+', ' ', cleaned_text)
            cleaned_text = cleaned_text.strip()

            logger.info(f"Text Cleaning completely Sucessfully......")
            
            return cleaned_text

        except Exception as e:
            logger.error(f"Error in text cleaning for SOP Manufaturing:{e}")
            raise
    

    @staticmethod
    def text_cleaning_for_BMR(text:List[str])-> List[str]:
        try:
            pass
        except Exception as e:
            logger.info(f"Error in text cleaning for BMR: {e}")
            raise