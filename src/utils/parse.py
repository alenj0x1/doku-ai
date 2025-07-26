import config
import os
from dotenv import load_dotenv

load_dotenv()

REPLACEMENT_MODIFIERS: dict[str, str] = {
  '{{product_name}}': config.APP_NAME
}

def replacement_modifiers(text: str):
  for key, value in REPLACEMENT_MODIFIERS.items():
    text = text.replace(key, value)

  return text