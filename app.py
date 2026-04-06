import streamlit as st
import pandas as pd
import os
from datetime import datetime, date
from PIL import Image
import plotly.express as px

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="OrthoKlin | Business Intelligence", layout="wide")

# --- REGRAS DE SEGURANÇA (SENHAS DE CARGO) ---
SENHAS_CARGO = {
    "CRC": "CRC402001",
    "Gestor": "GER202601",
    "Suporte": "SU202601"
}

# --- CSS PERSONALIZADO (V26 - HEADER & ESTILO) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;900&display=swap');
    .stApp { background: #050507; color: #ffffff; font-family: 'Inter', sans-serif; }
    [data-testid="stSidebar"] { background-color: #000000 !important; border-right: 1px solid rgba(255, 255, 255, 0.05); width: 260px !important; }
    
    /* Ajuste para o Header não cobrir o conteúdo */
    .main .block-container { padding-top: 5rem !important; }

    /* Header de Perfil Superior Direto */
    .user-header {
        position: fixed; top: 0; right: 0; left: 260px;
        height: 70px; z-index: 999;
        display: flex; justify-content: flex-end; align-items: center;
        padding: 0 40px; background: rgba(5, 5, 7, 0.9);
        backdrop-filter: blur(10px); border-bottom: 1px solid rgba(255,255,255,0.05);
    }
    .user-info-box { text-align: right; border-right: 3px solid #e91e63; padding-right: 15px; }
    .user-name { font-weight: 800; font-size: 14px; color: #ffffff; margin: 0; }
    .user-role { font-size: 10px; color: #a855f7; font-weight: 700; text-transform: uppercase; margin: 0; letter-spacing: 1px; }

    div.stButton > button {
        background: transparent !important; color: #94a3b8 !important; border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 4px !important; padding: 4px 12px !important; font-size: 10px !important; font-weight: 600 !important;
        text-transform: uppercase; letter-spacing: 1.2px; width: 100% !important; margin-top: 10px; transition: 0.3s;
    }
    div.stButton > button:hover { background: linear-gradient(90deg, #8e44ad 0%, #e91e63 100%) !important; color: white !important; border: none !important; transform: translateX(3px); }

    .tag-agendado { background: #2ecc71; color: #000; padding: 2px 8px; border-radius: 4px; font-weight: 800; font-size: 9px; text-transform: uppercase; }
    .tag-pendente { background: #f1c40f; color: #000; padding: 2px 8px; border-radius: 4px; font-weight: 800; font-size: 9px; text-transform: uppercase; }
    .tag-followup { background: #e91e63; color: #fff; padding: 2px 8px; border-radius: 4px; font-weight: 800; font-size: 9px; text-transform: uppercase; }
    
    .glass-card { background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 20px; margin-bottom: 15px; }
    .gradient-text { background: linear-gradient(90deg, #a855f7, #e91e63); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; }
    </style>
    """, unsafe_allow_html=True)

# --- BANCO DE DADOS ---
FILE_LEADS = 'leads_orthoklin_v2.csv'
FILE_USERS = 'usuarios_orthoklin.csv'

def load_data():
    if os.path.exists(FILE_LEADS):
        df = pd.read_csv(FILE_LEADS)
        df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce').fillna(0.0)
        df['Data_Cadastro'] = pd.to_datetime(df['Data_Cadastro']).dt.date
        df['Data_Retorno'] = pd.to_datetime(df['Data_Retorno']).dt.date
        return df
    return pd.DataFrame(columns=['Nome','CPF','Telefone','Origem','Status','Valor','Data_Cadastro','Data_Retorno'])

def load_users():
    if os.path.exists(FILE_USERS): return pd.read_csv(FILE_USERS)
    # Admin padrão se o arquivo não existir
    df = pd.DataFrame([{'nome': 'Diretoria', 'user': 'admin', 'pass': 'ortho2026', 'cargo': 'Gestor'}])
    df.to_csv(FILE_USERS, index=False)
    return df

def save_data(df, file): df.to_csv(file, index=False)

def render_logo():
    if os.path.exists("logo.png"):
        st.image(Image.open("logo.png"), use_container_width=True)
    else:
        st.markdown("<h1 class='gradient-text' style='text-align:center;'>ORTHOKLIN</h1>", unsafe_allow_html=True)

# --- LOGICA DE SESSÃO ---
if 'logado' not in st.session_state: st.session_state['logado'] = False
if 'user_data' not in st.session_state: st.session_state['user_data'] = {}
if 'menu' not in st.session_state: st.session_state['menu'] = "Dash"

# --- TELA DE ACESSO ---
if not st.session_state['logado']:
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        render_logo()
        tab_login, tab_reg = st.tabs(["LOGIN", "CRIAR CONTA"])
        
        with tab_login:
            u = st.text_input("USUÁRIO")
            p = st.text_input("SENHA", type="password")
            if st.button("ACESSAR SISTEMA"):
                users = load_users()
                match = users[(users['user'] == u) & (users['pass'] == p)]
                if not match.empty:
                    st.session_state['user_data'] = match.iloc[0].to_dict()
                    st.session_state['logado'] = True
                    st.rerun()
                else: st.error("Acesso negado.")

        with tab_reg:
            with st.form("registro"):
                rn = st.text_input("Nome Completo")
                ru = st.text_input("Usuário de Acesso")
                rp = st.text_input("Senha Pessoal", type="password")
                rc = st.selectbox("Cargo", ["CRC", "Gestor", "Suporte"])
                rs = st.text_input(f"Senha de Autorização ({rc})", type="password")
                if st.form_submit_button("FINALIZAR CADASTRO"):
                    if rs == SENHAS_CARGO[rc]:
                        users = load_users()
                        new_user = {'nome':rn, 'user':ru, 'pass':rp, 'cargo':rc}
                        users = pd.concat([users, pd.DataFrame([new_user])], ignore_index=True)
                        save_data(users, FILE_USERS)
                        st.success("Conta criada! Vá para Login.")
                    else: st.error("Senha de cargo incorreta.")

else:
    # --- HEADER DINÂMICO ---
    u_info = st.session_state['user_data']
    st.markdown(f"""
        <div class="user-header">
            <div class="user-info-box">
                <p class="user-name">{u_info.get('nome','').upper()}</p>
                <p class="user-role">{u_info.get('cargo','')}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    df = load_data()

    # --- SIDEBAR ---
    with st.sidebar:
        render_logo()
        st.write("###")
        if st.button("DASHBOARD"): st.session_state['menu'] = "Dash"
        if st.button("GESTAO DE LEADS"): st.session_state['menu'] = "Gestao"
        
        # Acesso condicional ao BI e Configurações
        if u_info['cargo'] in ["Gestor", "Suporte"]:
            if st.button("BI & FINANCEIRO"): st.session_state['menu'] = "BI"
            if st.button("CONFIGURAÇÕES / EQUIPE"): st.session_state['menu'] = "Config"
            
        if st.button("NOVO CADASTRO"): st.session_state['menu'] = "Novo"
        if st.button("MEU PERFIL"): st.session_state['menu'] = "Perfil"
        st.write("---")
        if st.button("SAIR"): st.session_state['logado'] = False; st.rerun()

    # --- CONTEÚDO ---
    if st.session_state['menu'] == "Dash":
        st.markdown("<h1 class='gradient-text'>RESUMO DIÁRIO</h1>", unsafe_allow_html=True)
        hoje = date.today()
        c1, c2, c3 = st.columns(3)
        c1.markdown(f'<div class="glass-card"><small>RETORNOS HOJE</small><br><b>{len(df[df["Data_Retorno"] == hoje])}</b></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="glass-card"><small>NOVOS LEADS (MÊS)</small><br><b>{len(df[df["Data_Cadastro"] >= hoje.replace(day=1)])}</b></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="glass-card"><small>STATUS AGENDADO</small><br><b style="color:#2ecc71;">{len(df[df["Status"] == "Agendado"])}</b></div>', unsafe_allow_html=True)

    elif st.session_state['menu'] == "BI":
        st.markdown("<h1 class='gradient-text'>INTELIGÊNCIA FINANCEIRA</h1>", unsafe_allow_html=True)
        total = df['Valor'].sum()
        c1, c2, c3 = st.columns(3)
        c1.markdown(f'<div class="glass-card"><small>FATURAMENTO GERAL</small><br><b style="font-size:24px; color:#2ecc71;">R$ {total:,.2f}</b></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="glass-card"><small>TICKET MÉDIO</small><br><b style="font-size:24px;">R$ {total/len(df) if len(df)>0 else 0:,.2f}</b></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="glass-card"><small>FOLLOW-UP ATIVO</small><br><b style="font-size:24px; color:#e91e63;">R$ {df[df["Status"]=="Follow-up"]["Valor"].sum():,.2f}</b></div>', unsafe_allow_html=True)
        st.plotly_chart(px.pie(df, values='Valor', names='Origem', hole=0.6, template="plotly_dark"), use_container_width=True)

    elif st.session_state['menu'] == "Gestao":
        st.markdown("<h1 class='gradient-text'>GESTOR DE PACIENTES</h1>", unsafe_allow_html=True)
        busca = st.text_input("BUSCAR POR NOME")
        df_f = df[df['Nome'].str.contains(busca, case=False)] if busca else df
        for idx, row in df_f.iterrows():
            with st.container():
                st.markdown(f'<div class="glass-card"><b>{row["Nome"].upper()}</b> | Status: {row["Status"]}<br><small>WhatsApp: {row["Telefone"]} | Valor: R$ {row["Valor"]:,.2f}</small></div>', unsafe_allow_html=True)
                if u_info['cargo'] in ["Gestor", "Suporte"]:
                    if st.button("APAGAR LEAD", key=f"del_{idx}"):
                        df = df.drop(idx); save_data(df, FILE_LEADS); st.rerun()

    elif st.session_state['menu'] == "Novo":
        st.markdown("<h1 class='gradient-text'>NOVO CADASTRO</h1>", unsafe_allow_html=True)
        with st.form("novo_lead"):
            n, c, t = st.text_input("NOME"), st.text_input("CPF"), st.text_input("WHATSAPP")
            o, s, v = st.selectbox("ORIGEM", ["Instagram", "Google Ads", "Indicação"]), st.selectbox("STATUS", ["Pendente", "Follow-up"]), st.number_input("VALOR")
            dr = st.date_input("RETORNO")
            if st.form_submit_button("SALVAR"):
                new = {'Nome':n, 'CPF':c, 'Telefone':t, 'Origem':o, 'Status':s, 'Valor':v, 'Data_Cadastro':date.today(), 'Data_Retorno':dr}
                df = pd.concat([df, pd.DataFrame([new])], ignore_index=True); save_data(df, FILE_LEADS); st.rerun()

    elif st.session_state['menu'] == "Perfil":
        st.markdown("<h1 class='gradient-text'>MEU PERFIL</h1>", unsafe_allow_html=True)
        with st.form("edit_p"):
            en = st.text_input("Nome", value=u_info['nome'])
            eu = st.text_input("Usuário", value=u_info['user'])
            ep = st.text_input("Nova Senha", value=u_info['pass'], type="password")
            ec = st.selectbox("Cargo", ["CRC", "Gestor", "Suporte"], index=["CRC", "Gestor", "Suporte"].index(u_info['cargo']))
            es = st.text_input("Confirme a Senha de Autorização do Cargo", type="password")
            if st.form_submit_button("ATUALIZAR MEUS DADOS"):
                if es == SENHAS_CARGO[ec]:
                    users = load_users()
                    users.loc[users['user'] == u_info['user'], ['nome', 'user', 'pass', 'cargo']] = [en, eu, ep, ec]
                    save_data(users, FILE_USERS)
                    st.session_state['user_data'] = {'nome':en, 'user':eu, 'pass':ep, 'cargo':ec}
                    st.success("Dados atualizados!"); st.rerun()
                else: st.error("Senha de autorização de cargo inválida.")

    elif st.session_state['menu'] == "Config":
        st.markdown("<h1 class='gradient-text'>EQUIPE E ACESSOS</h1>", unsafe_allow_html=True)
        udf = load_users()
        for i, r in udf.iterrows():
            with st.container():
                st.markdown(f'<div class="glass-card"><b>{r["nome"]}</b> - {r["cargo"]} (Login: {r["user"]})</div>', unsafe_allow_html=True)
                if r['user'] != 'admin' and r['user'] != u_info['user']:
                    if st.button("REMOVER MEMBRO", key=f"rem_{i}"):
                        udf = udf.drop(i); save_data(udf, FILE_USERS); st.rerun()
