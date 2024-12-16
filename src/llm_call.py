import os
import time
from datetime import date
from threading import Thread
from openai import OpenAI

import torch
from semantic_kernel.kernel_pydantic import KernelBaseSettings
from typing import ClassVar, Optional
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
from peft import PeftModel
from transformers import BitsAndBytesConfig
from src.logger_setting import LoggerTemplate
from logging import DEBUG
file_path = os.path.basename(os.path.abspath(__file__))
logger_template = LoggerTemplate(file_path, f'./logs/{file_path[0:-3]}.log', print_to_console=True, level=DEBUG)
logger = logger_template.get_logger()



class LocalLLMCallSettings(KernelBaseSettings):
    env_prefix: ClassVar[str] = "LLM_"
    name_or_path: str
    quantized: bool
    cache_dir: str
    device: str

class DeployedLLMSetting(KernelBaseSettings):
    env_prefix: ClassVar[str] = "LLM_"
    base_api: str
    api_key: str

class LocalLLMCall:
    def __init__(self, lora_path: Optional[str] = None):
        self.settings = LocalLLMCallSettings.create()
        if self.settings.quantized:
            nf4_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_use_double_quant=True,
                bnb_4bit_compute_dtype=torch.bfloat16
            )
        try:
            logger.info("开始加载基础模型...")
            model = AutoModelForCausalLM.from_pretrained(
                self.settings.name_or_path,
                device_map=self.settings.device,
                trust_remote_code=True,
                cache_dir=self.settings.cache_dir,
                quantization_config=nf4_config if self.settings.quantized else None
            )
            logger.info("加载基础模型成功！！！")
            self.base_model = model
        except Exception as e:
            logger.error(f"加载基础模型失败。错误原因为{e}，请检测模型路径是否正确。")
        if lora_path:
            try:
                logger.info("开始加载lora模型...")
                self.model = PeftModel.from_pretrained(self.base_model, lora_path, adapter_name=os.path.basename(lora_path))
                self.model.set_adapter(os.path.basename(lora_path))
                logger.info("加载lora模型成功！！！")
            except Exception as e:
                logger.error(f"加载lora模型失败。错误原因为{e}\n开始使用基础模型...")
                self.model = self.base_model
        else:
            self.model = self.base_model
        self.tokenizer = AutoTokenizer.from_pretrained(self.settings.name_or_path,
                                                       use_fast=False,
                                                       trust_remote_code=True,
                                                       cache_dir=self.settings.cache_dir
                                                       )
        self.streamer = TextIteratorStreamer(self.tokenizer, skip_prompt=True)
        self.eos_token = "<|im_end|>"

    def chat(self, messages, llm_config=None):
        if llm_config is None:
            llm_config = dict()
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
            pad_token_id=self.tokenizer.eos_token_id
        )
        model_inputs = self.tokenizer(text, return_tensors="pt").to(self.settings.device)

        with torch.no_grad():
            generated_ids = self.model.generate(
                model_inputs["input_ids"],
                attention_mask=model_inputs["attention_mask"],
                temperature= llm_config.get("temperature", 0.9),
                max_new_tokens=llm_config.get("max_new_tokens", 512),
                top_k=llm_config.get("top_k", None),
                top_p=llm_config.get("top_p", None),
                do_sample=llm_config.get("do_sample", None),
                eos_token_id=self.tokenizer.eos_token_id,
                use_cache=True
            )

        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]

        return self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

    def stream_chat(self, messages, llm_config=None):
        if llm_config is None:
            llm_config = dict()
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
            pad_token_id=self.tokenizer.eos_token_id
        )
        model_inputs = self.tokenizer(text, return_tensors="pt").to(self.settings.device)
        generation_kwargs = dict(model_inputs,
                                 streamer=self.streamer,
                                 temperature=llm_config.get("temperature", 0.9),
                                 max_new_tokens=llm_config.get("max_new_tokens", 1024),
                                 top_k=llm_config.get("top_k", None),
                                 top_p=llm_config.get("top_p", None),
                                 do_sample=llm_config.get("do_sample", None)
                                 )
        thread = Thread(target=self.model.generate, kwargs=generation_kwargs)

        with torch.no_grad():
            thread.start()
            for _chunk in self.streamer:
                if self.eos_token in _chunk:
                    _chunk = _chunk.replace(self.eos_token, '')
                yield _chunk

class DeployedLLMCall:
    def __init__(self, llm_setting: DeployedLLMSetting = DeployedLLMSetting):
        self.settings = llm_setting.create()



if __name__ == '__main__':

    lora = r"E:\duguang-ocr-onnx\role_playing\src\1.8B\sft_sql"

    llm_call = LocalLLMCall()
    result = llm_call.stream_chat(
        [
            {"role": "user", "content": "你好"}
        ]
    )
    res = ""
    for chunk in result:
        print(chunk, end="", flush=True)
        time.sleep(0.1)
    # print(result)


