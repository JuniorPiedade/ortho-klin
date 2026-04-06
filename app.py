import streamlit as st
import pandas as pd
import os
from datetime import datetime, date

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="OrthoKlin | Sistema de Gestão", layout="wide")

# --- CSS PERSONALIZADO (LOGIN & SISTEMA) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;900&display=swap');
    .stApp { background: #050507; color: #ffffff; font-family: 'Inter', sans-serif; }
    
    /* Botões Minimalistas */
    div.stButton > button {
        background: transparent !important; color: #94a3b8 !important; border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 4px !important; padding: 4px 12px !important; font-size: 10px !important; font-weight: 600 !important;
        text-transform: uppercase; letter-spacing: 1.2px; width: 100% !important; margin-top: 10px; transition: 0.3s;
    }
    div.stButton > button:hover { background: linear-gradient(90deg, #8e44ad 0%, #e91e63 100%) !important; color: white !important; border: none !important; }

    /* Links de rodapé (Recuperar/Criar) */
    .auth-link {
        font-size: 11px; color: #64748b; text-align: center; cursor: pointer; transition: 0.3s; margin-top: 15px;
    }
    .auth-link:hover { color: #e91e63; }

    .gradient-text { background: linear-gradient(90deg, #a855f7, #e91e63); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; }
    .glass-card { background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 30px; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO DE ESTADOS ---
if 'logado' not in st.session_state: st.session_state['logado'] = False
if 'auth_mode' not in st.session_state: st.session_state['auth_mode'] = "login" # login, cadastro, recuperar

# --- TELA DE ACESSO (REFORMULADA) ---
if not st.session_state['logado']:
    _, col, _ = st.columns([1, 1, 1])
    
    with col:
        st.write("####")
        if os.path.exists("logo.png"): 
            st.image("logo.png", use_container_width=True)
        else:
            st.markdown("<h1 class='gradient-text' style='text-align:center;'>ORTHOKLIN</h1>", unsafe_allow_html=True)

        # MODO: LOGIN
        if st.session_state['auth_mode'] == "login":
            st.markdown("<p style='text-align:center; color:#64748b; font-size:12px; letter-spacing:1px;'>SISTEMA DE GESTÃO IA</p>", unsafe_allow_html=True)
            u = st.text_input("USUÁRIO", placeholder="seu.nome")
            p = st.text_input("SENHA", type="password", placeholder="••••••••")
            
            if st.button("ACESSAR"):
                if u == "admin" and p == "ortho2026":
                    st.session_state['logado'] = True
                    st.rerun()
                else:
                    st.error("Credenciais inválidas.")

            # Links de Rodapé
            c1, c2 = st.columns(2)
            if c1.button("CRIAR PERFIL"): 
                st.session_state['auth_mode'] = "cadastro"
                st.rerun()
            if c2.button("PERDI A SENHA"): 
                st.session_state['auth_mode'] = "recuperar"
                st.rerun()

        # MODO: CRIAR PERFIL
        elif st.session_state['auth_mode'] == "cadastro":
            st.markdown("<h3 style='text-align:center;'>NOVO PERFIL</h3>", unsafe_allow_html=True)
            new_u = st.text_input("DEFINIR USUÁRIO")
            new_p = st.text_input("DEFINIR SENHA", type="password")
            new_p_confirm = st.text_input("CONFIRMAR SENHA", type="password")
            
            if st.button("SOLICITAR CADASTRO"):
                st.success("Solicitação enviada ao administrador!")
            
            if st.button("VOLTAR AO LOGIN"):
                st.session_state['auth_mode'] = "login"
                st.rerun()

        # MODO: RECUPERAR SENHA
        elif st.session_state['auth_mode'] == "recuperar":
            st.markdown("<h3 style='text-align:center;'>RESGATAR SENHA</h3>", unsafe_allow_html=True)
            st.markdown("<p style='font-size:11px; color:#64748b;'>Insira seu e-mail ou usuário para receber as instruções de redefinição.</p>", unsafe_allow_html=True)
            email_resgate = st.text_input("E-MAIL OU USUÁRIO")
            
            if st.button("ENVIAR CÓDIGO"):
                st.info(f"Se o usuário {email_resgate} existir, um código será enviado.")
            
            if st.button("VOLTAR AO LOGIN"):
                st.session_state['auth_mode'] = "login"
                st.rerun()

# --- ÁREA LOGADA (SISTEMA) ---
else:
    # (Aqui entra o restante do seu código de Dashboard, Gestão e Novo Cadastro)
    with st.sidebar:
        if os.path.exists("logo.png"): st.image("logo.png", use_container_width=True)
        st.write("---")
        if st.button("DASHBOARD"): st.session_state['menu'] = "Dash"
        if st.button("GESTAO DE LEADS"): st.session_state['menu'] = "Gestao"
        if st.button("NOVO CADASTRO"): st.session_state['menu'] = "Novo"
        st.write("---")
        if st.button("SAIR"):
            st.session_state['logado'] = False
            st.session_state['auth_mode'] = "login"
            st.rerun()

    st.markdown("<h1 class='gradient-text'>BEM-VINDO AO PAINEL</h1>", unsafe_allow_html=True)
    st.write("Sistema autenticado e operando.")
