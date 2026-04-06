import streamlit as st
import pandas as pd
import os
from datetime import datetime, date
from PIL import Image
import plotly.express as px

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="OrthoKlin | Enterprise", layout="wide")

# --- CSS EVOLUÍDO (V24) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;900&display=swap');
    .stApp { background: #050507; color: #ffffff; font-family: 'Inter', sans-serif; }
    
    /* Espaçamento para o Header não cobrir conteúdo */
    .main .block-container { padding-top: 5rem !important; }

    /* Header de Perfil Superior */
    .user-header {
        position: fixed; top: 0; right: 0; left: 260px;
        height: 60px; z-index: 99;
        display: flex; justify-content: flex-end; align-items: center;
        padding: 0 30px; background: rgba(5, 5, 7, 0.8);
        backdrop-filter: blur(15px); border-bottom: 1px solid rgba(255,255,255,0.05);
    }
    .user-info-box { text-align: right; border-right: 3px solid #e91e63; padding-right: 15px; }
    .user-name { font-weight: 800; font-size: 13px; color: #ffffff; margin: 0; }
    .user-role { font-size: 10px; color: #a855f7; font-weight: 700; text-transform: uppercase; margin: 0; }

    /* Sidebar e Botões */
    [data-testid="stSidebar"] { background-color: #000000 !important; border-right: 1px solid rgba(255, 255, 255, 0.05); }
    div.stButton > button {
        background: transparent !important; color: #94a3b8 !important; border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 4px !important; font-size: 10px !important; font-weight: 600 !important;
        text-transform: uppercase; width: 100% !important; transition: 0.3s;
    }
    div.stButton > button:hover { background: #e91e63 !important; color: white !important; border: none !important; }

    .glass-card { background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 20px; margin-bottom: 15px; }
    .gradient-text { background: linear-gradient(90deg, #a855f7, #e91e63); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; }
    </style>
    """, unsafe_allow_html=True)

# --- BANCOS DE DADOS ---
USER_FILE = 'usuarios_orthoklin.csv'
LEAD_FILE = 'leads_orthoklin_v2.csv'

def load_users():
    if os.path.exists(USER_FILE): return pd.read_csv(USER_FILE)
    df = pd.DataFrame([{'nome': 'Diretoria', 'user': 'admin', 'pass': 'ortho2026', 'cargo': 'Gestor'}])
    df.to_csv(USER_FILE, index=False); return df

def load_leads():
    if os.path.exists(LEAD_FILE):
        df = pd.read_csv(LEAD_FILE)
        df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce').fillna(0.0)
        df['Data_Cadastro'] = pd.to_datetime(df['Data_Cadastro']).dt.date
        df['Data_Retorno'] = pd.to_datetime(df['Data_Retorno']).dt.date
        return df
    return pd.DataFrame(columns=['Nome','CPF','Telefone','Origem','Status','Valor','Data_Cadastro','Data_Retorno'])

def save_db(df, file): df.to_csv(file, index=False)

# --- ESTADOS ---
if 'logado' not in st.session_state: st.session_state['logado'] = False
if 'user_data' not in st.session_state: st.session_state['user_data'] = {}
if 'menu' not in st.session_state: st.session_state['menu'] = "Dash"

# --- LOGIN ---
if not st.session_state['logado']:
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("<h1 class='gradient-text' style='text-align:center;'>ORTHOKLIN</h1>", unsafe_allow_html=True)
        u, p = st.text_input("USUÁRIO"), st.text_input("SENHA", type="password")
        if st.button("ENTRAR NO SISTEMA"):
            udf = load_users()
            match = udf[(udf['user'] == u) & (udf['pass'] == p)]
            if not match.empty:
                st.session_state['user_data'] = match.iloc[0].to_dict()
                st.session_state['logado'] = True; st.rerun()
            else: st.error("Incorreto.")
        
        if st.button("CRIAR NOVO ACESSO"):
            st.session_state['modo_cadastro'] = True
            
        if st.session_state.get('modo_cadastro'):
            with st.form("quick_reg"):
                n_n, n_u, n_p = st.text_input("Nome"), st.text_input("User"), st.text_input("Senha", type="password")
                if st.form_submit_button("CRIAR E LOGAR"):
                    udf = load_users()
                    new = {'nome': n_n, 'user': n_u, 'pass': n_p, 'cargo': 'CRC'}
                    udf = pd.concat([udf, pd.DataFrame([new])], ignore_index=True)
                    save_db(udf, USER_FILE)
                    st.session_state['user_data'] = new; st.session_state['logado'] = True; st.rerun()
else:
    # --- HEADER CORRIGIDO ---
    u_info = st.session_state['user_data']
    st.markdown(f"""
        <div class="user-header">
            <div class="user-info-box">
                <p class="user-name">{u_info.get('nome','').upper()}</p>
                <p class="user-role">{u_info.get('cargo','')}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # --- SIDEBAR ---
    with st.sidebar:
        st.markdown("<h2 class='gradient-text'>ORTHOKLIN</h2>", unsafe_allow_html=True)
        st.write("---")
        if st.button("🏠 DASHBOARD"): st.session_state['menu'] = "Dash"
        if st.button("👥 GESTÃO DE LEADS"): st.session_state['menu'] = "Gestao"
        if st.button("➕ NOVO CADASTRO"): st.session_state['menu'] = "Novo"
        
        if u_info['cargo'] == "Gestor":
            st.write("---")
            if st.button("📊 BI FINANCEIRO"): st.session_state['menu'] = "BI"
            if st.button("⚙️ CONFIGURAÇÕES"): st.session_state['menu'] = "Config"
        
        st.write("####")
        if st.button("🚪 SAIR"): st.session_state['logado'] = False; st.rerun()

    df_leads = load_leads()

    # --- PÁGINAS ---
    if st.session_state['menu'] == "Dash":
        st.markdown("<h1 class='gradient-text'>PAINEL DE CONTROLE</h1>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.markdown(f'<div class="glass-card"><small>LEADS ATIVOS</small><br><b>{len(df_leads)}</b></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="glass-card"><small>RETORNOS HOJE</small><br><b>{len(df_leads[df_leads["Data_Retorno"] == date.today()])}</b></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="glass-card"><small>TICKET MÉDIO</small><br><b>R$ {df_leads["Valor"].mean():,.2f}</b></div>', unsafe_allow_html=True)

    elif st.session_state['menu'] == "Config":
        st.markdown("<h1 class='gradient-text'>CONFIGURAÇÕES DO SISTEMA</h1>", unsafe_allow_html=True)
        t1, t2 = st.tabs(["👥 Membros da Equipe", "🔐 Permissões por Cargo"])
        
        with t1:
            udf = load_users()
            st.write("### Gestão de Membros")
            for i, r in udf.iterrows():
                col_m1, col_m2, col_m3 = st.columns([2,1,1])
                col_m1.markdown(f"**{r['nome']}** ({r['user']})")
                col_m2.write(f"Cargo: {r['cargo']}")
                if r['user'] != 'admin':
                    if col_m3.button("Remover", key=f"del_{i}"):
                        udf = udf.drop(i); save_db(udf, USER_FILE); st.rerun()
            
            with st.expander("➕ Adicionar Novo Membro"):
                with st.form("new_mem"):
                    n_n, n_u, n_p, n_c = st.text_input("Nome"), st.text_input("User"), st.text_input("Senha"), st.selectbox("Cargo", ["CRC", "Gestor"])
                    if st.form_submit_button("Salvar Membro"):
                        new = {'nome':n_n, 'user':n_u, 'pass':n_p, 'cargo':n_c}
                        udf = pd.concat([udf, pd.DataFrame([new])], ignore_index=True)
                        save_db(udf, USER_FILE); st.rerun()

        with t2:
            st.write("### Matriz de Permissões")
            st.info("Aqui você define o que cada perfil pode acessar no sistema.")
            perm_data = {
                "Recurso": ["Visualizar Dash", "Criar Leads", "Excluir Leads", "Ver BI Financeiro", "Gerenciar Equipe"],
                "CRC": ["✅", "✅", "❌", "❌", "❌"],
                "Gestor": ["✅", "✅", "✅", "✅", "✅"]
            }
            st.table(perm_data)

    elif st.session_state['menu'] == "Gestao":
        st.markdown("<h1 class='gradient-text'>GESTÃO DE PACIENTES</h1>", unsafe_allow_html=True)
        # O CRC pode ver os leads, mas o botão de excluir só aparece se o cargo permitir
        for idx, row in df_leads.iterrows():
            with st.container():
                st.markdown(f'<div class="glass-card"><b>{row["Nome"].upper()}</b> | R$ {row["Valor"]:,.2f}</div>', unsafe_allow_html=True)
                if u_info['cargo'] == "Gestor":
                    if st.button("Excluir Permanente", key=f"ex_{idx}"):
                        df_leads = df_leads.drop(idx); save_db(df_leads, LEAD_FILE); st.rerun()

    elif st.session_state['menu'] == "Novo":
        st.markdown("<h1 class='gradient-text'>CADASTRO DE LEAD</h1>", unsafe_allow_html=True)
        with st.form("add_l"):
            n, c, t = st.text_input("Nome"), st.text_input("CPF"), st.text_input("Telefone")
            v, dr = st.number_input("Valor Orcamento"), st.date_input("Data Retorno")
            if st.form_submit_button("REGISTRAR"):
                new = {'Nome':n,'CPF':c,'Telefone':t,'Origem':'Manual','Status':'Pendente','Valor':v,'Data_Cadastro':date.today(),'Data_Retorno':dr}
                df_leads = pd.concat([df_leads, pd.DataFrame([new])], ignore_index=True)
                save_db(df_leads, LEAD_FILE); st.rerun()

    elif st.session_state['menu'] == "BI":
        st.markdown("<h1 class='gradient-text'>ANÁLISE FINANCEIRA</h1>", unsafe_allow_html=True)
        st.plotly_chart(px.bar(df_leads, x='Nome', y='Valor', color='Origem', template="plotly_dark"))
