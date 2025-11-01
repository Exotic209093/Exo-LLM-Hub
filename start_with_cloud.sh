#!/bin/bash
echo "========================================"
echo "  Ollama Web Chat - Cloud Mode"
echo "========================================"
echo ""
echo "Setting up environment for Ollama Cloud..."
export OLLAMA_API_KEY='b9e0d00cbcbb47adb23ae389076c7d2e.met23afbTcatGW29LdbgXSqV'
echo "✅ API Key configured"
echo ""
echo "Starting Flask server..."
echo "Open your browser to: http://localhost:5000"
echo "Select 'Cloud Service' mode in the interface"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""
python3 app.py

