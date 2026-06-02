from telegram import Bot
from config import TOKEN, CHAT_ID

bot = Bot(token=TOKEN)

bot.send_message(
    chat_id=CHAT_ID,
    text="✅ TESTE DEFINITIVO: Railway conectado ao Telegram!"
)

print("Mensagem enviada com sucesso")
