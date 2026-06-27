from langchain_google_vertexai import ChatVertexAI,VertexAIEmbeddings
import vertexai
from dotenv import load_dotenv
load_dotenv()
import os

vertexai.init(
    project="gemini-model-499618",
    location="asia-south1"
)
primary_llm= ChatVertexAI(
    model=os.getenv("primary_chat_llm"),
    project="gemini-model-499618",
    location="us-central1",
)
secondary_llm= ChatVertexAI(
    model=os.getenv("secondary_chat_llm"),
    project="gemini-model-499618",
    location="us-central1",
)

chat_model=primary_llm.with_fallbacks([secondary_llm]) #the main chat generation model

embedding_model= VertexAIEmbeddings(
    model_name="gemini-embedding-001",
    project="gemini-model-499618",
    location="us-central1",
)
