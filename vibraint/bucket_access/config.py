# Configuration file for the Explainable Brains project.
# Set these via environment variables or a .env file (never commit credentials).
import os
from dotenv import load_dotenv

load_dotenv()

HETZNER_ACCESS_KEY  = os.environ["HETZNER_ACCESS_KEY"]
HETZNER_SECRET_KEY  = os.environ["HETZNER_SECRET_KEY"]
HETZNER_BUCKET_NAME = os.getenv("HETZNER_BUCKET_NAME", "explainable-brains")
HETZNER_ENDPOINT    = os.getenv("HETZNER_ENDPOINT", "https://fsn1.your-objectstorage.com")
