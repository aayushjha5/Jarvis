from openai import OpenAI
from dotenv import load_dotenv
import os

# install openai using pip install openai

#for storing api keys in env file
load_dotenv()
openaikey = os.getenv("OPENAI_KEY")


#connect to openAI using your api key
client = OpenAI(api_key=f"{openaikey}")

completion = client.chat.completions.create(
    model = "gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud"},
        {"role": "user", "content": "what is coding"}
    ]
)

print(completion.choices[0].message.content)