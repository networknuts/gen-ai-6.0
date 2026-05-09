import redis
import time

# SETUP REDIS CONNECTION
redis_client = redis.Redis(
    host='localhost', 
    port=6379, 
    decode_responses=True
    )

job_id = input("Enter the Job ID: ")

while True:
    result = redis_client.get(f"rag:response:{job_id}")
    if result:
        print("OUTPUT\n")
        print(result)
        break
    print("Waiting for 5 seconds before trying again.")
    time.sleep(5)