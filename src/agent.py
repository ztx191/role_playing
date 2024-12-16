import os
import json
from typing import ClassVar, Optional
import jinja2
from semantic_kernel.kernel_pydantic import KernelBaseSettings
from datetime import datetime

from src.llm_call import LocalLLMCall
from src.logger_setting import LoggerTemplate
from logging import DEBUG
file_path = os.path.basename(os.path.abspath(__file__))
logger_template = LoggerTemplate(file_path, f'./logs/{file_path[0:-3]}.log', print_to_console=True, level=DEBUG)
logger = logger_template.get_logger()

class RoleSetting(KernelBaseSettings):
    env_prefix: ClassVar[str] = "ROLE_"
    system_setting: str
    character_cards_path: str
    character_card: str = "张晓"
    user_name: str = "主人"
    history_prompt: str
    opening_remarks: str
    rag_prompt: str
    chat_history_path: str
    chat_history_size: int

class RAGSetting(KernelBaseSettings):
    env_prefix: ClassVar[str] = "RAG_"
    embedding_model: str
    rerank_model: str
    vector_db: str
    tok_k: int


class CharacterCard:
    def __init__(self, role_setting: RoleSetting = RoleSetting,
                 character_card: Optional[str] = None,
                 user_name: Optional[str] = None
                 ):
        self.role_setting = role_setting.create()
        if character_card:
            self.character_card = character_card
        else:
            self.character_card = self.role_setting.character_card
        if user_name:
            self.user_name = user_name
        else:
            self.user_name = self.role_setting.user_name
        self.character_setting = self.load_character_setting()
        self.chat_history_path = self.role_setting.chat_history_path
        self.chat_history = list()

    def load_character_setting(self):
        try:
            with open(os.path.join(self.role_setting.character_cards_path, f"{self.character_card}.txt"), "r", encoding="utf-8") as f:
                character_setting = f.read()
        except FileNotFoundError:
            logger.error("角色卡未找到")
            character_setting = "角色卡未找到"
        return character_setting

    def create_character_card(self, character_name: str, character_setting: str, user_name: str):
        with open(os.path.join(self.role_setting.character_cards_path, f"{character_name}.txt"), "w", encoding="utf-8") as f:
            f.write(character_setting)
        return CharacterCard(character_card=character_name, user_name=user_name)

    def save_chat_history(self):
        save_path = os.path.join(self.role_setting.chat_history_path, f"{self.character_card}")
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        logger.info(f"开始保存{self.user_name}与{self.character_card}的对话记录")
        save_path = os.path.join(save_path, f"{self.user_name}_{datetime.now().timestamp()}.json")
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(self.chat_history, f, ensure_ascii=False, indent=4)
        logger.info(f"保存成功，保存路径为：{save_path}")

    def load_last_chat_history(self):
        load_path = os.path.join(self.role_setting.chat_history_path, f"{self.character_card}")
        if not os.path.exists(load_path):
            logger.error(f"{self.character_card}不存在！")
            return "历史加载失败"
        else:
            user_chat = [file for file in os.listdir(load_path) if file.split("_")[0] == self.user_name]
            user_chat = sorted(user_chat, key=lambda x: float(x.replace(".join", "").split("_")[-1]))
            load_path = os.path.join(load_path, user_chat[-1])
            logger.info(f"开始加载{self.user_name}与{self.character_card}的最后一次对话记录")
            with open(load_path, "r", encoding="utf-8") as f:
                chat_history = json.load(f)
            logger.info(f"加载成功！")
            return chat_history

    def set_character_card(self, character_name: str, character_setting: str):
        pass

    def set_user_name(self, user_name: str):
        self.user_name = user_name

    def get_size_chat_history(self, size: int):
        return get_chat_size_history(self.chat_history, size)

    def get_chat_history(self):
        return self.chat_history

def pop_up_window():
    pass


def get_chat_size_history(history: list, size: int):
    chat_history = history[-size:]
    return chat_history

class RoleAgent:
    def __init__(self, agent_setting: RoleSetting = RoleSetting,
                 use_rag: bool = False, lora_path = None):
        if use_rag:
            self.rag_prompt = None
            self.rag_setting = None
            self.init_rag()
        self.use_rag = use_rag
        self.agent_setting = agent_setting.create()
        self.llm_call = LocalLLMCall(lora_path)
        self.system_prompt, self.history_prompt, self.opening_remarks = self.get_system_prompt()
        self.system_message = list()
        self.character_card = None
        self.chat_history_size = self.agent_setting.chat_history_size


    def get_user_input(self, user_input: str, character_card: str = None,
                       character_setting: str = None, user_name: str = None):
        if user_input.lower() == "y":
            logger.info("开始创建角色卡...")
            # input_character_card = input("请输入角色卡名称：(按回车结束)：")
            # input_character_setting = input("请输入角色卡设定：(按回车结束)：")
            # input_user_name = input("对话中你希望扮演的角色：(比如：主人，按回车结束)：")
            new_character_card = self.character_card.create_character_card(character_name=character_card,
                                                                          character_setting=character_setting,
                                                                          user_name=user_name)

            logger.info(f"角色卡“{character_card}”创建完成！")
            self.character_card = new_character_card
        else:
            if not self.character_card:
                logger.info("你当前未选择角色卡，开始加载默认角色“张晓”")
                self.character_card = CharacterCard(character_card="张晓")

    def choose_character_card(self, character_card: Optional[str] = None, user_name: Optional[str] = None,
                              character_setting: Optional[str] = None, callback=pop_up_window):
        now_character_card = CharacterCard(character_card=character_card)
        if now_character_card.character_setting == "角色卡未找到":
            return self, "角色卡未找到"
        else:
            logger.info(f"开始加载角色卡{character_card}")
            self.character_card = now_character_card
            return self, None

    def get_system_prompt(self):
        with open(self.agent_setting.system_setting, "r", encoding="utf-8") as f:
            system_prompt = f.read()
        system_prompt = jinja2.Template(system_prompt)
        with open(self.agent_setting.history_prompt, "r", encoding="utf-8") as f:
            history_prompt = f.read()
        history_prompt = jinja2.Template(history_prompt)
        with open(self.agent_setting.opening_remarks, "r", encoding="utf-8") as f:
            opening_remarks = f.read()
        opening_remarks = jinja2.Template(opening_remarks)
        return system_prompt, history_prompt, opening_remarks

    def init_rag(self, rag_setting: RAGSetting = RAGSetting):
        self.rag_setting = rag_setting.create()
        with open(self.agent_setting.rag_prompt, "r", encoding="utf-8") as f:
            rag_prompt = f.read()
        rag_prompt = jinja2.Template(rag_prompt)
        self.rag_prompt = rag_prompt
        pass

    def get_top_k(self, query: str):
        if not self.use_rag:
            return query
        else:
            pass

    def role_chat(self, query: str, history: Optional[list] = None):
        system_prompt = self.system_prompt.render(character_card=self.character_card.character_card,
                                                  user_name=self.character_card.user_name,
                                                  character_setting=self.character_card.character_setting)
        opening_remarks = self.opening_remarks.render(character_card=self.character_card.character_card,
                                                      user_name=self.character_card.user_name)
        self.system_message = [{"role": "system", "content": system_prompt}]
        if not history:
            messages = self.system_message
            if query == "":
                if not self.character_card.chat_history:
                    message = [{"role": "user", "content": opening_remarks}]
                    messages.extend(message)
                    result = self.llm_call.chat(messages)
                    message.extend([{"role": "assistant", "content": result}])
                    self.character_card.chat_history.extend(message)
                    return result
                else:
                    return "你想要对我说什么"
            else:
                message = [{"role": "user", "content": query}]
                if len(self.character_card.chat_history) > self.chat_history_size:
                    logger.info(f"当前对话历史记录过多，将截断至对话记录中最近的{self.chat_history_size}个记录")
                    _history = get_chat_size_history(self.character_card.chat_history, self.chat_history_size)
                else:
                    _history = self.character_card.chat_history
                messages.extend(_history)
                messages.extend(message)
                result = self.llm_call.chat(messages)
                message.extend([{"role": "assistant", "content": result}])
                self.character_card.chat_history.extend(message)
                return result
        else:
            # 加载当前对话环境中两者最近一次聊天记录
            # 若长度超过设定值，截断
            if len(history) > self.chat_history_size:
                logger.info(f"当前对话历史记录过多，将截断至对话记录中最近的{self.chat_history_size}个记录")
                _history = get_chat_size_history(history, self.chat_history_size)
            else:
                _history = history
            if query == "":
                return ""
            else:
                message = [{"role": "user", "content": query}]
                messages = self.system_message
                messages.extend(_history)
                messages.extend(message)
                result = self.llm_call.chat(messages)
                message.extend([{"role": "assistant", "content": result}])
                history.extend(message)
                self.character_card.chat_history.extend(history)
                return result
    def save_chat_history(self):
        if not self.character_card:
            logger.info("你当前未选择角色卡，无法保存聊天记录")
            return "无法保存"
        else:
            self.character_card.save_chat_history()
            return "保存成功"






