import asyncio
from PyCharacterAI import get_client

class CharacterChat:
    def __init__(self, token, character_id):
        self.token = token
        self.character_id = character_id
        self.client = None
        self.chat_id = None

    async def setup(self):
        self.client = await get_client(token=self.token)
        chat, _ = await self.client.chat.create_chat(self.character_id)
        self.chat_id = chat.chat_id

    async def get_response(self, message):
        if not self.client:
            await self.setup()
        answer = await self.client.chat.send_message(self.character_id, self.chat_id, message, streaming=False)
        return answer[0].get_primary_candidate().text if answer else "No response."

    async def close(self):
        if self.client:
            await self.client.close_session()

# Example usage
async def main():

    bot = CharacterChat("e52b470beb8be2cc0e5b34dd6a7332157b391ab", "S54dIDelfofnZPprHP5hSyMcLwogfH2uo8UTEHeD0E")
    await bot.setup()
    response = await bot.get_response("Hello!")
    print(response)
    await bot.close()

# Run the example
# asyncio.run(main())
