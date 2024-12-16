import os
import time
import requests

SERVER_URL = "http://cc_server:5000"


def create_botnet_file():
    """Create a new file and register a bot in server."""
    
    bot_id = os.getenv("HOSTNAME")
    
    with open("/app/botnet.md", "w") as f:
        f.write("# Botnet Active\n")
        f.write("This bot is now part of the botnet network.\n")
        f.write(f"Bot ID: {bot_id}\n")
        
    print(f"Bot {bot_id} created its botnet.md file.")
    
    # Register bot in C&C server
    try:
        response = requests.post(f"{SERVER_URL}/register", json={"bot_id": bot_id})
        if response.status_code == 200:
            print(f"Bot {bot_id} registered successfully.")
            return
        else:
            print(f"Failed to register bot {bot_id}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error registering bot: {e}")

def execute_command(command):
    if command == "update a file":
        with open("/app/botnet.md", "a") as f:
            f.write("New log entry added to botnet.md\n")
        print(f"Bot {os.getenv('HOSTNAME')} updated botnet.md with a new log entry.")
    elif command == "inactive":
        print(f"Bot {os.getenv('HOSTNAME')} is inactive, waiting for activation.")

def activate_next():
    """Request server to activate next bot."""
    
    bot_id = os.getenv("HOSTNAME")
    try:
        response = requests.post(f"{SERVER_URL}/activate_next", json={"bot_id": bot_id})
        if response.status_code == 200:
            status = response.json().get("status")
            if status == "next_bot_activated":
                activated_bot = response.json().get("activated_bot")
                print(f"New machine infected: Bot {activated_bot} activated by {bot_id}.")
            elif status == "no_more_bots":
                print("No more bots to activate.")
                return
            else:
                print(f"Failed to activate next bot.")
        else:
            print(f"Failed to contact server for next bot activation.")
    except Exception as e:
        print(f"Error activating next bot: {e}")

def main():
    create_botnet_file()
    while True:
        try:
            bot_id = os.getenv("HOSTNAME")
            # Request commands to C&C
            response = requests.get(f"{SERVER_URL}/command", params={"bot_id": bot_id})
            if response.status_code == 200:
                command = response.json().get("command", "fail")
                execute_command(command)
                # If bot is active, activate the next one
                if command == "update a file":
                    activate_next()
            else:
                print(f"Bot {bot_id} failed to fetch command from C&C server.")
        except Exception as e:
            print(f"Bot {bot_id} Error connecting to C&C server: {e}")
        time.sleep(5)  # 5 second cooldown

if __name__ == "__main__":
    main()

