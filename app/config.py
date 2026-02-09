
import os

APP_NAME = os.getenv("APP_NAME", "WISE MCP Backbone")
PORT = int(os.getenv("PORT", "8000"))

SERVER_SECRET = os.getenv("NORTH_SERVER_SECRET", "")
DB_PATH = os.getenv("DB_PATH", "data.db")
DEBUG = os.getenv("DEBUG", "false").lower() in ("1", "true", "yes", "y")

