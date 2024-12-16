import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained(r"D:\model\google\gemma-2-2b-it")
model = AutoModelForCausalLM.from_pretrained(
    r"D:\model\google\gemma-2-2b-it",
    torch_dtype=torch.float16,
    device_map="cuda",
)

messages = [
    {"role": "user", "content": "给我写一首关于机器学习的诗，用中文回答"},
]
input_ids = tokenizer.apply_chat_template(messages, return_tensors="pt", return_dict=True).to("cuda")

outputs = model.generate(**input_ids, max_new_tokens=256)
print(tokenizer.decode(outputs[0]))

