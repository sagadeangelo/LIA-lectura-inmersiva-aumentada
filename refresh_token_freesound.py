import requests
from dotenv import load_dotenv
import os
import datetime

# Ruta del log
LOG_FILE = f"token_refresh_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

def log(msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now()}] {msg}\n")
    try:
        print(msg)
    except UnicodeEncodeError:
        print(msg.encode("utf-8", errors="replace").decode("utf-8"))

class FreesoundAuth:
    def __init__(self, env_path=".env"):
        self.env_path = env_path
        load_dotenv(env_path)
        self.client_id = os.getenv("FREESOUND_CLIENT_ID")
        self.client_secret = os.getenv("FREESOUND_CLIENT_SECRET")
        self.refresh_token = os.getenv("FREESOUND_REFRESH_TOKEN")
        self.access_token = os.getenv("FREESOUND_ACCESS_TOKEN")

    def refresh_access_token(self):
        url = "https://freesound.org/apiv2/oauth2/access_token/"
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token
        }

        response = requests.post(url, data=data)

        if response.status_code == 200:
            tokens = response.json()
            self.access_token = tokens["access_token"]
            self.refresh_token = tokens["refresh_token"]

            self._update_env({
                "FREESOUND_ACCESS_TOKEN": self.access_token,
                "FREESOUND_REFRESH_TOKEN": self.refresh_token
            })

            log("Tokens actualizados correctamente.")
        else:
            log(f"Error al refrescar token: {response.status_code}")
            log(response.text)

    def _update_env(self, nuevos_valores: dict):
        lines = []
        with open(self.env_path, "r") as f:
            for line in f:
                if line.strip() == "" or line.startswith("#"):
                    lines.append(line)
                    continue
                key = line.split("=")[0]
                if key in nuevos_valores:
                    lines.append(f"{key}={nuevos_valores[key]}\n")
                    nuevos_valores.pop(key)
                else:
                    lines.append(line)

        for key, val in nuevos_valores.items():
            lines.append(f"{key}={val}\n")

        with open(self.env_path, "w") as f:
            f.writelines(lines)

# 👉 Ejecutar
if __name__ == "__main__":
    try:
        log("Ejecutando actualización de token...")
        auth = FreesoundAuth(".env")
        auth.refresh_access_token()
    except Exception as e:
        log(f"Error inesperado: {str(e)}")