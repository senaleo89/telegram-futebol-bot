from telegram import Bot
from config import TOKEN, CHAT_ID
import time

print("TOKEN existe?", TOKEN is not None)
print("CHAT_ID:", CHAT_ID)

try:
    bot = Bot(token=TOKEN)
    bot.send_message(
        chat_id=CHAT_ID,
        text="✅ Teste Telegram funcionando!"
    )
    print("Mensagem enviada com sucesso")
except Exception as erro:
    print("ERRO AO ENVIAR:", erro)

while True:
    time.sleep(60)
