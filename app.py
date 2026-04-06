import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="OrthoKlin | Sistema de Inteligência", layout="wide")

# --- CSS FUTURISTA COM HEADER CENTRALIZADO ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;900&display=swap');
    
    /* Configuração Geral */
    .stApp { background: #050507; color: #ffffff; font-family: 'Inter', sans-serif; }
    
    /* Esconder Sidebar original do Streamlit para o novo design */
    [data-testid="stSidebar"] { display: none; }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }

    /* HEADER DE NAVEGAÇÃO CENTRALIZADO */
    .nav-container {
        display: flex;
        justify-content: center;
        gap: 20px;
        padding: 20px 0;
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(10px);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        position: sticky;
        top: 0;
        z-index: 999;
        margin-bottom: 40px;
    }

    /* ESTILO DAS TAGS DE STATUS */
    .tag-agendado { background: #2ecc71; color: #000; padding: 4px 12px; border-radius: 6px; font-weight: 800; font-size: 10px; }
    .tag-pendente { background: #f1c40f; color: #000; padding: 4px 12px; border-radius: 6px; font-weight: 800; font-size: 10px; }
    .tag-followup { background: #e91e63; color: #fff; padding: 4px 12px; border-radius: 6px; font-weight: 800; font-size: 10px; }
    .tag-tratamento { background: #3498db; color: #fff; padding: 4px 12px; border-radius: 6px; font-weight: 800; font-size: 10px; }

    /* CARDS E BOTÕES */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 25px;
        transition: 0.3s ease;
    }
    
    .gradient-text {
        background: linear-gradient(90deg, #a855f7, #e91e63);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-weight: 900;
    }

    /* Sobrescrevendo botões do Streamlit para o topo */
    div.stButton > button {
        background: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        padding: 10px 25px !important;
        font-weight: 600 !important;
        transition: 0.3s !important;
    }
    div.stButton > button:hover {
        background: linear-gradient(90deg, #8e44ad, #e91e63) !important;
        border: none !important;
        transform: translateY(-2px);
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

# --- ESTADO DA SESSÃO ---
if 'logado' not in st.session_state: st.session_state['logado'] = False
if 'aba_ativa' not in st.session_state: st.session_state['aba_ativa'] = "Dashboard"

# --- TELA DE ACESSO ---
if not st.session_state['logado']:
    _, col, _ = st.columns([1, 1, 1])
    with col:
        st.write("#")
        if os.path.exists("logo.png"): st.image("logo.png")
        st.markdown("<h1 class='gradient-text' style='text-align:center;'>CENTRAL DE COMANDO</h1>", unsafe_allow_html=True)
        u = st.text_input("UTILIZADOR")
        p = st.text_input("SENHA", type="password")
        if st.button("ACESSAR"):
            if u == "admin" and p == "ortho2026":
                st.session_state['logado'] = True
                st.rerun()
else:
    df = load_data()

    # --- HEADER CENTRALIZADO (MENU DE TOPO) ---
    _, nav_col, _ = st.columns([1, 4, 1])
    with nav_col:
        c1, c2, c3, c4 = st.columns(4)
        if c1.button("📊 DASHBOARD"): st.session_state['aba_ativa'] = "Dashboard"
        if c2.button("👥 GESTÃO"): st.session_state['aba_ativa'] = "Gestao"
        if c3.button("➕ REGISTRO"): st.session_state['aba_ativa'] = "Novo"
        if c4.button("🚪 SAIR"):
            st.session_state['logado'] = False
            st.rerun()
    st.markdown("---")

    # --- ABA: DASHBOARD ---
    if st.session_state['aba_ativa'] == "Dashboard":
        st.markdown("<h2 class='gradient-text'>DESEMPENHO DA CLÍNICA</h2>", unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        c1.markdown(f'<div class="glass-card"><small>TOTAL EM ORÇAMENTOS</small><br><b style="font-size:24px;">R$ {df["Valor"].sum():,.2f}</b></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="glass-card"><small>AGUARDANDO (PENDENTES)</small><br><b style="font-size:24px; color:#f1c40f;">R$ {df[df["Status"] == "Pendente"]["Valor"].sum():,.2f}</b></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="glass-card"><small>EM FOLLOW-UP</small><br><b style="font-size:24px; color:#e91e63;">{len(df[df["Status"] == "Follow-up"])} Leads</b></div>', unsafe_allow_html=True)

        st.write("#")
        if not df.empty:
            fig = px.pie(df, names='Status', hole=0.7, 
                         color='Status',
                         color_discrete_map={'Agendado':'#2ecc71', 'Pendente':'#f1c40f', 'Follow-up':'#e91e63', 'Em tratamento':'#3498db'})
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white", showlegend=True)
            st.plotly_chart(fig, use_container_width=True)

    # --- ABA: GESTÃO (COM TAGS COLORIDAS) ---
    elif st.session_state['aba_ativa'] == "Gestao":
        st.markdown("<h2 class='gradient-text'>BASE DE LEADS</h2>", unsafe_allow_html=True)
        busca = st.text_input("🔍 PESQUISAR POR NOME OU CPF")
        
        df_f = df
        if busca:
            df_f = df[df['Nome'].str.contains(busca, case=False) | df['CPF'].str.contains(busca)]

        for idx, row in df_f.iterrows():
            # Definir classe da tag baseada no status
            status_class = "tag-followup" if row['Status'] == "Follow-up" else \
                           "tag-agendado" if row['Status'] == "Agendado" else \
                           "tag-pendente" if row['Status'] == "Pendente" else "tag-tratamento"
            
            with st.container():
                st.markdown(f"""
                    <div class="glass-card" style="margin-bottom: 10px;">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span style="font-size:18px; font-weight:800;">{row['Nome'].upper()}</span>
                            <span class="{status_class}">{row['Status'].upper()}</span>
                        </div>
                        <div style="color:#666; font-size:12px; margin-top:5px;">
                            VALOR: R$ {row['Valor']:,.2f} | TELEFONE: {row['Telefone']} | CANAL: {row['Origem']}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                col_bt1, col_bt2, col_bt3, _ = st.columns([1, 1, 2, 4])
                if col_bt1.button("EDITAR", key=f"e_{idx}"): st.session_state['edit_idx'] = idx
                if col_bt2.button("APAGAR", key=f"d_{idx}"):
                    df = df.drop(idx)
                    save_data(df)
                    st.rerun()
