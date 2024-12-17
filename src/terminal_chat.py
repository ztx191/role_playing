from src.llm_call import LocalLLMCall, GPTModel
from src.agent import RoleAgent


def init_agent():
    role_agent = RoleAgent()
    agent, status = role_agent.choose_character_card("张晓", "主人")
    return agent

def main_chat():
    agent = init_agent()
    print(f"欢迎使用智障聊天机器人，当前为默认角色{agent.character_card.character_card}")
    print("指令：\nc清空历史，\nh切换角色卡，\ns保存对话历史，\nq退出，\nenter键开始后续")
    while True:
        user_input = input("请输入：")
        if user_input.lower() == "c":
            if not agent.character_card.chat_history:
                print("当前无历史记录")
            else:
                agent.save_chat_history()
                agent.character_card.chat_history = list()
            continue
        elif user_input.lower() == "s":
            if not agent.character_card.chat_history:
                print("当前无历史记录")
            else:
                agent.save_chat_history()
            continue
        elif user_input.lower() == "q":
            print("退出")
            return
        elif user_input.lower() == "h":
            input_c = input("请输入角色卡名称(enter键结束)：")
            agent, status = agent.choose_character_card(input_c)
            if status == "角色卡未找到":
                input_user_main = input("角色卡未找到，是否创建该角色卡：")
                if input_user_main.lower() == "y":
                    input_s = input("请输入角色卡设定：")
                    agent.get_user_input(input_user_main, input_c, input_s)
                    print("创建角色卡成功")
                else:
                    print("创建角色卡失败！enter键继续当前聊天")
            else:
                print("切换角色卡成功")
            continue
        else:
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

