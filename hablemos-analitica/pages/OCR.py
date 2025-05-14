# Configurar credenciales de Azure
# VISION_ENDPOINT = "https://cvexaple.cognitiveservices.azure.com/"
# VISION_KEY = "a4351427e9c84c4296c8cbdadebe6caa"

import os
import streamlit as st
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from PIL import Image

# Configuración de Azure AI Vision
VISION_ENDPOINT = os.getenv("VISION_ENDPOINT", "https://cvexaple.cognitiveservices.azure.com/")
VISION_KEY = os.getenv("VISION_KEY", "a4351427e9c84c4296c8cbdadebe6caa")

# Crear cliente de Azure AI Vision
client = ImageAnalysisClient(
    endpoint=VISION_ENDPOINT,
    credential=AzureKeyCredential(VISION_KEY)
)

# Interfaz de usuario en Streamlit
st.title("📄 OCR para Facturas")

# Cargar imagen
uploaded_file = st.file_uploader("📂 Sube una factura (JPG, PNG)", type=["jpg", "png"])

if uploaded_file:
    # Mostrar imagen cargada
    image = Image.open(uploaded_file)
    st.image(image, caption="Factura Cargada", use_container_width=False)

    # Botón para procesar OCR
    if st.button("🔍 Analizar Texto"):
        with st.spinner("Procesando..."):
            # Guardar temporalmente la imagen
            temp_image_path = "temp_invoice.jpg"
            image.save(temp_image_path)

            # Analizar imagen con Azure AI Vision
            with open(temp_image_path, "rb") as img_file:
                result = client.analyze(
                    image_data=img_file,
                    visual_features=[VisualFeatures.READ]
                )

            # Extraer texto detectado
            extracted_text = "\n".join(
                [line.text for block in result.read.blocks for line in block.lines]
            )

            # Mostrar resultado
            st.subheader("📜 Texto Extraído:")
            st.text_area("", extracted_text, height=300)

            # Eliminar imagen temporal
            os.remove(temp_image_path)


