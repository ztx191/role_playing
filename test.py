

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


def test_character_card():
    from src.agent import CharacterCard
    card = CharacterCard()
    print()

def test_load_history():
    from src.agent import CharacterCard
    card = CharacterCard(character_card="a", user_name="b")
    print(card.load_last_chat_history())

def test_create_character_card():
    from src.agent import CharacterCard
    card = CharacterCard()
    while True:
        c = input("请输入角色卡名称：")
        character_list = card.get_character_list()
        if c not in character_list:
            print("角色卡不存在，是否创建该角色卡？")
            n = input("y/n")
            if n == "y":
                s = input("请输入角色卡设定：")
                card.create_character_card(c, s)
                print("创建角色卡成功")
            else:
                print("创建角色卡失败！")
        else:
            print("角色卡已存在，是否修改其设定？")
            n = input("y/n")
            if n == "y":
                s = input("请输入角色卡设定：")
                card.create_character_card(c, s)
                print("修改角色卡成功")
            else:
                print("修改角色卡失败！")

def test_agent_choose():
    from src.agent import RoleAgent
    agent = RoleAgent()
    agent.load_default_setting()
    character_list = agent.character_card.get_character_list()
    c = input("请输入角色卡名称：")
    if c in character_list:
        agent.choose_character_card(c)
        print(f"切换角色卡{agent.character_card.character_card}成功")
        n = input("请选择你的角色：")
        agent.character_card.set_user_name(n)
        print("你的角色创建成功")
    else:
        u = input("是否创建该角色")
        if u == "y":
            s = input("请输入角色卡设定：")
            agent.choose_character_card(c, s)
            print("创建角色卡成功")
            s1 = input("是否切换为该角色卡？")
            if s1 == "y":
                agent.choose_character_card(c, user_switch=True)
                print(f"切换到角色{agent.character_card.character_card}")
            else:
                print(f"未切换该角色卡，切换到当前角色卡{agent.character_card.character_card}")
        else:
            agent.choose_character_card(c, user_main=False)
            print(f"切换到角色{agent.character_card.character_card}")



def test_openai():
    clint = OpenAI(
        api_key="sk-W6yiaxzMXDVmfT0mOGPxy2PbJfOJivW8kZHgtZ6ghlWWAqY4",
        base_url="https://api.aiproxy.io/v1"
    )
    system = """
    下面我会给你一段python代码，该段代码将功能接口串起来组成了一个角色扮演聊天机器人的业务流程。你的任务是将这段代码转变为flask框架的web服务。服务包含前端和后端，你需要返回前端html文件和后端接口python文件。
    前端界居中，包含三个部分：title，聊天框界面和按键。聊天框中用户输入居右模型输出居左，聊天框下面有“清空记录”、“保存记录”、“创建角色卡”、“切换角色卡”、“Chat”五个按钮。
    后端接口有六个route：第一个是route('/')显示界面；第二个是route('/save_history')用于保存用户与当前角色卡的聊天记录；第三个是route('/clear')用于清除用户与当前角色卡的聊天记录，同时前端聊天框中用户和角色卡的聊天文字也清除
    第四个是route('/create_character')用于创建角色卡；第五个是route('/choose_character')用于切换角色卡，用户切换的角色卡并输入用户扮演的角色后，保存用户与当前角色卡的聊天记录，并清空当前聊天框界面文字；第六个是route('/chat')用户与当前角色卡聊天，并将聊天记录显示在聊天框界面上。
    用户切换角色卡时，提示用户的输入角色卡和用户扮演的角色，用弹窗交互，用户创建新角色卡时提示用户输入用弹窗提醒，保存历史记录和清除历史记录提示用户的输入用弹窗交互。
    """

    c = """
    python代码为：
        from src.agent import RoleAgent
        def init_agent():
            role_agent = RoleAgent()
            role_agent.load_default_setting()
            role_agent.load_llm()
            return role_agent
        
        def main_chat():
            agent = init_agent()
            print(f"欢迎使用角色扮演聊天机器人")
            print("指令：\nc清空历史，\nh切换角色卡，\ns保存对话历史，\nq退出，\nb创建角色卡，\nenter键开始后续")
            while True:
                user_input = input("请输入：")
                if user_input.lower() == "c":
                    if not agent.character_card.chat_history:
                        print("当前无历史记录")
                    else:
                        agent.save_chat_history()
                        agent.character_card.chat_history = list()
                        print("历史记录已清空")
                elif user_input.lower() == "s":
                    if not agent.character_card.chat_history:
                        print("当前无历史记录")
                    else:
                        agent.save_chat_history()
                        print("历史记录已保存")
                elif user_input.lower() == "q":
                    print("退出")
                    return
                elif user_input.lower() == "h":
                    input_c = input("请输入角色卡名称(enter键结束)：")
                    if input_c in agent.character_card.get_character_list():
                        agent.choose_character_card(input_c)
                        print("切换角色卡成功")
                    else:
                        input_user_main = input("角色卡未找到，是否创建该角色卡：")
                        if input_user_main.lower() == "y":
                            input_s = input("请输入角色卡设定：")
                            agent.choose_character_card(input_c, input_s)
                            print("创建角色卡成功")
                            input_user_s1 = input("是否切换至该角色卡：")
                            if input_user_s1.lower() == "y":
                                agent.choose_character_card(input_c, user_switch=True)
                                print(f"切换到角色{agent.character_card.character_card}")
                            else:
                                print(f"未切换该角色卡，切换到当前角色卡{agent.character_card.character_card}")
                        else:
                            print("创建角色卡失败！enter键继续当前聊天")
        
                elif user_input.lower() == "b":
                    print("开始创建角色卡！")
                    c = input("请输入角色卡名称：")
                    if c in agent.character_card.get_character_list():
                        m = input("角色卡已存在，是否修改其设定？")
                        if m == "y":
                            s = input("请输入角色卡设定：")
                            agent.character_card.create_character_card(c, s)
                            print("修改角色卡设定成功！enter键继续")
                        else:
                            agent.character_card.create_character_card(c, user_main=False)
                            print("未修改角色卡设定！enter键继续")
                    else:
                        s = input("请输入角色卡设定：")
                        agent.character_card.create_character_card(c, s)
                        print("创建角色卡成功！enter键继续")
        
                else:
                    print(f"当前角色卡为{agent.character_card.character_card}")
                    if not agent.character_card.user_name:
                        input_u = input("请输入您想扮演的角色：")
                    else:
                        input_u = agent.character_card.user_name
                    agent.character_card.set_user_name(input_u)
                    print(f"当前你在和{agent.character_card.character_card}聊天, 你扮演的角色是{agent.character_card.user_name}")
                    print(agent.character_card.character_card + "：" + agent.role_chat(""))
                    while True:
                        print("输入‘#’键结束聊天")
                        query = input(f"{agent.character_card.user_name}：")
                        if query == "#":
                            break
                        result = agent.role_chat(query)
                        print(agent.character_card.character_card + "：" +result)
        
        if __name__ == '__main__':
            main_chat()
    """
    res = clint.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": c}
        ]
    )
    print(res.choices[0].message.content)



if __name__ == '__main__':
    # result = openai_chat()
    # get_completion()
    # for chunk in result:
    #     print(chunk, end="", flush=True)
    # test_openai_call()
    # test_local_model()
    # test_anthropic()
    # test_agent()
    # test_load_history()
    # test_create_character_card()
    # test_agent_choose()
    test_openai()