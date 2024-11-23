from modelLoad import load_model, query_model
from openai import OpenAI

# Example Usage
index, metadata = load_model()
model = 'gpt-3.5-turbo'
client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Write a haiku about recursion in programming."
        }
    ]
)

print(completion.choices[0].message)

while(results != "exit"):
    user_query= input("What can I help you with: ")
    results = query_model(user_query, index, metadata)
    for result in results:
        print(result)