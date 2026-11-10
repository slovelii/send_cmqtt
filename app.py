import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform

# ─────────────────────────────────────────────
# CONFIGURACIÓN DE LA PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Supermarket Light Control — Frescura & Iluminación",
    page_icon="🍎",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# ESTILOS CSS: TEMÁTICA SUPERMERCADO (TEXTOS BLANCOS SOBRE AZUL)
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif !important;
    }

    /* Fondo principal limpio y comercial (Blanco impecable) */
    .stApp {
        background-color: #f8fafc !important;
    }

    /* Barra lateral estilo central de operaciones */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 2px solid #e2e8f0;
    }

    /* Tarjetas estilo góndola / estante de supermercado */
    .market-card {
        background: #ffffff !important;
        border: 2px solid #e2e8f0;
        border-top: 5px solid #2563eb; /* Acento Azul */
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }

    .recommendation-card {
        background: #eff6ff !important;
        border: 1px solid #bfdbfe;
        border-left: 5px solid #2563eb;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 15px;
    }

    /* Títulos institucionales */
    h1, h2, h3 {
        color: #1e3a8a !important;
        font-weight: 700 !important;
    }

    /* Botones corporativos en Azul con letras BLANCAS */
    .stButton button {
        background-color: #2563eb !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 10px 20px;
        transition: all 0.2s ease;
    }

    .stButton button span {
        color: #ffffff !important;
    }

    .stButton button:hover {
        background-color: #1d4ed8 !important;
        transform: translateY(-1px);
    }

    /* Forzar texto blanco en componentes o contenedores con fondo azul */
    .badge-azul, .stMarkdown div[style*="background-color: #e2e8f0"] {
        color: #ffffff !important;
    }

    p, span, label {
        color: #334155 !important;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# VARIABLES DE ESTADO Y CONFIGURACIÓN MQTT
# ─────────────────────────────────────────────
broker = "157.230.214.127"
port = 1883

def on_publish(client, userdata, result):
    print("El dato ha sido publicado con éxito \n")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(1)
    message_received = str(message.payload.decode("utf-8"))
    st.info(f"🛰️ Respuesta del sistema central: {message_received}")

# ─────────────────────────────────────────────
# BARRA LATERAL: INFORMACIÓN Y ESTADO DEL SISTEMA
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🛒 Panel de Control de Tienda")
    st.markdown("Gestiona la iluminación inteligente de las secciones de frutas y verduras para optimizar la exhibición y frescura.")
    st.divider()
    st.markdown(f"💻 **Entorno:** Python {platform.python_version()}")
    st.markdown(f"🌐 **Broker MQTT:** `{broker}`")
    st.markdown("🔴 **Estado:** Conectado a Red Comercial")

# ─────────────────────────────────────────────
# ENCABEZADO PRINCIPAL (SIMULACIÓN DE PASILLOS)
# ─────────────────────────────────────────────
st.markdown("""
<div class="market-card" style="text-align: center;">
    <span style="background-color: #fee2e2; color: #dc2626; font-weight: 700; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem;">🍎 SECCIÓN: FRUTAS & VERDURAS 🥦</span>
    <h1 style="margin: 10px 0 5px 0;">Control Lumínico de Supermercado</h1>
    <p style="color: #64748b; font-size: 0.95rem; margin: 0;">
        Ajusta la intensidad de la luz para realzar los colores naturales de los productos frescos y reducir el consumo energético fuera de horario.
    </p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# GUÍA DE RECOMENDACIONES SEGÚN LA HORA DEL DÍA
# ─────────────────────────────────────────────
st.markdown("""
<div class="recommendation-card">
    <h4 style="color: #1e40af !important; margin-top: 0;">⏰ Recomendaciones de Iluminación por Franja Horaria</h4>
    <ul style="margin-bottom: 0; padding-left: 20px; color: #1e293b;">
        <li><b>Mañana (07:00 - 12:00) - Intensidad Alta (80% - 100%):</b> Luz blanca y brillante para simular luz natural, ideal para resaltar la frescura matutina de hortalizas y verduras de hoja verde.</li>
        <li><b>Tarde (12:00 - 18:00) - Intensidad Media (60% - 75%):</b> Luz equilibrada para mantener el atractivo visual en frutas tropicales y de colores cálidos (manzanas, naranjas, tomates).</li>
        <li><b>Noche / Cierre (18:00 - 22:00) - Intensidad Reducida (30% - 45%):</b> Luz de acento suave para pasillos con menor afluencia de público, generando ahorro energético sin perder visibilidad.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CONTROL DE ILUMINACIÓN (INTERRUPTORES PRINCIPALES)
# ─────────────────────────────────────────────
st.markdown("### 💡 Control de Energía General del Pasillo")
col1, col2 = st.columns(2)

with col1:
    if st.button('🔴 ENCENDER LUCES (ON)', use_container_width=True):
        act1 = "ON"
        client1 = paho.Client("SUPERMARKET-ON")                                     
        client1.on_publish = on_publish                                       
        client1.connect(broker, port)  
        message = json.dumps({"Act1": act1})
        client1.publish("cmqtt_s", message)
        st.success("✨ ¡Luces del pasillo encendidas con éxito!")

with col2:
    if st.button('🔵 APAGAR LUCES (OFF)', use_container_width=True):
        act1 = "OFF"
        client1 = paho.Client("SUPERMARKET-OFF")                                     
        client1.on_publish = on_publish                                       
        client1.connect(broker, port)  
        message = json.dumps({"Act1": act1})
        client1.publish("cmqtt_s", message)
        st.warning("🌙 ¡Luces del pasillo apagadas / modo ahorro!")

st.divider()

# ─────────────────────────────────────────────
# CONTROL ANALÓGICO (INTENSIDAD DE LUZ / DIMMER)
# ─────────────────────────────────────────────
st.markdown("### 🎚️ Ajuste de Intensidad Lumínica (Dimmer)")

values = st.slider('Selecciona el porcentaje de intensidad para las góndolas de frutas:', 0.0, 100.0, 50.0)

# Visualizador dinámico del nivel seleccionado con fondo azul y letras BLANCAS
st.markdown(f"""
<div style="background-color: #2563eb; border-radius: 8px; padding: 12px; text-align: center; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
    <span style="font-weight: 600; color: #ffffff;">Nivel de brillo configurado: </span>
    <span style="font-size: 1.3rem; font-weight: 700; color: #ffffff;">{values}%</span>
</div>
""", unsafe_allow_html=True)

if st.button('📡 Enviar Valor de Intensidad al Pasillo', use_container_width=True):
    client1 = paho.Client("SUPERMARKET-ANALOG")                                     
    client1.on_publish = on_publish                                       
    client1.connect(broker, port)   
    message = json.dumps({"Analog": float(values)})
    client1.publish("cmqtt_a", message)
    st.success(f"🚀 ¡Intensidad de {values}% enviada correctamente al sistema de iluminación de frutas y verduras!")
