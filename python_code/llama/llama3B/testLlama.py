from transformers import pipeline
import torch
modelPath = "C:\\Users\\natht\\CodeByte\\python_code\\llama\\Llama3B"

pipe = pipeline(
    "text-generation",
    model = modelPath,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)

message = [
    {"role": "system", "content": "You are an AI helper to aid the user in performing actions accross the database."},
    {"role": "first_message", "content": "Give the user a welcoming message"},
]

response = pipe(
    message,
    max_new_tokens=500,
)

outputResponse = response[0]["generated_text"][-1]
print(outputResponse['content'])

with open('output.txt', 'w', encoding="utf-8") as text_file:
    text_file.write(outputResponse['content'])
