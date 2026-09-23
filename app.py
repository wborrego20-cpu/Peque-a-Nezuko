# Nezuko
import streamlit as st
import json
import os

# Configuración de la página web
st.set_page_config(page_title="IA de Walter", page_icon="🤖", layout="centered")

ARCHIVO_MEMORIA = "memoria_asistente.json"

def cargar_memoria():
    if os.path.exists(ARCHIVO_MEMORIA):
        with open(ARCHIVO_MEMORIA, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "usuario": "Walter",
        "historial": []
    }

def guardar_memoria(memoria):
    with open(ARCHIVO_MEMORIA, "w", encoding="utf-8") as f:
        json.dump(memoria, f, ensure_ascii=False, indent=4)

# Inicializar estado de la app
if "memoria" not in st.session_state:
    st.session_state.memoria = cargar_memoria()

# --- INTERFAZ GRÁFICA ---
st.title("🤖 Asistente Virtual")
st.write(f"Bienvenido, **{st.session_state.memoria['usuario']}**.")

# Panel lateral para personalizar la interfaz
st.sidebar.header("🎨 Personalización")
color_tema = st.sidebar.color_picker("Color principal del asistente", "#4F46E5")

# Mostrar el historial de la conversación en la web
for mensaje in st.session_state.memoria["historial"]:
    with st.chat_message(mensaje["rol"]):
        st.write(mensaje["texto"])

# Entrada de texto del usuario
if entrada := st.chat_input("Escribe tu mensaje aquí..."):
    # Guardar y mostrar mensaje del usuario
    st.session_state.memoria["historial"].append({"rol": "user", "texto": entrada})
    with st.chat_message("user"):
        st.write(entrada)

    # Generar respuesta de la IA
    texto_lc = entrada.lower()
    nombre = st.session_state.memoria["usuario"]

    if "hola" in texto_lc:
        respuesta = f"¡Hola, {nombre}! ¿Cómo puedo ayudarte hoy?"
    elif "cómo me llamo" in texto_lc or "quién soy" in texto_lc:
        respuesta = f"Te llamas {nombre}."
    else:
        respuesta = f"Entendido, {nombre}. Guardé tu mensaje en mi registro."

    # Guardar y mostrar respuesta de la IA
    st.session_state.memoria["historial"].append({"rol": "assistant", "texto": respuesta})
    with st.chat_message("assistant"):
        st.write(respuesta)

    # Guardar permanentemente en el archivo JSON
    guardar_memoria(st.session_state.memoria)
