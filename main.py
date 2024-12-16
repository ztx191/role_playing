from src.agent import RoleSetting
import os
if __name__ == '__main__':
    setting = RoleSetting.create()
    path = os.path.join(setting.character_cards_path, f"{setting.character_card}.txt")
    with open(path, "r", encoding="utf-8") as f:
        data = f.read()
    print(data)