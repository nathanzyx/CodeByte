import torch
from transformers import AutoModelForCausalLM, AutoProcessor

# Model name
MODEL_NAME = "microsoft/Phi-4-multimodal-instruct"

# Load the processor (for handling text & images)
# processor = AutoProcessor.from_pretrained(MODEL_NAME)

# Load the model (ensure it's on CUDA if available)
# device = "cuda" if torch.cuda.is_available() else "cpu"
model = AutoModelForCausalLM.from_pretrained("microsoft/Phi-4-multimodal-instruct", trust_remote_code=True)

# Example text input
# text_input = "What is the capital of France?"
# # inputs = processor(text=text_input, return_tensors="pt").to(device)

# # Generate response
# with torch.no_grad():
#     output = model.generate(text_input, max_length=100)

# # Decode and print output
# decoded_output = processor.batch_decode(output, skip_special_tokens=True)
# print(decoded_output[0])
