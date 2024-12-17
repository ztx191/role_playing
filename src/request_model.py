from pydantic import BaseModel
from typing import Optional

class StartRequest(BaseModel):
    model_from : str = "deployed"
    local_lora_path : Optional[str] = None

class CharacterCardRequest(BaseModel):
    character_name : Optional[str] = None
    character_setting : Optional[str] = None
    user_name : Optional[str] = None
    user_input : Optional[str] = None