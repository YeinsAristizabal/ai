import requests

# Datos de Azure Custom Vision
endpoint = "https://southcentralus.api.cognitive.microsoft.com/"
prediction_key = "d1d4da077e9949a3b084aae1af79b97a"
project_id = "eabe2cb6-5fb3-47d8-8932-779ed14213e7"
publish_iteration_name = "Iteration1"

prediction_url = f"{endpoint}/customvision/v3.0/Prediction/{project_id}/detect/iterations/{publish_iteration_name}/image"

headers = {
    "Content-Type": "application/octet-stream",
    "Prediction-Key": prediction_key
}

# Prueba con una imagen local (ajusta la ruta)
image_path = "hablemos-analitica\\images-9-_jpeg.rf.a60f44f442c15d9460681382717239f8.jpg"

with open(image_path, "rb") as img_file:
    img_bytes = img_file.read()

response = requests.post(prediction_url, headers=headers, data=img_bytes)

# Imprimir respuesta de Azure
print("Código de respuesta:", response.status_code)
print("Respuesta JSON:", response.json())
