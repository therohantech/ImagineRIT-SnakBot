import requests
import asyncio
import random
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

# Function to query Mistral via Ollama
def get_mistral_response(prompt):
    url = "http://localhost:11434/api/generate"
    payload = {"model": "mistral", "prompt": prompt}
    response = requests.post(url, json=payload)
    return response.json()["response"]

# Main conversation loop
async def conversation_loop():
    char_ai_bot = CharacterChat("e52b470beb8be2cc0e5b34dd6a7332157b391ab", "S54dIDelfofnZPprHP5hSyMcLwogfH2uo8UTEHeD0E")

    await char_ai_bot.setup()

    # Mistral generates the first message dynamically
    mistral_message = get_mistral_response("Start a conversation as a visitor at Imagine RIT.")
    print(f"\nMistral: {mistral_message}")

    while True:
        # Get response from CharacterAI
        char_ai_response = await char_ai_bot.get_response(mistral_message)
        print(f"CharacterAI: {char_ai_response}")

        # Check if either side wants to end the chat
        if "BYE#" in mistral_message.upper() or "BYE#" in char_ai_response.upper():
            print("\nConversation ended.")
            break

        # Mistral responds
        mistral_message = get_mistral_response(char_ai_response)
        print(f"\nMistral: {mistral_message}")

        # Add human-like delay
        await asyncio.sleep(random.uniform(1.5, 3.5))

    await char_ai_bot.close()

# Run the chatbot conversation
asyncio.run(conversation_loop())
