from pymongo import MongoClient

# connect to database
client = MongoClient("mongodb://localhost:27017")

dbs = client.list_database_names()
print(dbs)