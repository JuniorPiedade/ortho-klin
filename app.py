import streamlit as st
import pandas as pd
import os
import plotly.express as px

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="OrthoKlin | AI Dashboard", layout="wide")

# --- CSS FUTURISTA PREMIUM (GLASSMORPHISM) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;900&display=swap');
    
    /* Fundo Dark Mode IA */
    .stApp {
        background: #050507;
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }

    /* Sidebar Estilizada */
    [data-testid="stSidebar"] {
        background: rgba(0, 0, 0, 0.6) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }

    /* Cards com Glassmorphism */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 25px;
        margin-bottom: 20px;
        transition: 0.4s ease;
    }
    .glass-card:hover {
        border: 1px solid #e91e63;
        box-shadow: 0 0 20px rgba(233, 30, 99, 0.1);
    }

    /* KPI Headers */
    .kpi-label {
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 2px;
        color: #64748b;
        text-transform: uppercase;
        margin-bottom: 5px;
    }
    .kpi-value {
        font-size: 28px;
        font-weight: 900;
        background: linear-gradient(90deg, #8e44ad, #e91e63);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Botões com Glow Neon */
    div.stButton > button {
        background: linear-gradient(90deg, #8e44ad 0%, #e91e63 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        height: 45px !important;
        width: 100% !important;
        box-shadow: 0 4px 15px rgba(233, 30, 99, 0.2);
    }
    div.stButton > button:hover {
        box-shadow: 0 0 25px rgba(233, 30, 99, 0.5) !important;
        transform: translateY(-2px);
    }

    /* Botão WhatsApp Neon */
    .btn-whats {
        display: block;
        background: #25d366;
        color: white !important;
        text-align: center;
        padding: 12px;
        border-radius: 8px;
        font-weight: 800;
        font-size: 12px;
        text-decoration: none;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CARREGAMENTO DE DADOS ---
FILE = 'leads_orthoklin.csv'
def load_data():
    if os.path.exists(FILE):
        df = pd.read_csv(FILE)
        df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce').fillna(0.0)
        return df
    return pd.DataFrame(columns=['Nome','CPF','Telefone','Origem','Status','Valor'])

# --- LÓGICA DE NAVEGAÇÃO ---
if 'logado' not in st.session_state: st.session_state['logado'] = False
if 'menu' not in st.session_state: st.session_state['menu'] = "Dashboard"

if not st.session_state['logado']:
    _, col, _ = st.columns([1, 1, 1])
    with col:
        st.write("#")
        st.markdown("<h1 style='text-align:center; font-weight:900;'>ACESSO GERAL</h1>", unsafe_allow_html=True)
        user = st.text_input("USUÁRIO")
        pw = st.text_input("SENHA", type="password")
        if st.button("ENTRAR"):
            if user == "admin" and pw == "ortho2026":
                st.session_state['logado'] = True
                st.rerun()
            else: st.error("Acesso Negado")
else:
    df = load_data()
    
    # --- SIDEBAR FIXA ---
    with st.sidebar:
        st.markdown("<h2 style='letter-spacing:2px;'>ORTHOKLIN</h2>", unsafe_allow_html=True)
        st.write("---")
        if st.button("DASHBOARD"): st.session_state['menu'] = "Dashboard"
        if st.button("GESTÃO GERAL"): st.session_state['menu'] = "Gestão"
        if st.button("NOVO CADASTRO"): st.session_state['menu'] = "Novo"
        st.write("---")
        if st.button("SAIR"):
            st.session_state['logado'] = False
            st.rerun()

    # --- ABA DASHBOARD ---
    if st.session_state['menu'] == "Dashboard":
        st.markdown("<h1 style='font-weight:900; letter-spacing:-1px;'>PERFORMANCE IA</h1>", unsafe_allow_html=True)
        
        # MÉTRICAS TOP
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="glass-card"><p class="kpi-label">Faturamento Total</p><p class="kpi-value">R$ {df["Valor"].sum():,.2f}</p></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="glass-card"><p class="kpi-label">Pendentes</p><p class="kpi-value">R$ {df[df["Status"]=="Pendente"]["Valor"].sum():,.2f}</p></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="glass-card"><p class="kpi-label">Leads</p><p class="kpi-value">{len(df)}</p></div>', unsafe_allow_html=True)

        if not df.empty:
            fig = px.area(df.groupby('Origem')['Valor'].sum().reset_index(), x='Origem', y='Valor', color_discrete_sequence=['#e91e63'])
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
            st.plotly_chart(fig, use_container_width=True)

    # --- ABA GESTÃO ---
    elif st.session_state['menu'] == "Gestão":
        st.markdown("<h1 style='font-weight:900;'>BASE DE DADOS</h1>", unsafe_allow_html=True)
        busca = st.text_input("PESQUISAR NOME OU CPF")
        
        df_f = df
        if busca: df_f = df[df['Nome'].str.contains(busca, case=False)]

        for idx, row in df_f.iterrows():
            with st.container():
                st.markdown(f"""
                    <div class="glass-card">
                        <div style="display:flex; justify-content:space-between;">
                            <span style="font-weight:800; font-size:18px;">{row['Nome'].upper()}</span>
                            <span style="color:#e91e63; font-weight:900;">{row['Status'].upper()}</span>
                        </div>
                        <p style="color:#64748b; font-size:13px; margin-top:5px;">VALOR: R$ {row['Valor']:,.2f} | ORIGEM: {row['Origem']}</p>
                        <a href="https://api.whatsapp.com/send?phone={row['Telefone']}" target="_blank" class="btn-whats">CONTATAR PACIENTE</a>
                    </div>
                """, unsafe_allow_html=True)
                
                col_ed, col_rm, _ = st.columns([1,1,4])
                if col_rm.button("REMOVER", key=f"rm_{idx}"):
                    df.drop(idx).to_csv(FILE, index=False)
                    st.rerun()

    # --- ABA NOVO ---
    elif st.session_state['menu'] == "Novo":
        st.markdown("<h1 style='font-weight:900;'>REGISTRAR PACIENTE</h1>", unsafe_allow_html=True)
        with st.form("cad_pro"):
            n = st.text_input("NOME")
            c1, c2 = st.columns(2)
            cp = c1.text_input("CPF")
            tl = c2.text_input("WHATSAPP")
            or_ = st.selectbox("ORIGEM", ["Instagram", "Google", "Facebook", "Indicação"])
            st_ = st.selectbox("STATUS", ["Pendente", "Em tratamento", "Agendado"])
            vl = st.number_input("VALOR R$", min_value=0.0)
            if st.form_submit_button("SALVAR INTELIGÊNCIA"):
                novo = {'Nome': n, 'CPF': cp, 'Telefone': tl, 'Origem': or_, 'Status': st_, 'Valor': vl}
                pd.concat([df, pd.DataFrame([novo])], ignore_index=True).to_csv(FILE, index=False)
                st.success("REGISTRADO")
