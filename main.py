import requests
import time
from telegram import Bot
from config import TOKEN, CHAT_ID, API_KEY, LIGAS_PERMITIDAS

bot = Bot(token=TOKEN)

alertas_enviados = set()

def enviar_alerta(texto):
    try:
        bot.send_message(
            chat_id=CHAT_ID,
            text=texto
        )
    except Exception as e:
        print(e)

def verificar_jogos():

    url = "https://v3.football.api-sports.io/fixtures?live=all"

    headers = {
        "x-apisports-key": API_KEY
    }

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

            casa = jogo["teams"]["home"]["name"]
            fora = jogo["teams"]["away"]["name"]

            gols_casa = jogo["goals"]["home"] or 0
            gols_fora = jogo["goals"]["away"] or 0

            minuto = jogo["fixture"]["status"]["elapsed"] or 0

            if minuto < 15:
                continue

            favorito = casa

            if gols_casa < gols_fora:

                chave = str(fixture_id)

                if chave not in alertas_enviados:

                    mensagem = f"""
🚨 FAVORITO PERDENDO

🏆 {jogo['league']['name']}

⚽ {casa} x {fora}

⭐ Favorito: {favorito}

📊 Placar:
{gols_casa} x {gols_fora}

⏱️ {minuto}'

🔥 Possível oportunidade
"""

                    enviar_alerta(mensagem)

                    alertas_enviados.add(chave)

    except Exception as erro:
        print("Erro:", erro)

while True:

    verificar_jogos()

    time.sleep(60)
