import asyncio
import sys
from agent.doku import Doku


async def main():
    doku = Doku()
    await doku.load_context()
    await doku.start_monitor()

    while True:
        question = input("Prompt: ")
        await doku.chat(content=question)


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
