import pypresence
import traceback
import requests
import logging
import hashlib
import socket
import time

DISCORD_BOT_ID = "1427340617800880330"


def updateOnlineOnSite(project):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]

    except Exception as e:
        logging.error(f"can't getting IP: {e}")

        return

    try:
        url = "https://ge3.pythonanywhere.com/updateOnline"
        # url = "http://127.0.0.1:5000/updateOnline"

        response = requests.post(
            url=url,
            data={
                "ip": hashlib.sha256(ip.encode()).hexdigest()
            },
            timeout=2
        )

        # logging.info(f"status: {response.status_code}, response: {response.text}")

    except requests.exceptions.RequestException as e:
        logging.error(f"request failed: {e}")


def updateDiscordStatusRPS(project):
    RPC = None

    try:
        RPC = pypresence.Presence(DISCORD_BOT_ID)

        RPC.connect()

        RPC.update(
            details="Develops applications",
            large_image="logo",
            start=time.time(),
            buttons=[
                {"label": "Site", "url": "https://ge3.pythonanywhere.com/"}
            ]
        )

    except pypresence.exceptions.DiscordNotFound:
        logging.info("discord is not found")

    except BaseException as e:
        logging.error(f"request failed: {traceback.format_exc()}")

    finally:
        try:
            RPC.close()

        except AssertionError:
            pass
