import streamlit as st
import pandas as pd
from datetime import datetime
import os
import plotly.express as px

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="OrthoKlin | Gestão", layout="wide")

# --- CSS MINIMALISTA PREMIUM ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    
    .stApp { background: #0a0a0c; color: #ffffff; font-family: 'Inter', sans-serif; }

    /* TEXTO DEGRADÊ */
    .gradient-text {
        background: linear-gradient(90deg, #8e44ad, #e91e63);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-weight: 800; font-size: 2.2rem;
    }

    /* BOTÕES DO MENU LATERAL (DEGRADÊ) */
    .stSidebar [data-testid="stWidgetLabel"] { display: none; } /* Esconde label do radio */
    
    div.stButton > button {
        background: linear-gradient(90deg, #8e44ad 0%, #e91e63 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 12px !important;
        width: 100% !important;
        height: 45px !important;
        transition: 0.3s;
    }
    div.stButton > button:hover { opacity: 0.85; transform: translateY(-1px); }

    /* BOTÃO WHATSAPP ESPECÍFICO */
    .btn-whatsapp {
        display: inline-block;
        background: #25d366;
        color: white !important;
        padding: 10px 20px;
        border-radius: 6px;
        text-decoration: none;
        font-weight: 700;
        font-size: 12px;
        text-align: center;
        width: 100%;
    }

    /* CARD PACIENTE */
    .lead-card {
        background: rgba(255, 255, 255, 0.03);
        padding: 25px;
        border-radius: 10px;
        border-left: 4px solid #e91e63;
        margin-bottom: 20px;
    }

    .metric-top {
        background: rgba(255, 255, 255, 0.02);
        padding: 20px;
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
    }

    [data-testid="stSidebar"] { background-color: #000000 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE DADOS ---
LEADS_FILE = 'leads_orthoklin.csv'

def load_data():
    if os.path.exists(LEADS_FILE):
        df = pd.read_csv(LEADS_FILE)
        df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce').fillna(0.0)
        return df
    return pd.DataFrame(columns=['Nome','CPF','Telefone','Origem','Status','Valor'])

# --- GESTÃO DE ACESSO ---
if 'logado' not in st.session_state: st.session_state['logado'] = False

if not st.session_state['logado']:
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.write("#")
        if os.path.exists("logo.png"): st.image("logo.png")
        st.markdown('<p class="gradient-text" style="text-align:center">ACESSO GERAL</p>', unsafe_allow_html=True)
        u = st.text_input("UTILIZADOR")
        p = st.text_input("SENHA", type="password")
        if st.button("ACESSAR"):
            if u == "admin" and p == "ortho2026":
                st.session_state['logado'] = True
                st.rerun()
else:
    df = load_data()
    
    # --- SIDEBAR (BOTÕES DEGRADÊ) ---
    with st.sidebar:
        if os.path.exists("logo.png"): st.image("logo.png")
        st.write("---")
        
        # Simulando botões de menu com botões reais para ter o degradê individual
        if st.button("DASHBOARD REAL"): st.session_state['menu'] = "dash"
        if st.button("GESTAO FINANCEIRA"): st.session_state['menu'] = "pacientes"
        if st.button("NOVO PACIENTE"): st.session_state['menu'] = "novo"
        
        if 'menu' not in st.session_state: st.session_state['menu'] = "dash"
        
        st.write("---")
        if st.button("SAIR"):
            st.session_state['logado'] = False
            st.rerun()

    # --- ABA: GESTÃO (COM HEADER FINANCEIRO) ---
    if st.session_state['menu'] == "pacientes":
        val_pendente = df[df['Status'] == 'Pendente']['Valor'].sum()
        val_total = df['Valor'].sum()
        
        c1, c2 = st.columns(2)
        with c1: st.markdown(f'<div class="metric-top"><small>ORÇAMENTOS PENDENTES</small><br><b style="color:#f39c12; font-size:1.8rem">R$ {val_pendente:,.2f}</b></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="metric-top"><small>FATURAMENTO GERAL</small><br><b style="color:#e91e63; font-size:1.8rem">R$ {val_total:,.2f}</b></div>', unsafe_allow_html=True)

        st.write("---")
        busca = st.text_input("BUSCAR POR NOME OU CPF")
        
        df_f = df
        if busca: df_f = df[df['Nome'].str.contains(busca, case=False) | df['CPF'].astype(str).str.contains(busca)]

        for idx, row in df_f.iterrows():
            st.markdown(f"""
                <div class="lead-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-size:20px; font-weight:700;">{row['Nome'].upper()}</span>
                        <span style="color:#e91e63; font-weight:bold; font-size:12px;">{row['Status'].upper()}</span>
                    </div>
                    <div style="color:#666; margin-top:10px; font-size:13px; letter-spacing:1px;">
                        VALOR: R$ {row['Valor']:,.2f} | CPF: {row['CPF']} | ORIGEM: {row['Origem'].upper()}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # AÇÕES
            col_wa, col_ed, col_rm, _ = st.columns([2, 1, 1, 3])
            
            wa_link = f"https://api.whatsapp.com/send?phone={row['Telefone']}"
            col_wa.markdown(f'<a href="{wa_link}" target="_blank" class="btn-whatsapp">ENTRAR EM CONTATO</a>', unsafe_allow_html=True)
            
            if col_ed.button("EDITAR", key=f"ed_{idx}"):
                st.session_state['edit_idx'] = idx
            
            if col_rm.button("REMOVER", key=f"rm_{idx}"):
                df.drop(idx).to_csv(LEADS_FILE, index=False)
                st.rerun()

            if 'edit_idx' in st.session_state and st.session_state['edit_idx'] == idx:
                with st.form(f"f_ed_{idx}"):
                    nv = st.number_input("NOVO VALOR R$", value=float(row['Valor']))
                    ns = st.selectbox("STATUS", ["Pendente", "Em tratamento", "Agendado"])
                    if st.form_submit_button("CONFIRMAR"):
                        df.at[idx, 'Valor'] = nv
                        df.at[idx, 'Status'] = ns
                        df.to_csv(LEADS_FILE, index=False)
                        del st.session_state['edit_idx']
                        st.rerun()

    # --- ABA: DASHBOARD ---
    elif st.session_state['menu'] == "dash":
        st.markdown('<p class="gradient-text">PERFORMANCE</p>', unsafe_allow_html=True)
        if not df.empty:
            c1, c2 = st.columns(2)
            fig1 = px.pie(df, names='Status', hole=.7, color_discrete_sequence=['#8e44ad', '#e91e63'])
            fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white", showlegend=False)
            c1.plotly_chart(fig1, use_container_width=True)
            
            fig2 = px.bar(df.groupby('Origem')['Valor'].sum().reset_index(), x='Origem', y='Valor')
            fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
            c2.plotly_chart(fig2, use_container_width=True)

    # --- ABA: NOVO ---
    elif st.session_state['menu'] == "novo":
        st.markdown('<p class="gradient-text">NOVO PACIENTE</p>', unsafe_allow_html=True)
        with st.form("cad"):
            nome = st.text_input("NOME COMPLETO")
            c1, c2 = st.columns(2)
            cpf = c1.text_input("CPF")
            tel = c2.text_input("WHATSAPP")
            origem = st.selectbox("ORIGEM", ["Instagram", "Google", "Indicação", "Facebook"])
            status = st.selectbox("STATUS", ["Pendente", "Em tratamento", "Agendado"])
            valor = st.number_input("VALOR DO ORÇAMENTO R$", min_value=0.0)
            if st.form_submit_button("SALVAR PACIENTE"):
                novo = {'Nome': nome, 'CPF': cpf, 'Telefone': tel, 'Origem': origem, 'Status': status, 'Valor': valor}
                df = pd.concat([df, pd.DataFrame([novo])], ignore_index=True)
                df.to_csv(LEADS_FILE, index=False)
                st.success("REGISTRADO")
