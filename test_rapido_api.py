import requests

API_KEY = '8572376-60f3473d80b7a26079ec34be4'  # Reemplaza con tu clave de API válida
url = f'https://pixabay.com/api/?key={API_KEY}&q=nature&image_type=photo'

response = requests.get(url)
if response.status_code == 200:
    print("Datos obtenidos:", response.json())
else:
    print("Error:", response.status_code)
    print("Mensaje de error:", response.text)



