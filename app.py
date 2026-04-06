import streamlit as st
import pandas as pd
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="OrthoKlin | Dashboard", layout="wide")

# --- CSS FUTURISTA (DARK MODE) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;900&display=swap');
    
    .stApp { background: #050507; color: #ffffff; font-family: 'Inter', sans-serif; }
    
    /* Estilização da Sidebar para suportar a logo */
    [data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.8) !important;
        backdrop-filter: blur(15px);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Centralizar imagem na sidebar */
    [data-testid="stSidebarNav"] { padding-top: 20px; }

    /* Efeito de degradê nos títulos */
    .gradient-text {
        background: linear-gradient(90deg, #8e44ad, #e91e63);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO PARA RENDERIZAR A LOGO ---
def render_logo():
    if os.path.exists("logo.png"):
        # use_container_width=True garante que ela se ajuste à largura da sidebar/coluna
        st.image("logo.png", use_container_width=True)
    else:
        # Fallback elegante caso o arquivo não seja encontrado
        st.markdown("<h2 class='gradient-text'>ORTHOKLIN</h2>", unsafe_allow_html=True)

# --- SISTEMA DE LOGIN ---
if 'logado' not in st.session_state: st.session_state['logado'] = False

if not st.session_state['logado']:
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.write("#")
        render_logo() # Logo na tela de entrada
        st.markdown("<p style='text-align:center; color:#64748b; font-size:12px; letter-spacing:2px;'>SISTEMA DE GESTÃO IA</p>", unsafe_allow_html=True)
        
        user = st.text_input("USUÁRIO")
        pw = st.text_input("SENHA", type="password")
        
        if st.button("ACESSAR PAINEL"):
            if user == "admin" and pw == "ortho2026":
                st.session_state['logado'] = True
                st.rerun()
            else:
                st.error("Credenciais inválidas")
else:
    # --- SIDEBAR COM LOGO ---
    with st.sidebar:
        render_logo() # Logo no topo do menu lateral
        st.write("---")
        menu = st.radio("NAVEGAÇÃO", ["DASHBOARD", "PACIENTES", "NOVO REGISTRO"])
        st.write("---")
        if st.button("ENCERRAR SESSÃO"):
            st.session_state['logado'] = False
            st.rerun()

    # --- CONTEÚDO PRINCIPAL ---
    st.markdown(f"<h1 class='gradient-text' style='text-align:left;'>{menu}</h1>", unsafe_allow_html=True)
    st.write(f"Bem-vindo ao centro de comando OrthoKlin.")
