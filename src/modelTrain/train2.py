from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import CSVLoader
from langchain_openai import OpenAIEmbeddings

# Load the CSV
loader = CSVLoader(file_path='src\\modelTrain\\cars.csv')
docs = loader.load()

# Create embeddings and store in FAISS
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(docs, embeddings)

vectorstore = FAISS.from_documents(docs, embeddings)

# Save the vector store to disk
vectorstore.save_local("car_vectorstore")
print("Vector store trained and saved.")