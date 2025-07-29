# App Store Connect AI Terminal

This project provides a web server that exposes the App Store Connect API and an AI-powered terminal client to interact with it using natural language.

## Project Structure

- `app_store_connect_server.py`: The main Flask server that exposes App Store Connect API endpoints.
- `ai_terminal_client.py`: The AI-powered terminal client.
- `app_store_connect_api.py`: A wrapper for the App Store Connect API.
- `ollama_integration.py`: Handles communication with the Ollama service.
- `web_server.py`: The underlying web server for the tools.
- `start_app_store_connect_server.sh`: A script to start the server.
- `requirements.txt`: Python dependencies.

## Setup

1.  **Install Dependencies:**
    Make sure you have Python 3 installed. Then, install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Install and run Ollama:**
    Follow the instructions at [Ollama's website](https://ollama.ai) to install and run Ollama on your system. You will also need to pull a model for the AI client to use:
    ```bash
    ollama pull deepseek-r1:1.5b 
    ```
    *(You can change the model in `ai_terminal_client.py`)*

3.  **App Store Connect API Key:**
    Make sure you have your App Store Connect API key (`.p8` file) and the correct `KEY_ID` and `ISSUER_ID`.

## How to Run

1.  **Start the Server:**
    Open a terminal and run the server script:
    ```bash
    ./start_app_store_connect_server.sh
    ```
    This will start the web server on `http://127.0.0.1:5001`.

2.  **Run the AI Client:**
    In a separate terminal, run the AI-powered client:
    ```bash
    python ai_terminal_client.py
    ```

You can now interact with the App Store Connect API by typing natural language commands in the client. For example: "list my apps" or "show me the builds for my app". 