import redis
import uuid 

# CONNECT TO THE REDIS INSTANCE

redis_client = redis.Redis(
    host='localhost', 
    port=6379, 
    decode_responses=True
    )

# CREATE AND PUSH PAYLOAD TO REDIS

def push_query(query):
    job_id = str(uuid.uuid4())

    payload = {
        "job_id": job_id,
        "query": query
    }
    redis_client.rpush("rag:requests",str(payload))
    return job_id

user_query = input("Human Query: ")
job = push_query(user_query)

print("Job sent to queue")
print(job)