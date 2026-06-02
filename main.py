import asyncio
import time
from telegram import Bot
from config import TOKEN, CHAT_ID

async def enviar_teste():
    bot = Bot(token=TOKEN)
    await bot.send_message(
        chat_id=CHAT_ID,
        text="✅ Agora sim! Bot conectado ao Telegram."
    )
    print("Mensagem enviada com sucesso")

asyncio.run(enviar_teste())

while True:
    time.sleep(60)
