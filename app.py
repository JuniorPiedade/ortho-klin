import streamlit as st
import pandas as pd
from datetime import datetime
import os
import plotly.express as px

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="OrthoKlin Pro | Gestão", layout="wide")

# --- CSS PREMIMUM (3D & ELEGÂNCIA) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap');

    .stApp {
        background: radial-gradient(circle at top right, #1a0826, #0a0a0c);
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }

    /* TÍTULOS COM BRILHO */
    .titulo-premium {
        background: linear-gradient(90deg, #ffffff 0%, #e91e63 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.5rem;
        margin-bottom: 20px;
    }

    /* CARDS 3D GLASSMORPISM */
    .lead-card {
        background: rgba(255, 255, 255, 0.03);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
        margin-bottom: 20px;
        transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .lead-card:hover {
        transform: translateY(-10px) scale(1.01);
        border: 1px solid #e91e63;
        box-shadow: 0 30px 60px rgba(233, 30, 99, 0.15);
    }

    /* BOTÕES COM EFEITO DE PROFUNDIDADE */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #8e44ad 0%, #e91e63 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        height: 50px !important;
        font-weight: 700 !important;
        letter-spacing: 1.5px;
        box-shadow: 0 10px 20px rgba(142, 68, 173, 0.4) !important;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        box-shadow: 0 15px 30px rgba(233, 30, 99, 0.6) !important;
        transform: translateY(-3px);
    }

    /* STATUS BADGE 3D */
    .badge-3d {
        padding: 6px 18px;
        border-radius: 30px;
        font-size: 10px;
        font-weight: 900;
        text-transform: uppercase;
        box-shadow: inset 0 2px 4px rgba(255,255,255,0.2);
    }

    /* SIDEBAR CUSTOM */
    [data-testid="stSidebar"] {
        background: rgba(10, 10, 12, 0.8) !important;
        backdrop-filter: blur(20px);
    }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE DADOS ---
FILE = 'leads_orthoklin.csv'
def load_data():
    if os.path.exists(FILE):
        df = pd.read_csv(FILE)
        df['Data Criação'] = pd.to_datetime(df['Data Criação']).dt.date
        df['Data Agendamento'] = pd.to_datetime(df['Data Agendamento']).dt.date
        return df
    return pd.DataFrame(columns=['Nome', 'CPF', 'Telefone', 'Origem', 'Status', 'Data Criação', 'Data Agendamento', 'Valor'])

# --- LOGIN ---
if 'logado' not in st.session_state: st.session_state['logado'] = False

if not st.session_state['logado']:
    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        st.write("#")
        if os.path.exists("logo.png"): st.image("logo.png")
        st.
