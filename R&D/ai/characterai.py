import asyncio

from PyCharacterAI import get_client
from PyCharacterAI.exceptions import SessionClosedError

token = "ae52b470beb8be2cc0e5b34dd6a7332157b391ab"
character_id = "FS54dIDelfofnZPprHP5hSyMcLwogfH2uo8UTEHeD0E"


async def main():
    client = await get_client(token=token)

    me = await client.account.fetch_me()
    print("Loading...")

    chat, greeting_message = await client.chat.create_chat(character_id)

    print(f"[{greeting_message.author_name}]: {greeting_message.get_primary_candidate().text}")

    try:
        while True:
            # NOTE: input() is blocking function!
            message = input(f"[{me.name}]: ")

            answer = await client.chat.send_message(character_id, chat.chat_id, message, streaming=True)

            printed_length = 0
            async for message in answer:
                if printed_length == 0:
                    print(f"[{message.author_name}]: ", end="")

                text = message.get_primary_candidate().text
                print(text[printed_length:], end="")

                printed_length = len(text)
            print("\n")

    except SessionClosedError:
        print("session closed. Bye!")

    finally:
        # Don't forget to explicitly close the session
        await client.close_session()

asyncio.run(main())