from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv

# SETUP THE ENVIRONMENT

load_dotenv()
PDF_PATH = "doc.pdf"

# LOAD THE PDF 
loader = PyPDFLoader(PDF_PATH)
# CONVERT PDF TO TEXT
docs = loader.load()

# DECIDE ON CHUNKING STRATEGY
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=400
)
# CHUNK PDF AND STORE IN A VARIABLE
chunked_docs = text_splitter.split_documents(docs)

# CHOOSE AN EMBEDDING MODEL
EMBEDDINGS = OpenAIEmbeddings(
    model="text-embedding-3-large")

# STORE THE CHUNKS IN THE VECTOR DATABASE

VECTOR_DB_URL = "http://localhost:6333"
COLLECTION_NAME = "product_doc_collection"

qdrant = QdrantVectorStore.from_documents(
    chunked_docs,
    EMBEDDINGS,
    url=VECTOR_DB_URL,
    prefer_grpc=False,
    collection_name=COLLECTION_NAME,
)

print("Ingestion completed successfully!")