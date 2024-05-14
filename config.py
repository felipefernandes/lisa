"""
Modulo de configuracao
"""
import os
from dotenv import load_dotenv

load_dotenv()

GEMINIKEY = os.getenv("GEMINIKEY")
# SLACK_API_TOKEN = os.getenv("SLACK_TOKEN")
# BOT_USER_OAUTH_TOKEN = os.getenv("BOT_OAUTH_TOKEN")
