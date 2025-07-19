import requests

# Variables
CLIENT_ID = "xQSJHajvYLSJCzsQVk9D"  # Reemplaza con tu Client ID
CLIENT_SECRET = "NutgyglQpd15PvthynaOTLHfwtgo1Wf5X8gFMh1e"  # Reemplaza con tu Client Secret
AUTHORIZATION_CODE = "d6qqxYU2hJ2ZWfzztxrwz2GZ8VoX5F"  # El código de autorización que obtuviste de Freesound
REDIRECT_URI = "http://freesound.org/home/app_permissions/permission_granted/."  # Callback URL (si es el caso)

# URL para obtener el Access Token
url = "https://freesound.org/apiv2/oauth2/access_token/"

# Parámetros de la solicitud POST
data = {
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "grant_type": "authorization_code",
    "code": AUTHORIZATION_CODE,
    "redirect_uri": REDIRECT_URI
}

# Realizar la solicitud POST
response = requests.post(url, data=data)

# Verificar la respuesta de la API
if response.status_code == 200:
    token_data = response.json()
    access_token = token_data.get("access_token", None)

    if access_token:
        print("Access Token obtenido:", access_token)  # Imprime el Access Token
    else:
        print("Error: No se pudo obtener el Access Token.")
else:
    print(f"Error al obtener el Access Token: {response.status_code}")
    print(response.json())
