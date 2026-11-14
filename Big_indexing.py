from dotenv import load_dotenv
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore 
from langchain_community.tools import tool, DuckDuckGoSearchRun

load_dotenv()

path= Path(__file__).parent/"Employee-Handbook.pdf"

document = []

document.extend(
    PyPDFLoader("Employee-Handbook.pdf").load()
)

text_splliter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 300
)

chunks = text_splliter.split_documents(documents=document)

embedding_model = OpenAIEmbeddings(
    model= "text-embedding-3-large"
)

vector_db = QdrantVectorStore.from_documents(
    documents= chunks,
    embedding= embedding_model,
    url = "http://localhost:6333",
    collection_name = "Big_project"
)
print("Indexing done😎...")
