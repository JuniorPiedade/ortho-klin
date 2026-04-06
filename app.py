import streamlit as st
import pandas as pd
from datetime import datetime
import os
import plotly.express as px

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="OrthoKlin | Sistema", layout="wide")

# --- CSS MINIMALISTA DE LUXO ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap');
    
    .stApp { 
        background: radial-gradient(circle at center, #1b0c26 0%, #0a0a0c 100%); 
        color: #ffffff; 
        font-family: 'Inter', sans-serif; 
    }

    /* TÍTULO EM DEGRADÊ */
    .gradient-text {
        background: linear-gradient(90deg, #8e44ad, #e91e63);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3rem;
        text-align: center;
        margin-bottom: 30px;
    }

    /* BOTÕES EXCLUSIVOS (DEGRADÊ) */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #8e44ad 0%, #e91e63 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        height: 50px !important;
        width: 100% !important;
        font-weight: 700 !important;
        letter-spacing: 1px;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        opacity: 0.9;
        transform: translateY(-2px);
    }

    /* CARD DE PACIENTE */
    .lead-card {
        background: rgba(255, 255, 255, 0.03);
        padding: 25px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }
    
    .status-tag {
        padding: 4px 12px;
        border-radius: 4px;
        font-size: 10px;
        font-weight: bold;
        text-transform: uppercase;
    }

    /* SIDEBAR */
    [data-testid="stSidebar"] {
        background: rgba(0, 0, 0, 0.5) !important;
        backdrop-filter: blur(10px);
    }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE DADOS ---
LEADS_FILE = 'leads_orthoklin.csv'
USERS_FILE = 'usuarios_ortho.csv'

def load_users():
    if os.path.exists(USERS_FILE): return pd.read_csv(USERS_FILE)
    return pd.DataFrame([["admin", "ortho2026"]], columns=['usuario', 'senha'])

# --- GESTÃO DE ESTADO ---
if 'logado' not in st.session_state: st.session_state['logado'] = False
if 'tela' not in st.session_state: st.session_state['tela'] = 'login'

# --- TELA DE ACESSO ---
if not st.session_state['logado']:
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.write("#")
        # Tentativa de carregar a logo (PNG ou JPG)
        if os.path.exists("logo.png"): st.image("logo.png")
        elif os.path.exists("logo.jpg"): st.image("logo.jpg")
        
        st.markdown('<p class="gradient-text">Acesso Geral</p>', unsafe_allow_html=True)
        
        if st.session_state['tela'] == 'login':
            u = st.text_input("Utilizador")
            p = st.text_input("Senha", type="password")
            
            if st.button("ACESSAR"):
                df_u = load_users()
                if ((df_u['usuario'] == u) & (df_u['senha'] == p)).any():
                    st.session_state['logado'] = True
                    st.rerun()
                else: st.error("Incorreto.")
            
            st.write("---")
            if st.button("CRIAR PRIMEIRO ACESSO"):
                st.session_state['tela'] = 'registro'
                st.rerun()

        else: # REGISTRO
            st.subheader("Novo Cadastro")
            new_u = st.text_input("Novo Usuário")
            new_p = st.text_input("Nova Senha", type="password")
            if st.button("CONFIRMAR CADASTRO"):
                df_u = load_users()
                new_row = pd.DataFrame([[new_u, new_p]], columns=['usuario', 'senha'])
                pd.concat([df_u, new_row]).to_csv(USERS_FILE, index=False)
                st.success("Pronto!")
                st.session_state['tela'] = 'login'
                st.rerun()
            if st.button("VOLTAR"):
                st.session_state['tela'] = 'login'
                st.rerun()

# --- DASHBOARD ATIVO ---
else:
    df = pd.read_csv(LEADS_FILE) if os.path.exists(LEADS_FILE) else pd.DataFrame(columns=['Nome','CPF','Telefone','Origem','Status','Valor'])
    
    with st.sidebar:
        if os.path.exists("logo.png"): st.image("logo.png")
        elif os.path.exists("logo.jpg"): st.image("logo.jpg")
        st.write("#")
        menu = st.radio("Menu", ["Dashboard", "Pacientes", "Cadastro"])
        st.write("---")
        if st.button("SAIR"):
            st.session_state['logado'] = False
            st.rerun()

    if menu == "Dashboard":
        st.markdown('<p class="gradient-text" style="text-align:left; font-size:2rem;">Performance</p>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        if not df.empty:
            fig1 = px.pie(df, names='Origem', hole=.6, color_discrete_sequence=['#8e44ad', '#e91e63'])
            fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white")
            c1.plotly_chart(fig1, use_container_width=True)
            
            fig2 = px.bar(df.groupby('Status')['Valor'].sum().reset_index(), x='Status', y='Valor', color='Status', color_discrete_map={'Pendente':'#8e44ad', 'Agendado':'#e91e63'})
            fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
            c2.plotly_chart(fig2, use_container_width=True)

    elif menu == "Pacientes":
        st.markdown('<p class="gradient-text" style="text-align:left; font-size:2rem;">Base de Dados</p>', unsafe_allow_html=True)
        busca = st.text_input("Pesquisar Nome ou CPF")
        
        df_f = df
        if busca: df_f = df[df['Nome'].str.contains(busca, case=False) | df['CPF'].astype(str).str.contains(busca)]

        for idx, row in df_f.iterrows():
            st.markdown(f"""
                <div class="lead-card">
                    <div style="display:flex; justify-content:space-between;">
                        <span style="font-size:20px; font-weight:700;">{row['Nome']}</span>
                        <span class="status-tag" style="background:#e91e63;">{row['Status']}</span>
                    </div>
                    <div style="color:#aaa; margin-top:10px;">
                        R$ {row['Valor']:,.2f} | {row['Telefone']} | {row['Origem']}
                    </div>
                </div>
            """, unsafe_allow_html=True)

    elif menu == "Cadastro":
        st.markdown('<p class="gradient-text" style="text-align:left; font-size:2rem;">Novo Paciente</p>', unsafe_allow_html=True)
        with st.form("paciente"):
            n = st.text_input("Nome")
            c1, c2 = st.columns(2)
            cp = c1.text_input("CPF")
            tl = c2.text_input("WhatsApp")
            origem = st.selectbox("Origem", ["Instagram", "Google", "Facebook", "Indicação"])
            status = st.selectbox("Status", ["Pendente", "Em tratamento", "Agendado"])
            vl = st.number_input("Valor R$", min_value=0.0)
            if st.form_submit_button("SALVAR REGISTRO"):
                novo = {'Nome':n, 'CPF':cp, 'Telefone':tl, 'Origem':origem, 'Status':status, 'Valor':vl}
                df = pd.concat([df, pd.DataFrame([novo])], ignore_index=True)
                df.to_csv(LEADS_FILE, index=False)
                st.success("Salvo!")
                st.rerun()
