from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI



def create_chain():

    # Load the pre-trained vector store
    vectorstore = FAISS.load_local(
        "car_vectorstore", 
        embeddings=OpenAIEmbeddings(),
        allow_dangerous_deserialization=True
        )

    # Create a retriever and QA chain
    retriever = vectorstore.as_retriever()

    memory = ConversationBufferMemory(
        memory_key="chat_history", 
        return_messages=True
        )

    qa_chain = ConversationalRetrievalChain.from_llm(
        ChatOpenAI(), 
        retriever=retriever, 
        memory=memory, 
    )

    return qa_chain



if __name__ == "__main__":
    print("Chatbot ready! Ask me anything about our cars.")
    qa_chain = create_chain()
    while True:
        query = input("Customer: ")
        if query.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        response = qa_chain.invoke({"question": query})
        print(f"Car salesman: {response['answer']}")

