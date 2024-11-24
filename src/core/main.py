from modelLoad import create_chain
from stt import real_time_speech_to_text


def main():
    qa_chain = create_chain()

    print("Chatbot ready! Ask me anything about our cars.")
    while True:
        query = input("Customer: ")
        # query = real_time_speech_to_text()
        print(f'Customer: {query}')
        if query.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        response = qa_chain.invoke({"question": query})
        print(f"Car salesman: {response['answer']}")

main()