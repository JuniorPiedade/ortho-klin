import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="OrthoKlin | Sistema de Inteligência",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS FUTURISTA MINIMALISTA (V14) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;900&display=swap');
    
    /* Configuração Global Dark */
    .stApp { 
        background: #050507; 
        color: #ffffff; 
        font-family: 'Inter', sans-serif; 
    }
    
    /* SIDEBAR PRETA MINIMALISTA */
    [data-testid="stSidebar"] { 
        background-color: #000000 !important; 
        border-right: 1px solid rgba(255, 255, 255, 0.05);
        width: 260px !important;
    }

    /* BOTÕES DA SIDEBAR - DESIGN ULTRA MINIMALISTA */
    div.stButton > button {
        background: transparent !important;
        color: #94a3b8 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 4px !important;
        padding: 4px 12px !important;
        font-size: 10px !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        width: 100% !important;
        margin-bottom: 8px !important;
        transition: all 0.3s ease;
        text-align: center;
    }

    /* HOVER DOS BOTÕES - ATIVAÇÃO NEON */
    div.stButton > button:hover {
        background: linear-gradient(90deg, #8e44ad 0%, #e91e63 100%) !important;
        color: white !important;
        border: none !important;
        transform: translateX(3px);
        box-shadow: 0 0 15px rgba(233, 30, 99, 0.2);
    }

    /* TAGS DE STATUS (SISTEMA DE CORES) */
    .tag-agendado { background: #2ecc71; color: #000; padding: 2px 8px; border-radius: 4px; font-weight: 800; font-size: 9px; text-transform: uppercase; }
    .tag-pendente { background: #f1c40f; color: #000; padding: 2px 8px; border-radius: 4px; font-weight: 800; font-size: 9px; text-transform: uppercase; }
    .tag-followup { background: #e91e63; color: #fff; padding: 2px 8px; border-radius: 4px; font-weight: 800; font-size: 9px; text-transform: uppercase; }
    .tag-tratamento { background: #3498db; color: #fff; padding: 2px 8px; border-radius: 4px; font-weight: 800; font-size: 9px; text-transform: uppercase; }

    /* CARDS EM GLASSMORPHISM */
    .glass-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        transition: 0.3s;
    }
    .glass-card:hover {
        border-color: rgba(233, 30, 99, 0.3);
    }
    
    /* TEXTO EM GRADIENTE */
    .gradient-text {
        background: linear-gradient(90deg, #a855f7, #e91e63);
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        letter-spacing: -0.5px;
    }

    /* Inputs e Forms */
    input { background: rgba(255,255,255,0.05) !important; color: white !important; border-radius: 8px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- BANCO DE DADOS (CSV) ---
FILE = 'leads_orthoklin.csv'

def load_data():
    if os.path.exists(FILE):
        df = pd.read_csv(FILE)
        df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce').fillna(0.0)
        df['CPF'] = df['CPF'].astype(str)
        return df
    return pd.DataFrame(columns=['Nome','CPF','Telefone','Origem','Status','Valor'])

def save_data(df):
    df.to_csv(FILE, index=False)

# --- LÓGICA DE SESSÃO ---
if 'logado' not in st.session_state: st.session_state['logado'] = False
if 'menu' not in st.session_state: st.session_state['menu'] = "Dash"

# --- TELA DE LOGIN ---
if not st.
