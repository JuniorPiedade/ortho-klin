import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

# --- CONFIGURAÇÃO VISUAL ORTHOKLIN ---
st.set_page_config(page_title="OrthoKlin - Gestão de Leads", layout="wide")

# CSS personalizado com a paleta de cores da sua logo
st.markdown("""
    <style>
    /* Fundo e Fonte */
    .main { background-color: #f8f9fa; }
    
    /* Botões com degradê da logo */
    .stButton>button { 
        width: 100%; 
        border-radius: 10px; 
        background: linear-gradient(90deg, #8e44ad 0%, #e91e63 100%); 
        color: white; 
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover { opacity: 0.8; color: white; }

    /* Cards de Leads */
    .lead-card {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        border-left: 8px solid #8e44ad;
    }
    
    .status-badge {
        padding: 5px 15px;
        border-radius: 50px;
        font-size: 11px;
        text-transform: uppercase;
        color: white;
        font-weight: bold;
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

# --- INTERFACE LOGADA ---
if 'logado' not in st.session_state: st.session_state['logado'] = True # Ativado para teste

df = load_leads()

# --- BARRA LATERAL COM LOGO ---
with st.sidebar:
    # Tenta carregar a logo se ela existir no GitHub
    if os.path.exists("logo.jpg"):
        st.image("logo.jpg", use_column_width=True)
    else:
        st.title("OrthoKlin")
        st.info("Dica: Sobe o ficheiro 'logo.jpg' para o GitHub para aparecer aqui!")
    
    st.divider()
    aba = st.radio("Menu", ["📊 Painel Geral", "➕ Novo Lead", "☎️ Follow-up"])
    
    st.divider()
    total = df['Valor'].sum()
    st.metric("Total em Orçamentos", f"€ {total:,.2f}")

# --- CONTEÚDO PRINCIPAL ---
if aba == "📊 Painel Geral":
    st.header("Gestão de Leads OrthoKlin")
    
    col_busca, col_filtro = st.columns([3, 1])
    busca = col_busca.text_input("🔍 Buscar por nome ou CPF...")
    status_sel = col_filtro.selectbox("Status", ["Todos", "Pendente", "Em tratamento", "Agendado"])

    # Filtros
    df_f = df
    if busca:
        df_f = df[df['Nome'].str.contains(busca, case=False) | df['CPF'].str.contains(busca)]
    if status_sel != "Todos":
        df_f = df_f[df_f['Status'] == status_sel]

    # Lista de Cards
    for idx, row in df_f.iterrows():
        # Lógica de cores
        cor_status = "#f39c12" if row['Status'] == "Pendente" else "#3498db" if row['Status'] == "Agendado" else "#27ae60"
        
        st.markdown(f"""
            <div class="lead-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-size: 20px; font-weight: bold; color: #2c3e50;">{row['Nome']}</span>
                    <span class="status-badge" style="background-color: {cor_status};">{row['Status']}</span>
                </div>
                <div style="margin-top: 15px; color: #7f8c8d; font-size: 14px;">
                    <b>📱 WhatsApp:</b> {row['Telefone']} | <b>📂 Origem:</b> {row['Origem']} | <b>💰 Valor:</b> € {row['Valor']}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Ações
        c1, c2, _ = st.columns([1, 1, 4])
        wa_link = f"https://api.whatsapp.com/send?phone={row['Telefone']}"
        c1.markdown(f"[**Chamar no Whats**]({wa_link})")
        if c2.button("🗑️ Apagar", key=f"btn_{idx}"):
            df = df.drop(idx)
            df.to_csv(LEADS_FILE, index=False)
            st.rerun()

elif aba == "➕ Novo Lead":
    st.header("Registrar Novo Orçamento")
    with st.form("form_ortho"):
        nome = st.text_input("Nome do Paciente")
        c1, c2 = st.columns(2)
        cpf = c1.text_input("CPF")
        tel = c2.text_input("WhatsApp (ex: 351...)")
        origem = st.selectbox("Origem", ["Instagram", "Google", "Indicação", "Facebook"])
        status = st.selectbox("Status Inicial", ["Pendente", "Em tratamento", "Agendado"])
        valor = st.number_input("Valor do Tratamento (€)", min_value=0.0)
        data_ag = st.date_input("Data de Agendamento")
        
        if st.form_submit_button("Guardar Paciente"):
            novo = {'Nome': nome, 'CPF': cpf, 'Telefone': tel, 'Origem': origem, 'Status': status, 
                    'Data Criação': datetime.now().date(), 'Data Agendamento': data_ag, 'Valor': valor}
            df = pd.concat([df, pd.DataFrame([novo])], ignore_index=True)
            df.to_csv(LEADS_FILE, index=False)
            st.success("Paciente registrado com sucesso!")
