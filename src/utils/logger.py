from colorama import Fore


def reading_filepath(scope: str, type: str, filepath: str):
    print(
        f"{Fore.MAGENTA}[{scope}] {Fore.LIGHTYELLOW_EX}[{type}] {Fore.RESET}Reading the file path: {Fore.GREEN}{filepath} {Fore.RESET}"
    )


def mongo_operation(scope: str, type: str, identifier: str):
    print(
        f"{Fore.MAGENTA}[{scope}] {Fore.LIGHTYELLOW_EX}[Mongo Operation] {Fore.BLUE}[{type}] {Fore.RESET}Identifier: {Fore.GREEN}{identifier} {Fore.RESET}"
    )
