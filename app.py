import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="OrthoKlin | AI Dashboard", layout="wide")

# --- CSS FUTURISTA & GLASSMORPHISM ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;900&display=swap');
    .stApp { background: #050507; color: #ffffff; font-family: 'Inter', sans-serif; }
    [data-testid="stSidebar"] { background: rgba(0, 0, 0, 0.8) !important; backdrop-filter: blur(20px); border-right: 1px solid rgba(255, 255, 255, 0.05); }
    
    .gradient-text {
        background: linear-gradient(90deg, #a855f7, #e91e63);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-weight: 900;
    }

    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
    }

    div.stButton > button {
        background: linear-gradient(90deg, #8e44ad 0%, #e91e63 100%) !important;
        color: white !important; border: none !important; border-radius: 8px !important;
        font-weight: 700 !important; text-transform: uppercase; width: 100% !important;
    }
    
    .status-tag {
        padding: 2px 10px; border-radius: 5px; font-size: 10px; font-weight: 800; text-transform: uppercase;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE DADOS ---
FILE = 'leads_orthoklin.csv'

def load_data():
    if os.path.exists(FILE):
        df = pd.read_csv(FILE)
        df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce').fillna(0.0)
        # Garante que a coluna CPF seja tratada como string para busca
        df['CPF'] = df['CPF'].astype(str)
        return df
    return pd.DataFrame(columns=['Nome','CPF','Telefone','Origem','Status','Valor'])

def save_data(df):
    df.to_csv(FILE, index=False)

# --- GESTÃO DE ACESSO ---
if 'logado' not in st.session_state: st.session_state['logado'] = False
if 'menu' not in st.session_state: st.session_state['menu'] = "Dashboard"

if not st.session_state['logado']:
    _, col, _ = st.columns([1, 1, 1])
    with col:
        if os.path.exists("logo.png"): st.image("logo.png")
        st.markdown("<h1 class='gradient-text' style='text-align:center;'>ACESSO GERAL</h1>", unsafe_allow_html=True)
        u = st.text_input("USUÁRIO")
        p = st.text_input("SENHA", type="password")
        if st.button("ENTRAR NO SISTEMA"):
            if u == "admin" and p == "ortho2026":
                st.session_state['logado'] = True
                st.rerun()
else:
    df = load_data()
    
    # --- SIDEBAR ---
    with st.sidebar:
        if os.path.exists("logo.png"): st.image("logo.png")
        st.write("---")
        if st.button("DASHBOARD"): st.session_state['menu'] = "Dashboard"
        if st.button("GESTÃO DE LEADS"): st.session_state['menu'] = "Gestao"
        if st.button("NOVO CADASTRO"): st.session_state['menu'] = "Novo"
        st.write("---")
        if st.button("SAIR"):
            st.session_state['logado'] = False
            st.rerun()

    # --- ABA: DASHBOARD ---
    if st.session_state['menu'] == "Dashboard":
        st.markdown("<h1 class='gradient-text'>INTELIGÊNCIA COMERCIAL</h1>", unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        fat_total = df['Valor'].sum()
        fat_pendente = df[df['Status'] == 'Pendente']['Valor'].sum()
        follow_ups = len(df[df['Status'] == 'Follow-up'])

        c1.markdown(f'<div class="glass-card"><small>FATURAMENTO TOTAL</small><br><b style="font-size:22px;">R$ {fat_total:,.2f}</b></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="glass-card"><small>ORÇAMENTOS PENDENTES</small><br><b style="font-size:22px; color:#e91e63;">R$ {fat_pendente:,.2f}</b></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="glass-card"><small>PACIENTES EM FOLLOW-UP</small><br><b style="font-size:22px; color:#a855f7;">{follow_ups}</b></div>', unsafe_allow_html=True)

        if not df.empty:
            st.write("### Distribuição de Leads por Status")
            # Gráfico de Pizza solicitado
            fig_pizza = px.pie(df, names='Status', hole=0.6, 
                               color_discrete_map={'Pendente':'#e91e63', 'Agendado':'#a855f7', 'Follow-up':'#f39c12', 'Em tratamento':'#2ecc71'})
            fig_pizza.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white")
            st.plotly_chart(fig_pizza, use_container_width=True)

    # --- ABA: GESTÃO DE LEADS (BUSCA, EDIÇÃO, REMOÇÃO) ---
    elif st.session_state['menu'] == "Gestao":
        st.markdown("<h1 class='gradient-text'>GESTÃO DE LEADS</h1>", unsafe_allow_html=True)
        
        # Filtro de Busca por Nome ou CPF
        busca = st.text_input("🔍 BUSCAR POR NOME OU CPF")
        
        df_f = df
        if busca:
            df_f = df[df['Nome'].str.contains(busca, case=False) | df['CPF'].str.contains(busca)]

        for idx, row in df_f.iterrows():
            with st.container():
                st.markdown(f"""
                    <div class="glass-card">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span style="font-size:18px; font-weight:800;">{row['Nome'].upper()}</span>
                            <span class="status-tag" style="background:#e91e63;">{row['Status']}</span>
                        </div>
                        <div style="color:#888; font-size:13px; margin-top:5px;">
                            CPF: {row['CPF']} | ORÇAMENTO: R$ {row['Valor']:,.2f} | ORIGEM: {row['Origem']}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                b1, b2, b3, _ = st.columns([1, 1, 2, 4])
                
                # AÇÃO EDITAR
                if b1.button("EDITAR", key=f"ed_{idx}"):
                    st.session_state['edit_idx'] = idx
                
                # AÇÃO REMOVER
                if b2.button("APAGAR", key=f"rm_{idx}"):
                    df = df.drop(idx)
                    save_data(df)
                    st.rerun()

                # AÇÃO WHATSAPP
                wa_link = f"https://api.whatsapp.com/send?phone={row['Telefone']}"
                b3.markdown(f'<a href="{wa_link}" target="_blank" style="text-decoration:none;"><button style="background:#25d366; color:white; border:none; padding:8px; border-radius:5px; width:100%; font-weight:bold; cursor:pointer;">WHATSAPP</button></a>', unsafe_allow_html=True)

                # FORMULÁRIO DE EDIÇÃO
                if 'edit_idx' in st.session_state and st.session_state['edit_idx'] == idx:
                    with st.form(f"form_edit_{idx}"):
                        st.write(f"Editando Registro de {row['Nome']}")
                        nv_valor = st.number_input("Valor R$", value=float(row['Valor']))
                        nv_status = st.selectbox("Status", ["Pendente", "Agendado", "Follow-up", "Em tratamento"], 
                                                 index=["Pendente", "Agendado", "Follow-up", "Em tratamento"].index(row['Status']))
                        if st.form_submit_button("CONFIRMAR ALTERAÇÕES"):
                            df.at[idx, 'Valor'] = nv_valor
                            df.at[idx, 'Status'] = nv_status
                            save_data(df)
                            del st.session_state['edit_idx']
                            st.rerun()

    # --- ABA: NOVO CADASTRO ---
    elif st.session_state['menu'] == "Novo":
        st.markdown("<h1 class='gradient-text'>NOVO CADASTRO</h1>", unsafe_allow_html=True)
        with st.form("cad_pro"):
            nome = st.text_input("NOME COMPLETO")
            c1, c2 = st.columns(2)
            cpf = c1.text_input("CPF")
            tel = c2.text_input("TELEFONE (COM DDD)")
            orig = st.selectbox("ORIGEM", ["Instagram", "Google Ads", "Indicação", "Facebook"])
            stat = st.selectbox("STATUS", ["Pendente", "Agendado", "Follow-up", "Em tratamento"])
            val = st.number_input("VALOR DO ORÇAMENTO R$", min_value=0.0)
            
            if st.form_submit_button("SALVAR REGISTRO"):
                novo = {'Nome': nome, 'CPF': cpf, 'Telefone': tel, 'Origem': orig, 'Status': stat, 'Valor': val}
                df = pd.concat([df, pd.DataFrame([novo])], ignore_index=True)
                save_data(df)
                st.success("Paciente registrado com sucesso!")
                st.rerun()
