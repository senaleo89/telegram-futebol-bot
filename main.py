from telegram import Bot
from config import TOKEN, CHAT_ID
import time

bot = Bot(token=TOKEN)

bot.send_message(
    chat_id=CHAT_ID,
    text="✅ TESTE FINAL FUNCIONANDO!"
)

print("Mensagem enviada")

while True:
    time.sleep(60)
