import streamlit as st
import pandas as pd
import os
from datetime import datetime, date
from PIL import Image
import plotly.express as px

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="OrthoKlin | Enterprise BI", layout="wide")

# --- SENHAS DE CARGO ---
SENHAS_CARGO = {"CRC": "CRC402001", "Gestor": "GER202601", "Suporte": "SU202601"}

# --- CSS PREMIUN COM ANIMAÇÃO DE DEGRADÊ (V27) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;900&display=swap');
    
    /* Fundo com Degradê Animado */
    .stApp {
        background: linear-gradient(135deg, #050507 0%, #0c0c14 50%, #050507 100%);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }

    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Ajuste de Layout */
    .main .block-container { padding-top: 6rem !important; }
    [data-testid="stSidebar"] { background-color: rgba(0, 0, 0, 0.8) !important; backdrop-filter: blur(10px); border-right: 1px solid rgba(255, 255, 255, 0.05); width: 260px !important; }

    /* Header de Perfil Superior */
    .user-header {
        position: fixed; top: 0; right: 0; left: 260px;
        height: 70px; z-index: 999;
        display: flex; justify-content: flex-end; align-items: center;
        padding: 0 40px; background: rgba(5, 5, 7, 0.5);
        backdrop-filter: blur(15px); border-bottom: 1px solid rgba(255,255,255,0.05);
    }
    .user-info-box { text-align: right; border-right: 3px solid #e91e63; padding-right: 15px; }
    .user-name { font-weight: 800; font-size: 14px; color: #ffffff; margin: 0; }
    .user-role { font-size: 10px; color: #a855f7; font-weight: 700; text-transform: uppercase; margin: 0; letter-spacing: 1px; }

    /* Estilização de Cards e Botões */
    .glass-card { 
        background: rgba(255, 255, 255, 0.03); 
        border: 1px solid rgba(255, 255, 255, 0.08); 
        border-radius: 16px; padding: 25px; margin-bottom: 20px;
        backdrop-filter: blur(5px);
    }
    
    div.stButton > button {
        background: rgba(255,255,255,0.02) !important; color: #94a3b8 !important; border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 6px !important; padding: 6px 15px !important; font-size: 11px !important; font-weight: 600 !important;
        text-transform: uppercase; width: 100% !important; transition: 0.4s;
    }
    div.stButton > button:hover { 
        background: linear-gradient(90deg, #8e44ad, #e91e63) !important; 
        color: white !important; border: none !important; transform: scale(1.02);
    }

    .gradient-text { background: linear-gradient(90deg, #a855f7, #e91e63); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE DADOS ---
FILE_LEADS = 'leads_orthoklin_v2.csv'
FILE_USERS = 'usuarios_orthoklin.csv'

def load_data(file, columns):
    if os.path.exists(file):
        df = pd.read_csv(file)
        if 'Valor' in df.columns: df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce').fillna(0.0)
        for col in ['Data_Cadastro', 'Data_Retorno']:
            if col in df.columns: df[col] = pd.to_datetime(df[col]).dt.date
        return df
    return pd.DataFrame(columns=columns)

def save_data(df, file): df.to_csv(file, index=False)

# --- SESSÃO ---
if 'logado' not in st.session_state: st.session_state['logado'] = False
if 'user_data' not in st.session_state: st.session_state['user_data'] = {}
if 'menu' not in st.session_state: st.session_state['menu'] = "Dash"

# --- LOGIN / REGISTRO ---
if not st.session_state['logado']:
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("<h1 class='gradient-text' style='text-align:center;'>ORTHOKLIN</h1>", unsafe_allow_html=True)
        t1, t2 = st.tabs(["LOGIN", "CADASTRO"])
        
        with t1:
            u = st.text_input("USUÁRIO")
            p = st.text_input("SENHA", type="password")
            if st.button("ACESSAR"):
                users = load_data(FILE_USERS, ['nome','user','pass','cargo'])
                # Admin padrão
                if not users.any().any() and u == "admin" and p == "ortho2026":
                    st.session_state['user_data'] = {'nome':'Admin','user':'admin','pass':'ortho2026','cargo':'Gestor'}
                    st.session_state['logado'] = True; st.rerun()
                
                match = users[(users['user'] == u) & (users['pass'] == p)]
                if not match.empty:
                    st.session_state['user_data'] = match.iloc[0].to_dict()
                    st.session_state['logado'] = True; st.rerun()
                else: st.error("Acesso Negado.")

        with t2:
            with st.form("reg"):
                rn, ru, rp = st.text_input("Nome"), st.text_input("User"), st.text_input("Senha Pessoal", type="password")
                rc = st.selectbox("Cargo", ["CRC", "Gestor", "Suporte"])
                rs = st.text_input(f"Chave de Autorização {rc}", type="password")
                if st.form_submit_button("CRIAR CONTA"):
                    if rs == SENHAS_CARGO[rc]:
                        users = load_data(FILE_USERS, ['nome','user','pass','cargo'])
                        users = pd.concat([users, pd.DataFrame([{'nome':rn,'user':ru,'pass':rp,'cargo':rc}])], ignore_index=True)
                        save_data(users, FILE_USERS); st.success("Sucesso! Faça Login.")
                    else: st.error("Chave incorreta.")
else:
    # --- HEADER ---
    u = st.session_state['user_data']
    st.markdown(f'<div class="user-header"><div class="user-info-box"><p class="user-name">{u["nome"].upper()}</p><p class="user-role">{u["cargo"]}</p></div></div>', unsafe_allow_html=True)

    # --- SIDEBAR ---
    with st.sidebar:
        st.markdown("<h2 class='gradient-text'>ORTHOKLIN</h2>", unsafe_allow_html=True)
        st.write("---")
        if st.button("📊 DASHBOARD"): st.session_state['menu'] = "Dash"
        if st.button("👥 GESTÃO LEADS"): st.session_state['menu'] = "Gestao"
        if st.button("➕ NOVO CADASTRO"): st.session_state['menu'] = "Novo"
        if u['cargo'] in ["Gestor", "Suporte"]:
            if st.button("📈 BI FINANCEIRO"): st.session_state['menu'] = "BI"
            if st.button("⚙️ CONFIGURAÇÕES"): st.session_state['menu'] = "Config"
        if st.button("👤 MEU PERFIL"): st.session_state['menu'] = "Perfil"
        st.write("---")
        if st.button("🚪 SAIR"): st.session_state['logado'] = False; st.rerun()

    df = load_data(FILE_LEADS, ['Nome','CPF','Telefone','Origem','Status','Valor','Data_Cadastro','Data_Retorno'])

    # --- DASHBOARD ---
    if st.session_state['menu'] == "Dash":
        st.markdown("<h1 class='gradient-text'>RESUMO EXECUTIVO</h1>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        hoje = date.today()
        c1.markdown(f'<div class="glass-card"><small>RETORNOS HOJE</small><br><b style="font-size:28px;">{len(df[df["Data_Retorno"] == hoje])}</b></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="glass-card"><small>CONVERSÃO MÊS</small><br><b style="font-size:28px;">{len(df[df["Status"]=="Agendado"])}</b></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="glass-card"><small>TICKET MÉDIO</small><br><b style="font-size:28px; color:#2ecc71">R$ {df["Valor"].mean():,.0f}</b></div>', unsafe_allow_html=True)

    # --- GESTÃO ---
    elif st.session_state['menu'] == "Gestao":
        st.markdown("<h1 class='gradient-text'>CONTROLE DE PACIENTES</h1>", unsafe_allow_html=True)
        busca = st.text_input("Filtrar por nome...")
        df_f = df[df['Nome'].str.contains(busca, case=False)] if busca else df
        for idx, row in df_f.iterrows():
            with st.container():
                st.markdown(f'<div class="glass-card"><b>{row["Nome"].upper()}</b> | Valor: R$ {row["Valor"]:,.2f}<br><small>Status: {row["Status"]} | Retorno: {row["Data_Retorno"]}</small></div>', unsafe_allow_html=True)
                if u['cargo'] in ["Gestor", "Suporte"]:
                    if st.button("Excluir", key=f"del_{idx}"):
                        df = df.drop(idx); save_data(df, FILE_LEADS); st.rerun()

    # --- PERFIL ---
    elif st.session_state['menu'] == "Perfil":
        st.markdown("<h1 class='gradient-text'>EDITAR PERFIL</h1>", unsafe_allow_html=True)
        with st.form("perfil_edit"):
            en, eu, ep = st.text_input("Nome", u['nome']), st.text_input("User", u['user']), st.text_input("Senha", u['pass'], type="password")
            ec = st.selectbox("Cargo", ["CRC", "Gestor", "Suporte"], index=["CRC", "Gestor", "Suporte"].index(u['cargo']))
            es = st.text_input(f"Chave de Autorização para {ec}", type="password")
            if st.form_submit_button("SALVAR"):
                if es == SENHAS_CARGO[ec]:
                    users = load_data(FILE_USERS, [])
                    users.loc[users['user'] == u['user'], ['nome','user','pass','cargo']] = [en, eu, ep, ec]
                    save_data(users, FILE_USERS)
                    st.session_state['user_data'] = {'nome':en,'user':eu,'pass':ep,'cargo':ec}
                    st.success("Atualizado!"); st.rerun()
                else: st.error("Chave inválida.")

    # --- NOVO ---
    elif st.session_state['menu'] == "Novo":
        st.markdown("<h1 class='gradient-text'>CADASTRAR LEAD</h1>", unsafe_allow_html=True)
        with st.form("novo"):
            n, v = st.text_input("Nome"), st.number_input("Valor")
            dr = st.date_input("Data Retorno")
            if st.form_submit_button("REGISTRAR"):
                df = pd.concat([df, pd.DataFrame([{'Nome':n,'Valor':v,'Data_Cadastro':date.today(),'Data_Retorno':dr, 'Status':'Pendente'}])], ignore_index=True)
                save_data(df, FILE_LEADS); st.rerun()

    # --- BI ---
    elif st.session_state['menu'] == "BI":
        st.markdown("<h1 class='gradient-text'>BUSINESS INTELLIGENCE</h1>", unsafe_allow_html=True)
        st.plotly_chart(px.bar(df, x='Nome', y='Valor', color='Status', template="plotly_dark"), use_container_width=True)

    # --- CONFIG ---
    elif st.session_state['menu'] == "Config":
        st.markdown("<h1 class='gradient-text'>EQUIPE</h1>", unsafe_allow_html=True)
        users = load_data(FILE_USERS, [])
        st.dataframe(users[['nome','user','cargo']])
