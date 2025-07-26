import asyncio
import sys
from agent.doku import Doku


async def main():
    doku = Doku()
    await doku.load_context()


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
