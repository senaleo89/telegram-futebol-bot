import asyncio
import requests

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

from config import TOKEN, CHAT_ID, API_KEY, LIGAS_PERMITIDAS

alertas = set()

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "✅ Bot online e monitorando partidas!"
    )

async def teste(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "✅ Teste realizado com sucesso!"
    )

async def verificar_jogos(app):

    headers = {
        "x-apisports-key": API_KEY
    }

    url = "https://v3.football.api-sports.io/fixtures?live=all"
url_stats = "https://v3.football.api-sports.io/fixtures/statistics?fixture="
    try:

        resposta = requests.get(
            url,
            headers=headers,
            timeout=30
        )

        dados = resposta.json()

        for jogo in dados.get("response", []):

            liga_id = jogo["league"]["id"]

            if liga_id not in LIGAS_PERMITIDAS:
                continue

            fixture_id = jogo["fixture"]["id"]
stats_resposta = requests.get(
    url_stats + str(fixture_id),
    headers=headers,
    timeout=30
)

stats_dados = stats_resposta.json()
            minuto = jogo["fixture"]["status"]["elapsed"] or 0

            if minuto < 20:
                continue

            casa = jogo["teams"]["home"]["name"]
            fora = jogo["teams"]["away"]["name"]

            gols_casa = jogo["goals"]["home"] or 0
            gols_fora = jogo["goals"]["away"] or 0

            if gols_casa >= gols_fora:
                continue

            chave = str(fixture_id)

            if chave in alertas:
                continue

            liga = jogo["league"]["name"]
escanteios_casa = 0
escanteios_fora = 0

finalizacoes_casa = 0
finalizacoes_fora = 0

try:

    estatisticas = stats_dados["response"]

    for time_stats in estatisticas:

        team_name = time_stats["team"]["name"]

        for stat in time_stats["statistics"]:

            if stat["type"] == "Corner Kicks":

                if team_name == casa:
                    escanteios_casa = stat["value"] or 0
                else:
                    escanteios_fora = stat["value"] or 0

            if stat["type"] == "Shots on Goal":

                if team_name == casa:
                    finalizacoes_casa = stat["value"] or 0
                else:
                    finalizacoes_fora = stat["value"] or 0

except:
    pass
            mensagem = f"""
mensagem = f"""
🚨 ALERTA AO VIVO

🏆 {liga}

⚽ {casa} x {fora}

📊 Placar:
{gols_casa} x {gols_fora}

⏱️ {minuto}'

📈 Estatísticas

🎯 Chutes no gol:
{finalizacoes_casa} x {finalizacoes_fora}

🚩 Escanteios:
{escanteios_casa} x {escanteios_fora}

🔥 Time da casa está perdendo
"""

            await app.bot.send_message(
                chat_id=CHAT_ID,
                text=mensagem
            )

            alertas.add(chave)

    except Exception as erro:
        print("ERRO:", erro)

async def monitorar(app):

    while True:

        await verificar_jogos(app)

        await asyncio.sleep(60)

async def iniciar(app):

    print("Bot iniciado!")

    asyncio.create_task(monitorar(app))

def main():

    app = Application.builder().token(TOKEN).post_init(iniciar).build()

    app.add_handler(CommandHandler("status", status))

    app.add_handler(CommandHandler("teste", teste))

    app.run_polling()

main()
