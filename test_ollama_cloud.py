"""
Test script for Ollama Cloud Service
This script tests the connection to Ollama cloud using the official Python client
"""
import os
from ollama import Client

# Get API key from environment variable
api_key = os.environ.get('OLLAMA_API_KEY')

if not api_key:
    print("ERROR: OLLAMA_API_KEY environment variable is not set!")
    print("\nTo set it, run one of these commands first:\n")
    print("PowerShell:")
    print('  $env:OLLAMA_API_KEY = "b9e0d00cbcbb47adb23ae389076c7d2e.met23afbTcatGW29LdbgXSqV"')
    print("\nCommand Prompt:")
    print('  set OLLAMA_API_KEY=b9e0d00cbcbb47adb23ae389076c7d2e.met23afbTcatGW29LdbgXSqV')
    print("\nBash/Zsh:")
    print('  export OLLAMA_API_KEY="b9e0d00cbcbb47adb23ae389076c7d2e.met23afbTcatGW29LdbgXSqV"')
    print("\nThen run this script again.")
    exit(1)

# Create Ollama client with cloud endpoint and API key
print("Connecting to Ollama cloud service...")
client = Client(
    host='https://ollama.com',
    headers={'Authorization': f'Bearer {api_key}'}
)

# List available models
try:
    print("\nFetching available models...")
    models = client.list()
    print(f"\n✅ Successfully connected to Ollama cloud!")
    print(f"\nAvailable models ({len(models['models'])} found):")
    for model in models['models']:
        print(f"  - {model['name']}")
except Exception as e:
    print(f"\n❌ Error fetching models: {e}")
    exit(1)

# Test chat with a model
print("\n" + "="*50)
print("Testing chat with a model...")
print("="*50)

messages = [
    {
        'role': 'user',
        'content': 'Why is the sky blue?',
    },
]

# Use the first available model, or default to a common one
if models['models']:
    test_model = models['models'][0]['name']
else:
    test_model = 'llama2'  # fallback

print(f"\nModel: {test_model}")
print(f"Question: {messages[0]['content']}")
print(f"\nResponse: ", end='', flush=True)

try:
    for part in client.chat(test_model, messages=messages, stream=True):
        print(part['message']['content'], end='', flush=True)
    print("\n\n✅ Chat test completed successfully!")
except Exception as e:
    print(f"\n\n❌ Error during chat: {e}")
    print("\nNote: Make sure the model exists and is available with your API key.")

