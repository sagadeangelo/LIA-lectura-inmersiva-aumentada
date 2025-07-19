import requests

# Variables
CLIENT_ID = "q9iOYCeepM5CCgnSpIaH"  # Reemplaza con tu Client ID
CLIENT_SECRET = "Q7Qz1YYTxu5cpuOvS7eBMUn07NZfekQCx4r1hO7j"  # Reemplaza con tu Client Secret
AUTHORIZATION_CODE = "1lmbjz3j4ZOCsuZibdramehaoALHuJ"  # El código de autorización que obtuviste de Freesound
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
