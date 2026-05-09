import redis
import ast
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv
from openai import OpenAI 

# ENVIRONMENT SETUP
load_dotenv()
client = OpenAI()

VECTOR_DB_URL = "http://localhost:6333"
COLLECTION_NAME = "product_doc_collection"
EMBEDDINGS = OpenAIEmbeddings(
    model="text-embedding-3-large")

# REDIS SETUP

redis_client = redis.Redis(
    host='localhost', 
    port=6379, 
    decode_responses=True
    )

# CONNECT TO VECTOR DATABASE

qdrant = QdrantVectorStore.from_existing_collection(
    embedding=EMBEDDINGS,
    collection_name=COLLECTION_NAME,
    url=VECTOR_DB_URL,
)

print("Worker started, Ready to process queries.")

while True:
    queue_name, raw_payload = redis_client.blpop("rag:requests")
    payload = ast.literal_eval(raw_payload)
    job_id = payload['job_id']
    query = payload['query']

    print(f"Processing Query: {job_id}")
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
    answer = response.output_text

    redis_client.set(
        f"rag:response:{job_id}",
        answer,
        ex=86400
    )
    print(f"Job {job_id} completed successfully!")