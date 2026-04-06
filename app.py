import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
import plotly.express as px # Biblioteca para gráficos modernos

# --- CONFIGURAÇÃO VISUAL ULTRA-FUTURISTA (OrthoKlin) ---
st.set_page_config(page_title="OrthoKlin Pro - Gestão Futurista", layout="wide", initial_sidebar_state="expanded")

# CSS Avançado: Glassmorphism e Cores da Logo
st.markdown("""
    <style>
    /* Fundo Principal e Fontes */
    .main { background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%); font-family: 'Segoe UI', sans-serif; }
    
    /* Sidebar com Efeito Vidro (Glassmorphism) */
    .css-1d391kg { 
        background-color: rgba(255, 255, 255, 0.4) !important; 
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.18);
    }
    
    /* Botões Futuristas com degradê da logo */
    .stButton>button { 
        width: 100%; 
        border-radius: 50px; 
        background: linear-gradient(90deg, #8e44ad 0%, #e91e63 100%); 
        color: white; 
        font-weight: 600;
        text-transform: uppercase;
        border: none;
        box-shadow: 0 4px 15px rgba(233, 30, 99, 0.3);
        transition: all 0.3s ease;
    }
    .stButton>button:hover { box-shadow: 0 6px 20px rgba(233, 30, 99, 0.5); transform: translateY(-2px); color: white; }

    /* Cards de Leads Premium (Glassmorphism Light) */
    .lead-card {
        background: rgba(255, 255, 255, 0.7);
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
        backdrop-filter: blur(4px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        margin-bottom: 25px;
        transition: 0.3s;
    }
    .lead-card:hover { transform: translateY(-5px); box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.15); }
    
    /* Status Badge Colorida */
    .status-badge {
        padding: 6px 16px;
        border-radius: 50px;
        font-size: 10px;
        text-transform: uppercase;
        color: white;
        font-weight: 700;
        letter-spacing: 1px;
    }
    
    /* Metrificação na Sidebar */
    .stMetric { background-color: rgba(255, 255, 255, 0.5); padding: 15px; border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES DE DADOS (Persistência) ---
LEADS_FILE = 'leads_orthoklin.csv'

def load_leads():
    if os.path.exists(LEADS_FILE):
        df = pd.read_csv(LEADS_FILE)
        df['Data Criação'] = pd.to_datetime(df['Data Criação']).dt.date
        df['Data Agendamento'] = pd.to_datetime(df['Data Agendamento']).dt.date
        df['Valor'] = df['Valor'].fillna(0.0) # Tratar valores nulos
        return df
    return pd.DataFrame(columns=['Nome', 'CPF', 'Telefone', 'Origem', 'Status', 'Data Criação', 'Data Agendamento', 'Valor'])

# --- SISTEMA DE LOGIN (Simplificado para o exemplo) ---
if 'logado' not in st.session_state: st.session_state['logado'] = True

if not st.session_state['logado']:
    st.title("🔐 Acesso OrthoKlin Pro")
    # Lógica de login aqui (removida para teste rápido)
else:
    df = load_leads()
    
    # --- BARRA LATERAL FUTURISTA ---
    with st.sidebar:
        # Carregar a logo PNG transparente
        if os.path.exists("logo.png"):
            st.image("logo.png", use_column_width=True)
        else:
            st.title("OrthoKlin")
            st.warning("Dica: Sobe o ficheiro 'logo.png' (transparente) para o GitHub!")
        
        st.divider()
        aba = st.radio("Menu de Navegação", ["📊 Dashboard", "📝 Gestão de Leads", "➕ Cadastrar"])
        
        st.divider()
        total_valor = df['Valor'].sum()
        st.metric("Receita Potencial", f"€ {total_valor:,.2f}")
        st.divider()
        if st.button("Sair (Logout)"): st.session_state['logado'] = False; st.rerun()

    # --- CONTEÚDO PRINCIPAL ---
    
    # 1. ABA DASHBOARD (Gráficos)
    if aba == "📊 Dashboard":
        st.header("Dashboard Futurista OrthoKlin")
        
        # Gráfico 1: Origem dos Leads (Pizza Moderno)
        c1, c2 = st.columns(2)
        
        origem_counts = df['Origem'].value_counts().reset_index()
        origem_counts.columns = ['Origem', 'Quantidade']
        
        fig1 = px.pie(origem_counts, values='Quantidade', names='Origem', 
                     title='Distribuição por Origem',
                     hole=.4, # Gráfico Donut (mais moderno)
                     color_discrete_sequence=['#8e44ad', '#e91e63', '#3498db', '#27ae60'])
        fig1.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        c1.plotly_chart(fig1, use_container_width=True)
        
        # Gráfico 2: Valor por Status (Barras Moderno)
        status_valor = df.groupby('Status')['Valor'].sum().reset_index()
        fig2 = px.bar(status_valor, x='Status', y='Valor', 
                     title='Orçamentos por Status (€)',
                     color='Status',
                     color_discrete_map={'Pendente': '#f39c12', 'Agendado': '#3498db', 'Em tratamento': '#27ae60'})
        fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        c2.plotly_chart(fig2, use_container_width=True)

    # 2. ABA GESTÃO DE LEADS (Visualização e Filtros)
    elif aba == "📝 Gestão de Leads":
        st.header("Central de Pacientes")
        
        col_busca, col_filtro = st.columns([3, 1])
        busca = col_busca.text_input("🔍 Buscar por nome ou CPF...")
        status_sel = col_filtro.selectbox("Status", ["Todos", "Pendente", "Em tratamento", "Agendado"])

        # Lógica de Filtros
        df_f = df
        if busca:
            df_f = df[df['Nome'].str.contains(busca, case=False) | df['CPF'].astype(str).str.contains(busca)]
        if status_sel != "Todos":
            df_f = df_f[df_f['Status'] == status_sel]

        # Lista de Cards Premium
        for idx, row in df_f.iterrows():
            # Cores de Status que combinam com a logo
            cor_status = "#f39c12" if row['Status'] == "Pendente" else "#3498db" if row['Status'] == "Agendado" else "#27ae60"
            
            # HTML do Card com Glassmorphism e Degradê na Borda Esquerda
            st.markdown(f"""
                <div class="lead-card" style="border-left: 10px solid; border-image: linear-gradient(to bottom, #8e44ad, #e91e63) 1 100%;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 22px; font-weight: 700; color: #333;">{row['Nome']}</span>
                        <span class="status-badge" style="background-color: {cor_status};">{row['Status']}</span>
                    </div>
                    <div style="margin-top: 18px; color: #555; font-size: 15px; display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                        <div><b>📱 WhatsApp:</b> {row['Telefone']}</div>
                        <div><b>CPF:</b> {row['CPF']}</div>
                        <div><b>📂 Origem:</b> {row['Origem']}</div>
                        <div style="color: #e91e63; font-size: 18px;"><b>💰 € {row['Valor']:,.2f}</b></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Ações Rápidas (Botões pequenos)
            c1, c2, _ = st.columns([1, 1, 4])
            wa_link = f"https://api.whatsapp.com/send?phone={row['Telefone']}&text=Olá {row['Nome']}, tudo bem?"
            c1.markdown(f"[📞 **WhatsApp**]({wa_link})")
            if c2.button("🗑️ Apagar", key=f"btn_{idx}"):
                df = df.drop(idx)
                df.to_csv(LEADS_FILE, index=False)
                st.rerun()

    # 3. ABA CADASTRAR (Formulário Moderno)
    elif aba == "➕ Cadastrar":
        st.header("Registrar Novo Paciente")
        with st.form("form_ortho_pro"):
            nome = st.text_input("Nome Completo do Paciente")
            c1, c2 = st.columns(2)
            cpf = c1.text_input("CPF (somente números)")
            tel = c2.text_input("WhatsApp (ex: 351...)")
            origem = st.selectbox("Como chegou?", ["Instagram", "Google", "Indicação", "Facebook"])
            status = st.selectbox("Status Inicial", ["Pendente", "Em tratamento", "Agendado"])
            valor = st.number_input("Valor do Orçamento (€)", min_value=0.0)
            data_ag = st.date_input("Data do Próximo Agendamento")
            
            if st.form_submit_button("Guardar Paciente"):
                novo = {'Nome': nome, 'CPF': cpf, 'Telefone': tel, 'Origem': origem, 'Status': status, 
                        'Data Criação': datetime.now().date(), 'Data Agendamento': data_ag, 'Valor': valor}
                df = pd.concat([df, pd.DataFrame([novo])], ignore_index=True)
                df.to_csv(LEADS_FILE, index=False)
                st.success("Paciente registrado no sistema OrthoKlin Pro!")
