import aiohttp
import requests
import json
# from src.agent import RoleAgent, CharacterCard
# role_agent = RoleAgent()
from openai import OpenAI
# while True:
#     character_card = input("请选择角色卡：")
#     role_agent, status = role_agent.choose_character_card(character_card)
#     if status == "角色卡未找到":
#         user_input = input("当前无该角色卡，是否创建该角色卡：")
#         if user_input == "y":
#             input_c = character_card
#             input_s = input("请输入角色卡描述：")
#             role_agent.get_user_input("y", input_c, input_s)
#         else:
#             role_agent.get_user_input("n")
#     print("角色卡已选择")
#     input_u = input("请输入用户名：")
#     role_agent.character_card.set_user_name(input_u)
#     print(f"当前你在和{role_agent.character_card.character_card}聊天, 你扮演的角色是{role_agent.character_card.user_name}")
#     query = input("请输入问题：")
#     result = role_agent.role_chat(query)
#     print(result)
#     print(role_agent.character_card.chat_history)
# role_agent.choose_character_card(character_card="张晓")
# role_agent.character_card.set_user_name("主人")
# print(f"你是{role_agent.character_card.character_card}的{role_agent.character_card.user_name}")
# cnt = 0
# while cnt < 5:
#     query = input("请输入问题：")
#     result = role_agent.role_chat(query)
#     print(result)
#     print()
#     print(role_agent.character_card.chat_history)
#     cnt += 1
# role_agent.character_card.save_chat_history()
# client = aiohttp.ClientSession()
# result = client.post()

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


if __name__ == '__main__':
    # result = openai_chat()
    # get_completion()
    # for chunk in result:
    #     print(chunk, end="", flush=True)
    # test_openai_call()
    test_local_model()