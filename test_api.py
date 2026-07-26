import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if api_key:
    print("API key loaded successfully!")
else:
    print("API key not found. Check your .env file.")
    exit()

client = OpenAI(api_key=api_key)

try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Say hello briefly."}
        ],
        max_tokens=10
    )
    print("API call successful!")
    print(f"Response: {response.choices[0].message.content}")
except Exception as e:
    print(f"API call failed: {e}")
