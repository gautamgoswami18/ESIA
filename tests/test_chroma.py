import chromadb

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_collection("employee_resumes")

print("Collection Name :", collection.name)
print("Total Documents :", collection.count())