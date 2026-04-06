import streamlit as st
import pandas as pd
from datetime import datetime
import os
import plotly.express as px

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="OrthoKlin Pro | Gestão", layout="wide")

# --- CSS PREMIUM (3D, ELEGÂNCIA & DEGRADÊ) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap');

    .stApp {
        background: radial-gradient(circle at top right, #1a0826, #0a0a0c);
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }

    /* TÍTULOS COM BRILHO MAGENTA */
    .titulo-premium {
        background: linear-gradient(90deg, #ffffff 0%, #e91e63 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.5rem;
        margin-bottom: 10px;
    }

    /* CARDS 3D GLASSMORPISM */
    .lead-card {
        background: rgba(255, 255, 255, 0.03);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
        margin-bottom: 20px;
        transition: 0.4s ease;
    }
    .lead-card:hover {
        transform: translateY(-5px);
        border: 1px solid #e91e63;
        background: rgba(255, 255, 255, 0.05);
    }

    /* BOTÕES COM DEGRADÊ E SOMBRA NEON */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #8e44ad 0%, #e91e63 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        height: 50px !important;
        font-weight: 700 !important;
        box-shadow: 0 8px 20px rgba(233, 30, 99, 0.3) !important;
    }
    div.stButton > button:hover {
        box-shadow: 0 12px 30px rgba(233, 30, 99, 0.6) !important;
        transform: scale(1.02);
    }

    /* BADGE DE STATUS */
    .badge-3d {
        padding: 6px 18px;
        border-radius: 30px;
        font-size: 10px;
        font-weight: 900;
        text-transform: uppercase;
        color: white;
    }

    /* SIDEBAR */
    [data-testid="stSidebar"] {
        background: rgba(10, 10, 12, 0.9) !important;
        backdrop-filter: blur(15px);
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES DE DADOS ---
FILE = 'leads_orthoklin.csv'
def load_data():
    if os.path.exists(FILE):
        df = pd.read_csv(FILE)
        df['Data Criação'] = pd.to_datetime(df['Data Criação']).dt.date
        df['Data Agendamento'] = pd.to_datetime(df['Data Agendamento']).dt.date
        return df
    return pd.DataFrame(columns=['Nome', 'CPF', 'Telefone', 'Origem', 'Status', 'Data Criação', 'Data Agendamento', 'Valor'])

# --- LOGIN ---
if 'logado' not in st.session_state: 
    st.session_state['logado'] = False

if not st.session_state['logado']:
    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        st.write("#")
        if os.path.exists("logo.png"): st.image("logo.png")
        st.markdown('<p class="titulo-premium">Acesso Geral</p>', unsafe_allow_html=True)
        user = st.text_input("💎 Utilizador")
        pw = st.text_input("🔑 Senha", type="password")
        if st.button("DESBLOQUEAR SISTEMA"):
            if user == "admin" and pw == "ortho2026":
                st.session_state['logado'] = True
                st.rerun()
            else: 
                st.error("Acesso Negado")
else:
    df = load_data()
    
    # --- SIDEBAR ---
    with st.sidebar:
        if os.path.exists("logo.png"): st.image("logo.png")
        st.write("---")
        menu = st.radio("SISTEMA", ["💎 Dashboard", "📂 Pacientes", "✨ Novo Registro"])
        st.write("---")
        st.metric("FATURAMENTO TOTAL", f"R$ {df['Valor'].sum():,.2f}")
        if st.button("🚀 SAIR DO SISTEMA"):
            st.session_state['logado'] = False
            st.rerun()

    # --- DASHBOARD ---
    if menu == "💎 Dashboard":
        st.markdown('<p class="titulo-premium">Performance Vital</p>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        if not df.empty:
            fig1 = px.pie(df, names='Origem', hole=.6, title="Canais de Aquisição",
                         color_discrete_sequence=['#8e44ad', '#e91e63', '#6c5ce7'])
            fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white")
            c1.plotly_chart(fig1, use_container_width=True)

            status_sum = df.groupby('Status')['Valor'].sum().reset_index()
            fig2 = px.bar(status_sum, x='Status', y='Valor', title="Volume Financeiro (R$)",
                         color='Status', color_discrete_map={'Pendente':'#f39c12', 'Agendado':'#3498db', 'Em tratamento':'#27ae60'})
            fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
            c2.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("Nenhum dado para exibir no momento.")

    # --- LISTA DE PACIENTES ---
    elif menu == "📂 Pacientes":
        st.markdown('<p class="titulo-premium">Base de Dados</p>', unsafe_allow_html=True)
        busca = st.text_input("🔎 Pesquisar por Nome ou CPF")
        
        df_f = df
        if busca: 
            df_f = df[df['Nome'].str.contains(busca, case=False) | df['CPF'].astype(str).str.contains(busca)]

        for idx, row in df_f.iterrows():
            cor_status = "#f39c12" if row['Status'] == "Pendente" else "#3498db" if row['Status'] == "Agendado" else "#27ae60"
            st.markdown(f"""
                <div class="lead-card">
                    <div style="display: flex; justify-content: space-between;">
                        <span style="font-size: 24px; font-weight: 700; color: #fff;">{row['Nome']}</span>
                        <span class="badge-3d" style="background-color: {cor_status};">{row['Status']}</span>
                    </div>
                    <div style="margin-top: 15px; color: #ccc; font-size: 15px;">
                        📍 {row['Origem']} | 📞 {row['Telefone']} | <b style="color:#e91e63; font-size: 20px;">R$ {row['Valor']:,.2f}</b>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            c1, c2, _ = st.columns([1,1,3])
            c1.markdown(f"[💬 **WhatsApp**](https://api.whatsapp.com/send?phone={row['Telefone']})")
            if c2.button("🗑️ Remover", key=f"del_{idx}"):
                df.drop(idx).to_csv(FILE, index=False)
                st.rerun()

    # --- NOVO REGISTRO ---
    elif menu == "✨ Novo Registro":
        st.markdown('<p class="titulo-premium">Novo Paciente</p>', unsafe_allow_html=True)
        with st.form("form_add"):
            nome = st.text_input("Nome Completo")
            c1, c2 = st.columns(2)
            cpf = c1.text_input("CPF")
            tel = c2.text_input("WhatsApp (ex: 55...)")
            origem = st.selectbox("Origem", ["Instagram", "Google", "Facebook", "Indicação"])
            status = st.selectbox("Status", ["Pendente", "Em tratamento", "Agendado"])
            valor = st.number_input("Valor R$", min_value=0.0)
            data_ag = st.date_input("Agendamento")
            
            if st.form_submit_button("💎 FINALIZAR REGISTRO"):
                novo_lead = {'Nome': nome, 'CPF': cpf, 'Telefone': tel, 'Origem': origem, 'Status': status, 
                             'Data Criação': datetime.now().date(), 'Data Agendamento': data_ag, 'Valor': valor}
                pd.concat([df, pd.DataFrame([novo_lead])], ignore_index=True).to_csv(FILE, index=False)
                st.success("Paciente registrado com sucesso!")
                st.rerun()
