# Complete Usage Guide

## 🎯 Three Ways to Use This Application

---

## Method 1: Local Ollama (Easiest for local setup)

### Prerequisites
- Ollama installed on your machine
- At least one model pulled

### Steps

1. **Install Ollama** (if not already installed)
   ```bash
   # Visit https://ollama.ai to download
   ```

2. **Pull a model**
   ```bash
   ollama pull llama2
   # or
   ollama pull mistral
   ```

3. **Start Ollama service**
   ```bash
   ollama serve
   ```

4. **Run the web app**
   ```bash
   # Windows
   start.bat
   
   # Linux/Mac
   ./start.sh
   ```

5. **Use the interface**
   - Open http://localhost:5000
   - Click "🖥️ Local Hosting" (already selected by default)
   - Click "Load Models"
   - Select a model and start chatting!

---

## Method 2: Cloud Service with Web Interface

### Prerequisites
- Valid Ollama cloud API key
- Internet connection

### Steps

1. **Run the cloud-enabled launcher**
   ```bash
   # Windows
   start_with_cloud.bat
   
   # Linux/Mac
   ./start_with_cloud.sh
   ```

2. **Use the interface**
   - Open http://localhost:5000
   - Click "☁️ Cloud Service"
   - API key should be pre-filled
   - Click "Load Models"
   - Select a model and start chatting!

---

## Method 3: Test Cloud Connection (Python Script)

### Prerequisites
- Valid Ollama cloud API key
- Python environment set up

### Steps

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set API key**
   ```bash
   # Windows PowerShell
   $env:OLLAMA_API_KEY = "your-api-key-here"
   
   # Windows Command Prompt
   set OLLAMA_API_KEY=your-api-key-here
   
   # Linux/Mac
   export OLLAMA_API_KEY="your-api-key-here"
   
   # Or use the helper script
   # Windows: set_api_key.bat
   # Linux/Mac: source set_api_key.sh
   ```

3. **Run test script**
   ```bash
   python test_ollama_cloud.py
   ```

This will:
- Verify your API key
- List all available models
- Run a test chat conversation
- Show detailed error messages if something goes wrong

---

## 🔧 Configuration Options

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OLLAMA_URL` | Default Ollama endpoint | `http://localhost:11434` |
| `OLLAMA_API_KEY` | Cloud service API key | None (must be set for cloud) |
| `FLASK_DEBUG` | Enable Flask debug mode | `False` |

### Setting Environment Variables

**Windows PowerShell:**
```powershell
$env:OLLAMA_API_KEY = "your-api-key"
$env:OLLAMA_URL = "https://ollama.com"
```

**Windows Command Prompt:**
```cmd
set OLLAMA_API_KEY=your-api-key
set OLLAMA_URL=https://ollama.com
```

**Linux/Mac:**
```bash
export OLLAMA_API_KEY="your-api-key"
export OLLAMA_URL="https://ollama.com"
```

---

## 🚨 Troubleshooting

### Local Mode Issues

**"Failed to connect to Ollama"**
- ✅ Check if Ollama is running: `ollama serve`
- ✅ Verify URL is `http://localhost:11434`
- ✅ Check firewall settings

**"No models found"**
- ✅ Pull a model: `ollama pull llama2`
- ✅ List models: `ollama list`

### Cloud Mode Issues

**"Failed to connect to Ollama" or "Max retries exceeded"**
- ✅ Verify URL is `https://ollama.com` (not cloud.ollama.ai)
- ✅ Check internet connection
- ✅ Verify API key is correct

**"API key is required"**
- ✅ Make sure you entered the API key in the interface
- ✅ Or set `OLLAMA_API_KEY` environment variable

**"Unauthorized" error (401)**
- ✅ Your API key may be invalid or expired
- ✅ Check the cloud dashboard for a new key
- ✅ Ensure no extra spaces in the API key

**"NameResolutionError" or DNS errors**
- ✅ Check for typos in the URL (common: `olama` vs `ollama`)
- ✅ Verify internet connection
- ✅ Try different DNS servers

### Test Script Errors

**"ImportError: No module named 'ollama'"**
```bash
pip install -r requirements.txt
```

**"OLLAMA_API_KEY environment variable is not set"**
```bash
# Use one of the helper scripts
# Windows
set_api_key.bat

# Linux/Mac (important: use 'source')
source set_api_key.sh
```

**"TypeError: can only concatenate str (not 'NoneType') to str"**
- This means the API key environment variable is not set
- Set it using one of the methods above

---

## 💡 Tips & Best Practices

### API Key Security
- ✅ Never commit API keys to version control
- ✅ Use environment variables for production
- ✅ The web interface doesn't persist keys (they're in memory only)
- ✅ Regenerate keys periodically

### Performance
- ✅ Local mode is faster but requires local resources
- ✅ Cloud mode is slower but uses cloud resources
- ✅ Choose larger models for better quality (if resources allow)

### Model Selection
- 🖥️ **Local**: Use models you've pulled with `ollama pull`
- ☁️ **Cloud**: Use models available in your cloud subscription
- 📊 **Size matters**: Larger models (70B+) are better but slower

### Conversation Tips
- ✅ Use "Clear Chat" to start fresh conversations
- ✅ Longer conversations use more tokens/memory
- ✅ Be specific in your questions for better responses

---

## 📚 Additional Resources

- [Ollama Documentation](https://github.com/ollama/ollama)
- [Ollama Model Library](https://ollama.ai/library)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

## 🆘 Still Need Help?

1. Check the [README.md](README.md) for installation instructions
2. Review the [QUICK_START.md](QUICK_START.md) for quick reference
3. Run `test_ollama_cloud.py` to diagnose connection issues
4. Check the browser console for JavaScript errors
5. Check the Flask server logs for backend errors

---

**Happy chatting! 🚀**

