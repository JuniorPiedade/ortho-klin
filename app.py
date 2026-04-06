import streamlit as st
import pandas as pd
import os
from datetime import datetime, date
from PIL import Image
import plotly.express as px

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="OrthoKlin | Enterprise BI", layout="wide", initial_sidebar_state="expanded")

# --- CSS PREMIUN (V21: HEADER, PERFIS E GLASSMORPHISM) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;900&display=swap');
    .stApp { background: #050507; color: #ffffff; font-family: 'Inter', sans-serif; }
    [data-testid="stSidebar"] { background-color: #000000 !important; border-right: 1px solid rgba(255, 255, 255, 0.05); width: 260px !important; }
    
    /* Header de Perfil no Topo Direito */
    .user-header {
        position: fixed; top: 1rem; right: 2rem;
        text-align: right; z-index: 1000;
        padding: 8px 15px; border-radius: 8px;
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
    }
    .user-name { font-weight: 800; font-size: 11px; color: #ffffff; margin: 0; letter-spacing: 0.5px; }
    .user-role { font-size: 9px; color: #e91e63; font-weight: 700; text-transform: uppercase; margin: 0; }

    /* Botões Sidebar */
    div.stButton > button {
        background: transparent !important; color: #94a3b8 !important; border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 4px !important; padding: 4px 12px !important; font-size: 10px !important; font-weight: 600 !important;
        text-transform: uppercase; letter-spacing: 1.2px; width: 100% !important; margin-top: 8px; transition: 0.3s;
    }
    div.stButton > button:hover { background: linear-gradient(90deg, #8e44ad 0%, #e91e63 100%) !important; color: white !important; border: none !important; transform: translateX(4px); }

    /* Tags e Cards */
    .tag-agendado { background: #2ecc71; color: #000; padding: 2px 8px; border-radius: 4px; font-weight: 800; font-size: 9px; text-transform: uppercase; }
    .tag-pendente { background: #f1c40f; color: #000; padding: 2px 8px; border-radius: 4px; font-weight: 800; font-size: 9px; text-transform: uppercase; }
    .tag-followup { background: #e91e63; color: #fff; padding: 2px 8px; border-radius: 4px; font-weight: 800; font-size: 9px; text-transform: uppercase; }
    .data-alerta { color: #ff4b4b; font-weight: 700; }
    
    .glass-card { background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 20px; margin-bottom: 15px; }
    .gradient-text { background: linear-gradient(90deg, #a855f7, #e91e63); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; }
    
    /* Inputs */
    input, select, textarea { background: rgba(255,255,255,0.05) !important; color: white !important; border: 1px solid rgba(255,255,255,0.1) !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE ARQUIVOS (DATABASE) ---
LEAD_FILE = 'leads_orthoklin_v2.csv'
USER_FILE = 'usuarios_orthoklin.csv'

def load_leads():
    if os.path.exists(LEAD_FILE):
        df = pd.read_csv(LEAD_FILE)
        df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce').fillna(0.0)
        df['Data_Cadastro'] = pd.to_datetime(df['Data_Cadastro']).dt.date
        df['Data_Retorno'] = pd.to_datetime(df['Data_Retorno']).dt.date
        return df
    return pd.DataFrame(columns=['Nome','CPF','Telefone','Origem','Status','Valor','Data_Cadastro','Data_Retorno'])

def load_users():
    if os.path.exists(USER_FILE):
        return pd.read_csv(USER_FILE)
    df = pd.DataFrame([{'nome': 'Diretoria Ortho', 'user': 'admin', 'pass': 'ortho2026', 'cargo': 'Gestor'}])
    df.to_csv(USER_FILE, index=False)
    return df

def save_data(df, filename): df.to_csv(filename, index=False)

def render_logo():
    if os.path.exists("logo.png"):
        try: st.image(Image.open("logo.png"), use_container_width=True)
        except: st.markdown("<h1 class='gradient-text' style='text-align:center;'>ORTHOKLIN</h1>", unsafe_allow_html=True)
    else: st.markdown("<h1 class='gradient-text' style='text-align:center;'>ORTHOKLIN</h1>", unsafe_allow_html=True)

# --- LÓGICA DE SESSÃO ---
if 'logado' not in st.session_state: st.session_state['logado'] = False
if 'user_data' not in st.session_state: st.session_state['user_data'] = None
if 'menu' not in st.session_state: st.session_state['menu'] = "Dash"

# --- TELA DE ACESSO ---
if not st.session_state['logado']:
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.write("####")
        render_logo()
        u = st.text_input("USUÁRIO", placeholder="seu.nome")
        p = st.text_input("SENHA", type="password", placeholder="••••••")
        if st.button("ACESSAR"):
            users_df = load_users()
            match = users_df[(users_df['user'] == u) & (users_df['pass'] == p)]
            if not match.empty:
                st.session_state['logado'] = True
                st.session_state['user_data'] = match.iloc[0].to_dict()
                st.rerun()
            else: st.error("Acesso negado. Verifique usuário e senha.")
else:
    # --- HEADER DINÂMICO ---
    user = st.session_state['user_data']
    st.markdown(f"""
        <div class="user-header">
            <p class="user-name">{user['nome'].upper()}</p>
            <p class="user-role">{user['cargo']}</p>
        </div>
    """, unsafe_allow_html=True)

    df_leads = load_leads()

    # --- SIDEBAR COM CONTROLE DE ACESSO ---
    with st.sidebar:
        render_logo()
        st.write("###")
        if st.button("DASHBOARD"): st.session_state['menu'] = "Dash"
        if st.button("GESTAO DE LEADS"): st.session_state['menu'] = "Gestao"
        if st.button("NOVO CADASTRO"): st.session_state['menu'] = "Novo"
        
        if user['cargo'] == "Gestor":
            st.write("---")
            if st.button("BI FINANCEIRO"): st.session_state['menu'] = "BI"
            if st.button("EQUIPE / CARGOS"): st.session_state['menu'] = "Config"
            
        st.write("---")
        if st.button("SAIR DO SISTEMA"):
            st.session_state['logado'] = False
            st.rerun()

    # --- NAVEGAÇÃO ---

    # 1. DASHBOARD
    if st.session_state['menu'] == "Dash":
        st.markdown("<h1 class='gradient-text'>OVERVIEW</h1>", unsafe_allow_html=True)
        hoje = date.today()
        c1, c2, c3 = st.columns(3)
        c1.markdown(f'<div class="glass-card"><small>RETORNOS HOJE</small><br><b>{len(df_leads[df_leads["Data_Retorno"] == hoje])}</b></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="glass-card"><small>ORÇAMENTOS ABERTOS</small><br><b>{len(df_leads[df_leads["Status"] != "Em tratamento"])}</b></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="glass-card"><small>MÉDIA DE CONVERSÃO</small><br><b>{len(df_leads[df_leads["Status"]=="Em tratamento"])/len(df_leads)*100 if len(df_leads)>0 else 0:.1f}%</b></div>', unsafe_allow_html=True)

    # 2. GESTÃO DE LEADS
    elif st.session_state['menu'] == "Gestao":
        st.markdown("<h1 class='gradient-text'>GESTÃO OPERACIONAL</h1>", unsafe_allow_html=True)
        busca = st.text_input("PESQUISAR NOME OU CPF")
        df_f = df_leads[df_leads['Nome'].str.contains(busca, case=False) | df_leads['CPF'].str.contains(busca)] if busca else df_leads
        
        for idx, row in df_f.sort_values(by='Data_Retorno').iterrows():
            tag = "tag-followup" if row['Status'] == "Follow-up" else "tag-agendado" if row['Status'] == "Agendado" else "tag-pendente"
            cor_data = "data-alerta" if row['Data_Retorno'] <= date.today() and row['Status'] != 'Em tratamento' else ""
            
            with st.container():
                st.markdown(f"""
                    <div class="glass-card">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span style="font-weight:600;">{row['Nome'].upper()}</span>
                            <span class="{tag}">{row['Status']}</span>
                        </div>
                        <div style="font-size:11px; margin-top:8px; color:#64748b;">
                            CPF: {row['CPF']} | CANAL: {row['Origem']} | <span class="{cor_data}">RETORNO: {row['Data_Retorno'].strftime('%d/%m/%Y')}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                b1, b2, b3, _ = st.columns([1,1,2,4])
                if b1.button("EDITAR", key=f"e_{idx}"): st.session_state['edit_idx'] = idx
                if b2.button("APAGAR", key=f"r_{idx}"): 
                    df_leads = df_leads.drop(idx); save_data(df_leads, LEAD_FILE); st.rerun()
                wa = f"https://api.whatsapp.com/send?phone={row['Telefone']}"
                b3.markdown(f'<a href="{wa}" target="_blank"><button style="background:#25d366; color:white; border:none; padding:8px; border-radius:6px; cursor:pointer; font-size:10px; width:100%; font-weight:700;">WHATSAPP</button></a>', unsafe_allow_html=True)

                if 'edit_idx' in st.session_state and st.session_state['edit_idx'] == idx:
                    with st.form(f"f_{idx}"):
                        nv_s = st.selectbox("Status", ["Pendente", "Agendado", "Follow-up", "Em tratamento"])
                        nv_v = st.number_input("Valor", value=float(row['Valor']))
                        nv_r = st.date_input("Data Retorno", value=row['Data_Retorno'])
                        if st.form_submit_button("SALVAR ALTERAÇÕES"):
                            df_leads.at[idx, 'Status'], df_leads.at[idx, 'Valor'], df_leads.at[idx, 'Data_Retorno'] = nv_s, nv_v, nv_r
                            save_data(df_leads, LEAD_FILE); del st.session_state['edit_idx']; st.rerun()

    # 3. NOVO CADASTRO
    elif st.session_state['menu'] == "Novo":
        st.markdown("<h1 class='gradient-text'>NOVO PACIENTE</h1>", unsafe_allow_html=True)
        with st.form("cad_lead"):
            n = st.text_input("NOME COMPLETO")
            c1, c2 = st.columns(2); cp = c1.text_input("CPF"); tl = c2.text_input("TELEFONE (DDD+NÚMERO)")
            c3, c4 = st.columns(2); or_ = c3.selectbox("ORIGEM", ["Instagram", "Google Ads", "Indicação"]); vl = c4.number_input("VALOR ORÇAMENTO", min_value=0.0)
            dr = st.date_input("DATA DE RETORNO", value=date.today())
            if st.form_submit_button("REGISTRAR"):
                new_l = {'Nome': n, 'CPF': cp, 'Telefone': tl, 'Origem': or_, 'Status': 'Pendente', 'Valor': vl, 'Data_Cadastro': date.today(), 'Data_Retorno': dr}
                df_leads = pd.concat([df_leads, pd.DataFrame([new_l])], ignore_index=True); save_data(df_leads, LEAD_FILE); st.rerun()

    # 4. BI FINANCEIRO (GESTOR)
    elif st.session_state['menu'] == "BI":
        st.markdown("<h1 class='gradient-text'>INTELIGÊNCIA FINANCEIRA</h1>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.markdown(f'<div class="glass-card"><small>FATURAMENTO GERAL</small><br><b style="color:#2ecc71; font-size:24px;">R$ {df_leads["Valor"].sum():,.2f}</b></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="glass-card"><small>TICKET MÉDIO</small><br><b style="font-size:24px;">R$ {df_leads["Valor"].sum()/len(df_leads) if len(df_leads)>0 else 0:,.2f}</b></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="glass-card"><small>POTENCIAL FOLLOW-UP</small><br><b style="color:#e91e63; font-size:24px;">R$ {df_leads[df_leads["Status"]=="Follow-up"]["Valor"].sum():,.2f}</b></div>', unsafe_allow_html=True)
        
        st.write("###")
        col1, col2 = st.columns(2)
        fig1 = px.pie(df_leads, values='Valor', names='Origem', hole=0.6, title="Receita por Canal")
        fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white")
        col1.plotly_chart(fig1, use_container_width=True)
        
        df_leads['Mes'] = pd.to_datetime(df_leads['Data_Cadastro']).dt.strftime('%m/%Y')
        fig2 = px.line(df_leads.groupby('Mes')['Valor'].sum().reset_index(), x='Mes', y='Valor', title="Evolução Mensal")
        fig2.update_traces(line_color='#e91e63')
        fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
        col2.plotly_chart(fig2, use_container_width=True)

    # 5. CONFIGURAÇÃO DE EQUIPE (GESTOR)
    elif st.session_state['menu'] == "Config":
        st.markdown("<h1 class='gradient-text'>EQUIPE & ACESSOS</h1>", unsafe_allow_html=True)
        u_df = load_users()
        
        with st.expander("ADICIONAR NOVO MEMBRO"):
            with st.form("add_user"):
                nn = st.text_input("Nome"); nu = st.text_input("Usuário"); np = st.text_input("Senha"); nc = st.selectbox("Cargo", ["CRC", "Gestor"])
                if st.form_submit_button("CRIAR"):
                    u_df = pd.concat([u_df, pd.DataFrame([{'nome':nn,'user':nu,'pass':np,'cargo':nc}])], ignore_index=True)
                    save_data(u_df, USER_FILE); st.rerun()
        
        for i, r in u_df.iterrows():
            with st.container():
                st.markdown(f'<div class="glass-card"><b>{r["nome"]}</b> | Cargo: {r["cargo"]} | User: {r["user"]}</div>', unsafe_allow_html=True)
                col1, col2, _ = st.columns([2, 2, 4])
                if r['user'] != 'admin':
                    if col1.button(f"REFAZER SENHA", key=f"res_{i}"): st.session_state[f"reset_{i}"] = True
                    if col2.button(f"EXCLUIR ACESSO", key=f"del_{i}"): 
                        u_df = u_df.drop(i); save_data(u_df, USER_FILE); st.rerun()
                    
                    if st.session_state.get(f"reset_{i}"):
                        ns = st.text_input("Nova Senha", key=f"ns_{i}")
                        if st.button("SALVAR SENHA", key=f"btn_{i}"):
                            u_df.at[i, 'pass'] = ns; save_data(u_df, USER_FILE); st.success("Senha alterada!"); st.rerun()
