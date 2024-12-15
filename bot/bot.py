import os
import time
import requests

SERVER_URL = "http://cc_server:5000"

def create_botnet_file():
    """Crea un archivo botnet.md y registra el bot en el servidor."""
    bot_id = os.getenv("HOSTNAME")  # ID único del contenedor
    with open("/app/botnet.md", "w") as f:
        f.write("# Botnet Active\n")
        f.write("This bot is now part of the botnet network.\n")
        f.write(f"Bot ID: {bot_id}\n")
    print(f"Bot {bot_id} created its botnet.md file.")
    # Enviar registro al servidor
    try:
        response = requests.post(f"{SERVER_URL}/register", json={"bot_id": bot_id})
        if response.status_code == 200:
            print(f"Bot {bot_id} registered successfully.")
        else:
            print(f"Failed to register bot {bot_id}.")
    except Exception as e:
        print(f"Error registering bot: {e}")

def execute_command(command):
    """Ejecuta el comando recibido del servidor."""
    if command == "Update botnet.md":
        with open("/app/botnet.md", "a") as f:
            f.write("New log entry added to botnet.md\n")
        print(f"Bot {os.getenv('HOSTNAME')} updated botnet.md with a new log entry.")
    elif command == "inactive":
        print(f"Bot {os.getenv('HOSTNAME')} is inactive, waiting for activation.")

def activate_next():
    """Solicita al servidor que active el siguiente bot."""
    bot_id = os.getenv("HOSTNAME")
    try:
        response = requests.post(f"{SERVER_URL}/activate_next", json={"bot_id": bot_id})
        if response.status_code == 200 and response.json().get("status") == "next_bot_activated":
            activated_bot = response.json().get("activated_bot")
            print(f"New machine infected: Bot {activated_bot} activated by {bot_id}.")
        elif response.status_code == 200:
            print("No more bots to activate.")
        else:
            print(f"Failed to activate next bot.")
    except Exception as e:
        print(f"Error activating next bot: {e}")

def main():
    create_botnet_file()
    while True:
        try:
            bot_id = os.getenv("HOSTNAME")
            # Solicita comandos al servidor de C&C
            response = requests.get(f"{SERVER_URL}/command", params={"bot_id": bot_id})
            if response.status_code == 200:
                command = response.json().get("command", "No Command")
                execute_command(command)
                # Si este bot está activo, activa el siguiente
                if command == "Update botnet.md":
                    activate_next()
            else:
                print(f"Bot {bot_id} failed to fetch command from C&C server.")
        except Exception as e:
            print(f"Bot {bot_id} Error connecting to C&C server: {e}")
        time.sleep(5)  # Espera 5 segundos antes de volver a intentar

if __name__ == "__main__":
    main()

