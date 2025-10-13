from pypresence import Presence
import requests
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
        print(f"ERROR: can't getting IP: {e}")

        return

    try:
        url = "https://artyom7777.pythonanywhere.com/updateOnline"
        # url = "http://127.0.0.1:5000/updateOnline"

        response = requests.post(
            url=url,
            data={
                "ip": hashlib.sha256(ip.encode()).hexdigest()
            },
            timeout=2
        )

        # print(f"LOG: status: {response.status_code}, Response: {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"ERROR: request failed: {e}")


def updateDiscordStatusRTS(project):
    RPC = Presence(DISCORD_BOT_ID)
    RPC.connect()

    RPC.update(
        details="Develops applications",
        large_image="logo",
        start=time.time(),
        buttons=[
            {"label": "Download", "url": "https://artyom7777.pythonanywhere.com/"}
        ]
    )
