# LLM Integration Setup Guide

This guide explains how to set up the Byron Katie Bot to use a Large Language Model (LLM) API via Ollama.

## Overview

The Byron Katie Bot now supports two modes:

1. **NLP Mode (Default)**: Uses traditional NLP with spaCy for text transformation
2. **LLM Mode (Optional)**: Uses Ollama API with models like Gemma 2 for generative responses

The bot automatically falls back to NLP mode if the LLM is unavailable.

## Quick Start

### Running in NLP Mode (Default)

No configuration needed - just run the app:

```bash
python CH05A-BK_Bot_Web_App.py
```

### Running with LLM Mode

1. **Deploy Ollama on Render or other hosting service**
   
   - Use the Ollama Docker image
   - Make sure the API is accessible via HTTP/HTTPS
   - Pull the Gemma 2 model: `ollama pull gemma2`

2. **Configure Environment Variables**

   Create a `.env` file or set environment variables:

   ```bash
   export LLM_ENABLED=true
   export LLM_API_URL=https://your-ollama-instance.onrender.com
   export LLM_MODEL=gemma2
   export LLM_TIMEOUT=30
   ```

   Or use a `.env` file (copy from `.env.example`):

   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

3. **Run the Application**

   ```bash
   python CH05A-BK_Bot_Web_App.py
   ```

## Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `LLM_ENABLED` | Enable LLM mode | `false` | No |
| `LLM_API_URL` | Ollama API endpoint URL | Empty | Yes (for LLM mode) |
| `LLM_MODEL` | Model name to use | `gemma2` | No |
| `LLM_TIMEOUT` | API timeout in seconds | `30` | No |
| `SECRET_KEY` | Flask session secret | Auto-generated | No |

## API Endpoints

### GET /status

Check current configuration and mode:

```bash
curl http://localhost:5000/status
```

Response:
```json
{
  "llm_enabled": true,
  "llm_available": true,
  "llm_api_url": "https://your-api.com",
  "llm_model": "gemma2",
  "current_mode": "LLM",
  "can_toggle": true
}
```

### POST /toggle_mode

Switch between NLP and LLM modes (only if LLM is available):

```bash
curl -X POST http://localhost:5000/toggle_mode
```

Response:
```json
{
  "status": "success",
  "mode": "NLP",
  "message": "Switched to NLP mode"
}
```

### GET /reset

Reset the conversation session:

```bash
curl http://localhost:5000/reset
```

## Deploying Ollama on Render

1. Create a new Web Service on Render
2. Use Docker deployment
3. Docker image: `ollama/ollama:latest`
4. After deployment, pull the model:
   ```bash
   # SSH into your Render service
   ollama pull gemma2
   ```
5. Copy your Render URL and use it as `LLM_API_URL`

## Testing the Integration

### Test Configuration

```bash
python3 -c "import config; print(f'LLM Enabled: {config.LLM_ENABLED}'); print(f'API URL: {config.LLM_API_URL}')"
```

### Test LLM Client

```bash
python3 << 'EOF'
from llm_client import LLMClient
client = LLMClient()
print(f"LLM Available: {client.is_available()}")
if client.is_available():
    result = client.generate_response("Test message")
    print(f"Result: {result}")
EOF
```

### Test API Endpoint

```bash
# Start the server
python CH05A-BK_Bot_Web_App.py &

# Test the status endpoint
curl http://localhost:5000/status | python3 -m json.tool

# Test a chat message
curl "http://localhost:5000/get?msg=I%20am%20anxious" | python3 -m json.tool
```

## Troubleshooting

### LLM Not Available

If you see `"llm_available": false`:

1. Check that `LLM_API_URL` is set correctly
2. Verify your Ollama instance is running
3. Test the API directly: `curl YOUR_API_URL/api/tags`

### Timeouts

If requests timeout:

1. Increase `LLM_TIMEOUT` value
2. Check network connectivity to Ollama instance
3. Verify the model is loaded on Ollama

### Automatic Fallback

The bot automatically falls back to NLP mode if:
- LLM API is not configured
- LLM API is unavailable
- LLM API returns an error

Check the console logs for error messages.

## Example Ollama API Format

The bot sends requests in this format:

```json
{
  "model": "gemma2",
  "prompt": "System prompt + conversation context + user message",
  "stream": false
}
```

Expected response:
```json
{
  "response": "Generated response text",
  "model": "gemma2",
  "context": [...]
}
```

## Security Notes

- Never commit your `.env` file with real credentials
- Use environment variables in production
- Keep your `SECRET_KEY` secure
- Use HTTPS for production deployments
- Validate and sanitize all user inputs

## Support

For issues or questions:
- Check the console logs for error messages
- Use `/status` endpoint to verify configuration
- Test with NLP mode first to isolate issues
- Ensure your Ollama instance is properly configured
