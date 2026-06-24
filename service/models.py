from langchain_google_vertexai import ChatVertexAI,VertexAIEmbeddings
from google import genai
from dotenv import load_dotenv
import os
load_dotenv()
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "GOOGLE_APPLICATION_CREDENTIALS.json" # Vertex AI credentials JSON 
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

# with open("audio.wav", "rb") as f:
#     audio_bytes = f.read()

# response = client.models.generate_content(
#     model="gemini-2.5-flash",
#     contents=[
#         {
#             "mime_type": "audio/wav",
#             "data": audio_bytes,
#         },
#         "Transcribe this audio."
#     ]
# )

