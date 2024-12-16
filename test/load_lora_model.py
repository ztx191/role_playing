from transformers import AutoModelForCausalLM
import torch
from peft import PeftModel
lora_path = r"E:\duguang-ocr-onnx\role_playing\src\1.8B\sft_sql"
base_model_path = r"D:\model\Qwen1.5-1.8B-chat"

model = AutoModelForCausalLM.from_pretrained(base_model_path, device_map="cuda", torch_dtype=torch.bfloat16,
                                                 trust_remote_code=False)

model = PeftModel.from_pretrained(model, lora_path, adapter_name="sql")

model.set_adapter("sql")

print(model)
