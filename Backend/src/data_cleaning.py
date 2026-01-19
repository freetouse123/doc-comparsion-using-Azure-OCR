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
            HEADER_PATTERNS = [
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
            FOOTER_PATTERNS = [
                # Standard footer: Page X of Y + Name + Date + Version
                r'Page\s*\d+\s*of\s*\d+\s*[A-Za-z\s]+\d{2}/\d{2}/\d{4}\s*\d{2}:\d{2}:\d{2}\s*V\d+',
                
                # Alternative: Version first
                r'V\d+\s*[A-Za-z\s]+\d{2}/\d{2}/\d{4}\s*\d{2}:\d{2}:\d{2}\s*Page\s*\d+\s*of\s*\d+',
                
                # Just page number pattern
                r'Page\s*\d+\s*of\s*\d+',
            ]
            
            cleaned_text = text
            
            # Remove all header patterns
            for pattern in HEADER_PATTERNS:
                cleaned_text = re.sub(pattern, '', cleaned_text, flags=re.IGNORECASE | re.DOTALL)
            
            # Remove all footer patterns
            for pattern in FOOTER_PATTERNS:
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
    def text_cleaning_for_BMR(text:str)->str:
        try:
            # Header patterns - appearing at top of pages
            HEADER_PATTERNS = [
                # Full header block with product name, BMR number, batch size
                r'Product\s*Name:\s*Aripiprazole\s*Tablets\s*USP\s*5\s*mg.*?'
                r'BMR\s*No\.\s*&\s*Version\s*No\.\s*F1\\BMR\\\d+\s*&\s*[\d\.]+\s*Product\s*Code:\s*\d+.*?'
                r'Batch\s*Size\s*in\s*Kg\s*/\s*Liter:\s*[\d,\.]+\s*kg\s*Batch\s*Size\s*in\s*Unit:\s*[\d,\.]+\s*Tablets',
                
                # Standalone product name line
                r'Product\s*Name:\s*Aripiprazole\s*Tablets\s*USP\s*5\s*mg',
                
                # BMR and product code line
                r'BMR\s*No\.\s*&\s*Version\s*No\.\s*F1\\BMR\\\d+\s*&\s*[\d\.]+\s*Product\s*Code:\s*\d+',
                
                # Batch size line
                r'Batch\s*Size\s*in\s*Kg\s*/\s*Liter:\s*[\d,\.]+\s*kg\s*Batch\s*Size\s*in\s*Unit:\s*[\d,\.]+\s*Tablets',
                
                # Company branding
                r'Alembic\s*Touching\s*Lives\s*over\s*\d+\s*years',

                # removing the header
                r'Touching\s*Lives\s*over\s*\d+\s*years',
            ]
            
            # Footer patterns - appearing at bottom of pages
            FOOTER_PATTERNS = [
                # Format number with effective date (various formats)
                r'Format\s*No\s*\.?\s*:\s*C\\QA\\SOP\\\d+-F\d+-[\d\.]+\s*Effective\s*Date\s*:\s*\d{2}/\d{2}/\d{4}[\'\"]?',
                
                r'Format\s*No\s*\.?\s*:\s*C\\QASOP\\\d+-F\d+-[\d\.]+\s*Effective\s*Date\s*:\s*\d{2}/\d{2}/\d{4}[\'\"]?',
                
                # Footer with preceding colon
                r':\s*Format\s*No\s*\.?\s*:\s*C\\QA\\?SOP\\\d+-F\d+-[\d\.]+\s*Effective\s*Date\s*:\s*\d{2}/\d{2}/\d{4}[\'\"]?',
                
                # Signature table footer combination
                r'Sr\.\s*No\.?\s*Name\s*Signature.*?Format\s*No\s*\.?\s*:\s*C\\QA\\?SOP\\\d+-F\d+-[\d\.]+\s*Effective\s*Date\s*:\s*\d{2}/\d{2}/\d{4}[\'\"]?',
                
                # Generalized version of the previously hardcoded example
                r'Format\s*No\s*\.?\s*:\s*C\\QASOP\\\d{4}-F\d{3}-[\d.]+\s*Effective\s*Date\s*:\s*\d{2}/\d{2}/\d{4}[\'\"]?', 

                # Catch any remaining format line at end of string - more flexible
                r'Format\s*No\s*\.?\s*:\s*C[\\/]+[A-Z]+[\\/]*\d+-F\d+-[\d\.]+\s*Effective\s*Date\s*:\s*\d{2}/\d{2}/\d{4}[\'\"]?',
            
            ]
            
            cleaned_text = text
            
            # Remove headers (preserve line breaks)
            for pattern in HEADER_PATTERNS:
                cleaned_text = re.sub(
                    pattern,
                    '\n',  # Replace with single newline to maintain separation
                    cleaned_text,
                    flags=re.IGNORECASE | re.DOTALL
                )
            
            # Remove footers (preserve line breaks)
            for pattern in FOOTER_PATTERNS:
                cleaned_text = re.sub(
                    pattern,
                    '',  # Replace with empty string
                    cleaned_text,
                    flags=re.IGNORECASE | re.DOTALL | re.MULTILINE
                )
            
            # Clean up excessive whitespace while preserving structure
            # Remove more than 2 consecutive newlines
            cleaned_text = re.sub(r'\n{3,}', '\n\n', cleaned_text)
            
            # Remove trailing/leading whitespace on each line
            lines = cleaned_text.split('\n')
            lines = [line.rstrip() for line in lines]
            cleaned_text = '\n'.join(lines)
            
            # Remove leading and trailing whitespace from entire text
            cleaned_text = cleaned_text.strip()
            
            return cleaned_text
        
        except Exception as e:
            logger.info(f"Error in text cleaning for BMR: {e}")
            raise
    
    def extract_and_clean_bmr(text:str):
        """
        Complete extraction and cleaning pipeline for BMR documents.
        
        Args:
            pdf_text (str): Raw text extracted from PDF
            
        Returns:
            str: Cleaned and formatted text
        """
        # Apply header/footer removal
        cleaned_text = DataCleaning().text_cleaning_for_BMR(text)
        
        # Additional post-processing (optional)
        # Remove page numbers if present
        cleaned_text = re.sub(r'^\d+\s*$', '', cleaned_text, flags=re.MULTILINE)
        
        # Remove standalone horizontal rules or dividers
        cleaned_text = re.sub(r'^[-_=]{3,}\s*$', '', cleaned_text, flags=re.MULTILINE)
        
        # Final cleanup of excessive blank lines
        cleaned_text = re.sub(r'\n{3,}', '\n\n', cleaned_text)
        
        return cleaned_text.strip()