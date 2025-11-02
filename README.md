# Byron Katie Bot Demo

## Description

I started this project as a learning activity for natural language processing (NLP). Having developed an interest in the applications of conversational AI in mental health, I decided to create Lucy; a chatbot designed to lead the user through a therapeutic process called the Byron Katie method.

The bot now supports two modes:
- **NLP Mode**: Uses traditional NLP techniques with spaCy for text transformation
- **LLM Mode**: Integrates with large language models via API (Ollama with Gemma 2)

## Demo
Watch demo on Youtube: https://youtu.be/sZ9m_7gdY6U

![](Lucy-Demo-20200128.gif)

## Setup

### Basic Setup (NLP Mode Only)

1. Install dependencies:
```bash
pip install Flask requests
```

2. Run the application:
```bash
python CH05A-BK_Bot_Web_App.py
```

### LLM Mode Setup (Optional)

To enable LLM integration with Ollama:

1. Deploy an Ollama instance (e.g., on Render) with the Gemma 2 model
2. Copy `.env.example` to `.env` and configure:
```bash
cp .env.example .env
```

3. Edit `.env` with your settings:
```
LLM_ENABLED=true
LLM_API_URL=https://your-ollama-service.onrender.com
LLM_MODEL=gemma2
```

4. Run the application with environment variables:
```bash
python CH05A-BK_Bot_Web_App.py
```

The app will automatically use LLM mode if configured, or fall back to NLP mode.

## API Endpoints

- `GET /` - Main chat interface
- `GET /get?msg=<message>` - Get bot response
- `GET /reset` - Reset conversation session
- `POST /toggle_mode` - Toggle between NLP and LLM modes (if LLM is available)
- `GET /status` - Get current configuration and mode status

## Configuration

Environment variables:
- `SECRET_KEY` - Flask secret key for session management
- `LLM_ENABLED` - Enable LLM mode (true/false)
- `LLM_API_URL` - URL of the Ollama API endpoint
- `LLM_MODEL` - Model name to use (default: gemma2)
- `LLM_TIMEOUT` - API request timeout in seconds (default: 30)



