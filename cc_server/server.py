from flask import Flask, request, jsonify

app = Flask(__name__)
registered_bots = []  # Lista de bots registrados
active_bots = []      # Lista de bots activos

@app.route('/register', methods=['POST'])
def register_bot():
    """Registra un bot con su ID."""
    bot_id = request.json.get("bot_id")
    if bot_id and bot_id not in registered_bots:
        registered_bots.append(bot_id)
        print(f"Bot {bot_id} registered.")
        # Activar el primer bot registrado automáticamente
        if len(active_bots) == 0:
            active_bots.append(bot_id)
            print(f"Bot {bot_id} activated as the first bot.")
        return jsonify({"status": "registered"}), 200
    return jsonify({"status": "already_registered"}), 200

@app.route('/command', methods=['GET'])
def send_command():
    """Envía comandos específicos a los bots."""
    bot_id = request.args.get("bot_id")
    if bot_id in active_bots:
        return jsonify({"command": "Update botnet.md", "details": "Append a new log entry"}), 200
    elif bot_id in registered_bots and bot_id not in active_bots:
        # Si el bot no está activo, responde con "inactive"
        return jsonify({"command": "inactive"}), 200
    return jsonify({"command": "No Command"}), 200

@app.route('/activate_next', methods=['POST'])
def activate_next_bot():
    """Activa el siguiente bot registrado."""
    bot_id = request.json.get("bot_id")
    if bot_id in active_bots:
        # Buscar un bot inactivo para activar
        for bot in registered_bots:
            if bot not in active_bots:
                active_bots.append(bot)
                print(f"Bot {bot} activated by {bot_id}.")
                return jsonify({"status": "next_bot_activated", "activated_bot": bot}), 200
        return jsonify({"status": "no_more_bots"}), 200
    return jsonify({"status": "not_authorized"}), 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

