# --- CSS ATUALIZADO (BOTÕES MINIMALISTAS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;900&display=swap');
    
    .stApp { background: #050507; color: #ffffff; font-family: 'Inter', sans-serif; }
    
    /* SIDEBAR */
    [data-testid="stSidebar"] { 
        background-color: #000000 !important; 
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }

    /* BOTÕES DA SIDEBAR - ESTILO MINIMALISTA */
    div.stButton > button {
        background: transparent !important; /* Fundo transparente por padrão */
        color: #94a3b8 !important; /* Cor cinza azulado discreto */
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 6px !important;
        padding: 6px 15px !important; /* Botão mais baixo e menos largo */
        font-size: 10px !important; /* Fonte pequena */
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 1.5px; /* Espaçamento entre letras para luxo */
        width: auto !important; /* Não ocupa a tela toda */
        margin: 5px 0 !important;
        transition: 0.4s;
    }

    /* HOVER - BRILHO DISCRETO */
    div.stButton > button:hover {
        background: linear-gradient(90deg, #8e44ad 0%, #e91e63 100%) !important;
        color: white !important;
        border: none !important;
        transform: translateX(5px); /* Desloca levemente para o lado em vez de subir */
        box-shadow: 0 0 15px rgba(233, 30, 99, 0.2);
    }

    /* TAGS DE STATUS (MANTIDAS) */
    .tag-agendado { background: #2ecc71; color: #000; padding: 2px 8px; border-radius: 4px; font-weight: 800; font-size: 9px; text-transform: uppercase; }
    .tag-pendente { background: #f1c40f; color: #000; padding: 2px 8px; border-radius: 4px; font-weight: 800; font-size: 9px; text-transform: uppercase; }
    .tag-followup { background: #e91e63; color: #fff; padding: 2px 8px; border-radius: 4px; font-weight: 800; font-size: 9px; text-transform: uppercase; }
    
    .gradient-text {
        background: linear-gradient(90deg, #a855f7, #e91e63);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-weight: 900;
        letter-spacing: -1px;
    }
    </style>
    """, unsafe_allow_html=True)
