import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pandas as pd
import json

# Load the CSV data
df = pd.read_csv("src\\modelTrain\\cars.csv")

# Initialize the embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Generate embeddings and prepare metadata
print("Generating embeddings and metadata...")
embeddings = []
metadata = []

for i, row in df.iterrows():
    # Create a description string for embedding
    description = (
        f"{row['Year']} {row['Make']} {row['Model']}, {row['Drivetrain']}, "
        f"Engine: {row['EngineDisplacementCubicInches']} cubic inches, {row['Transmission_Description']}, "
        f"Fuel efficiency: {row['CityMPG']} MPG city, {row['HighwayMPG']} MPG highway, "
        f"Price: ${row['SellingPrice']}, {row['ExteriorColor']} exterior, {row['InteriorColor']} interior. "
        f"Market class: {row['MarketClass']}."
    )
    
    # Generate an embedding for the description
    embedding = embedding_model.encode(description)
    embeddings.append(embedding)
    
    # Prepare metadata for retrieval
    metadata.append({
        "Type": row["Type"],
        "Make": row["Make"],
        "Model": row["Model"],
        "Year": row["Year"],
        "Drivetrain": row["Drivetrain"],
        "Transmission": row["Transmission"],
        "Fuel_Type": row["Fuel_Type"],
        "CityMPG": row["CityMPG"],
        "HighwayMPG": row["HighwayMPG"],
        "PassengerCapacity": row["PassengerCapacity"],
        "SellingPrice": row["SellingPrice"],
        "ExteriorColor": row["ExteriorColor"],
        "InteriorColor": row["InteriorColor"]
    })

# Convert embeddings to a NumPy array
embeddings = np.array(embeddings, dtype='float32')

# Create and populate the FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)
print(f"FAISS index created with {len(embeddings)} embeddings.")

# Save the FAISS index
faiss.write_index(index, "car_features_index.faiss")

# Save the metadata to a JSON file
with open("car_metadata.json", "w") as f:
    json.dump(metadata, f)

print("Model saved: FAISS index and metadata.")
