from src.agent import RoleAgent, CharacterCard
role_agent = RoleAgent()

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
role_agent.choose_character_card(character_card="张晓")
role_agent.character_card.set_user_name("主人")
print(f"你是{role_agent.character_card.character_card}的{role_agent.character_card.user_name}")
cnt = 0
while cnt < 5:
    query = input("请输入问题：")
    result = role_agent.role_chat(query)
    print(result)
    print()
    print(role_agent.character_card.chat_history)
    cnt += 1
role_agent.character_card.save_chat_history()
