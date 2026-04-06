import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
import plotly.express as px

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="OrthoKlin Pro | Dashboard", layout="wide", initial_sidebar_state="expanded")

# --- CSS FUTURISTA (DARK MODE & GRADIENTS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;700&display=swap');

    /* Fundo Geral e Fontes */
    .stApp {
        background: radial-gradient(circle at top right, #1e0b2e, #0f0f12);
        color: #ffffff;
        font-family: 'Rajdhani', sans-serif;
    }

    /* BARRA LATERAL (Glassmorphism) */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(15px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* BOTÕES COM DEGRADÊ NEON */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #8e44ad 0%, #e91e63 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.8rem 2rem !important;
        font-weight: bold !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 0 15px rgba(233, 30, 99, 0.4);
        transition: 0.4s all;
    }
    div.stButton > button:hover {
        box-shadow: 0 0 25px rgba(233, 30, 99, 0.7);
        transform: scale(1.02);
    }

    /* CARDS DE LEADS (Efeito Vidro) */
    .lead-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 25px;
        border-radius: 20px;
        margin-bottom: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transition: 0.3s;
    }
    .lead-card:hover {
        border: 1px solid #e91e63;
        background: rgba(255, 255, 255, 0.08);
    }

    /* BADGES */
    .status-badge {
        padding: 6px 16px;
        border-radius: 50px;
        font-size: 11px;
        font-weight: bold;
        text-transform: uppercase;
    }

    /* INPUTS */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        background-color: rgba(255,255,255,0.05) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE DADOS ---
LEADS_FILE = 'leads_orthoklin.csv'

def load_data():
    if os.path.exists(LEADS_FILE):
        df = pd.read_csv(LEADS_FILE)
        df['Data Criação'] = pd.to_datetime(df['Data Criação']).dt.date
        df['Data Agendamento'] = pd.to_datetime(df['Data Agendamento']).dt.date
        return df
    return pd.DataFrame(columns=['Nome', 'CPF', 'Telefone', 'Origem', 'Status', 'Data Criação', 'Data Agendamento', 'Valor'])

# --- CONTROLE DE ACESSO ---
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

def tela_login():
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.write("#")
        st.write("#")
        if os.path.exists("logo.png"):
            st.image("logo.png")
        st.title("🛡️ Acesso Restrito")
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        if st.button("Entrar no Dashboard"):
            if usuario == "admin" and senha == "ortho2026": # Mude aqui sua senha!
                st.session_state['autenticado'] = True
                st.rerun()
            else:
                st.error("Credenciais inválidas")

def dashboard():
    df = load_data()
    
    # Barra Lateral
    with st.sidebar:
        if os.path.exists("logo.png"):
            st.image("logo.png")
        st.write("---")
        menu = st.radio("NAVEGAÇÃO", ["📊 Dashboard Vital", "👥 Lista de Pacientes", "➕ Novo Cadastro"])
        
        st.write("---")
        total_geral = df['Valor'].sum()
        st.metric("Faturamento em Leads", f"R$ {total_geral:,.2f}")
        
        if st.button("🚪 Logout"):
            st.session_state['autenticado'] = False
            st.rerun()

    # Conteúdo por aba
    if menu == "📊 Dashboard Vital":
        st.title("📈 Performance OrthoKlin")
        c1, c2 = st.columns(2)
        
        if not df.empty:
            # Gráfico Neon 1
            fig1 = px.pie(df, names='Origem', hole=.5, title="Canais de Entrada",
                         color_discrete_sequence=['#8e44ad', '#e91e63', '#6c5ce7', '#ff7675'])
            fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white", showlegend=True)
            c1.plotly_chart(fig1, use_container_width=True)

            # Gráfico Neon 2
            status_valor = df.groupby('Status')['Valor'].sum().reset_index()
            fig2 = px.bar(status_valor, x='Status', y='Valor', title="Volume Financeiro por Etapa",
                         color='Status', color_discrete_map={'Pendente':'#f39c12', 'Agendado':'#3498db', 'Em tratamento':'#27ae60'})
            fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
            c2.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("Aguardando dados para gerar inteligência.")

    elif menu == "👥 Lista de Pacientes":
        st.title("🗂️ Gestão de Pacientes")
        busca = st.text_input("🔍 Pesquisar por Nome ou CPF")
        
        df_f = df
        if busca:
            df_f = df[df['Nome'].str.contains(busca, case=False) | df['CPF'].astype(str).str.contains(busca)]

        for idx, row in df_f.iterrows():
            cor_st = "#f39c12" if row['Status'] == "Pendente" else "#3498db" if row['Status'] == "Agendado" else "#27ae60"
            st.markdown(f"""
                <div class="lead-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 24px; font-weight: bold; color: #fff;">{row['Nome']}</span>
                        <span class="status-badge" style="background-color: {cor_st};">{row['Status']}</span>
                    </div>
                    <div style="margin-top: 15px; display: grid; grid-template-columns: 1fr 1fr; gap: 10px; color: #bbb;">
                        <div>📱 <b>Whats:</b> {row['Telefone']}</div>
                        <div>📂 <b>Origem:</b> {row['Origem']}</div>
                        <div style="font-size: 20px; color: #e91e63;"><b>R$ {row['Valor']:,.2f}</b></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            c1, c2, _ = st.columns([1, 1, 4])
            if c1.markdown(f"[💬 **WhatsApp**](https://api.whatsapp.com/send?phone={row['Telefone']})"): pass
            if c2.button("🗑️ Remover", key=f"del_{idx}"):
                df = df.drop(idx)
                df.to_csv(LEADS_FILE, index=False)
                st.rerun()

    elif menu == "➕ Novo Cadastro":
        st.title("✨ Inserir Novo Lead")
        with st.form("new_lead_form"):
            n = st.text_input("Nome do Paciente")
            c1, c2 = st.columns(2)
            cp = c1.text_input("CPF")
            tl = c2.text_input("WhatsApp (ex: 55...)")
            or_ = st.selectbox("Origem", ["Instagram", "Google", "Facebook", "Indicação"])
            st_ = st.selectbox("Status", ["Pendente", "Em tratamento", "Agendado"])
            vl = st.number_input("Valor do Orçamento (R$)", min_value=0.0)
            dt = st.date_input("Data do Agendamento")
            
            if st.form_submit_button("FINALIZAR CADASTRO"):
                novo_p = {'Nome': n, 'CPF': cp, 'Telefone': tl, 'Origem': or_, 'Status': st_, 
                          'Data Criação': datetime.now().date(), 'Data Agendamento': dt, 'Valor': vl}
                df = pd.concat([df, pd.DataFrame([novo_p])], ignore_index=True)
                df.to_csv(LEADS_FILE, index=False)
                st.success("Paciente adicionado à rede OrthoKlin!")
                st.rerun()

# --- LÓGICA FINAL ---
if st.session_state['autenticado']:
    dashboard()
else:
    tela_login()
