import streamlit as st
import pandas as pd
import os
from datetime import datetime, date
from PIL import Image
import plotly.express as px

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="OrthoKlin | Enterprise BI", layout="wide", initial_sidebar_state="expanded")

# --- CSS PREMIUN (V22) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;900&display=swap');
    .stApp { background: #050507; color: #ffffff; font-family: 'Inter', sans-serif; }
    [data-testid="stSidebar"] { background-color: #000000 !important; border-right: 1px solid rgba(255, 255, 255, 0.05); width: 260px !important; }
    
    .user-header {
        position: fixed; top: 1rem; right: 2rem;
        text-align: right; z-index: 1000;
        padding: 8px 15px; border-radius: 8px;
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
    }
    .user-name { font-weight: 800; font-size: 11px; color: #ffffff; margin: 0; letter-spacing: 0.5px; }
    .user-role { font-size: 9px; color: #e91e63; font-weight: 700; text-transform: uppercase; margin: 0; }

    div.stButton > button {
        background: transparent !important; color: #94a3b8 !important; border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 4px !important; padding: 4px 12px !important; font-size: 10px !important; font-weight: 600 !important;
        text-transform: uppercase; letter-spacing: 1.2px; width: 100% !important; margin-top: 8px; transition: 0.3s;
    }
    div.stButton > button:hover { background: linear-gradient(90deg, #8e44ad 0%, #e91e63 100%) !important; color: white !important; border: none !important; transform: translateX(4px); }

    .tag-agendado { background: #2ecc71; color: #000; padding: 2px 8px; border-radius: 4px; font-weight: 800; font-size: 9px; text-transform: uppercase; }
    .tag-pendente { background: #f1c40f; color: #000; padding: 2px 8px; border-radius: 4px; font-weight: 800; font-size: 9px; text-transform: uppercase; }
    .tag-followup { background: #e91e63; color: #fff; padding: 2px 8px; border-radius: 4px; font-weight: 800; font-size: 9px; text-transform: uppercase; }
    .data-alerta { color: #ff4b4b; font-weight: 700; }
    
    .glass-card { background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 20px; margin-bottom: 15px; }
    .gradient-text { background: linear-gradient(90deg, #a855f7, #e91e63); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE ---
LEAD_FILE = 'leads_orthoklin_v2.csv'
USER_FILE = 'usuarios_orthoklin.csv'

def load_leads():
    if os.path.exists(LEAD_FILE):
        df = pd.read_csv(LEAD_FILE)
        df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce').fillna(0.0)
        df['Data_Cadastro'] = pd.to_datetime(df['Data_Cadastro']).dt.date
        df['Data_Retorno'] = pd.to_datetime(df['Data_Retorno']).dt.date
        return df
    return pd.DataFrame(columns=['Nome','CPF','Telefone','Origem','Status','Valor','Data_Cadastro','Data_Retorno'])

def load_users():
    if os.path.exists(USER_FILE):
        return pd.read_csv(USER_FILE)
    # Garante a criação do arquivo com colunas corretas
    df = pd.DataFrame([{'nome': 'Diretoria Ortho', 'user': 'admin', 'pass': 'ortho2026', 'cargo': 'Gestor'}])
    df.to_csv(USER_FILE, index=False)
    return df

def save_data(df, filename): df.to_csv(filename, index=False)

def render_logo():
    if os.path.exists("logo.png"):
        try: st.image(Image.open("logo.png"), use_container_width=True)
        except: st.markdown("<h1 class='gradient-text' style='text-align:center;'>ORTHOKLIN</h1>", unsafe_allow_html=True)
    else: st.markdown("<h1 class='gradient-text' style='text-align:center;'>ORTHOKLIN</h1>", unsafe_allow_html=True)

# --- SESSION STATE ---
if 'logado' not in st.session_state: st.session_state['logado'] = False
if 'user_data' not in st.session_state: st.session_state['user_data'] = {}
if 'menu' not in st.session_state: st.session_state['menu'] = "Dash"

# --- TELA DE ACESSO ---
if not st.session_state['logado']:
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.write("####")
        render_logo()
        u = st.text_input("USUÁRIO")
        p = st.text_input("SENHA", type="password")
        
        col_btn1, col_btn2 = st.columns(2)
        if col_btn1.button("ACESSAR"):
            users_df = load_users()
            match = users_df[(users_df['user'] == u) & (users_df['pass'] == p)]
            if not match.empty:
                st.session_state['user_data'] = match.iloc[0].to_dict()
                st.session_state['logado'] = True
                st.rerun()
            else: st.error("Acesso negado.")

        if col_btn2.button("CRIAR ACESSO"):
            st.session_state['create_mode'] = True

        if st.session_state.get('create_mode'):
            with st.form("new_acc"):
                new_n = st.text_input("Nome Completo")
                new_u = st.text_input("Novo Usuário")
                new_p = st.text_input("Senha", type="password")
                if st.form_submit_button("FINALIZAR E ENTRAR"):
                    u_df = load_users()
                    new_entry = {'nome': new_n, 'user': new_u, 'pass': new_p, 'cargo': 'CRC'}
                    u_df = pd.concat([u_df, pd.DataFrame([new_entry])], ignore_index=True)
                    save_data(u_df, USER_FILE)
                    st.session_state['user_data'] = new_entry
                    st.session_state['logado'] = True
                    st.rerun()
else:
    # --- HEADER DINÂMICO (COM TRAVA DE SEGURANÇA) ---
    u_info = st.session_state.get('user_data', {})
    u_nome = u_info.get('nome', 'Usuário').upper()
    u_cargo = u_info.get('cargo', 'Membro')

    st.markdown(f"""
        <div class="user-header">
            <p class="user-name">{u_nome}</p>
            <p class="user-role">{u_cargo}</p>
        </div>
    """, unsafe_allow_html=True)

    df_leads = load_leads()

    # --- SIDEBAR ---
    with st.sidebar:
        render_logo()
        st.write("###")
        if st.button("DASHBOARD"): st.session_state['menu'] = "Dash"
        if st.button("GESTAO DE LEADS"): st.session_state['menu'] = "Gestao"
        if st.button("NOVO CADASTRO"): st.session_state['menu'] = "Novo"
        if u_cargo == "Gestor":
            if st.button("BI FINANCEIRO"): st.session_state['menu'] = "BI"
            if st.button("EQUIPE / CARGOS"): st.session_state['menu'] = "Config"
        st.write("---")
        if st.button("SAIR"):
            st.session_state['logado'] = False
            st.rerun()

    # --- CONTEÚDO ---
    if st.session_state['menu'] == "Dash":
        st.markdown("<h1 class='gradient-text'>OVERVIEW</h1>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.markdown(f'<div class="glass-card"><small>TOTAL DE LEADS</small><br><b>{len(df_leads)}</b></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="glass-card"><small>RETORNOS HOJE</small><br><b>{len(df_leads[df_leads["Data_Retorno"] == date.today()])}</b></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="glass-card"><small>VALOR EM ABERTO</small><br><b>R$ {df_leads[df_leads["Status"] != "Em tratamento"]["Valor"].sum():,.2f}</b></div>', unsafe_allow_html=True)

    elif st.session_state['menu'] == "Gestao":
        st.markdown("<h1 class='gradient-text'>GESTÃO</h1>", unsafe_allow_html=True)
        busca = st.text_input("BUSCAR PACIENTE")
        df_f = df_leads[df_leads['Nome'].str.contains(busca, case=False)] if busca else df_leads
        for idx, row in df_f.sort_values(by='Data_Retorno').iterrows():
            with st.container():
                st.markdown(f'<div class="glass-card"><b>{row["Nome"].upper()}</b> | {row["Status"]}<br><small>Retorno: {row["Data_Retorno"]}</small></div>', unsafe_allow_html=True)
                if st.button("APAGAR", key=f"del_{idx}"):
                    df_leads = df_leads.drop(idx); save_data(df_leads, LEAD_FILE); st.rerun()

    elif st.session_state['menu'] == "Novo":
        st.markdown("<h1 class='gradient-text'>CADASTRO</h1>", unsafe_allow_html=True)
        with st.form("add_lead"):
            n = st.text_input("Nome")
            c = st.text_input("CPF")
            t = st.text_input("Telefone")
            v = st.number_input("Valor", min_value=0.0)
            dr = st.date_input("Retorno")
            if st.form_submit_button("SALVAR"):
                new = {'Nome':n,'CPF':c,'Telefone':t,'Origem':'Instagram','Status':'Pendente','Valor':v,'Data_Cadastro':date.today(),'Data_Retorno':dr}
                df_leads = pd.concat([df_leads, pd.DataFrame([new])], ignore_index=True)
                save_data(df_leads, LEAD_FILE); st.success("OK!"); st.rerun()

    elif st.session_state['menu'] == "BI":
        st.markdown("<h1 class='gradient-text'>BI & FINANCEIRO</h1>", unsafe_allow_html=True)
        st.metric("Faturamento Geral", f"R$ {df_leads['Valor'].sum():,.2f}")
        fig = px.pie(df_leads, values='Valor', names='Status', hole=0.5)
        st.plotly_chart(fig)

    elif st.session_state['menu'] == "Config":
        st.markdown("<h1 class='gradient-text'>EQUIPE</h1>", unsafe_allow_html=True)
        u_df = load_users()
        st.dataframe(u_df[['nome', 'user', 'cargo']])
                    if st.session_state.get(f"reset_{i}"):
                        ns = st.text_input("Nova Senha", key=f"ns_{i}")
                        if st.button("SALVAR SENHA", key=f"btn_{i}"):
                            u_df.at[i, 'pass'] = ns; save_data(u_df, USER_FILE); st.success("Senha alterada!"); st.rerun()
