import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime, date

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="OrthoKlin | Business Intelligence", layout="wide")

# --- CSS AVANÇADO (V15) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;900&display=swap');
    .stApp { background: #050507; color: #ffffff; font-family: 'Inter', sans-serif; }
    [data-testid="stSidebar"] { background-color: #000000 !important; border-right: 1px solid rgba(255, 255, 255, 0.05); width: 260px !important; }
    
    /* Botões Minimalistas */
    div.stButton > button {
        background: transparent !important; color: #94a3b8 !important; border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 4px !important; padding: 4px 12px !important; font-size: 10px !important; font-weight: 600 !important;
        text-transform: uppercase; letter-spacing: 1.2px; width: 100% !important; margin-bottom: 8px !important; transition: 0.3s;
    }
    div.stButton > button:hover { background: linear-gradient(90deg, #8e44ad 0%, #e91e63 100%) !important; color: white !important; border: none !important; transform: translateX(3px); }

    /* Tags de Status e Data */
    .tag-agendado { background: #2ecc71; color: #000; padding: 2px 8px; border-radius: 4px; font-weight: 800; font-size: 9px; }
    .tag-pendente { background: #f1c40f; color: #000; padding: 2px 8px; border-radius: 4px; font-weight: 800; font-size: 9px; }
    .tag-followup { background: #e91e63; color: #fff; padding: 2px 8px; border-radius: 4px; font-weight: 800; font-size: 9px; }
    .data-alerta { color: #ff4b4b; font-weight: 700; }
    .data-ok { color: #64748b; }

    .glass-card { background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 20px; margin-bottom: 15px; }
    .gradient-text { background: linear-gradient(90deg, #a855f7, #e91e63); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; }
    </style>
    """, unsafe_allow_html=True)

# --- BANCO DE DADOS ---
FILE = 'leads_orthoklin_v2.csv'

def load_data():
    if os.path.exists(FILE):
        df = pd.read_csv(FILE)
        df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce').fillna(0.0)
        # Conversão de datas
        df['Data_Cadastro'] = pd.to_datetime(df['Data_Cadastro']).dt.date
        df['Data_Retorno'] = pd.to_datetime(df['Data_Retorno']).dt.date
        return df
    return pd.DataFrame(columns=['Nome','CPF','Telefone','Origem','Status','Valor','Data_Cadastro','Data_Retorno'])

def save_data(df):
    df.to_csv(FILE, index=False)

# --- LOGIN ---
if 'logado' not in st.session_state: st.session_state['logado'] = False
if 'menu' not in st.session_state: st.session_state['menu'] = "Dash"

if not st.session_state['logado']:
    _, col, _ = st.columns([1, 1, 1])
    with col:
        st.write("###")
        if os.path.exists("logo.png"): st.image("logo.png", use_container_width=True)
        st.markdown("<h2 class='gradient-text' style='text-align:center;'>CENTRAL ORTHOKLIN</h2>", unsafe_allow_html=True)
        u = st.text_input("USUÁRIO")
        p = st.text_input("SENHA", type="password")
        if st.button("AUTENTICAR"):
            if u == "admin" and p == "ortho2026":
                st.session_state['logado'] = True
                st.rerun()
else:
    df = load_data()
    
    # --- SIDEBAR ---
    with st.sidebar:
        if os.path.exists("logo.png"): st.image("logo.png", use_container_width=True)
        st.write("###")
        if st.button("DASHBOARD"): st.session_state['menu'] = "Dash"
        if st.button("GESTAO DE LEADS"): st.session_state['menu'] = "Gestao"
        if st.button("NOVO CADASTRO"): st.session_state['menu'] = "Novo"
        st.write("---")
        if st.button("SAIR"):
            st.session_state['logado'] = False
            st.rerun()

    # --- 1. DASHBOARD COM FILTRO DE PERÍODO ---
    if st.session_state['menu'] == "Dash":
        st.markdown("<h1 class='gradient-text'>DESEMPENHO</h1>", unsafe_allow_html=True)
        
        # Filtro de Data no Topo
        col_f1, col_f2 = st.columns(2)
        data_ini = col_f1.date_input("Início", date.today().replace(day=1))
        data_fim = col_f2.date_input("Fim", date.today())
        
        df_periodo = df[(df['Data_Cadastro'] >= data_ini) & (df['Data_Cadastro'] <= data_fim)]

        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="glass-card"><small style="color:#64748b;">FATURAMENTO NO PERÍODO</small><br><b style="font-size:22px;">R$ {df_periodo["Valor"].sum():,.2f}</b></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="glass-card"><small style="color:#64748b;">NOVOS LEADS</small><br><b style="font-size:22px; color:#a855f7;">{len(df_periodo)}</b></div>', unsafe_allow_html=True)
        with c3: 
            retornos_hoje = len(df[df['Data_Retorno'] == date.today()])
            st.markdown(f'<div class="glass-card"><small style="color:#64748b;">RETORNOS PARA HOJE</small><br><b style="font-size:22px; color:#e91e63;">{retornos_hoje}</b></div>', unsafe_allow_html=True)

        if not df_periodo.empty:
            fig = px.bar(df_periodo.groupby('Data_Cadastro')['Valor'].sum().reset_index(), x='Data_Cadastro', y='Valor', title="Evolução Financeira no Período")
            fig.update_traces(marker_color='#e91e63')
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
            st.plotly_chart(fig, use_container_width=True)

    # --- 2. GESTÃO COM DATA DE RETORNO ---
    elif st.session_state['menu'] == "Gestao":
        st.markdown("<h1 class='gradient-text'>GESTÃO ATIVA</h1>", unsafe_allow_html=True)
        busca = st.text_input("BUSCAR NOME OU CPF")
        
        df_f = df
        if busca:
            df_f = df[df['Nome'].str.contains(busca, case=False) | df['CPF'].str.contains(busca)]

        # Ordenar por data de retorno (mais próximos primeiro)
        df_f = df_f.sort_values(by='Data_Retorno')

        for idx, row in df_f.iterrows():
            # Lógica de Alerta de Data
            hoje = date.today()
            data_ret = row['Data_Retorno']
            estilo_data = "data-alerta" if data_ret <= hoje and row['Status'] != 'Em tratamento' else "data-ok"
            
            tag_class = "tag-followup" if row['Status'] == "Follow-up" else "tag-agendado" if row['Status'] == "Agendado" else "tag-pendente"
            
            with st.container():
                st.markdown(f"""
                    <div class="glass-card">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span style="font-size:16px; font-weight:600;">{row['Nome'].upper()}</span>
                            <span class="{tag_class}">{row['Status'].upper()}</span>
                        </div>
                        <div style="margin-top:10px; font-size:11px;">
                            <span style="color:#64748b;">PRÓXIMO CONTATO:</span> <span class="{estilo_data}">{data_ret.strftime('%d/%m/%Y')}</span>
                            <span style="margin-left:15px; color:#64748b;">VALOR:</span> R$ {row['Valor']:,.2f}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                b_ed, b_rm, b_wa, _ = st.columns([1, 1, 2, 4])
                if b_ed.button("EDITAR", key=f"e_{idx}"): st.session_state['edit_idx'] = idx
                if b_rm.button("APAGAR", key=f"r_{idx}"):
                    df = df.drop(idx); save_data(df); st.rerun()
                
                link_wa = f"https://api.whatsapp.com/send?phone={row['Telefone']}"
                b_wa.markdown(f'<a href="{link_wa}" target="_blank" style="text-decoration:none;"><button style="background:#25d366; color:white; border:none; padding:8px; border-radius:6px; width:100%; font-weight:700; cursor:pointer; font-size:10px; text-transform:uppercase;">Chamar no Whats</button></a>', unsafe_allow_html=True)

                if 'edit_idx' in st.session_state and st.session_state['edit_idx'] == idx:
                    with st.form(f"ed_{idx}"):
                        nv_s = st.selectbox("Status", ["Pendente", "Agendado", "Follow-up", "Em tratamento"], index=0)
                        nv_v = st.number_input("Valor", value=float(row['Valor']))
                        nv_r = st.date_input("Nova Data de Retorno", value=row['Data_Retorno'])
                        if st.form_submit_button("ATUALIZAR"):
                            df.at[idx, 'Status'] = nv_s
                            df.at[idx, 'Valor'] = nv_v
                            df.at[idx, 'Data_Retorno'] = nv_r
                            save_data(df); del st.session_state['edit_idx']; st.rerun()

    # --- 3. NOVO CADASTRO COM DATAS ---
    elif st.session_state['menu'] == "Novo":
        st.markdown("<h1 class='gradient-text'>NOVO PACIENTE</h1>", unsafe_allow_html=True)
        with st.form("cad_v2"):
            nome = st.text_input("NOME COMPLETO")
            c1, c2 = st.columns(2)
            cpf = c1.text_input("CPF")
            tel = c2.text_input("TELEFONE")
            
            c3, c4, c5 = st.columns(3)
            origem = c3.selectbox("ORIGEM", ["Instagram", "Google Ads", "Indicação"])
            status = c4.selectbox("STATUS", ["Pendente", "Agendado", "Follow-up"])
            valor = c5.number_input("VALOR R$", min_value=0.0)
            
            # Upgrade: Data de Retorno automática (padrão 2 dias depois)
            data_retorno = st.date_input("AGENDAR PRÓXIMO CONTATO (RETORNO)", value=date.today())
            
            if st.form_submit_button("SALVAR NO SISTEMA"):
                novo = {
                    'Nome': nome, 'CPF': cpf, 'Telefone': tel, 'Origem': origem, 
                    'Status': status, 'Valor': valor, 
                    'Data_Cadastro': date.today(), 'Data_Retorno': data_retorno
                }
                df = pd.concat([df, pd.DataFrame([novo])], ignore_index=True)
                save_data(df); st.success("Paciente registrado!"); st.rerun()
