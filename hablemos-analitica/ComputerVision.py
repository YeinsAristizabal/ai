import streamlit as st
import cv2
import requests
import numpy as np
import tempfile
import os
from PIL import Image


# Page Configuration
st.set_page_config(
    page_title="Seguridad en obras",
    layout="wide"
)

# Configuración de Azure Custom Vision
endpoint = "https://southcentralus.api.cognitive.microsoft.com/"
prediction_key = "d1d4da077e9949a3b084aae1af79b97a"
project_id = "eabe2cb6-5fb3-47d8-8932-779ed14213e7"
publish_iteration_name = "Iteration1"
prediction_url = f"{endpoint}/customvision/v3.0/Prediction/{project_id}/detect/iterations/{publish_iteration_name}/image"
headers = {
    "Content-Type": "application/octet-stream",
    "Prediction-Key": prediction_key
}

st.title("🦺 Seguridad en obras de construcción en tiempo real")

# Cargar video original
uploaded_file = st.file_uploader("📂 Sube un video", type=["mp4", "avi", "mov"], key="original_video")

if uploaded_file is not None:
    # Guardar video en un archivo temporal
    temp_video_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
    with open(temp_video_path, "wb") as f:
        f.write(uploaded_file.read())

    # Mostrar video original
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📽️ Video Original")
        st.video(temp_video_path)

    # Botón para iniciar detección
    if st.button("🔍 Detectar"):
        # Leer el video
        cap = cv2.VideoCapture(temp_video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Carpeta temporal para guardar frames procesados
        temp_dir = tempfile.mkdtemp()
        frame_files = []

        frame_interval = max(1, frame_count // 15)  # Tomar 15 frames uniformemente
        frame_idx = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if frame_idx % frame_interval == 0:
                # Convertir frame a imagen con PIL y guardarla
                img_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                frame_file = os.path.join(temp_dir, f"frame_{frame_idx}.png")
                img_pil.save(frame_file, format="PNG")
                frame_files.append(frame_file)

                # Enviar frame a Azure Custom Vision
                _, img_encoded = cv2.imencode('.jpg', frame)
                img_bytes = img_encoded.tobytes()
                response = requests.post(prediction_url, headers=headers, data=img_bytes)
                result = response.json()

                if "predictions" in result:
                    for prediction in result["predictions"]:
                        if prediction["probability"] > 0.5:
                            bbox = prediction.get("boundingBox", {})
                            left = int(bbox["left"] * frame_width)
                            top = int(bbox["top"] * frame_height)
                            width = int(bbox["width"] * frame_width)
                            height = int(bbox["height"] * frame_height)
                            cv2.rectangle(frame, (left, top), (left + width, top + height), (0, 255, 0), 2)
                            label = f"{prediction['tagName']} ({prediction['probability']:.2f})"
                            cv2.putText(frame, label, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            frame_idx += 1

        cap.release()

        # Guardar el video reconstruido a partir de las imágenes
        processed_video_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(processed_video_path, fourcc, fps, (frame_width, frame_height))

        for frame_file in frame_files:
            img = cv2.imread(frame_file)
            out.write(img)

        out.release()

        st.success("✅ El procesamiento ha finalizado. Ahora, sube el video procesado.")

# **Nuevo**: Opción para subir manualmente el video procesado
processed_video_uploaded = st.file_uploader("📤 Sube el video procesado", type=["mp4"], key="processed_video")

if processed_video_uploaded is not None:
    # Guardar el video procesado en un archivo temporal
    temp_processed_video_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
    with open(temp_processed_video_path, "wb") as f:
        f.write(processed_video_uploaded.read())

    # Mostrar el video procesado en la interfaz
    with col2:
        st.subheader("🎞️ Video Procesado")
        st.video(temp_processed_video_path)
