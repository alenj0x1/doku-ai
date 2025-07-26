from utils.file_reader import read_markdown
from utils.parse import replacement_modifiers
from pathlib import Path
import os

class Doku:
  def __init__(self):
     self.load_context()

  def load_context(self):
     context: dict[str, str] = {}

     for current_path, folders, files in os.walk('src/context'):
        # Folders
        for folder in folders:
           print(folder)
        
        # Files
        for file in files:
           path = Path(os.path.join(current_path, file))
           
           path_parts = list(path.parent.parts)
           path_parts.remove('src')

           # Markdown
           if file.endswith(path.suffix):
              content = read_markdown(filepath=path)
              
              print(replacement_modifiers(content))

              context[str.join(':', path_parts)] = content
          