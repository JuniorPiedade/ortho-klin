import streamlit as st
import pandas as pd
import os
import plotly.express as px

# --- CONFIG ---
st.set_page_config(page_title="OrthoKlin | Dashboard", layout="wide")

# --- CSS ---
st.markdown("""
<style>
.stApp { background: radial-gradient(circle at top, #0a0a12, #050507); color: white; }

.gradient-text {
    background: linear-gradient(90deg, #a855f7, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 900;
}

.card {
    background: rgba(255,255,255,0.05);
    padding:20px;
    border-radius:16px;
    margin-bottom:10px;
}

.subtext { color: #9ca3af; }
</style>
""", unsafe_allow_html=True)

# --- LOGO ---
def render_logo():
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    else:
        st.markdown("<h2 class='gradient-text'>ORTHOKLIN</h2>", unsafe_allow_html=True)

# --- SESSION ---
if 'logado' not in st.session_state:
    st.session_state['logado'] = False

if 'users' not in st.session_state:
    st.session_state['users'] = {"admin": "ortho2026"}

if 'tela' not in st.session_state:
    st.session_state['tela'] = "login"

# --- LEADS ---
if 'leads' not in st.session_state:
    st.session_state['leads'] = pd.DataFrame([
        {"Nome": "Ana", "CPF": "111", "Status": "Agendado", "Faturamento": 500},
        {"Nome": "Carlos", "CPF": "222", "Status": "Pendente", "Faturamento": 0},
        {"Nome": "João", "CPF": "333", "Status": "Follow-up", "Faturamento": 200},
    ])

# --- TELAS ---
def tela_login():
    _, col, _ = st.columns([1,1.2,1])
    with col:
        render_logo()
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
            if st.button("Esqueci senha"):
                st.session_state['tela'] = "recuperar"
                st.rerun()

def tela_cadastro():
    st.markdown("<h2 class='gradient-text'>Criar Conta</h2>", unsafe_allow_html=True)
    user = st.text_input("Novo usuário")
    pw = st.text_input("Senha", type="password")

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

# --- APP ---
else:
    with st.sidebar:
        render_logo()
        menu = st.radio("Menu", ["Dashboard", "Leads", "Novo Registro"])
        if st.button("Sair"):
            st.session_state['logado'] = False
            st.rerun()

    df = st.session_state['leads']

    # --- DASHBOARD ---
    if menu == "Dashboard":
        st.markdown("<h1 class='gradient-text'>Dashboard</h1>", unsafe_allow_html=True)

        total = len(df)
        faturamento = df["Faturamento"].sum()
        follow = len(df[df["Status"] == "Follow-up"])

        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown(f"<div class='card'><h3>Leads</h3><h2>{total}</h2></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='card'><h3>Faturamento</h3><h2>R$ {faturamento}</h2></div>", unsafe_allow_html=True)
        with c3:
            st.markdown(f"<div class='card'><h3>Follow-up</h3><h2>{follow}</h2></div>", unsafe_allow_html=True)

        # --- GRÁFICO ---
        fig = px.pie(df, names='Status', title='Status dos Leads')
        st.plotly_chart(fig, use_container_width=True)

    # --- LEADS ---
    elif menu == "Leads":
        st.markdown("<h1 class='gradient-text'>Leads</h1>", unsafe_allow_html=True)

        busca = st.text_input("Buscar por nome ou CPF")

        df_filtrado = df.copy()
        if busca:
            df_filtrado = df[
                df["Nome"].str.contains(busca, case=False) |
                df["CPF"].str.contains(busca)
            ]

        st.dataframe(df_filtrado, use_container_width=True)

        # --- EDIÇÃO ---
        st.subheader("Editar Lead")
        cpf_edit = st.text_input("CPF do lead")

        if cpf_edit:
            lead = df[df["CPF"] == cpf_edit]

            if not lead.empty:
                nome = st.text_input("Nome", value=lead.iloc[0]["Nome"])
                status = st.selectbox(
                    "Status",
                    ["Agendado", "Pendente", "Follow-up"],
                    index=["Agendado", "Pendente", "Follow-up"].index(lead.iloc[0]["Status"])
                )
                fat = st.number_input("Faturamento", value=int(lead.iloc[0]["Faturamento"]))

                if st.button("Salvar Alterações"):
                    idx = df[df["CPF"] == cpf_edit].index[0]
                    st.session_state['leads'].at[idx, "Nome"] = nome
                    st.session_state['leads'].at[idx, "Status"] = status
                    st.session_state['leads'].at[idx, "Faturamento"] = fat
                    st.success("Atualizado!")
            else:
                st.error("Lead não encontrado")

    # --- NOVO ---
    elif menu == "Novo Registro":
        st.markdown("<h1 class='gradient-text'>Novo Lead</h1>", unsafe_allow_html=True)

        nome = st.text_input("Nome")
        cpf = st.text_input("CPF")
        status = st.selectbox("Status", ["Agendado", "Pendente", "Follow-up"])
        fat = st.number_input("Faturamento", 0)

        if st.button("Salvar"):
            novo = pd.DataFrame([{
                "Nome": nome,
                "CPF": cpf,
                "Status": status,
                "Faturamento": fat
            }])

            st.session_state['leads'] = pd.concat([df, novo], ignore_index=True)
            st.success("Lead cadastrado!")
