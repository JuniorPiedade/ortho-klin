import streamlit as st
import pandas as pd
import os

# --- CONFIG ---
st.set_page_config(page_title="OrthoKlin | Dashboard", layout="wide")

# --- CSS FUTURISTA ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;900&display=swap');

.stApp { 
    background: radial-gradient(circle at top, #0a0a12, #050507); 
    color: #ffffff; 
    font-family: 'Inter', sans-serif; 
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: rgba(10, 10, 20, 0.7) !important;
    backdrop-filter: blur(20px);
}

/* GRADIENTE TEXTO */
.gradient-text {
    background: linear-gradient(90deg, #a855f7, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 900;
}

/* BOTÕES */
.stButton>button {
    background: linear-gradient(90deg, #7c3aed, #ec4899);
    color: white;
    border-radius: 12px;
    transition: 0.3s;
    box-shadow: 0 0 10px rgba(236, 72, 153, 0.4);
}

.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 20px rgba(236, 72, 153, 0.8);
}

/* CARDS */
.card {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    padding: 20px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 0 20px rgba(168, 85, 247, 0.15);
    transition: 0.3s;
}

.card:hover {
    transform: translateY(-5px);
}

/* SUBTEXT */
.subtext {
    color: #9ca3af;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

# --- LOGO ---
def render_logo():
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    else:
        st.markdown("<h2 class='gradient-text'>ORTHOKLIN</h2>", unsafe_allow_html=True)

# --- SESSION STATE ---
if 'logado' not in st.session_state:
    st.session_state['logado'] = False

if 'users' not in st.session_state:
    st.session_state['users'] = {"admin": "ortho2026"}

if 'tela' not in st.session_state:
    st.session_state['tela'] = "login"

# --- TELAS ---
def tela_login():
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        render_logo()
        st.markdown("<p class='subtext' style='text-align:center;'>SISTEMA DE GESTÃO IA</p>", unsafe_allow_html=True)

        user = st.text_input("Usuário")
        pw = st.text_input("Senha", type="password")

        if st.button("ACESSAR"):
            if user in st.session_state['users'] and st.session_state['users'][user] == pw:
                st.session_state['logado'] = True
                st.rerun()
            else:
                st.error("Credenciais inválidas")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Criar conta"):
                st.session_state['tela'] = "cadastro"
                st.rerun()
        with c2:
            if st.button("Esqueci a senha"):
                st.session_state['tela'] = "recuperar"
                st.rerun()

def tela_cadastro():
    st.markdown("<h2 class='gradient-text'>Criar Conta</h2>", unsafe_allow_html=True)

    user = st.text_input("Novo usuário")
    pw = st.text_input("Nova senha", type="password")

    if st.button("Cadastrar"):
        st.session_state['users'][user] = pw
        st.success("Conta criada!")
        st.session_state['tela'] = "login"
        st.rerun()

    if st.button("Voltar"):
        st.session_state['tela'] = "login"
        st.rerun()

def tela_recuperar():
    st.markdown("<h2 class='gradient-text'>Recuperar Senha</h2>", unsafe_allow_html=True)

    user = st.text_input("Usuário")

    if st.button("Recuperar"):
        if user in st.session_state['users']:
            st.info(f"Senha: {st.session_state['users'][user]}")
        else:
            st.error("Usuário não encontrado")

    if st.button("Voltar"):
        st.session_state['tela'] = "login"
        st.rerun()

# --- LOGIN FLOW ---
if not st.session_state['logado']:
    if st.session_state['tela'] == "login":
        tela_login()
    elif st.session_state['tela'] == "cadastro":
        tela_cadastro()
    elif st.session_state['tela'] == "recuperar":
        tela_recuperar()

# --- APP PRINCIPAL ---
else:
    with st.sidebar:
        render_logo()
        menu = st.radio("Menu", ["Dashboard", "Pacientes", "Novo Registro"])
        if st.button("Sair"):
            st.session_state['logado'] = False
            st.rerun()

    # --- DADOS MOCK ---
    df = pd.DataFrame({
        "Paciente": ["Ana", "Carlos", "João", "Marina"],
        "Idade": [25, 40, 33, 29],
        "Status": ["Ativo", "Ativo", "Inativo", "Ativo"]
    })

    total = len(df)
    ativos = len(df[df["Status"] == "Ativo"])
    inativos = len(df[df["Status"] == "Inativo"])

    # --- DASHBOARD ---
    if menu == "Dashboard":
        st.markdown("<h1 class='gradient-text'>Dashboard</h1>", unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown(f"<div class='card'><h3>Pacientes</h3><h2>{total}</h2></div>", unsafe_allow_html=True)

        with c2:
            st.markdown(f"<div class='card'><h3>Ativos</h3><h2>{ativos}</h2></div>", unsafe_allow_html=True)

        with c3:
            st.markdown(f"<div class='card'><h3>Inativos</h3><h2>{inativos}</h2></div>", unsafe_allow_html=True)

        st.dataframe(df, use_container_width=True)

    elif menu == "Pacientes":
        st.markdown("<h1 class='gradient-text'>Pacientes</h1>", unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True)

    elif menu == "Novo Registro":
        st.markdown("<h1 class='gradient-text'>Novo Paciente</h1>", unsafe_allow_html=True)

        nome = st.text_input("Nome")
        idade = st.number_input("Idade", 0, 120)
        status = st.selectbox("Status", ["Ativo", "Inativo"])

        if st.button("Salvar"):
            st.success("Paciente cadastrado (simulação)")
