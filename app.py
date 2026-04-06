import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
import plotly.express as px

# --- CONFIGURAÇÃO VISUAL PREMIUM ORTHOKLIN ---
st.set_page_config(page_title="OrthoKlin Pro - CRM", layout="wide")

# CSS Avançado para Forçar o Degradê e Identidade Visual
st.markdown("""
    <style>
    /* Fundo Geral */
    .main { background-color: #fcfcfc; }
    
    /* BOTÕES COM DEGRADÊ REAL (Roxo -> Rosa) */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #8e44ad 0%, #e91e63 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 0.6rem 2rem !important;
        font-weight: bold !important;
        box-shadow: 0 4px 15px rgba(142, 68, 173, 0.3) !important;
        text-transform: uppercase;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(233, 30, 99, 0.4) !important;
    }

    /* CARD DE LEAD COM BORDA EM DEGRADÊ */
    .lead-card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 20px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        border-left: 8px solid;
        border-image: linear-gradient(to bottom, #8e44ad, #e91e63) 1 100%;
    }

    /* Ajuste de Cor nos Textos e Ícones */
    .stMetric label { color: #8e44ad !important; font-weight: bold !important; }
    h1, h2, h3 { color: #2c3e50; font-family: 'Arial', sans-serif; }
    
    /* Badges de Status */
    .status-badge {
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 800;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES DE DADOS ---
LEADS_FILE = 'leads_orthoklin.csv'

def load_leads():
    if os.path.exists(LEADS_FILE):
        df = pd.read_csv(LEADS_FILE)
        df['Data Criação'] = pd.to_datetime(df['Data Criação']).dt.date
        df['Data Agendamento'] = pd.to_datetime(df['Data Agendamento']).dt.date
        return df
    return pd.DataFrame(columns=['Nome', 'CPF', 'Telefone', 'Origem', 'Status', 'Data Criação', 'Data Agendamento', 'Valor'])

# --- APP ---
df = load_leads()

# Sidebar
with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_column_width=True)
    else:
        st.title("OrthoKlin")
    
    st.markdown("---")
    aba = st.radio("Navegação", ["📊 Dashboard", "📝 Lista de Leads", "➕ Novo Paciente"])
    
    st.markdown("---")
    total = df['Valor'].sum()
    st.metric("Total em Orçamentos", f"R$ {total:,.2f}")

# 1. ABA DASHBOARD
if aba == "📊 Dashboard":
    st.header("Análise OrthoKlin")
    c1, c2 = st.columns(2)
    
    if not df.empty:
        # Gráfico Donut (Origem)
        fig1 = px.pie(df, names='Origem', hole=.4, title="Origem dos Pacientes",
                     color_discrete_sequence=['#8e44ad', '#e91e63', '#3498db'])
        c1.plotly_chart(fig1, use_container_width=True)
        
        # Gráfico Barras (Valor por Status)
        status_val = df.groupby('Status')['Valor'].sum().reset_index()
        fig2 = px.bar(status_val, x='Status', y='Valor', title="Valores por Status (R$)",
                     color='Status', color_discrete_map={'Pendente':'#f39c12', 'Agendado':'#3498db', 'Em tratamento':'#27ae60'})
        c2.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Cadastre o primeiro lead para ver os gráficos!")

# 2. ABA LISTA DE LEADS
elif aba == "📝 Lista de Leads":
    st.header("Gerenciamento de Pacientes")
    busca = st.text_input("🔍 Buscar por Nome ou CPF")
    
    df_f = df
    if busca:
        df_f = df[df['Nome'].str.contains(busca, case=False) | df['CPF'].astype(str).str.contains(busca)]

    for idx, row in df_f.iterrows():
        cor = "#f39c12" if row['Status'] == "Pendente" else "#3498db" if row['Status'] == "Agendado" else "#27ae60"
        
        st.markdown(f"""
            <div class="lead-card">
                <div style="display: flex; justify-content: space-between;">
                    <span style="font-size: 20px; font-weight: bold;">{row['Nome']}</span>
                    <span class="status-badge" style="background-color: {cor};">{row['Status']}</span>
                </div>
                <div style="margin-top: 10px; color: #555;">
                    <b>📱 WhatsApp:</b> {row['Telefone']} | <b>📂 Origem:</b> {row['Origem']} | <b style="color:#e91e63;">💰 R$ {row['Valor']:,.2f}</b>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        c1, c2, _ = st.columns([1, 1, 4])
        wa_url = f"https://api.whatsapp.com/send?phone={row['Telefone']}"
        c1.markdown(f"[💬 WhatsApp]({wa_url})")
        if c2.button("🗑️ Excluir", key=f"del_{idx}"):
            df = df.drop(idx)
            df.to_csv(LEADS_FILE, index=False)
            st.rerun()

# 3. ABA NOVO PACIENTE
elif aba == "➕ Novo Paciente":
    st.header("Novo Cadastro")
    with st.form("add"):
        nome = st.text_input("Nome")
        c1, c2 = st.columns(2)
        cpf = c1.text_input("CPF")
        tel = c2.text_input("WhatsApp")
        origem = st.selectbox("Origem", ["Instagram", "Google", "Facebook", "Indicação"])
        status = st.selectbox("Status", ["Pendente", "Em tratamento", "Agendado"])
        valor = st.number_input("Valor (R$)", min_value=0.0)
        data = st.date_input("Data de Agendamento")
        
        if st.form_submit_button("Salvar Paciente"):
            novo = {'Nome': nome, 'CPF': cpf, 'Telefone': tel, 'Origem': origem, 'Status': status, 
                    'Data Criação': datetime.now().date(), 'Data Agendamento': data, 'Valor': valor}
            df = pd.concat([df, pd.DataFrame([novo])], ignore_index=True)
            df.to_csv(LEADS_FILE, index=False)
            st.success("Salvo com sucesso!")
            st.rerun()
