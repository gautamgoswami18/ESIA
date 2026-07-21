# test_agent.py

import asyncio

from app.agent.esira_agent import ESIRAAgent


async def main():

    agent = ESIRAAgent()

    response = await agent.ask(
        "Find Python Developers"
    )

    print(response)


asyncio.run(main())