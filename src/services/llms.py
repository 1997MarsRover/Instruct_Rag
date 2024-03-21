import os 
from typing import Optional
from langchain_openai import ChatOpenAI, OpenAI, AzureOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAI
from dotenv import load_dotenv
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from langchain_openai import AzureOpenAI
from llama.cpp import LLama
from huggingface_hub import hf_hub_download

class Llms:
    def __init__(self, model_provider: str, model_name: Optional[str] = None):
        load_dotenv()
        self.model_provider = model_provider
        self.model_name = model_name

    def get_chat_model(self, api_key: Optional[str] = None):
        if self.model_provider == 'openai':
            if api_key:
                return ChatOpenAI(model= self.model_name, openai_api_key=api_key)
            else:
                return ChatOpenAI(model= self.model_name, openai_api_key=os.getenv('OPENAI_API_KEY'))
        elif self.model_provider == 'google':
            if api_key:
                return ChatGoogleGenerativeAI(model = self.model_name, google_api_key=os.getenv('GOOGLE_API_KEY'), safety_settings={
                                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE
                            })
            else:
                return ChatGoogleGenerativeAI(model = self.model_name, google_api_key=os.getenv('GOOGLE_API_KEY'), safety_settings={
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE
                })
        elif self.model_provider == 'azure':
            return AzureOpenAI(deployment_name = "gpt-35-turbo", model_name = "gpt-3.5-turbo-1106")
        elif self.model_provider == 'mistral':
            mistral_path = "TheBloke/Mistral-7B-Instruct-v0.2-GGUF"
            mistral_q4_basename = "mistral-7b-instruct-v0.2.Q4_K_M.gguf"
            model_path = hf_hub_download(repo_id=mistral_path, filename=mistral_q4_basename)
            return Llama(
                        model_path=model_path,
                        n_gpu_layers=--1, # The number of layers to put on the GPU. The rest will be on the CPU. If you don't know how many layers there are, you can use -1 to move all
                        n_batch = 2048, # Should be between 1 and n_ctx, consider the amount of VRAM in your GPU.
                        n_ctx=2048,
                        logits_all=False,
                            )
        else:
            raise Exception("Invalid model provider we currently support only openai, azure and google models")
        
    def get_llm(self, api_key: Optional[str] = None):
        if self.model_provider == 'openai':
            if api_key:
                return OpenAI(model= self.model_name, openai_api_key=api_key)
            else:
                return OpenAI(model= self.model_name, openai_api_key=os.getenv('OPENAI_API_KEY'))
        elif self.model_provider == 'google':
            if api_key:
                return GoogleGenerativeAI(model = self.model_name, google_api_key=api_key,safety_settings={
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE
            })
            else:
                return GoogleGenerativeAI(model = self.model_name, google_api_key=os.getenv('GOOGLE_API_KEY'),safety_settings={
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE
                })
    
        else:
            raise Exception("Invalid model provider we currently support only openai, azure and google models")
