# App Store Connect MCP Server

This project provides an **MCP (Model Context Protocol) server** that exposes App Store Connect API functionality for use with AI assistants like Claude in Cursor IDE. It allows you to interact with App Store Connect programmatically through natural language queries.

## What is MCP?

MCP (Model Context Protocol) is a standard that allows AI assistants to securely connect to external data sources and tools. This server implements the MCP protocol to provide App Store Connect functionality to AI assistants.

## Features

- **App Management**: List apps, get app information, and manage app metadata
- **Build Management**: List and manage app builds
- **Beta Testing**: Manage beta groups, testers, and TestFlight distributions
- **Version Management**: Submit apps for review and release new versions
- **Performance Metrics**: Access app performance data
- **Secure Authentication**: Uses App Store Connect API keys for secure access

## Project Structure

### Core Files
- `app_store_connect_server.py`: Main MCP server implementing the JSON-RPC protocol
- `app_store_connect_api.py`: Core API wrapper with business logic
- `start_app_store_connect_server.sh`: Server startup script with environment setup
- `check_tools.py`: Utility for testing MCP tool discovery
- `requirements.txt`: Python dependencies
- `AppStoreConnectAuthKey.p8`: Your App Store Connect API private key

### AppStore Service Module (`appstore_service/`)
- `AppStore.py`: Main service class orchestrating all operations
- `api_auth.py`: Handles JWT authentication with App Store Connect
- `app_info_service.py`: App information and metadata operations
- `build_service.py`: Build management functionality
- `beta_service.py`: Beta testing and TestFlight operations
- `version_service.py`: App version and release management
- `performance_service.py`: App performance metrics
- `config.py`: Configuration constants (requires setup)
- `utils.py`: Shared utility functions

## Setup

### 1. Install Dependencies

Make sure you have Python 3.10+ installed, then install the required packages:

```bash
pip install -r requirements.txt
```

### 2. App Store Connect API Configuration

You need to set up App Store Connect API access:

1. **Generate API Key**: Go to [App Store Connect](https://appstoreconnect.apple.com/) → Users and Access → Keys → Create API Key
2. **Download the `.p8` file** and place it as `AppStoreConnectAuthKey.p8` in the project root
3. **Configure credentials** in `appstore_service/config.py`:

```python
KEY_ID = "YOUR_KEY_ID"  # 10-character key ID from App Store Connect
ISSUER_ID = "YOUR_ISSUER_ID"  # UUID from App Store Connect
PRIVATE_KEY_PATH = "AppStoreConnectAuthKey.p8"  # Path to your .p8 file
APP_ID = "YOUR_APP_ID"  # Your app's ID (optional, for specific operations)
EXPIRATION_MINUTES = 19  # JWT token expiration (max 20 minutes)
```

### 3. MCP Configuration

This server is designed to work with MCP-compatible AI assistants. For Cursor IDE:

1. Add this server to your MCP configuration
2. The server will start automatically when needed
3. Use the startup script: `./start_app_store_connect_server.sh`

## Usage

### With AI Assistants (Recommended)

Once configured with an MCP-compatible AI assistant, you can use natural language commands:

- "List all my apps"
- "Show me the latest builds for [app bundle ID]"
- "Create a new beta group for testing"
- "Submit version 1.2.3 for review"
- "Add a beta tester to the internal group"

### Direct API Access

The server exposes these MCP tools:

- `list_apps`: Get all applications
- `get_app_info`: Get detailed app information  
- `list_builds`: Get builds for an app
- `list_beta_groups`: Get beta testing groups
- `list_beta_testers`: Get testers in a group
- `create_beta_group`: Create new beta group
- `submit_for_review`: Submit app for App Store review
- `release_version`: Release a new app version

## Development

### Testing the Server

Test tool discovery:
```bash
python check_tools.py
```

### Logs

Server logs are written to `logs/app_store_connect_server.log` for debugging.

### Environment Setup

The startup script (`start_app_store_connect_server.sh`) automatically:
- Initializes pyenv if available
- Sets Python version to 3.10.4
- Configures logging
- Starts the MCP server

## Security Notes

- Keep your `.p8` API key file secure and never commit it to version control
- The `.gitignore` is configured to exclude sensitive files
- API tokens expire automatically (max 20 minutes)
- All communications use HTTPS when connecting to Apple's servers

## Troubleshooting

### Common Issues

1. **Authentication Errors**: Verify your KEY_ID, ISSUER_ID, and .p8 file are correct
2. **Permission Errors**: Ensure your API key has the necessary permissions in App Store Connect
3. **Python Version**: This project requires Python 3.10+ for optimal compatibility

### Debug Mode

Check the log file at `logs/app_store_connect_server.log` for detailed error information.

## Requirements

- Python 3.10+
- Valid App Store Connect API key
- MCP-compatible AI assistant (like Claude in Cursor)
- Active Apple Developer account

## License

This project is for educational and development purposes. Ensure compliance with Apple's App Store Connect API terms of service. 