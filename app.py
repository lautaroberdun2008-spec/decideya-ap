import streamlit as st
import uuid
import json
import os
from openai import OpenAI
client = OpenAI()
st.set_page_config(page_title="DecideYa", page_icon="🧠")

st.title("🧠 DecideYa")
st.write("Tomá decisiones estructuradas en segundos.")

# -----------------------------
# IDENTIFICADOR DE USUARIO
# -----------------------------
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

user_id = st.session_state.user_id

# -----------------------------
# BASE DE DATOS (ARCHIVO)
# -----------------------------
DB_FILE = "usage.json"

if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump({}, f)

with open(DB_FILE, "r") as f:
    data = json.load(f)

if user_id not in data:
    data[user_id] = {"count": 0}

# -----------------------------
# LÍMITE DE USO
# -----------------------------
MAX_USES = 5

if data[user_id]["count"] >= MAX_USES:
    st.error("🚫 Llegaste al límite. Activá DecideYa Pro.")
    st.stop()

# -----------------------------
# INPUTS GUIADOS
# -----------------------------
decision = st.text_input("¿Cuál es la decisión que tenés que tomar?")
option_a = st.text_input("Opción A")
option_b = st.text_input("Opción B")
context = st.text_area("Contexto (opcional, pero recomendado)")

# -----------------------------
# BOTÓN
# -----------------------------
if st.button("Analizar decisión"):

    if decision.strip() == "" or option_a.strip() == "" or option_b.strip() == "":
        st.warning("Completá todos los campos.")
        st.stop()

    # SUMAR USO
    data[user_id]["count"] += 1
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

    st.subheader("🧠 Análisis inteligente")

    prompt = f"""
Sos un asistente experto en toma de decisiones.

Analizá esta situación:

Decisión: {decision}

Opción 1: {option_a}
Opción 2: {option_b}

Contexto: {context}

Respondé con:
1. Análisis de opción 1 (pros y contras)
2. Análisis de opción 2 (pros y contras)
3. Comparación clara
4. Recomendación concreta
5. Acción inmediata

Usá lenguaje claro, humano y directo.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        resultado = response.choices[0].message.content
        st.write(resultado)

    except Exception as e:
        st.error("Error con la IA")
        st.write(e)

    remaining = MAX_USES - data[user_id]["count"]
    st.info(f"Usos restantes: {remaining}")