from colorama import Fore

def reading_filepath(scope: str, type: str, filepath: str):
  print(f"{Fore.MAGENTA}[{scope}] {Fore.LIGHTYELLOW_EX}[{type}] {Fore.RESET}Reading the file path: {Fore.GREEN}{filepath} {Fore.RESET}")