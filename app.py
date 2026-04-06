import streamlit as st
import pandas as pd
from datetime import datetime
import os
import plotly.express as px

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="OrthoKlin | Gestão Pro", layout="wide")

# --- CSS SOFISTICADO ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    
    .stApp { background: #0f0f12; color: #ffffff; font-family: 'Inter', sans-serif; }

    /* TEXTO DEGRADÊ */
    .gradient-text {
        background: linear-gradient(90deg, #8e44ad, #e91e63);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-weight: 800; font-size: 2.2rem;
    }

    /* HEADER DE MÉTRICAS NO TOPO */
    .metric-card-top {
        background: rgba(255, 255, 255, 0.05);
        padding: 15px 25px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
    }

    /* BOTÕES */
    div.stButton > button {
        background: linear-gradient(90deg, #8e44ad 0%, #e91e63 100%) !important;
        color: white !important; border: none !important; border-radius: 8px !important;
        font-weight: 600 !important; transition: 0.3s;
    }
    
    /* CARD PACIENTE */
    .lead-card {
        background: rgba(255, 255, 255, 0.02);
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #e91e63;
        margin-bottom: 15px;
    }

    /* ESTILO SIDEBAR */
    [data-testid="stSidebar"] { background-color: #050505 !important; border-right: 1px solid #222; }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE DADOS ---
LEADS_FILE = 'leads_orthoklin.csv'
USERS_FILE = 'usuarios_ortho.csv'

def load_data():
    if os.path.exists(LEADS_FILE):
        df = pd.read_csv(LEADS_FILE)
        df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce').fillna(0.0)
        return df
    return pd.DataFrame(columns=['Nome','CPF','Telefone','Origem','Status','Valor'])

def save_data(df):
    df.to_csv(LEADS_FILE, index=False)

# --- GESTÃO DE ACESSO ---
if 'logado' not in st.session_state: st.session_state['logado'] = False

if not st.session_state['logado']:
    # [Mantém a lógica de login anterior para poupar espaço]
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.write("#")
        if os.path.exists("logo.png"): st.image("logo.png")
        st.markdown('<p class="gradient-text" style="text-align:center">Acesso Geral</p>', unsafe_allow_html=True)
        u = st.text_input("Utilizador")
        p = st.text_input("Senha", type="password")
        if st.button("ACESSAR SISTEMA"):
            if u == "admin" and p == "ortho2026": # Simplificado para teste
                st.session_state['logado'] = True
                st.rerun()
else:
    df = load_data()
    
    # --- BARRA LATERAL (SOFISTICADA) ---
    with st.sidebar:
        if os.path.exists("logo.png"): st.image("logo.png")
        st.write("### 💎 Navegação")
        menu = st.radio("", ["📊 Dashboard Real", "👥 Gestão de Pacientes", "➕ Novo Cadastro"])
        st.write("---")
        st.write("🔐 Sessão Ativa: Admin")
        if st.button("ENCERRAR SESSÃO"):
            st.session_state['logado'] = False
            st.rerun()

    # --- ABA: GESTÃO DE PACIENTES (COM HEADER FINANCEIRO) ---
    if menu == "👥 Gestão de Pacientes":
        # HEADER DE FATURAMENTO NO TOPO
        val_pendente = df[df['Status'] == 'Pendente']['Valor'].sum()
        val_total = df['Valor'].sum()
        
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="metric-card-top"><small>ORÇAMENTOS PENDENTES</small><br><b style="color:#f39c12; font-size:1.5rem">R$ {val_pendente:,.2f}</b></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="metric-card-top"><small>FATURAMENTO GERAL</small><br><b style="color:#e91e63; font-size:1.5rem">R$ {val_total:,.2f}</b></div>', unsafe_allow_html=True)
        with c3: 
            if st.button("➕ NOVO PACIENTE"): 
                # Função rápida para saltar para cadastro se quiseres, ou abrir modal
                st.info("Usa a aba 'Novo Cadastro' no menu lateral")

        st.write("---")
        busca = st.text_input("🔍 Localizar por Nome ou CPF")
        
        df_f = df
        if busca: df_f = df[df['Nome'].str.contains(busca, case=False) | df['CPF'].astype(str).str.contains(busca)]

        for idx, row in df_f.iterrows():
            with st.container():
                st.markdown(f"""
                    <div class="lead-card">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span style="font-size:20px; font-weight:600;">{row['Nome']}</span>
                            <span style="background:#e91e63; padding:3px 10px; border-radius:5px; font-size:10px; font-weight:bold;">{row['Status']}</span>
                        </div>
                        <div style="color:#888; margin-top:8px; font-size:14px;">
                            <b>💰 R$ {row['Valor']:,.2f}</b> | 📱 {row['Telefone']} | 📂 {row['Origem']}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # BOTÕES DE AÇÃO
                b1, b2, b3, _ = st.columns([1, 1, 1, 4])
                if b1.button("✏️ Editar", key=f"edit_{idx}"):
                    st.session_state['edit_idx'] = idx
                if b2.button("🗑️ Apagar", key=f"del_{idx}"):
                    df = df.drop(idx)
                    save_data(df)
                    st.rerun()
                b3.markdown(f"[💬 Whats](https://api.whatsapp.com/send?phone={row['Telefone']})")

                # FORMULÁRIO DE EDIÇÃO (Aparece apenas se clicar em editar)
                if 'edit_idx' in st.session_state and st.session_state['edit_idx'] == idx:
                    with st.form(f"form_edit_{idx}"):
                        st.write(f"Editando: {row['Nome']}")
                        new_status = st.selectbox("Status", ["Pendente", "Em tratamento", "Agendado"], index=["Pendente", "Em tratamento", "Agendado"].index(row['Status']))
                        new_valor = st.number_input("Valor R$", value=float(row['Valor']))
                        if st.form_submit_button("Salvar Alterações"):
                            df.at[idx, 'Status'] = new_status
                            df.at[idx, 'Valor'] = new_valor
                            save_data(df)
                            del st.session_state['edit_idx']
                            st.rerun()

    # --- ABA: DASHBOARD ---
    elif menu == "📊 Dashboard Real":
        st.markdown('<p class="gradient-text">Análise de Performance</p>', unsafe_allow_html=True)
        if not df.empty:
            c1, c2 = st.columns(2)
            fig1 = px.pie(df, names='Status', hole=.6, color_discrete_sequence=['#8e44ad', '#e91e63', '#2ecc71'])
            c1.plotly_chart(fig1, use_container_width=True)
            
            fig2 = px.bar(df, x='Origem', y='Valor', color='Origem', title="Receita por Canal")
            fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
            c2.plotly_chart(fig2, use_container_width=True)

    # --- ABA: NOVO CADASTRO ---
    elif menu == "➕ Novo Cadastro":
        st.markdown('<p class="gradient-text">Novo Paciente</p>', unsafe_allow_html=True)
        with st.form("cadastro_pro"):
            nome = st.text_input("Nome Completo")
            c1, c2 = st.columns(2)
            cpf = c1.text_input("CPF")
            tel = c2.text_input("WhatsApp")
            orig = st.selectbox("Origem", ["Instagram", "Google", "Indicação", "Facebook"])
            stat = st.selectbox("Status", ["Pendente", "Em tratamento", "Agendado"])
            val = st.number_input("Valor do Orçamento R$", min_value=0.0)
            if st.form_submit_button("SALVAR REGISTRO 💎"):
                novo = {'Nome': nome, 'CPF': cpf, 'Telefone': tel, 'Origem': orig, 'Status': stat, 'Valor': val}
                df = pd.concat([df, pd.DataFrame([novo])], ignore_index=True)
                save_data(df)
                st.success("Paciente registado com sucesso!")
