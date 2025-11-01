import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestIndexRoute:
    """Test the index route"""
    
    def test_index_route(self, client):
        """Test that the index route returns the HTML template"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Ollama Chat' in response.data


class TestModelsEndpoint:
    """Test the /api/models endpoint"""
    
    def test_get_models_success(self, client):
        """Test successful model retrieval"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'models': [
                {'name': 'llama2'},
                {'name': 'mistral'},
                {'name': 'codellama'}
            ]
        }
        mock_response.raise_for_status = Mock()
        
        with patch('app.requests.get', return_value=mock_response):
            response = client.post('/api/models', 
                                 json={'ollama_url': 'http://localhost:11434'})
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['success'] is True
            assert 'models' in data
            assert len(data['models']) == 3
            assert 'llama2' in data['models']
            assert 'mistral' in data['models']
            assert 'codellama' in data['models']
    
    def test_get_models_with_default_url(self, client):
        """Test model retrieval with default OLLAMA_URL"""
        mock_response = Mock()
        mock_response.json.return_value = {'models': [{'name': 'llama2'}]}
        mock_response.raise_for_status = Mock()
        
        with patch('app.requests.get', return_value=mock_response):
            response = client.post('/api/models', json={})
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['success'] is True
    
    def test_get_models_url_stripping(self, client):
        """Test that trailing slashes are stripped from URL"""
        mock_response = Mock()
        mock_response.json.return_value = {'models': []}
        mock_response.raise_for_status = Mock()
        
        with patch('app.requests.get', return_value=mock_response) as mock_get:
            client.post('/api/models', 
                       json={'ollama_url': 'http://localhost:11434/'})
            
            # Verify URL was stripped
            call_args = mock_get.call_args
            assert call_args[0][0] == 'http://localhost:11434/api/tags'
    
    def test_get_models_with_api_key(self, client):
        """Test model retrieval with API key"""
        mock_response = Mock()
        mock_response.json.return_value = {'models': []}
        mock_response.raise_for_status = Mock()
        
        with patch('app.requests.get', return_value=mock_response) as mock_get:
            client.post('/api/models', 
                       json={
                           'ollama_url': 'http://localhost:11434',
                           'api_key': 'test-key-123'
                       })
            
            # Verify Authorization header was set
            call_kwargs = mock_get.call_args[1]
            assert 'headers' in call_kwargs
            assert call_kwargs['headers']['Authorization'] == 'Bearer test-key-123'
    
    def test_get_models_connection_error(self, client):
        """Test handling of connection errors"""
        with patch('app.requests.get', side_effect=Exception('Connection refused')):
            response = client.post('/api/models', 
                                 json={'ollama_url': 'http://localhost:11434'})
            
            assert response.status_code == 500
            data = json.loads(response.data)
            assert data['success'] is False
            assert 'error' in data
    
    def test_get_models_http_error(self, client):
        """Test handling of HTTP errors"""
        import requests
        
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError('404 Not Found')
        
        with patch('app.requests.get', return_value=mock_response):
            response = client.post('/api/models', 
                                 json={'ollama_url': 'http://localhost:11434'})
            
            assert response.status_code == 500
            data = json.loads(response.data)
            assert data['success'] is False
            assert 'error' in data
    
    def test_get_models_empty_models_list(self, client):
        """Test handling of empty models list"""
        mock_response = Mock()
        mock_response.json.return_value = {'models': []}
        mock_response.raise_for_status = Mock()
        
        with patch('app.requests.get', return_value=mock_response):
            response = client.post('/api/models', 
                                 json={'ollama_url': 'http://localhost:11434'})
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['success'] is True
            assert data['models'] == []


class TestChatEndpoint:
    """Test the /api/chat endpoint"""
    
    def test_chat_success_streaming(self, client):
        """Test successful chat streaming"""
        # Mock the streaming response
        mock_stream_response = [
            b'{"message": {"content": "Hello"}, "done": false}\n',
            b'{"message": {"content": " world"}, "done": false}\n',
            b'{"done": true}\n'
        ]
        
        mock_response = Mock()
        mock_response.iter_lines.return_value = mock_stream_response
        mock_response.raise_for_status = Mock()
        
        with patch('app.requests.post', return_value=mock_response):
            response = client.post('/api/chat',
                                 json={
                                     'ollama_url': 'http://localhost:11434',
                                     'model': 'llama2',
                                     'messages': [{'role': 'user', 'content': 'Hello'}]
                                 })
            
            assert response.status_code == 200
            assert response.content_type == 'text/event-stream; charset=utf-8'
            
            # Read the streamed data
            data = b''.join(response.response)
            assert b'data: ' in data
    
    def test_chat_missing_model(self, client):
        """Test chat endpoint with missing model"""
        response = client.post('/api/chat',
                             json={
                                 'ollama_url': 'http://localhost:11434',
                                 'messages': [{'role': 'user', 'content': 'Hello'}]
                             })
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'Model not specified' in data['error']
    
    def test_chat_missing_messages(self, client):
        """Test chat endpoint with missing messages"""
        response = client.post('/api/chat',
                             json={
                                 'ollama_url': 'http://localhost:11434',
                                 'model': 'llama2'
                             })
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'No messages provided' in data['error']
    
    def test_chat_with_api_key(self, client):
        """Test chat endpoint with API key"""
        mock_stream_response = [b'{"done": true}\n']
        mock_response = Mock()
        mock_response.iter_lines.return_value = mock_stream_response
        mock_response.raise_for_status = Mock()
        
        with patch('app.requests.post', return_value=mock_response) as mock_post:
            client.post('/api/chat',
                       json={
                           'ollama_url': 'http://localhost:11434',
                           'api_key': 'test-key-123',
                           'model': 'llama2',
                           'messages': [{'role': 'user', 'content': 'Hello'}]
                       })
            
            # Verify Authorization header was set
            call_kwargs = mock_post.call_args[1]
            assert 'headers' in call_kwargs
            assert call_kwargs['headers']['Authorization'] == 'Bearer test-key-123'
            assert call_kwargs['headers']['Content-Type'] == 'application/json'
    
    def test_chat_url_stripping(self, client):
        """Test that trailing slashes are stripped from URL"""
        mock_stream_response = [b'{"done": true}\n']
        mock_response = Mock()
        mock_response.iter_lines.return_value = mock_stream_response
        mock_response.raise_for_status = Mock()
        
        with patch('app.requests.post', return_value=mock_response) as mock_post:
            client.post('/api/chat',
                       json={
                           'ollama_url': 'http://localhost:11434/',
                           'model': 'llama2',
                           'messages': [{'role': 'user', 'content': 'Hello'}]
                       })
            
            # Verify URL was stripped
            call_args = mock_post.call_args[0]
            assert call_args[0] == 'http://localhost:11434/api/chat'
    
    def test_chat_streaming_request_format(self, client):
        """Test that the request to Ollama is formatted correctly"""
        mock_stream_response = [b'{"done": true}\n']
        mock_response = Mock()
        mock_response.iter_lines.return_value = mock_stream_response
        mock_response.raise_for_status = Mock()
        
        with patch('app.requests.post', return_value=mock_response) as mock_post:
            messages = [{'role': 'user', 'content': 'Hello'}]
            client.post('/api/chat',
                       json={
                           'ollama_url': 'http://localhost:11434',
                           'model': 'llama2',
                           'messages': messages
                       })
            
            # Verify the request JSON is correct
            call_kwargs = mock_post.call_args[1]
            assert 'json' in call_kwargs
            assert call_kwargs['json']['model'] == 'llama2'
            assert call_kwargs['json']['messages'] == messages
            assert call_kwargs['json']['stream'] is True
            assert call_kwargs['stream'] is True
            assert call_kwargs['timeout'] == 60
    
    def test_chat_streaming_error_handling(self, client):
        """Test error handling in streaming"""
        import requests
        
        with patch('app.requests.post', 
                  side_effect=requests.exceptions.RequestException('Connection error')):
            response = client.post('/api/chat',
                                 json={
                                     'ollama_url': 'http://localhost:11434',
                                     'model': 'llama2',
                                     'messages': [{'role': 'user', 'content': 'Hello'}]
                                 })
            
            # Should still return 200 with error in stream
            assert response.status_code == 200
            data = b''.join(response.response)
            assert b'error' in data.lower()
    
    def test_chat_streaming_json_error(self, client):
        """Test handling of invalid JSON in stream"""
        mock_stream_response = [
            b'{"message": {"content": "Hello"}, "done": false}\n',
            b'invalid json\n',  # Invalid JSON
            b'{"done": true}\n'
        ]
        
        mock_response = Mock()
        mock_response.iter_lines.return_value = mock_stream_response
        mock_response.raise_for_status = Mock()
        
        with patch('app.requests.post', return_value=mock_response):
            response = client.post('/api/chat',
                                 json={
                                     'ollama_url': 'http://localhost:11434',
                                     'model': 'llama2',
                                     'messages': [{'role': 'user', 'content': 'Hello'}]
                                 })
            
            # Should handle gracefully and continue
            assert response.status_code == 200
    
    def test_chat_done_flag_stops_streaming(self, client):
        """Test that streaming stops when done flag is True"""
        mock_stream_response = [
            b'{"message": {"content": "Hello"}, "done": false}\n',
            b'{"done": true}\n',
            b'{"message": {"content": "should not appear"}, "done": false}\n'
        ]
        
        mock_response = Mock()
        mock_response.iter_lines.return_value = mock_stream_response
        mock_response.raise_for_status = Mock()
        
        with patch('app.requests.post', return_value=mock_response):
            response = client.post('/api/chat',
                                 json={
                                     'ollama_url': 'http://localhost:11434',
                                     'model': 'llama2',
                                     'messages': [{'role': 'user', 'content': 'Hello'}]
                                 })
            
            assert response.status_code == 200
            data = b''.join(response.response)
            # Should not contain content after done flag
            assert b'should not appear' not in data
    
    def test_chat_general_exception_handling(self, client):
        """Test general exception handling in chat endpoint"""
        # Simulate a general exception by patching stream_with_context
        from flask import stream_with_context
        with patch('app.stream_with_context', side_effect=Exception('Stream error')):
            response = client.post('/api/chat',
                                 json={
                                     'ollama_url': 'http://localhost:11434',
                                     'model': 'llama2',
                                     'messages': [{'role': 'user', 'content': 'Hello'}]
                                 })
            
            # Should handle gracefully
            assert response.status_code == 500
            data = json.loads(response.data)
            assert data['success'] is False
            assert 'error' in data
    
    def test_chat_streaming_general_exception(self, client):
        """Test general exception handling in streaming generator"""
        mock_response = Mock()
        mock_response.iter_lines.side_effect = Exception('Unexpected stream error')
        mock_response.raise_for_status = Mock()
        
        with patch('app.requests.post', return_value=mock_response):
            response = client.post('/api/chat',
                                 json={
                                     'ollama_url': 'http://localhost:11434',
                                     'model': 'llama2',
                                     'messages': [{'role': 'user', 'content': 'Hello'}]
                                 })
            
            # Should handle gracefully and stream error
            assert response.status_code == 200
            data = b''.join(response.response)
            assert b'error' in data.lower()


class TestEnvironmentVariables:
    """Test environment variable handling"""
    
    def test_default_ollama_url(self, client):
        """Test that default OLLAMA_URL is used when not provided"""
        import os
        original_url = os.environ.get('OLLAMA_URL')
        
        try:
            # Set a test URL
            os.environ['OLLAMA_URL'] = 'http://test:11434'
            
            # Reload app module to get new env var
            import importlib
            import app
            importlib.reload(app)
            
            # Verify default is set
            assert app.OLLAMA_URL == 'http://test:11434'
            
        finally:
            # Restore original
            if original_url:
                os.environ['OLLAMA_URL'] = original_url
            else:
                os.environ.pop('OLLAMA_URL', None)

