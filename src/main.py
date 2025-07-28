from core.doku import Doku
from pathlib import Path
from core.chroma_manager import ChromaManager

doku = Doku()
chroma_manager = ChromaManager("chroma_db")

current_dir = Path.cwd()


def main():
    while True:
        question = input("question: ")

        response = doku.chat_retrieval(
            question, retriever=chroma_manager.retriever("taka")
        )

        print(response["source_documents"])
        print("-----------------------------------------")
        print(response["result"])


main()
