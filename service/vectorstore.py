from langchain_chroma.vectorstores import Chroma
from service.models import embedding_model
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from fastapi import status,HTTPException,UploadFile
import tempfile
import traceback


splitter=RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=100
)
vectorDB=Chroma(
    collection_name="resumes",
    persist_directory="Documents",
    embedding_function=embedding_model,
    collection_metadata={
    "hnsw:space": "cosine"
}
)

async def store_resume_vector(resume:UploadFile,user_id:int):
    try:
        await resume.seek(0)
        pdf_bytes = await resume.read()
        with tempfile.NamedTemporaryFile(
            suffix=".pdf",
            delete=False
        ) as temp_file:
            temp_file.write(pdf_bytes)
            temp_path = temp_file.name
        loader = PyPDFLoader(temp_path)
        docs = loader.load()
        chunks = splitter.split_documents(docs)
        for chunk in chunks:
            chunk.metadata["user_id"] = user_id  

        vectorDB.add_documents(chunks)
    except Exception as e:
        print(traceback.format_exc())
        raise


def delete_resume_vector(user_id: int):
    try:
        # delete only documents belonging to this user
        response = vectorDB._collection.delete(
            where={"user_id": user_id}
        )
        return response
    except Exception as e :
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))
    