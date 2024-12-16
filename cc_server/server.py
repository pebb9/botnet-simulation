from flask import Flask, request, jsonify

app = Flask(__name__)
registered_bots = []
active_bots = []

@app.route('/register', methods=['POST'])
def register_bot():
    bot_id = request.json.get("bot_id")
    if bot_id and bot_id not in registered_bots:
        registered_bots.append(bot_id)
        print(f"Bot {bot_id} registered.")
        
        # Activate firts bot
        if len(active_bots) == 0:
            active_bots.append(bot_id)
            print(f"Bot {bot_id} activated as the first bot.")
        return jsonify({"status": "registered"}), 200
    return jsonify({"status": "already_registered"}), 200

@app.route('/command', methods=['GET'])
def send_command():
    bot_id = request.args.get("bot_id")
    if bot_id in active_bots:
        return jsonify({"command": "update a file", "details": "Append a new log entry"}), 200
    
    elif bot_id in registered_bots and bot_id not in active_bots:
        # If bot is inactive, responds "inactive"
        return jsonify({"command": "inactive"}), 200
    return jsonify({"command": "fail"}), 200

@app.route('/activate_next', methods=['POST'])
def activate_next_bot():
    bot_id = request.json.get("bot_id")
    if bot_id in active_bots:
        # Search an inactive bot
        for bot in registered_bots:
            if bot not in active_bots:
                active_bots.append(bot)
                print(f"Bot {bot} activated by {bot_id}.")
                return jsonify({"status": "next_bot_activated", "activated_bot": bot}), 200
        
        # No more bots registered
        if len(registered_bots) == len(active_bots):
            return jsonify({"status": "no_more_bots"}), 200
        
    return jsonify({"status": "not_authorized"}), 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

