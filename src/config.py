from dotenv import load_dotenv
from os import getenv

load_dotenv()

PRODUCT_NAME = getenv("PRODUCT_NAME", "taka")
MONGO_URI = getenv("MONGO_URI")
MONGO_DATABASE = getenv("MONGO_DATABASE")
