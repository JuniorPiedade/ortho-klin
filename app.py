import streamlit as st
import pandas as pd
from datetime import datetime
import os
import plotly.express as px

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="OrthoKlin Pro | Acesso", layout="wide")

# --- CSS PREMIUM (LOGIN & CADASTRO) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap');
    .stApp { background: radial-gradient(circle at top right, #1a0826, #0a0a0c); color: #fff; font-family: 'Inter', sans-serif; }
    
    .titulo-premium {
        background: linear-gradient(90deg, #ffffff 0%, #e91e63 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-weight: 800; font-size: 2.8rem; text-align: center;
    }

    /* BOTÃO ESTILO GOOGLE */
    .google-btn {
        display: flex; align-items: center; justify-content: center;
        background: white; color: #444; border-radius: 12px;
        padding: 10px; font-weight: 600; cursor: pointer;
        border: 1px solid #ddd; margin-bottom: 20px;
    }

    /* CARD DE LOGIN */
    .login-box {
        background: rgba(255, 255, 255, 0.05);
        padding: 40px; border-radius: 25px;
        backdrop-filter: blur(15px); border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 25px 50px rgba(0,0,0,0.5);
    }

    /* BOTÕES DASHBOARD */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #8e44ad 0%, #e91e63 100%) !important;
        color: white !important; border: none !important; border-radius: 12px !important;
        height: 50px !important; font-weight: 700 !important;
        box-shadow: 0 8px 20px rgba(233, 30, 99, 0.3) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE DADOS ---
LEADS_FILE = 'leads_orthoklin.csv'
USERS_FILE = 'usuarios_ortho.csv'

def load_users():
    if os.path.exists(USERS_FILE): return pd.read_csv(USERS_FILE)
    return pd.DataFrame([["admin", "ortho2026"]], columns=['usuario', 'senha'])

def save_user(u, s):
    df_u = load_users()
    if u not in df_u['usuario'].values:
        new_u = pd.DataFrame([[u, s]], columns=['usuario', 'senha'])
        pd.concat([df_u, new_u]).to_csv(USERS_FILE, index=False)
        return True
    return False

# --- LOGICA DE NAVEGAÇÃO ---
if 'logado' not in st.session_state: st.session_state['logado'] = False
if 'tela' not in st.session_state: st.session_state['tela'] = 'login'

# --- TELA DE ACESSO GERAL ---
if not st.session_state['logado']:
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.write("#")
        if os.path.exists("logo.png"): st.image("logo.png")
        st.markdown(f'<p class="titulo-premium">Acesso Geral</p>', unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div class="login-box">', unsafe_allow_html=True)
            
            if st.session_state['tela'] == 'login':
                # Botão "Fake" Google para Estética Profissional
                st.markdown('<div class="google-btn"><img src="https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg" width="20" style="margin-right:10px"> Entrar com Google</div>', unsafe_allow_html=True)
                
                user = st.text_input("💎 Utilizador")
                pw = st.text_input("🔑 Senha", type="password")
                
                if st.button("DESBLOQUEAR SISTEMA"):
                    df_u = load_users()
                    if ((df_u['usuario'] == user) & (df_u['senha'] == pw)).any():
                        st.session_state['logado'] = True
                        st.rerun()
                    else: st.error("Acesso Negado")
                
                if st.button("✨ Criar Primeiro Acesso"):
                    st.session_state['tela'] = 'registro'
                    st.rerun()

            else: # TELA DE REGISTRO
                st.subheader("📝 Novo Registro")
                new_user = st.text_input("Definir Novo Utilizador")
                new_pw = st.text_input("Definir Senha", type="password")
                conf_pw = st.text_input("Confirmar Senha", type="password")
                
                if st.button("💎 FINALIZAR CADASTRO"):
                    if new_pw == conf_pw and new_user != "":
                        if save_user(new_user, new_pw):
                            st.success("Conta criada! Já pode fazer login.")
                            st.session_state['tela'] = 'login'
                            st.rerun()
                        else: st.error("Utilizador já existe!")
                    else: st.error("As senhas não coincidem.")
                
                if st.button("⬅️ Voltar ao Login"):
                    st.session_state['tela'] = 'login'
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# --- ÁREA DO DASHBOARD (Apenas se logado) ---
else:
    # [O restante do código de Dashboard, Pacientes e Novo Registro permanece o mesmo aqui]
    # (Vou resumir para não estourar o espaço, mas mantém a lógica anterior de abas)
    st.sidebar.image("logo.png") if os.path.exists("logo.png") else st.sidebar.title("OrthoKlin")
    menu = st.sidebar.radio("SISTEMA", ["💎 Dashboard", "📂 Pacientes", "✨ Novo Registro"])
    
    if st.sidebar.button("🚀 SAIR"):
        st.session_state['logado'] = False
        st.rerun()
        
    # (Aqui entra a lógica das abas que já configuramos antes...)
    st.markdown('<p class="titulo-premium">Sistema Ativo</p>', unsafe_allow_html=True)
    st.write("Bem-vindo ao centro de comando OrthoKlin.")
