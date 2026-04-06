import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="OrthoKlin | Gestão de Leads", layout="wide")

# --- CSS FUTURISTA (SIDEBAR + TAGS COLORIDAS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;900&display=swap');
    
    .stApp { background: #050507; color: #ffffff; font-family: 'Inter', sans-serif; }
    
    /* SIDEBAR CUSTOMIZADA */
    [data-testid="stSidebar"] { 
        background-color: #000000 !important; 
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }

    /* TAGS DE STATUS SEM EMOJI */
    .tag-agendado { background: #2ecc71; color: #000; padding: 4px 12px; border-radius: 6px; font-weight: 800; font-size: 10px; text-transform: uppercase; }
    .tag-pendente { background: #f1c40f; color: #000; padding: 4px 12px; border-radius: 6px; font-weight: 800; font-size: 10px; text-transform: uppercase; }
    .tag-followup { background: #e91e63; color: #fff; padding: 4px 12px; border-radius: 6px; font-weight: 800; font-size: 10px; text-transform: uppercase; }
    .tag-tratamento { background: #3498db; color: #fff; padding: 4px 12px; border-radius: 6px; font-weight: 800; font-size: 10px; text-transform: uppercase; }

    /* CARDS */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
    }
    
    .gradient-text {
        background: linear-gradient(90deg, #a855f7, #e91e63);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-weight: 900;
    }

    /* BOTÕES DA SIDEBAR (DEGRADÊ) */
    div.stButton > button {
        background: linear-gradient(90deg, #8e44ad 0%, #e91e63 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        width: 100% !important;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(233, 30, 99, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE DADOS ---
FILE = 'leads_orthoklin.csv'
def load_data():
    if os.path.exists(FILE):
        df = pd.read_csv(FILE)
        df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce').fillna(0.0)
        df['CPF'] = df['CPF'].astype(str)
        return df
    return pd.DataFrame(columns=['Nome','CPF','Telefone','Origem','Status','Valor'])

def save_data(df):
    df.to_csv(FILE, index=False)

# --- GESTÃO DE ACESSO ---
if 'logado' not in st.session_state: st.session_state['logado'] = False

if not st.session_state['logado']:
    _, col, _ = st.columns([1, 1, 1])
    with col:
        st.write("#")
        if os.path.exists("logo.png"): st.image("logo.png")
        st.markdown("<h2 class='gradient-text' style='text-align:center;'>ACESSO RESTRITO</h2>", unsafe_allow_html=True)
        u = st.text_input("USUÁRIO")
        p = st.text_input("SENHA", type="password")
        if st.button("ENTRAR"):
            if u == "admin" and p == "ortho2026":
                st.session_state['logado'] = True
                st.rerun()
else:
    df = load_data()
    
    # --- SIDEBAR LATERAL (BOTÕES SEM EMOJI) ---
    with st.sidebar:
        if os.path.exists("logo.png"): st.image("logo.png")
        st.write("---")
        if st.button("DASHBOARD"): st.session_state['menu'] = "Dash"
        if st.button("GESTAO DE LEADS"): st.session_state['menu'] = "Gestao"
        if st.button("NOVO CADASTRO"): st.session_state['menu'] = "Novo"
        st.write("---")
        if st.button("SAIR"):
            st.session_state['logado'] = False
            st.rerun()

    # Define menu padrão
    if 'menu' not in st.session_state: st.session_state['menu'] = "Dash"

    # --- ABA: DASHBOARD ---
    if st.session_state['menu'] == "Dash":
        st.markdown("<h1 class='gradient-text'>DESEMPENHO</h1>", unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        c1.markdown(f'<div class="glass-card"><small>VALOR TOTAL</small><br><b style="font-size:24px;">R$ {df["Valor"].sum():,.2f}</b></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="glass-card"><small>PENDENTES</small><br><b style="font-size:24px; color:#f1c40f;">R$ {df[df["Status"] == "Pendente"]["Valor"].sum():,.2f}</b></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="glass-card"><small>FOLLOW-UP</small><br><b style="font-size:24px; color:#e91e63;">{len(df[df["Status"] == "Follow-up"])} Leads</b></div>', unsafe_allow_html=True)

        if not df.empty:
            fig = px.pie(df, names='Status', hole=0.7, 
                         color='Status',
                         color_discrete_map={'Agendado':'#2ecc71', 'Pendente':'#f1c40f', 'Follow-up':'#e91e63', 'Em tratamento':'#3498db'})
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white", showlegend=True)
            st.plotly_chart(fig, use_container_width=True)

    # --- ABA: GESTÃO ---
    elif st.session_state['menu'] == "Gestao":
        st.markdown("<h1 class='gradient-text'>GESTÃO</h1>", unsafe_allow_html=True)
        busca = st.text_input("BUSCAR POR NOME OU CPF")
        
        df_f = df
        if busca:
            df_f = df[df['Nome'].str.contains(busca, case=False) | df['CPF'].str.contains(busca)]

        for idx, row in df_f.iterrows():
            status_class = "tag-followup" if row['Status'] == "Follow-up" else \
                           "tag-agendado" if row['Status'] == "Agendado" else \
                           "tag-pendente" if row['Status'] == "Pendente" else "tag-tratamento"
            
            with st.container():
                st.markdown(f"""
                    <div class="glass-card">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span style="font-size:18px; font-weight:800;">{row['Nome'].upper()}</span>
                            <span class="{status_class}">{row['Status'].
