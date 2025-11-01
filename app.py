from flask import Flask, render_template, request, jsonify, Response, stream_with_context
import requests
import json
import os

app = Flask(__name__)

# Store the Ollama URL (can be configured via environment variable or passed from frontend)
OLLAMA_URL = os.environ.get('OLLAMA_URL', 'http://localhost:11434')
OLLAMA_API_KEY = os.environ.get('OLLAMA_API_KEY', '')

@app.route('/')
def index():
    """Serve the main chat interface"""
    return render_template('index.html')

@app.route('/api/models', methods=['POST'])
def get_models():
    """Get available models from Ollama instance"""
    try:
        data = request.json
        ollama_url = data.get('ollama_url', OLLAMA_URL)
        api_key = data.get('api_key', OLLAMA_API_KEY)
        
        # Ensure URL doesn't end with a slash
        ollama_url = ollama_url.rstrip('/')
        
        # Check if cloud service and API key is required
        if 'ollama.com' in ollama_url and not api_key:
            return jsonify({
                'success': False,
                'error': 'API key is required for Ollama cloud service. Please enter your API key or set OLLAMA_API_KEY environment variable.'
            }), 400
        
        # Prepare headers
        headers = {}
        if api_key:
            headers['Authorization'] = f'Bearer {api_key}'
        
        response = requests.get(f'{ollama_url}/api/tags', headers=headers, timeout=10)
        response.raise_for_status()
        
        models_data = response.json()
        models = [model['name'] for model in models_data.get('models', [])]
        
        return jsonify({
            'success': True,
            'models': models
        })
    except requests.exceptions.RequestException as e:
        return jsonify({
            'success': False,
            'error': f'Failed to connect to Ollama: {str(e)}'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """Stream chat responses from Ollama"""
    try:
        data = request.json
        ollama_url = data.get('ollama_url', OLLAMA_URL).rstrip('/')
        api_key = data.get('api_key', OLLAMA_API_KEY)
        model = data.get('model')
        messages = data.get('messages', [])
        
        if not model:
            return jsonify({'success': False, 'error': 'Model not specified'}), 400
        
        if not messages:
            return jsonify({'success': False, 'error': 'No messages provided'}), 400
        
        # Check if cloud service and API key is required
        if 'ollama.com' in ollama_url and not api_key:
            return jsonify({
                'success': False, 
                'error': 'API key is required for Ollama cloud service.'
            }), 400
        
        # Prepare the request to Ollama
        ollama_request = {
            'model': model,
            'messages': messages,
            'stream': True
        }
        
        # Prepare headers
        headers = {'Content-Type': 'application/json'}
        if api_key:
            headers['Authorization'] = f'Bearer {api_key}'
        
        def generate():
            try:
                response = requests.post(
                    f'{ollama_url}/api/chat',
                    json=ollama_request,
                    headers=headers,
                    stream=True,
                    timeout=60
                )
                response.raise_for_status()
                
                for line in response.iter_lines():
                    if line:
                        chunk = json.loads(line)
                        yield f"data: {json.dumps(chunk)}\n\n"
                        
                        if chunk.get('done', False):
                            break
                            
            except requests.exceptions.RequestException as e:
                error_data = {'error': f'Ollama request failed: {str(e)}'}
                yield f"data: {json.dumps(error_data)}\n\n"
            except Exception as e:
                error_data = {'error': str(e)}
                yield f"data: {json.dumps(error_data)}\n\n"
        
        return Response(
            stream_with_context(generate()),
            mimetype='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'X-Accel-Buffering': 'no'
            }
        )
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

