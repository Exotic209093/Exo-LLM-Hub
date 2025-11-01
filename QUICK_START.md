# Quick Start Guide

## ✨ NEW: Enhanced UI with Dark Mode, Markdown & More!

## 🚀 Getting Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Start the Application
**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh && ./start.sh
```

### Step 3: Open Browser
Navigate to: **http://localhost:5000** (Enhanced UI - Recommended!)

Or: **http://localhost:5000/classic** (Classic UI)

### 🎉 New Features You'll Love
- 🌓 Dark mode toggle
- 📝 Markdown rendering with code highlighting  
- 📋 One-click message copying
- 💾 Export conversations (Text/MD/JSON)
- ⌨️ Keyboard shortcuts (`Ctrl+K`, `Ctrl+D`, etc.)

---

## 🎯 Usage Modes

### 🖥️ Local Hosting Mode (Default)

**When to use:** You have Ollama installed on your local machine

1. Click **"🖥️ Local Hosting"** button
2. URL is pre-filled: `http://localhost:11434`
3. Click **"Load Models"**
4. Select a model from dropdown
5. Start chatting!

**Prerequisites:**
- Ollama installed locally
- At least one model pulled (e.g., `ollama pull llama2`)

---

### ☁️ Cloud Service Mode

**When to use:** You want to use Ollama's cloud service

1. Click **"☁️ Cloud Service"** button
2. URL automatically changes to: `https://ollama.com`
3. API key is pre-filled (or enter your own)
4. Click **"Load Models"**
5. Select a model from dropdown
6. Start chatting!

**Prerequisites:**
- Valid Ollama cloud API key from [ollama.com](https://ollama.com)
- Active internet connection
- Endpoint: `https://ollama.com` (automatically set)

---

## 💡 Tips

### Switching Between Modes
- You can switch modes at any time
- The chat history is preserved
- Models need to be reloaded after switching

### API Key Management
- API keys are only stored in browser memory
- They are never saved to disk
- The password field hides your key from view

### Model Selection
- Different models may be available in local vs cloud
- Cloud models are typically more powerful
- Local models run on your hardware

### Clear Chat
- Click "Clear Chat" to start a fresh conversation
- This resets the conversation history
- Model selection remains unchanged

---

## 🔧 Troubleshooting

### Local Mode Issues
**"Failed to connect to Ollama"**
- Ensure Ollama is running: `ollama serve`
- Check the URL is correct
- Verify firewall settings

**"No models found"**
- Pull a model: `ollama pull llama2`
- Run `ollama list` to see installed models

### Cloud Mode Issues
**"Failed to connect to Ollama"**
- Verify your API key is correct
- Check your internet connection
- Ensure the cloud service is available

**"Unauthorized" error**
- Your API key may be invalid or expired
- Get a new API key from your dashboard

---

## ⌨️ Keyboard Shortcuts

- **Enter** - Send message
- **Shift + Enter** - New line in message

---

## 📝 Example Conversations

### For Code Help:
```
User: Write a Python function to reverse a string
AI: Here's a simple function...
```

### For General Questions:
```
User: Explain quantum computing in simple terms
AI: Quantum computing is...
```

### For Creative Writing:
```
User: Write a short story about a robot learning to paint
AI: Once upon a time...
```

---

## 🆘 Need Help?

Refer to the main [README.md](README.md) for:
- Detailed installation instructions
- API documentation
- Configuration options
- Security notes

---

**Enjoy chatting with your AI models! 🎉**

