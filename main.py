import asyncio
import requests
from telegram import Bot
from config import TOKEN, CHAT_ID, API_KEY, LIGAS_PERMITIDAS

bot = Bot(token=TOKEN)

alertas = set()

async def enviar(texto):
    await bot.send_message(
        chat_id=CHAT_ID,
        text=texto
    )

async def verificar_jogos():

    headers = {
        "x-apisports-key": API_KEY
    }

    url = "https://v3.football.api-sports.io/fixtures?live=all"

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

            mensagem = f"""
🚨 ALERTA AO VIVO

🏆 {liga}

⚽ {casa} x {fora}

📊 Placar:
{gols_casa} x {gols_fora}

⏱️ {minuto}'

🔥 Time da casa está perdendo
"""

            await enviar(mensagem)

            print("Alerta enviado")

            alertas.add(chave)

    except Exception as erro:
        print("ERRO:", erro)

async def main():

    print("Bot monitorando partidas...")

    while True:

        await verificar_jogos()

        await asyncio.sleep(60)

asyncio.run(main())
