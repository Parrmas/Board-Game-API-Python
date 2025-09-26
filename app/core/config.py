import os
from dotenv import load_dotenv

# Prefer .local.env if available
if os.path.exists(".local.env"):
    load_dotenv(".local.env")
else:
    load_dotenv(".env")

class Settings:
    MONGODB_URI: str = os.getenv("MONGODB_URI", "")
    API_URL: str = os.getenv("API_URL", "")

settings = Settings()
