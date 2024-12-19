from flask import Flask, send_from_directory, request, jsonify
from src.agent import RoleAgent

app = Flask(__name__)
agent = RoleAgent()


@app.route('/')
def index():
    global agent
    agent.load_default_setting()
    agent.load_llm()
    return send_from_directory('static','index.html')

@app.route('/save_history', methods=['POST'])
def save_history():
    global agent
    agent.save_chat_history()
    return jsonify({"message": "历史记录已保存", "clear_chat": True})


@app.route('/clear', methods=['POST'])
def clear_history():
    global agent
    agent.character_card.chat_history = list()
    return jsonify({"message": "历史记录已清空"})


@app.route('/create_character', methods=['POST'])
def create_character():
    global agent
    data = request.json
    character_name = data.get('character_name')
    character_setting = data.get('character_setting')

    if character_name in agent.character_card.get_character_list():
        return jsonify({"message": "角色卡已存在，是否修改其设定？", "action": "modify"})
    else:
        agent.choose_character_card(character_name, character_setting)
        return jsonify({"message": "创建角色卡成功", "action": "created"})


@app.route('/confirm_modify_character', methods=['POST'])
def confirm_modify_character():
    global agent
    data = request.json
    character_name = data.get('character_name')
    character_setting = data.get('character_setting')
    agent.choose_character_card(character_name, character_setting)
    return jsonify({"message": "修改角色卡设定成功"})


@app.route('/choose_character', methods=['POST'])
def choose_character():
    global agent
    data = request.json
    character_name = data.get('character_name')
    user_role = data.get('user_role')

    if character_name in agent.character_card.get_character_list():
        agent.choose_character_card(character_name, user_switch=True)
        agent.character_card.set_user_name(user_role)
        return jsonify({"message": f"切换到角色{agent.character_card.character_card}"})
    else:
        return jsonify({"message": "角色卡未找到"})


@app.route('/chat', methods=['POST'])
def chat():
    global agent
    data = request.json
    query = data.get('query')
    result = agent.role_chat(query)
    return jsonify({"response": result})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)



