"""Configuration module for Byron Katie Bot with LLM API support."""

import os

# LLM API Configuration
LLM_API_URL = os.environ.get('LLM_API_URL', '')
LLM_ENABLED = os.environ.get('LLM_ENABLED', 'false').lower() in ('true', '1', 'yes', 'on')
LLM_MODEL = os.environ.get('LLM_MODEL', 'gemma2')
LLM_TIMEOUT = int(os.environ.get('LLM_TIMEOUT', '30'))

# Flask Configuration
SECRET_KEY = os.environ.get('SECRET_KEY', None)
