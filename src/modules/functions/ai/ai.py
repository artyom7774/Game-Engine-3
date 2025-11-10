from src.variables import *

import traceback

import requests
import time

url = "https://artyom7777.pythonanywhere.com/ai"

def requestAI(message):
    data = {"message": message, "model": SETTINGS["model"]}

    response = requests.post(url, json=data)
    ids = response.json()["ids"]

    while True:
        try:
            status = requests.get(f"{url}/status/{ids}").json()

        except requests.exceptions.RequestException as e:
            return 1, traceback.format_exc()

        except BaseException as e:
            return 1, traceback.format_exc()

        if status["status"] == "completed":
            return 0, status["response"]

        if status["status"] == "error":
            return 1, status["error"]

        time.sleep(5)
