from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv
from openai import OpenAI 

# SETUP THE ENVIRONMENT
load_dotenv()
client = OpenAI()

VECTOR_DB_URL = "http://localhost:6333"
COLLECTION_NAME = "product_doc_collection"
EMBEDDINGS = OpenAIEmbeddings(
    model="text-embedding-3-large")

# CONNECT TO THE VECTOR DATABASE WITH RELEVANT COLLECTION
qdrant = QdrantVectorStore.from_existing_collection(
    embedding=EMBEDDINGS,
    collection_name=COLLECTION_NAME,
    url=VECTOR_DB_URL,
)

# ASK FOR USER QUERY
query = input("Enter Human Query: ")

# QUERY THE VECTOR DATABASE FOR RELEVANT CHUNKS
search_results = qdrant.similarity_search(query)

context_list = []

for result in search_results:
    chunk_block = f"""
    Page Content:
    {result.page_content}
    Page Number:
    {result.metadata.get("page_label","N/A")}
    """
    context_list.append(chunk_block)


SYSTEM_PROMPT = f"""
You are a RAG AI Assistant.
You have been given extracted content from a PDF document.
Each section includes:
- The text content
- The page number

Answer the user's query using ONLY this provided information.
If the answer is available:
- Respond clearly from data you have received
- Mention the relevant page number from where the data was extracted

If the answer is not available:
- Clearly state to the user that your knowledge base does not contain the answer

Context:
{context_list}
"""

response = client.responses.create(
    model="gpt-5.4-mini",
    input=query,
    instructions=SYSTEM_PROMPT
)

print(response.output_text)