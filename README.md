# Ollama Web Chat Application

A beautiful and modern web application for chatting with Ollama AI models. This application allows you to connect to any Ollama instance (local or cloud), select from available models, and have interactive conversations.

## Features

### Core Features
- 🌐 **Dual Mode Support** - Switch between Local Hosting and Cloud Service
- 🔑 **API Key Authentication** - Secure connection to Ollama cloud service
- 🖥️ **Local LLM Hosting** - Connect to your local Ollama instance
- ☁️ **Cloud Service Integration** - Use Ollama's cloud service with API key
- 🤖 **Multiple Model Support** - Select from any available model on your Ollama instance
- 💬 **Real-time Streaming** - See responses as they're generated

### Enhanced UI Features ✨ NEW!
- 🎨 **Modern Enhanced Interface** - Beautiful, polished design with smooth animations
- 🌓 **Dark Mode Toggle** - Switch between light and dark themes
- 📝 **Markdown Rendering** - Full markdown support with syntax highlighting
- 📋 **Copy Messages** - One-click copy for any message
- 💾 **Export Conversations** - Export as Text, Markdown, or JSON
- 🔔 **Toast Notifications** - Non-intrusive status updates
- ⌨️ **Keyboard Shortcuts** - Power user shortcuts for common actions
- 🟢 **Connection Status** - Live connection indicator in header
- 📊 **Model Information** - See current model at a glance
- 💡 **LocalStorage** - Saves your theme and mode preferences
- 📱 **Fully Responsive** - Perfect on desktop, tablet, and mobile

## 📚 Documentation

**New here?** Start with [START_HERE.md](START_HERE.md)!

Complete documentation index: [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)

---

## Prerequisites

- Python 3.7 or higher
- Access to an Ollama instance (local or cloud)

## Installation

1. Clone or download this repository to your local machine

2. Install the required Python packages:
```bash
pip install -r requirements.txt
```

## Usage

### Option 1: Quick Start (Local Mode)

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh  # Make script executable (first time only)
./start.sh
```

### Option 2: Cloud Mode with Pre-configured API Key

**Windows:**
```bash
start_with_cloud.bat
```

**Linux/Mac:**
```bash
chmod +x start_with_cloud.sh  # Make script executable (first time only)
./start_with_cloud.sh
```

### Option 3: Manual Start

**Windows:**
```bash
# Set API key (optional, for cloud mode)
set OLLAMA_API_KEY=your-api-key-here

# Start app
python app.py
```

**Linux/Mac:**
```bash
# Set API key (optional, for cloud mode)
export OLLAMA_API_KEY='your-api-key-here'

# Start app
python3 app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000              # Enhanced UI (default)
http://localhost:5000/classic      # Classic UI
```

**We recommend the enhanced version for the best experience!**

3. Configure your Ollama connection:
   
   **For Local Hosting:**
   - Click "🖥️ Local Hosting" button (default mode)
   - The URL will be pre-filled with `http://localhost:11434`
   - Click "Load Models" to fetch available models
   - Select a model from the dropdown
   
   **For Cloud Service:**
   - Click "☁️ Cloud Service" button
   - The URL will automatically change to `https://ollama.com`
   - Enter your API key (or use the pre-filled one)
   - Click "Load Models" to fetch available models
   - Select a model from the dropdown

4. Start chatting!
   - Type your message in the input box
   - Press Enter or click "Send"
   - Watch as the AI responds in real-time

## Configuration

### Environment Variables

You can optionally set a default Ollama URL using an environment variable:

```bash
# Windows
set OLLAMA_URL=http://your-ollama-instance:11434

# Linux/Mac
export OLLAMA_URL=http://your-ollama-instance:11434
```

### Ollama Setup

**For Local Hosting:**

If you don't have Ollama installed:

1. Visit [ollama.ai](https://ollama.ai) to download and install Ollama
2. Pull a model (e.g., `ollama pull llama2`)
3. The default local URL is `http://localhost:11434`

**For Cloud Service:**

1. Sign up for Ollama cloud service at [ollama.com](https://ollama.com)
2. Obtain your API key from the cloud dashboard
3. Enter your API key in the application when in Cloud Service mode
4. The application will automatically use the cloud endpoint: `https://ollama.com`

**Note:** The cloud service uses the endpoint `https://ollama.com` and requires Bearer token authentication with your API key.

## Testing the Connection

Before using the web interface, you can test your Ollama cloud connection:

**Windows:**
```bash
# Set API key
set_api_key.bat

# Run test
python test_ollama_cloud.py
```

**Linux/Mac:**
```bash
# Set API key (use 'source' to set in current shell)
source set_api_key.sh

# Run test
python3 test_ollama_cloud.py
```

This test script will:
- Verify your API key is set correctly
- List all available models
- Run a sample chat to confirm everything works

## Project Structure

```
.
├── app.py                      # Flask backend with API endpoints
├── templates/
│   ├── index.html             # Classic UI
│   └── index_enhanced.html    # Enhanced UI (default) ✨
├── requirements.txt           # Python dependencies
├── test_ollama_cloud.py       # Test script for cloud connection
│
├── start.bat                  # Windows launcher (local mode)
├── start.sh                   # Linux/Mac launcher (local mode)
├── start_with_cloud.bat       # Windows launcher (cloud mode)
├── start_with_cloud.sh        # Linux/Mac launcher (cloud mode)
├── set_api_key.bat            # Windows API key setup
├── set_api_key.sh             # Linux/Mac API key setup
│
├── README.md                  # This file
├── DOCUMENTATION_INDEX.md     # Complete docs index ✨
├── START_HERE.md              # Quick start guide
├── QUICK_START.md             # Quick reference
├── USAGE_GUIDE.md             # Detailed usage instructions
├── WHATS_NEW.md               # What's new in v2.0 ✨
├── ENHANCEMENT_SUMMARY.md     # Enhancement overview ✨
├── ENHANCEMENT_FEATURES.md    # Feature details ✨
├── UI_COMPARISON.md           # Classic vs Enhanced ✨
├── KEYBOARD_SHORTCUTS.md      # Shortcuts reference ✨
├── CHANGES_SUMMARY.md         # Implementation notes
└── .gitignore                 # Git ignore rules
```

## API Endpoints

### POST /api/models
Fetches available models from the Ollama instance.

**Request Body:**
```json
{
  "ollama_url": "http://localhost:11434",
  "api_key": "optional-for-cloud-service"
}
```

**Response:**
```json
{
  "success": true,
  "models": ["llama2", "mistral", "codellama"]
}
```

### POST /api/chat
Streams chat responses from the selected model.

**Request Body:**
```json
{
  "ollama_url": "http://localhost:11434",
  "api_key": "optional-for-cloud-service",
  "model": "llama2",
  "messages": [
    {"role": "user", "content": "Hello!"}
  ]
}
```

**Response:** Server-Sent Events (SSE) stream with JSON chunks

## Troubleshooting

### Can't connect to Ollama
- Verify your Ollama instance is running
- Check the URL is correct (include `http://` or `https://`)
- Ensure there are no firewall issues blocking the connection

### No models showing up
- Make sure you have models installed on your Ollama instance
- Run `ollama list` in terminal to see available models
- Try pulling a model: `ollama pull llama2`

### Application won't start
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check that port 5000 is not already in use
- Try running with: `python app.py`

## Browser Compatibility

This application works best in modern browsers:
- Chrome/Edge (recommended)
- Firefox
- Safari

## Security Notes

- This application is designed for development/personal use
- **Never share your API keys publicly** - Keep them secure and private
- **API keys are stored in memory only** - They are not persisted to disk
- For production deployment, consider adding user authentication
- Use HTTPS for cloud Ollama connections
- Be cautious about exposing your Ollama instance to the internet
- The password field for API key hides your key from shoulder-surfers but doesn't encrypt it in browser memory

## License

This project is open source and available for personal and commercial use.

## Contributing

Feel free to fork, modify, and improve this application!

## Support

If you encounter any issues or have questions:
1. Check the Troubleshooting section above
2. Verify your Ollama instance is working correctly
3. Check the browser console for error messages

---

Enjoy chatting with your AI models! 🚀

