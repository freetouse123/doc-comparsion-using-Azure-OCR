from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, DocumentContentFormat, DocumentAnalysisFeature
from openai import AzureOpenAI
from dotenv import load_dotenv
from config.config import DefaultConfig
import os

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

    def extract_data_using_ocr(self, file_bytes:bytes):
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
            print(f"error in Extracting data using OCR: {e}")
            raise
    
    def extract_data_without_using_ocr(file_bytes:bytes):
        try:
            pass
        except Exception as e:
            print(f"Error in Extracting data using the Fitz: {e}")
            raise
    
    def data_pre_processing(self, extracted_data:str):
        try:
            response = self.openai_client.completions.create(
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

            print(response.choices[0].message.content)

            return response.choices[0].message.content
        except Exception as e:
            print(f"Error in Data pre processing from Openai side: {e}")
            raise

    def main(self, file_bytes:bytes):
        try:
            page_wise_md, page_wise_ocr = self.extract_data_using_ocr(
                file_bytes= file_bytes
            )

            response= self.data_pre_processing(
                extracted_data='\n\n'.join(page_wise_ocr[:3])
            )
            return page_wise_md, page_wise_ocr, response

        except Exception as e:
            print(f"Error in Data extaction pipeline: {e}")
            raise

