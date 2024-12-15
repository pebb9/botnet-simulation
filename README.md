# Botnet Simulation with Docker

This project simulates a botnet using Docker and Flask. Each bot connects to a C&C (Command and Control) server, receives commands, and executes actions such as updating a `botnet.md` file. The main goal of this project is to understand how botnets operate and how to simulate their behavior in a controlled environment.

## Project Components

This project consists of two main services:

1. **C&C Server (Command and Control)**: A Flask server that sends commands to the bots.
2. **Bots**: Bot instances that connect to the C&C server, receive commands, and execute them.

## Architecture

The project is based on Docker Compose, which allows you to spin up multiple containers simulating the bots and the C&C server on a network.

The basic architecture consists of:

- **cc_server**: The C&C server that manages the bots.
- **bot**: The bots that connect to the server and receive commands.

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

- **C&C Server**: When the containers are started, the C&C server will start listening on port 5000.
- **Bots**: The bots will automatically register with the C&C server and receive a dynamic command to update a file named `botnet.md`.
- **botnet.md** File: This file is created or updated in the bot containers, with entries like "Bot X added a log entry".

## Automated Commands

The bots will automatically receive the following command upon registration:

```
Update botnet.md
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
