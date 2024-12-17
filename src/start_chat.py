from src.request_model import StartRequest, CharacterCardRequest
from src.llm_call import LocalLLMCall, GPTModel
from src.agent import RoleAgent

role_agent = RoleAgent()

def switch_character_card(setting: CharacterCardRequest):
    if not setting.character_name:
        _role_agent, status = role_agent.choose_character_card()
    else:
        _role_agent, status = role_agent.choose_character_card(setting.character_name)
    if status == "角色卡未找到":
        if setting.user_input.lower() == "y":
            print("开始创建角色卡...")
            # 后续补充
        _role_agent.get_user_input(setting.user_input,
                                   character_card=setting.character_name,
                                   user_name=setting.user_name)




def init_chat(settings: StartRequest):
    role_agent = RoleAgent()
    if settings.model_from == "local":
        client = LocalLLMCall(lora_path=settings.local_lora_path)
    if settings.model_from == "deployed":
        client = GPTModel()





