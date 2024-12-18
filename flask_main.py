from flask import Flask, request, jsonify, send_from_directory

from src.agent import RoleAgent

app = Flask(__name__)

# 初始化全局代理
role_agent = RoleAgent()
agent, _ = role_agent.choose_character_card("张晓", "主人")
agent.load_llm()

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')


@app.route('/chat', methods=['POST'])
def chat():
    global agent
    data = request.json
    user_input = data.get('input', '')
    user_name = data.get('user_name', None)

    if not user_name:
        return jsonify({"status": "error", "message": "请输入您想扮演的角色"})

    agent.character_card.set_user_name(user_name)

    response = agent.role_chat(user_input)
    conversation = {
        f"{user_name}": user_input,
        agent.character_card.character_card: response
    }

    return jsonify({
        "status": "success",
        "current_character": agent.character_card.character_card,
        "user_name": user_name,
        "response": response,
        "conversation": conversation
    })


@app.route('/change', methods=['POST'])
def change():
    global agent
    data = request.json
    new_character_name = data.get('new_character_name', '')

    agent, status = agent.choose_character_card(new_character_name)
    agent.character_card.set_user_name(None)

    if status == "角色卡未找到":
        create_new = data.get('create_new', False)
        if create_new:
            character_setting = data.get('character_setting', '')
            agent.get_user_input(create_new, new_character_name, character_setting)
            agent.character_card.set_user_name(None)
            return jsonify({"status": "success", "message": "创建角色卡成功"})
        else:
            return jsonify({"status": "error", "message": "角色卡未找到！"})
    else:
        return jsonify({"status": "success", "message": "切换角色卡成功"})


@app.route('/history', methods=['POST'])
def history():
    global agent
    data = request.json
    action = data.get('action', '').lower()

    if action == "clear":
        if not agent.character_card.chat_history:
            return jsonify({"status": "info", "message": "当前无历史记录"})
        else:
            agent.save_chat_history()
            agent.character_card.chat_history = list()
            return jsonify({"status": "success", "message": "历史记录已清空"})
    elif action == "save":
        if not agent.character_card.chat_history:
            return jsonify({"status": "info", "message": "当前无历史记录"})
        else:
            agent.save_chat_history()
            return jsonify({"status": "success", "message": "历史记录已保存"})
    elif action == "view":
        if not agent.character_card.chat_history:
            return jsonify({"status": "info", "message": "当前无历史记录"})
        else:
            return jsonify({"status": "success", "history": agent.character_card.chat_history})
    else:
        return jsonify({"status": "error", "message": "无效的操作"})


if __name__ == '__main__':
    app.run(debug=True)



