import requests
import json
from openai import OpenAI
from anthropic import Anthropic

def get_completion():
    headers = {'Content-Type': 'application/json'}
    data = {"model": "qwen2.5:0.5b", "messages": [{ "role": "user", "content": "为什么天空是蓝色的？" }]}
    response = requests.post(url='http://127.0.0.1:11434/api/chat', headers=headers, data=json.dumps(data))
    print(response)

def openai_chat():
    client = OpenAI(
        # 下面两个参数的默认值来自环境变量，可以不加
        api_key="abcd",
        base_url="http://127.0.0.1:11434/v1"
    )

    completion = client.chat.completions.create(
        model="qwen2.5:0.5b",
        # 定义对话消息列表
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "请写一首七言绝句, 描述夕阳"}
        ],
        stream=True
    )

    for chunk in completion:
        _result = chunk.choices[0].delta.content
        if _result:
            yield _result

def test_openai_call():
    from src.llm_call import GPTModel
    model = GPTModel()
    res = model.ordinary_chat([{"role": "user", "content": "你好"}])
    print(res)
    print(model.get_token_info())

def test_local_model():
    from src.llm_call import LocalLLMCall
    model = LocalLLMCall(lora_path="a")
    res = model.ordinary_chat([{"role": "user", "content": "你好"}])
    print(res)

def test_anthropic():
    client = Anthropic(
        api_key="sk-W6yiaxzMXDVmfT0mOGPxy2PbJfOJivW8kZHgtZ6ghlWWAqY4",
        base_url="https://api.aiproxy.io"
    )

    message = client.messages.create(
        system=[
            {
                "type": "text",
                "text": "你知道鲁迅但是你没有看过《朝花夕拾》",
            }],
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": "评价一下鲁迅的《朝花夕拾》"
            }
        ],
        model="claude-3-sonnet-20240229",
    )
    print(message)


def test():
    from src import start_chat


if __name__ == '__main__':
    # result = openai_chat()
    # get_completion()
    # for chunk in result:
    #     print(chunk, end="", flush=True)
    # test_openai_call()
    # test_local_model()
    test_anthropic()