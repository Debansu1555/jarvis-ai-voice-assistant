from openai import OpenAI
 
# pip install openai 
# if you saved the key under a different environment variable name, you can do something like:
client = OpenAI(
  api_key="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",
)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud"},
    {"role": "user", "content": "what is coding"}
  ]
)

print(completion.choices[0].message.content)