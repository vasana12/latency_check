import os
from dotenv import load_dotenv
import json
load_dotenv()
DB_INFO = json.loads(os.getenv("DB_INFO"))
TOKEN = os.getenv("TOKEN")
ACCEPTED_CLIENT_HOST = os.getenv("ACCEPTED_CLIENT_HOST")

