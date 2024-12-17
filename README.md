# Botnet Simulation with Docker

This project simulates a botnet using Docker and Flask. Each bot connects to a C&C (Command and Control) server, registers itself, and activates other bots dynamically, emulating how botnets propagate in real scenarios. The main goal of this project is to understand how botnets operate and how to simulate their behavior in a controlled environment.

## Project Components

This project consists of two main services:

1. **C&C Server (Command and Control)**: A Flask server that registers bots, sends commands, and manages their activation.
2. **Bots**: Bot instances that:

   - Register with the C&C server.
   - Execute commands (in this case, update a file) when activated.
   - Dynamically activate other bots.

## Architecture (Hybrid Model)

The botnet simulation uses a hybrid architecture that combines centralized and decentralized models:

1. **Centralized Control**:

   - The C&C (Command and Control) server acts as the central authority, managing the registration of bots and issuing commands.
   - Bots initially connect to the C&C server to register and receive commands.

2. **Dynamic Activation (Decentralized Propagation)**:

   - After the first bot is activated, it dynamically propagates the activation process to other bots.
   - Each active bot contacts the C&C server to activate the next inactive bot in the sequence.

This hybrid approach emulates real-world botnets that use centralized control for initial coordination and decentralized propagation to increase resilience and scalability.

## Requirements

- Docker
- Docker Compose

## Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/pebb9/botnet-simulation.git
   cd botnet-simulation
   ```

2. Build the images and bring up the containers using Docker Compose:

   ```bash
   docker-compose up --build --scale bot=3
   ```

   This will bring up 3 bot instances along with the C&C server.

## How It Works

1. **C&C Server Initialization**:

   - The server starts on port 5000.
   - Bots communicate with the server through the `/register` and `/command` endpoints.

2. **Bot Registration and Activation**:

   - Each bot registers itself upon startup and receives a "registration success" confirmation.
   - The first bot becomes active immediately and starts activating the other bots sequentially.

3. **Bot Activation Propagation**:

   - An active bot will send a request to the server to activate the next inactive bot.
   - This process continues until all bots are activated.

## Automated Commands

The activated bots will automatically receive the following command upon registration:

```
update a file
```

This command causes each bot to add a line to the `botnet.md` file with its container ID.

## Verification

You can verify that the bots are executing the commands correctly with the following command:

```bash
docker-compose logs -f
```

Additionally, you can check the `botnet.md` file within the bot containers to ensure the updates are being made.

## License

This project is licensed under the GNU GPL v3 License. See the `LICENSE` file for more details.
