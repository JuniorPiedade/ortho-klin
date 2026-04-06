import streamlit as st
import pandas as pd
import os
import plotly.express as px

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="OrthoKlin | Dashboard", layout="wide")

# --- CSS FUTURISTA (MANTIDO) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;900&display=swap');
    .stApp { background: #050507; color: #ffffff; font-family: 'Inter', sans-serif; }
    [data-testid="stSidebar"] { background: rgba(0, 0, 0, 0.8) !important; backdrop-filter: blur(20px); }
    .glass-card { background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 16px; padding: 20px; margin-bottom: 20px; }
    .kpi-value { font-size: 24px; font-weight: 900; background: linear-gradient(90deg, #8e44ad, #e91e63); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    div.stButton > button { background: linear-gradient(90deg, #8e44ad 0%, #e91e63 100%) !important; color: white !important; border: none !important; font-weight: 700 !important; text-transform: uppercase; width: 100% !important; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO PARA EXIBIR LOGO ---
def mostrar_logo():
    # Lista de possíveis nomes para sua logo
    arquivos_logo = ["Gemini_Generated_Image_17rbuh17rbuh17rb.jpg", "logo.jpg", "logo.png"]
    for arq in arquivos_logo:
        if os.path.exists(arq):
            st.image(arq, use_container_width=True)
            return
    st.markdown("### ORTHOKLIN") # Fallback caso a imagem não seja encontrada

# --- LÓGICA DE LOGIN ---
if 'logado' not in st.session_state: st.session_state['logado'] = False

if not st.session_state['logado']:
    _, col, _ = st.columns([1, 1, 1])
    with col:
        st.write("#")
        mostrar_logo() # Tenta carregar a logo na tela de login
        st.markdown("<h2 style='text-align:center; font-weight:900;'>ACESSO GERAL</h2>", unsafe_allow_html=True)
        user = st.text_input("USUÁRIO")
        pw = st.text_input("SENHA", type="password")
        if st.button("ENTRAR"):
            if user == "admin" and pw == "ortho2026":
                st.session_state['logado'] = True
                st.rerun()
            else: st.error("Acesso Negado")
else:
    # --- SIDEBAR ---
    with st.sidebar:
        mostrar_logo() # Tenta carregar a logo no topo da barra lateral
        st.write("---")
        if st.button("DASHBOARD"): st.session_state['menu'] = "Dash"
        if st.button("GESTÃO GERAL"): st.session_state['menu'] = "Gestao"
        if st.button("NOVO CADASTRO"): st.session_state['menu'] = "Novo"
        st.write("---")
        if st.button("SAIR"):
            st.session_state['logado'] = False
            st.rerun()

    # (O restante do código de Dashboard e Gestão continua aqui abaixo...)
    st.markdown("<h1 style='font-weight:900;'>SISTEMA ATIVO</h1>", unsafe_allow_html=True)
