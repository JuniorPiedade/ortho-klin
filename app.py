import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

# --- CONFIGURAÇÃO DE ARQUIVOS ---
LEADS_FILE = 'leads_v3.csv'
USERS_FILE = 'usuarios.csv'

# Função para carregar dados de leads
def load_leads():
    if os.path.exists(LEADS_FILE):
        df = pd.read_csv(LEADS_FILE)
        df['Data Criação'] = pd.to_datetime(df['Data Criação']).dt.date
        df['Data Agendamento'] = pd.to_datetime(df['Data Agendamento']).dt.date
        return df
    return pd.DataFrame(columns=['Nome', 'CPF', 'Telefone', 'Email', 'Origem', 'Status', 'Data Criação', 'Data Agendamento', 'Valor'])

# Função para carregar usuários
def load_users():
    if os.path.exists(USERS_FILE):
        return pd.read_csv(USERS_FILE)
    return pd.DataFrame(columns=['email', 'senha'])

# --- SISTEMA DE LOGIN ---
def login():
    st.sidebar.title("🔐 Acesso ao Sistema")
    aba_login = st.sidebar.radio("Escolha uma opção", ["Login", "Registrar-se"])
    
    users_df = load_users()

    if aba_login == "Registrar-se":
        new_email = st.sidebar.text_input("Novo Email")
        new_pass = st.sidebar.text_input("Nova Senha", type="password")
        if st.sidebar.button("Criar Conta"):
            if new_email in users_df['email'].values:
                st.sidebar.error("Email já cadastrado!")
            else:
                new_user = pd.DataFrame([[new_email, new_pass]], columns=['email', 'senha'])
                new_user.to_csv(USERS_FILE, mode='a', header=not os.path.exists(USERS_FILE), index=False)
                st.sidebar.success("Conta criada! Mude para Login.")

    elif aba_login == "Login":
        email = st.sidebar.text_input("Email")
        senha = st.sidebar.text_input("Senha", type="password")
        if st.sidebar.button("Entrar"):
            user = users_df[(users_df['email'] == email) & (users_df['senha'] == senha)]
            if not user.empty:
                st.session_state['logado'] = True
                st.rerun()
            else:
                st.sidebar.error("Usuário ou senha incorretos.")

# --- INÍCIO DO APP ---
if 'logado' not in st.session_state:
    st.session_state['logado'] = False

if not st.session_state['logado']:
    st.title("👋 Bem-vindo ao CRM Leads")
    st.info("Por favor, faça login na barra lateral para continuar.")
    login()
else:
    # --- ÁREA DO APP LOGADO ---
    df = load_leads()
    st.title("🎯 Gestão Pro: Leads & Orçamentos")
    
    if st.sidebar.button("Sair/Logout"):
        st.session_state['logado'] = False
        st.rerun()

    # --- BARRA DE BUSCA (SEARCH) ---
    st.subheader("🔍 Buscar Lead")
    termo_busca = st.text_input("Pesquisar por Nome ou CPF").lower()

    # --- FORMULÁRIO DE CADASTRO ---
    with st.expander("➕ Adicionar Novo Lead"):
        with st.form("form_novo"):
            c1, c2, c3 = st.columns(3)
            nome = c1.text_input("Nome Completo")
            cpf = c2.text_input("CPF")
            tel = c3.text_input("WhatsApp (ex: 351...)")
            
            origem = st.selectbox("Origem", ["Instagram", "Facebook", "Google", "Indicação", "Outro"])
            status = st.selectbox("Status", ["Pendente", "Em tratamento", "Agendado", "Finalizado"])
            data_ag = st.date_input("Data Agendamento", value=datetime.now())
            valor = st.number_input("Valor (€)", min_value=0.0)
            
            if st.form_submit_button("Salvar Lead"):
                novo = {'Nome': nome, 'CPF': cpf, 'Telefone': tel, 'Email': '', 'Origem': origem, 
                        'Status': status, 'Data Criação': datetime.now().date(), 
                        'Data Agendamento': data_ag, 'Valor': valor}
                df = pd.concat([df, pd.DataFrame([novo])], ignore_index=True)
                df.to_csv(LEADS_FILE, index=False)
                st.success("Lead salvo!")
                st.rerun()

    # --- LÓGICA DE FILTRO DE BUSCA ---
    dados_exibicao = df
    if termo_busca:
        dados_exibicao = df[
            (df['Nome'].str.lower().str.contains(termo_busca)) | 
            (df['CPF'].astype(str).str.contains(termo_busca))
        ]

    # --- ALERTAS E LISTAGEM ---
    st.divider()
    st.subheader("📋 Lista de Leads")
    
    if dados_exibicao.empty:
        st.write("Nenhum lead encontrado.")
    else:
        for index, row in dados_exibicao.iterrows():
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                col1.write(f"👤 **{row['Nome']}** (CPF: {row['CPF']})")
                col2.write(f"📅 Agenda: {row['Data Agendamento']}")
                col3.write(f"💰 {row['Valor']}€")
                
                # Link WhatsApp
                link_wa = f"https://api.whatsapp.com/send?phone={row['Telefone']}"
                col4.markdown(f"[WhatsApp]({link_wa})")
                st.write("---")
