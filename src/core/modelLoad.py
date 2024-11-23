import faiss
from sentence_transformers import SentenceTransformer
import json

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Load the FAISS index and metadata
def load_model():
    print("Loading FAISS index and metadata...")
    index = faiss.read_index("car_features_index.faiss")
    with open("car_metadata.json", "r") as f:
        metadata = json.load(f)
    print("Model loaded successfully.")
    return index, metadata

# Query the loaded model
def query_model(user_query, index, metadata, top_k=5):
    # Encode the user query
    query_embedding = embedding_model.encode(user_query).astype('float32').reshape(1, -1)

    # Search the FAISS index
    distances, indices = index.search(query_embedding, top_k)

    # Retrieve corresponding metadata
    results = [metadata[i] for i in indices[0] if i < len(metadata)]
    return results

# Example Usage
index, metadata = load_model()
results = ""
while(results != "exit"):
    user_query= input("What can I help you with: ")
    results = query_model(user_query, index, metadata)
    for result in results:
        print(result)
