import streamlit as st
import pandas as pd
import os
from datetime import datetime, date
from PIL import Image
import plotly.express as px

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="OrthoKlin | Gestão de Leads", layout="wide")

# --- CSS PERSONALIZADO (DESIGN PREMIUM & MINIMALISTA) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;900&display=swap');
    .stApp { background: #050507; color: #ffffff; font-family: 'Inter', sans-serif; }
    
    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #000000 !important; border-right: 1px solid rgba(255, 255, 255, 0.05); width: 260px !important; }

    /* Botões Minimalistas da Sidebar */
    div.stButton > button {
        background: transparent !important; color: #94a3b8 !important; border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 4px !important; padding: 4px 12px !important; font-size: 10px !important; font-weight: 600 !important;
        text-transform: uppercase; letter-spacing: 1.2px; width: 100% !important; margin-top: 10px; transition: 0.3s;
    }
    div.stButton > button:hover { background: linear-gradient(90deg, #8e44ad 0%, #e91e63 100%) !important; color: white !important; border: none !important; transform: translateX(3px); }

    /* Tags de Status */
    .tag-agendado { background: #2ecc71; color: #000; padding: 2px 8px; border-radius: 4px; font-weight: 800; font-size: 9px; text-transform: uppercase; }
    .tag-pendente { background: #f1c40f; color: #000; padding: 2px 8px; border-radius: 4px; font-weight: 800; font-size: 9px; text-transform: uppercase; }
    .tag-followup { background: #e91e63; color: #fff; padding: 2px 8px; border-radius: 4px; font-weight: 800; font-size: 9px; text-transform: uppercase; }
    .data-alerta { color: #ff4b4b; font-weight: 700; }
    
    /* Cards */
    .glass-card { background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 20px; margin-bottom: 15px; }
    .gradient-text { background: linear-gradient(90deg, #a855f7, #e91e63); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO DE RENDERIZAÇÃO DA LOGO ---
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

# --- BANCO DE DADOS (CSV) ---
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

# --- ESTADOS DO SISTEMA ---
if 'logado' not in st.session_state: st.session_state['logado'] = False
if 'auth_mode' not in st.session_state: st.session_state['auth_mode'] = "login"
if 'menu' not in st.session_state: st.session_state['menu'] = "Dash"

# --- TELA DE ACESSO ---
if not st.session_state['logado']:
    _, col, _ = st.columns([1, 1, 1])
    with col:
        st.write("####")
        render_logo()
        
        if st.session_state['auth_mode'] == "login":
            u = st.text_input("USUÁRIO", placeholder="admin")
            p = st.text_input("SENHA", type="password", placeholder="••••••")
            if st.button("ACESSAR"):
                # Verifica admin ou novo usuário criado na sessão
                if (u == "admin" and p == "ortho2026") or (u == st.session_state.get('novo_u') and p == st.session_state.get('novo_p')):
                    st.session_state['logado'] = True
                    st.rerun()
                else: st.error("Credenciais Inválidas.")
            
            c1, c2 = st.columns(2)
            if c1.button("CRIAR PERFIL"): st.session_state['auth_mode'] = "cadastro"; st.rerun()
            if c2.button("PERDI A SENHA"): st.session_state['auth_mode'] = "recuperar"; st.rerun()

        elif st.session_state['auth_mode'] == "cadastro":
            st.markdown("<h3 style='text-align:center;'>NOVO ACESSO</h3>", unsafe_allow_html=True)
            nu = st.text_input("USUÁRIO")
            np = st.text_input("SENHA", type="password")
            npc = st.text_input("CONFIRME A SENHA", type="password")
            if st.button("FINALIZAR E ENTRAR"):
                if nu and np == npc and len(np) > 3:
                    st.session_state['novo_u'], st.session_state['novo_p'] = nu, np
                    st.session_state['logado'] = True
                    st.rerun()
                else: st.error("Erro nos dados.")
            if st.button("VOLTAR"): st.session_state['auth_mode'] = "login"; st.rerun()

        elif st.session_state['auth_mode'] == "recuperar":
            st.markdown("<h3 style='text-align:center;'>RECUPERAR</h3>", unsafe_allow_html=True)
            st.text_input("E-MAIL")
            if st.button("ENVIAR"): st.info("Instruções enviadas.")
            if st.button("VOLTAR"): st.session_state['auth_mode'] = "login"; st.rerun()

# --- ÁREA INTERNA ---
else:
    df = load_data()
    with st.sidebar:
        render_logo()
        st.write("###")
        if st.button("DASHBOARD"): st.session_state['menu'] = "Dash"
        if st.button("GESTAO DE LEADS"): st.session_state['menu'] = "Gestao"
        if st.button("NOVO CADASTRO"): st.session_state['menu'] = "Novo"
        st.write("---")
        if st.button("SAIR"): 
            st.session_state['logado'] = False
            st.session_state['auth_mode'] = "login"
            st.rerun()

    # 📊 DASHBOARD COMPLETO
    if st.session_state['menu'] == "Dash":
        st.markdown("<h1 class='gradient-text'>DESEMPENHO</h1>", unsafe_allow_html=True)
        col_f1, col_f2 = st.columns(2)
        d_ini = col_f1.date_input("INÍCIO", date.today().replace(day=1))
        d_fim = col_f2.date_input("FIM", date.today())
        
        df_p = df[(df['Data_Cadastro'] >= d_ini) & (df['Data_Cadastro'] <= d_fim)]
        
        c1, c2, c3 = st.columns(3)
        c1.markdown(f'<div class="glass-card"><small>VALOR PERÍODO</small><br><b>R$ {df_p["Valor"].sum():,.2f}</b></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="glass-card"><small>NOVOS LEADS</small><br><b>{len(df_p)}</b></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="glass-card"><small>RETORNOS HOJE</small><br><b>{len(df[df["Data_Retorno"] == date.today()])}</b></div>', unsafe_allow_html=True)

        if not df_p.empty:
            fig = px.bar(df_p.groupby('Data_Cadastro')['Valor'].sum().reset_index(), x='Data_Cadastro', y='Valor')
            fig.update_traces(marker_color='#e91e63')
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
            st.plotly_chart(fig, use_container_width=True)

    # 👥 GESTÃO COM DADOS COMPLETOS
    elif st.session_state['menu'] == "Gestao":
        st.markdown("<h1 class='gradient-text'>GESTÃO</h1>", unsafe_allow_html=True)
        busca = st.text_input("BUSCAR NOME OU CPF")
        df_f = df[df['Nome'].str.contains(busca, case=False) | df['CPF'].str.contains(busca)] if busca else df
        
        for idx, row in df_f.sort_values(by='Data_Retorno').iterrows():
            hoje = date.today()
            tag = "tag-followup" if row['Status'] == "Follow-up" else "tag-agendado" if row['Status'] == "Agendado" else "tag-pendente"
            cor_data = "data-alerta" if row['Data_Retorno'] <= hoje and row['Status'] != 'Em tratamento' else ""
            
            with st.container():
                st.markdown(f"""
                    <div class="glass-card">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span style="font-weight:600;">{row['Nome'].upper()}</span>
                            <span class="{tag}">{row['Status']}</span>
                        </div>
                        <div style="font-size:11px; margin-top:10px; color:#64748b;">
                            CPF: {row['CPF']} | CANAL: {row['Origem']} | <span class="{cor_data}">RETORNO: {row['Data_Retorno'].strftime('%d/%m/%Y')}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                b1, b2, b3, _ = st.columns([1, 1, 2, 4])
                if b1.button("EDITAR", key=f"e_{idx}"): st.session_state['edit_idx'] = idx
                if b2.button("APAGAR", key=f"r_{idx}"): df = df.drop(idx); save_data(df); st.rerun()
                wa = f"https://api.whatsapp.com/send?phone={row['Telefone']}"
                b3.markdown(f'<a href="{wa}" target="_blank"><button style="background:#25d366; color:white; border:none; padding:8px; border-radius:6px; width:100%; font-weight:700; cursor:pointer; font-size:10px; text-transform:uppercase;">WhatsApp</button></a>', unsafe_allow_html=True)

                if 'edit_idx' in st.session_state and st.session_state['edit_idx'] == idx:
                    with st.form(f"ed_{idx}"):
                        nv_s = st.selectbox("Status", ["Pendente", "Agendado", "Follow-up", "Em tratamento"])
                        nv_v = st.number_input("Valor", value=float(row['Valor']))
                        nv_r = st.date_input("Data Retorno", value=row['Data_Retorno'])
                        if st.form_submit_button("SALVAR"):
                            df.at[idx, 'Status'], df.at[idx, 'Valor'], df.at[idx, 'Data_Retorno'] = nv_s, nv_v, nv_r
                            save_data(df); del st.session_state['edit_idx']; st.rerun()

    # ➕ NOVO CADASTRO COMPLETO
    elif st.session_state['menu'] == "Novo":
        st.markdown("<h1 class='gradient-text'>CADASTRO</h1>", unsafe_allow_html=True)
        with st.form("cad"):
            nome = st.text_input("NOME COMPLETO")
            c1, c2 = st.columns(2); cpf = c1.text_input("CPF"); tel = c2.text_input("TELEFONE (DDD + NÚMERO)")
            c3, c4 = st.columns(2); orig = c3.selectbox("ORIGEM", ["Instagram", "Google Ads", "Facebook", "Indicação"]); stat = c4.selectbox("STATUS", ["Pendente", "Follow-up"])
            val = st.number_input("VALOR ORÇAMENTO", min_value=0.0)
            ret = st.date_input("DATA DE RETORNO", value=date.today())
            if st.form_submit_button("REGISTRAR PACIENTE"):
                if nome and cpf and tel:
                    novo = {'Nome': nome, 'CPF': cpf, 'Telefone': tel, 'Origem': orig, 'Status': stat, 'Valor': val, 'Data_Cadastro': date.today(), 'Data_Retorno': ret}
                    df = pd.concat([df, pd.DataFrame([novo])], ignore_index=True); save_data(df); st.success("Registrado!"); st.rerun()
                else: st.warning("Preencha Nome, CPF e Telefone.")
