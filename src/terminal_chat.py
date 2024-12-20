from src.llm_call import LocalLLMCall, GPTModel
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
                agent.save_agent_chat_history()
                agent.character_card.chat_history = list()
                print("历史记录已清空")
        elif user_input.lower() == "s":
            if not agent.character_card.chat_history:
                print("当前无历史记录")
            else:
                agent.save_agent_chat_history()
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

