from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from azure.ai.documentintelligence.models import DocumentContentFormat 
from azure.ai.documentintelligence.models import DocumentAnalysisFeature
from openai import AzureOpenAI
from dotenv import load_dotenv
from config.config import DefaultConfig
from utils.helper import time_decorator
from utils.utils import extract_json_from_llm_response
from datetime import datetime

from typing import Dict
import json
import os
import fitz

load_dotenv()

class DataExtraction:
    def __init__(self):
        self.openai_client = AzureOpenAI(
            api_key = os.getenv("AZURE_OPENAI_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_version  = os.getenv("API_VERSION")
        )
        self.ocr_client = DocumentIntelligenceClient(
            endpoint = os.getenv("DOCUMENT_INTELLIGENCE_ENDPOINT"),
            credential=AzureKeyCredential(os.getenv("DOCUMENT_INTELLIGENCE_KEY"))
        )
        self.config = DefaultConfig()


    @time_decorator
    def extract_data_using_ocr(self, file_bytes:bytes):
        self.config.logger.info("Extracting the Data using the OCR")
        try:
            poller = self.ocr_client.begin_analyze_document(
                "prebuilt-layout", 
                AnalyzeDocumentRequest(bytes_source=file_bytes),
                # features=[DocumentAnalysisFeature.KEY_VALUE_PAIRS],
                output_content_format=DocumentContentFormat.MARKDOWN
            )
            result = poller.result()
            page_wise_md = result.content.split("<!-- PageBreak -->")

            page_wise_ocr = []

            for page_idx, page in enumerate(result.pages):
                page_wise_context = ""
                if not(page.lines):
                    import pdb;pdb.set_trace()
                for line_idx, line in enumerate(page.lines):
                    page_wise_context += line.content

                page_wise_ocr.append(page_wise_context)

            return page_wise_md, page_wise_ocr
        except Exception as e:
            self.config.logger.error(f"error in Extracting data using OCR: {e}")
            raise
    
    @time_decorator
    def extract_data_without_using_ocr(self, file_bytes:bytes):
        try:
            self.config.logger.info(f"Extracting the data without using the OCR model using the fitz")
            pdf_document = fitz.open(stream=file_bytes, filetype="pdf")

            page_wise_ocr = []
            for page_number in range(pdf_document.page_count):
                page = pdf_document.load_page(page_number)  # load page
                text = page.get_text("text")  # extract text
                page_wise_ocr.append(text)
            
            pdf_document.close()  # close the document

            # Optional: merge all pages into a single text
            final_text = "\n\n".join(page_wise_ocr)

            self.config.logger.info(f"Extracted text length: {len(final_text)} characters")
            self.config.logger.info(f"Extraction of the data without using the OCR completed...")
            return page_wise_ocr, final_text

        except Exception as e:
            self.config.logger.error(f"Error in Extracting data using the Fitz: {e}")
            raise
    
    
    @time_decorator
    def data_pre_processing(self, extracted_data: str) -> Dict:
        """
        Pre-process the extracted text using Azure OpenAI LLM and return structured JSON output.
        Validates that the response is a proper JSON object.
        """
        try:
            self.config.logger.info("Pre-processing the extracted text using the LLM...")

            response = self.openai_client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": self.config.PROMPTS["IDENTIFY_DATA_PROMPT"]["instruction"],
                    },
                    {
                        "role": "user",
                        "content": extracted_data,
                    }
                ],
                max_completion_tokens=13107,
                temperature=1.0,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0,
                model=os.getenv("AZURE_OPENAI_DEPLOYMENT")
            )

            self.config.logger.success(f"Complete data processing using the OpenAI")
            return response.choices[0].message.content
        except Exception as e:
            self.config.logger.error(f"Error in data pre-processing from OpenAI side: {e}")
            raise

    
    @time_decorator
    def main(self, file_bytes:bytes, OCR:bool=False):
        try:
            if OCR:
                self.config.logger.info(f"Data Extraction Pipeline with Azure OCR initialized successfully......")
                page_wise_md, page_wise_ocr = self.extract_data_using_ocr(
                    file_bytes= file_bytes
                )

                response= self.data_pre_processing(
                    extracted_data='\n\n'.join(page_wise_md[:3])
                )

                final_text = "\n\n".join(page_wise_ocr)

                ## Handling the json response
                import json
                try:
                    data = json.loads(response)
                except json.JSONDecodeError as e:
                    self.config.logger.error(f"Invalid JSON syntax: {e}")
                    data = extract_json_from_llm_response(response)

                # print(data)
                self.config.logger.success(f"Successfull completed the Extraction pipeline with Azure OCR.........")
                return final_text, data, page_wise_md
            

            else:
                self.config.logger.info("Data Extraction Pipeline started witout Azure OCR.......... ")
                page_wise_ocr, final_text = self.extract_data_without_using_ocr(
                    file_bytes= file_bytes
                )

                response= self.data_pre_processing(
                    extracted_data='\n\n'.join(page_wise_ocr[:3])
                )

                ## Handling the json response
                import json
                try:
                    data = json.loads(response)
                except json.JSONDecodeError as e:
                    self.config.logger.error(f"Invalid JSON syntax: {e}")
                    data = extract_json_from_llm_response(response)

                
                self.config.logger.success("Successfull completed the Extraction pipeline with Azure OCR.........")
                return final_text, data, response




        except Exception as e:
            self.config.logger.error(f"Error in Data extaction pipeline: {e}")
            raise

