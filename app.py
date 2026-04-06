import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="OrthoKlin | Sistema de Inteligência",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS FUTURISTA MINIMALISTA (V14) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;900&display=swap');
    
    /* Configuração Global Dark */
    .stApp { 
        background: #050507; 
        color: #ffffff; 
        font-family: 'Inter', sans-serif; 
    }
    
    /* SIDEBAR PRETA MINIMALISTA */
    [data-testid="stSidebar"] { 
        background-color: #000000 !important; 
        border-right: 1px solid rgba(255, 255, 255, 0.05);
        width: 260px !important;
    }

    /* BOTÕES DA SIDEBAR - DESIGN ULTRA MINIMALISTA */
    div.stButton > button {
        background: transparent !important;
        color: #94a3b8 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 4px !important;
        padding: 4px 12px !important;
        font-size: 10px !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        width: 100% !important;
        margin-bottom: 8px !important;
        transition: all 0.3s ease;
        text-align: center;
    }

    /* HOVER DOS BOTÕES - ATIVAÇÃO NEON */
    div.stButton > button:hover {
        background: linear-gradient(90deg, #8e44ad 0%, #e91e63 100%) !important;
        color: white !important;
        border: none !important;
        transform: translateX(3px);
        box-shadow: 0 0 15px rgba(233, 30, 99, 0.2);
    }

    /* TAGS DE STATUS (SISTEMA DE CORES) */
    .tag-agendado { background: #2ecc71; color: #000; padding: 2px 8px; border-radius: 4px; font-weight: 800; font-size: 9px; text-transform: uppercase; }
    .tag-pendente { background: #f1c40f; color: #000; padding: 2px 8px; border-radius: 4px; font-weight: 800; font-size: 9px; text-transform: uppercase; }
    .tag-followup { background: #e91e63; color: #fff; padding: 2px 8px; border-radius: 4px; font-weight: 800; font-size: 9px; text-transform: uppercase; }
    .tag-tratamento { background: #3498db; color: #fff; padding: 2px 8px; border-radius: 4px; font-weight: 800; font-size: 9px; text-transform: uppercase; }

    /* CARDS EM GLASSMORPHISM */
    .glass-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        transition: 0.3s;
    }
    .glass-card:hover {
        border-color: rgba(233, 30, 99, 0.3);
    }
    
    /* TEXTO EM GRADIENTE */
    .gradient-text {
        background: linear-gradient(90deg, #a855f7, #e91e63);
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        letter-spacing: -0.5px;
    }

    /* Inputs e Forms */
    input { background: rgba(255,255,255,0.05) !important; color: white !important; border-radius: 8px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- BANCO DE DADOS (CSV) ---
FILE = 'leads_orthoklin.csv'

def load_data():
    if os.path.exists(FILE):
        df = pd.read_csv(FILE)
        df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce').fillna(0.0)
        df['CPF'] = df['CPF'].astype(str)
        return df
    return pd.DataFrame(columns=['Nome','CPF','Telefone','Origem','Status','Valor'])

def save_data(df):
    df.to_csv(FILE, index=False)

# --- LÓGICA DE SESSÃO ---
if 'logado' not in st.session_state: st.session_state['logado'] = False
if 'menu' not in st.session_state: st.session_state['menu'] = "Dash"

# --- TELA DE LOGIN ---
if not st.session_state['logado']:
    _, col, _ = st.columns([1, 1, 1])
    with col:
        st.write("###")
        if os.path.exists("logo.png"): 
            st.image("logo.png", use_container_width=True)
        st.markdown("<h2 class='gradient-text' style='text-align:center;'>ACESSO RESTRITO</h2>", unsafe_allow_html=True)
        u = st.text_input("USUÁRIO", placeholder="admin")
        p = st.text_input("SENHA", type="password", placeholder="••••••")
        if st.button("AUTENTICAR"):
            if u == "admin" and p == "ortho2026":
                st.session_state['logado'] = True
                st.rerun()
            else:
                st.error("Credenciais incorretas.")
else:
    df = load_data()
    
    # --- SIDEBAR (BOTÕES MINIMALISTAS) ---
    with st.sidebar:
        if os.path.exists("logo.png"): 
            st.image("logo.png", use_container_width=True)
        st.write("###")
        if st.button("DASHBOARD"): st.session_state['menu'] = "Dash"
        if st.button("GESTAO DE LEADS"): st.session_state['menu'] = "Gestao"
        if st.button("NOVO CADASTRO"): st.session_state['menu'] = "Novo"
        st.write("---")
        if st.button("SAIR DO SISTEMA"):
            st.session_state['logado'] = False
            st.rerun()

    # --- NAVEGAÇÃO ---
    
    # 1. DASHBOARD
    if st.session_state['menu'] == "Dash":
        st.markdown("<h1 class='gradient-text'>DESEMPENHO</h1>", unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="glass-card"><small style="color:#64748b; letter-spacing:1px;">TOTAL GERAL</small><br><b style="font-size:22px;">R$ {df["Valor"].sum():,.2f}</b></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="glass-card"><small style="color:#64748b; letter-spacing:1px;">PENDENTES</small><br><b style="font-size:22px; color:#f1c40f;">R$ {df[df["Status"] == "Pendente"]["Valor"].sum():,.2f}</b></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="glass-card"><small style="color:#64748b; letter-spacing:1px;">FOLLOW-UP</small><br><b style="font-size:22px; color:#e91e63;">{len(df[df["Status"] == "Follow-up"])}</b></div>', unsafe_allow_html=True)

        if not df.empty:
            fig = px.pie(df, names='Status', hole=0.7, 
                         color='Status',
                         color_discrete_map={'Agendado':'#2ecc71', 'Pendente':'#f1c40f', 'Follow-up':'#e91e63', 'Em tratamento':'#3498db'})
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white", showlegend=True, margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig, use_container_width=True)

    # 2. GESTÃO DE LEADS
    elif st.session_state['menu'] == "Gestao":
        st.markdown("<h1 class='gradient-text'>GESTÃO</h1>", unsafe_allow_html=True)
        busca = st.text_input("PESQUISAR NOME OU CPF", placeholder="Digite para filtrar...")
        
        df_f = df
        if busca:
            df_f = df[df['Nome'].str.contains(busca, case=False) | df['CPF'].str.contains(busca)]

        for idx, row in df_f.iterrows():
            # Lógica de cores das tags
            s = row['Status']
            tag_class = "tag-followup" if s == "Follow-up" else "tag-agendado" if s == "Agendado" else "tag-pendente" if s == "Pendente" else "tag-tratamento"
            
            with st.container():
                st.markdown(f"""
                    <div class="glass-card">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span style="font-size:16px; font-weight:600; letter-spacing:0.5px;">{row['Nome'].upper()}</span>
                            <span class="{tag_class}">{s}</span>
                        </div>
                        <div style="color:#555; font-size:11px; margin-top:8px; font-weight:400;">
                            ORÇAMENTO: R$ {row['Valor']:,.2f} | CPF: {row['CPF']} | CANAL: {row['Origem'].upper()}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                b_ed, b_rm, b_wa, _ = st.columns([1, 1, 2, 4])
                
                if b_ed.button("EDITAR", key=f"e_{idx}"): 
                    st.session_state['edit_idx'] = idx
                
                if b_rm.button("APAGAR", key=f"r_{idx}"):
                    df = df.drop(idx)
                    save_data(df)
                    st.rerun()
                
                link_wa = f"https://api.whatsapp.com/send?phone={row['Telefone']}"
                b_wa.markdown(f'<a href="{link_wa}" target="_blank" style="text-decoration:none;"><button style="background:#25d366; color:white; border:none; padding:8px; border-radius:6px; width:100%; font-weight:700; cursor:pointer; font-size:10px; text-transform:uppercase;">WhatsApp</button></a>', unsafe_allow_html=True)

                # Form de Edição (se ativo)
                if 'edit_idx' in st.session_state and st.session_state['edit_idx'] == idx:
                    with st.form(f"form_edit_{idx}"):
                        nv_val = st.number_input("Valor", value=float(row['Valor']))
                        nv_sta = st.selectbox("Status", ["Pendente", "Agendado", "Follow-up", "Em tratamento"], index=["Pendente", "Agendado", "Follow-up", "Em tratamento"].index(s))
                        if st.form_submit_button("SALVAR"):
                            df.at[idx, 'Valor'] = nv_val
                            df.at[idx, 'Status'] = nv_sta
                            save_data(df)
                            del st.session_state['edit_idx']
                            st.rerun()

    # 3. NOVO CADASTRO
    elif st.session_state['menu'] == "Novo":
        st.markdown("<h1 class='gradient-text'>CADASTRO</h1>", unsafe_allow_html=True)
        with st.form("new_entry"):
            n = st.text_input("NOME COMPLETO")
            c1, c2 = st.columns(2)
            cp = c1.text_input("CPF")
            tl = c2.text_input("TELEFONE (DDD + NÚMERO)")
            or_ = st.selectbox("ORIGEM", ["Instagram", "Google Ads", "Facebook", "Indicação"])
            st_ = st.selectbox("STATUS INICIAL", ["Pendente", "Agendado", "Follow-up"])
            vl = st.number_input("VALOR ESTIMADO R$", min_value=0.0)
            
            if st.form_submit_button("FINALIZAR REGISTRO"):
                if n and cp and tl:
                    new_row = {'Nome': n, 'CPF': cp, 'Telefone': tl, 'Origem': or_, 'Status': st_, 'Valor': vl}
                    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                    save_data(df)
                    st.success("Paciente registrado.")
                    st.rerun()
                else:
                    st.warning("Preencha os campos obrigatórios.")
