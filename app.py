import streamlit as st
import pandas as pd
import os
from datetime import datetime, date
from PIL import Image
import plotly.express as px

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="OrthoKlin | Business Intelligence", layout="wide")

# --- CSS PERSONALIZADO (V19) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;900&display=swap');
    .stApp { background: #050507; color: #ffffff; font-family: 'Inter', sans-serif; }
    [data-testid="stSidebar"] { background-color: #000000 !important; border-right: 1px solid rgba(255, 255, 255, 0.05); width: 260px !important; }
    
    div.stButton > button {
        background: transparent !important; color: #94a3b8 !important; border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 4px !important; padding: 4px 12px !important; font-size: 10px !important; font-weight: 600 !important;
        text-transform: uppercase; letter-spacing: 1.2px; width: 100% !important; margin-top: 10px; transition: 0.3s;
    }
    div.stButton > button:hover { background: linear-gradient(90deg, #8e44ad 0%, #e91e63 100%) !important; color: white !important; border: none !important; transform: translateX(3px); }

    .tag-agendado { background: #2ecc71; color: #000; padding: 2px 8px; border-radius: 4px; font-weight: 800; font-size: 9px; text-transform: uppercase; }
    .tag-pendente { background: #f1c40f; color: #000; padding: 2px 8px; border-radius: 4px; font-weight: 800; font-size: 9px; text-transform: uppercase; }
    .tag-followup { background: #e91e63; color: #fff; padding: 2px 8px; border-radius: 4px; font-weight: 800; font-size: 9px; text-transform: uppercase; }
    
    .glass-card { background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 20px; margin-bottom: 15px; }
    .gradient-text { background: linear-gradient(90deg, #a855f7, #e91e63); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES AUXILIARES ---
def render_logo():
    path = "logo.png"
    if os.path.exists(path):
        try:
            img = Image.open(path)
            st.image(img, use_container_width=True)
        except:
            st.markdown("<h1 class='gradient-text' style='text-align:center;'>ORTHOKLIN</h1>", unsafe_allow_html=True)
    else:
        st.markdown("<h1 class='gradient-text' style='text-align:center;'>ORTHOKLIN</h1>", unsafe_allow_html=True)

FILE = 'leads_orthoklin_v2.csv'
def load_data():
    if os.path.exists(FILE):
        df = pd.read_csv(FILE)
        df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce').fillna(0.0)
        df['Data_Cadastro'] = pd.to_datetime(df['Data_Cadastro']).dt.date
        df['Data_Retorno'] = pd.to_datetime(df['Data_Retorno']).dt.date
        return df
    return pd.DataFrame(columns=['Nome','CPF','Telefone','Origem','Status','Valor','Data_Cadastro','Data_Retorno'])

def save_data(df):
    df.to_csv(FILE, index=False)

# --- SISTEMA DE LOGIN ---
if 'logado' not in st.session_state: st.session_state['logado'] = False
if 'auth_mode' not in st.session_state: st.session_state['auth_mode'] = "login"
if 'menu' not in st.session_state: st.session_state['menu'] = "Dash"

if not st.session_state['logado']:
    _, col, _ = st.columns([1, 1, 1])
    with col:
        st.write("####")
        render_logo()
        if st.session_state['auth_mode'] == "login":
            u = st.text_input("USUÁRIO")
            p = st.text_input("SENHA", type="password")
            if st.button("ACESSAR"):
                if (u == "admin" and p == "ortho2026") or (u == st.session_state.get('novo_u') and p == st.session_state.get('novo_p')):
                    st.session_state['logado'] = True
                    st.rerun()
                else: st.error("Erro no acesso.")
            c1, c2 = st.columns(2)
            if c1.button("CRIAR PERFIL"): st.session_state['auth_mode'] = "cadastro"; st.rerun()
            if c2.button("RECUPERAR"): st.session_state['auth_mode'] = "recuperar"; st.rerun()

        elif st.session_state['auth_mode'] == "cadastro":
            nu, np = st.text_input("USUÁRIO"), st.text_input("SENHA", type="password")
            if st.button("FINALIZAR E ENTRAR"):
                st.session_state['novo_u'], st.session_state['novo_p'], st.session_state['logado'] = nu, np, True
                st.rerun()
            if st.button("VOLTAR"): st.session_state['auth_mode'] = "login"; st.rerun()

else:
    df = load_data()
    with st.sidebar:
        render_logo()
        st.write("###")
        if st.button("DASHBOARD"): st.session_state['menu'] = "Dash"
        if st.button("GESTAO DE LEADS"): st.session_state['menu'] = "Gestao"
        if st.button("BI & FINANCEIRO"): st.session_state['menu'] = "BI"
        if st.button("NOVO CADASTRO"): st.session_state['menu'] = "Novo"
        st.write("---")
        if st.button("SAIR"): st.session_state['logado'] = False; st.rerun()

    # --- ABA: DASHBOARD (RESUMO RÁPIDO) ---
    if st.session_state['menu'] == "Dash":
        st.markdown("<h1 class='gradient-text'>RESUMO DIÁRIO</h1>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        hoje = date.today()
        c1.markdown(f'<div class="glass-card"><small>RETORNOS HOJE</small><br><b>{len(df[df["Data_Retorno"] == hoje])}</b></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="glass-card"><small>NOVOS LEADS (MÊS)</small><br><b>{len(df[df["Data_Cadastro"] >= hoje.replace(day=1)])}</b></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="glass-card"><small>STATUS AGENDADO</small><br><b style="color:#2ecc71;">{len(df[df["Status"] == "Agendado"])}</b></div>', unsafe_allow_html=True)

    # --- ABA: BI & FINANCEIRO (O UPGRADE!) ---
    elif st.session_state['menu'] == "BI":
        st.markdown("<h1 class='gradient-text'>INTELIGÊNCIA FINANCEIRA</h1>", unsafe_allow_html=True)
        
        # Métrica de Faturamento Geral
        total_geral = df['Valor'].sum()
        ticket_medio = total_geral / len(df) if len(df) > 0 else 0
        
        c1, c2, c3 = st.columns(3)
        c1.markdown(f'<div class="glass-card"><small>FATURAMENTO GERAL</small><br><b style="font-size:24px; color:#2ecc71;">R$ {total_geral:,.2f}</b></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="glass-card"><small>TICKET MÉDIO</small><br><b style="font-size:24px;">R$ {ticket_medio:,.2f}</b></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="glass-card"><small>POTENCIAL EM FOLLOW-UP</small><br><b style="font-size:24px; color:#e91e63;">R$ {df[df["Status"]=="Follow-up"]["Valor"].sum():,.2f}</b></div>', unsafe_allow_html=True)

        st.write("###")
        col_graf1, col_graf2 = st.columns(2)
        
        with col_graf1:
            st.markdown("<small>DISTRIBUIÇÃO POR CANAL (R$)</small>", unsafe_allow_html=True)
            fig_origem = px.pie(df, values='Valor', names='Origem', hole=0.6, color_discrete_sequence=px.colors.qualitative.Pastel)
            fig_origem.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white", showlegend=True)
            st.plotly_chart(fig_origem, use_container_width=True)
            
        with col_graf2:
            st.markdown("<small>EVOLUÇÃO MENSAL DE ORÇAMENTOS</small>", unsafe_allow_html=True)
            df['Mes_Ano'] = pd.to_datetime(df['Data_Cadastro']).dt.strftime('%m/%Y')
            evolucao = df.groupby('Mes_Ano')['Valor'].sum().reset_index()
            fig_evol = px.line(evolucao, x='Mes_Ano', y='Valor', markers=True)
            fig_evol.update_traces(line_color='#e91e63')
            fig_evol.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
            st.plotly_chart(fig_evol, use_container_width=True)

    # --- ABA: GESTÃO ---
    elif st.session_state['menu'] == "Gestao":
        st.markdown("<h1 class='gradient-text'>GESTÃO DE LEADS</h1>", unsafe_allow_html=True)
        busca = st.text_input("BUSCAR NOME OU CPF")
        df_f = df[df['Nome'].str.contains(busca, case=False) | df['CPF'].str.contains(busca)] if busca else df
        for idx, row in df_f.sort_values(by='Data_Retorno').iterrows():
            tag = "tag-followup" if row['Status'] == "Follow-up" else "tag-agendado" if row['Status'] == "Agendado" else "tag-pendente"
            with st.container():
                st.markdown(f'<div class="glass-card"><div style="display:flex; justify-content:space-between;"><b>{row["Nome"].upper()}</b><span class="{tag}">{row["Status"]}</span></div><small>CPF: {row["CPF"]} | Valor: R$ {row["Valor"]:,.2f} | Retorno: {row["Data_Retorno"]}</small></div>', unsafe_allow_html=True)
                b1, b2, _ = st.columns([1,1,4])
                if b1.button("APAGAR", key=f"d_{idx}"): df=df.drop(idx); save_data(df); st.rerun()
                wa = f"https://api.whatsapp.com/send?phone={row['Telefone']}"; b2.markdown(f'<a href="{wa}" target="_blank"><button style="background:#25d366; color:white; border:none; padding:8px; border-radius:6px; cursor:pointer; font-size:10px; width:100%;">WHATSAPP</button></a>', unsafe_allow_html=True)

    # --- ABA: NOVO ---
    elif st.session_state['menu'] == "Novo":
        st.markdown("<h1 class='gradient-text'>NOVO CADASTRO</h1>", unsafe_allow_html=True)
        with st.form("add"):
            n, c, t = st.text_input("NOME"), st.text_input("CPF"), st.text_input("WHATSAPP")
            o, s, v = st.selectbox("ORIGEM", ["Instagram", "Google Ads", "Indicação"]), st.selectbox("STATUS", ["Pendente", "Follow-up"]), st.number_input("VALOR", min_value=0.0)
            dr = st.date_input("DATA DE RETORNO")
            if st.form_submit_button("SALVAR"):
                new = {'Nome':n, 'CPF':c, 'Telefone':t, 'Origem':o, 'Status':s, 'Valor':v, 'Data_Cadastro':date.today(), 'Data_Retorno':dr}
                df = pd.concat([df, pd.DataFrame([new])], ignore_index=True); save_data(df); st.rerun()
