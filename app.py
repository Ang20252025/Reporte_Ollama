
import time
import requests
import streamlit as st

URL = "http://localhost:11434/api/chat"
MODELO = "qwen3:4b"

st.set_page_config(page_title="Diagnóstico tecnológico")
st.title("💻 Asistente de diagnóstico tecnológico")

st.write(
    "Describe el problema de tu computador "
    "para recibir orientación y recomendaciones."
)

problema = st.text_area("Describe el problema:")

instrucciones = """
Eres un asistente de mantenimiento tecnológico.
Responde en español claro.
Incluye:
1. Resumen del problema.
2. Posibles causas.
3. Revisiones iniciales seguras.
4. Recomendaciones preventivas.
5. Cuándo acudir a un técnico.

No afirmes que el diagnóstico es definitivo.
No recomiendes manipular componentes eléctricos
ni borrar archivos del sistema.
"""

if st.button("Generar diagnóstico"):
    if problema.strip():

        datos = {
            "model": MODELO,
            "messages": [
                {"role": "system", "content": instrucciones},
                {"role": "user", "content": problema}
            ],
            "stream": False
        }

        try:
            inicio = time.perf_counter()

            respuesta = requests.post(
                URL,
                json=datos,
                timeout=180
            )

            respuesta.raise_for_status()
            resultado = respuesta.json()

            tiempo = time.perf_counter() - inicio

            st.subheader("Resultado del análisis")
            st.write(resultado["message"]["content"])

            st.success(
                f"Tiempo de respuesta: {tiempo:.2f} segundos"
            )

        except requests.exceptions.ConnectionError:
            st.error(
                "No se pudo conectar con Ollama. "
                "Verifica que esté abierto."
            )

        except Exception as error:
            st.error(f"Error: {error}")

    else:
        st.warning("Debes escribir un problema.")
