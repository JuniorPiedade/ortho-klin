# --- SISTEMA DE LOGIN MELHORADO ---
if 'logado' not in st.session_state:
    st.session_state['logado'] = False

if 'users' not in st.session_state:
    st.session_state['users'] = {"admin": "ortho2026"}

if 'tela' not in st.session_state:
    st.session_state['tela'] = "login"


def tela_login():
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.write("#")
        render_logo()
        st.markdown("<p class='subtext' style='text-align:center;'>SISTEMA DE GESTÃO IA</p>", unsafe_allow_html=True)

        user = st.text_input("USUÁRIO")
        pw = st.text_input("SENHA", type="password")

        if st.button("ACESSAR"):
            if user in st.session_state['users'] and st.session_state['users'][user] == pw:
                st.session_state['logado'] = True
                st.rerun()
            else:
                st.error("Credenciais inválidas")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Criar conta"):
                st.session_state['tela'] = "cadastro"
                st.rerun()
        with col2:
            if st.button("Esqueci a senha"):
                st.session_state['tela'] = "recuperar"
                st.rerun()


def tela_cadastro():
    st.markdown("<h2 class='gradient-text'>Criar Conta</h2>", unsafe_allow_html=True)

    new_user = st.text_input("Novo usuário")
    new_pw = st.text_input("Nova senha", type="password")

    if st.button("Cadastrar"):
        st.session_state['users'][new_user] = new_pw
        st.success("Conta criada com sucesso!")
        st.session_state['tela'] = "login"
        st.rerun()

    if st.button("Voltar"):
        st.session_state['tela'] = "login"
        st.rerun()


def tela_recuperar():
    st.markdown("<h2 class='gradient-text'>Recuperar Senha</h2>", unsafe_allow_html=True)

    user = st.text_input("Digite seu usuário")

    if st.button("Recuperar"):
        if user in st.session_state['users']:
            st.info(f"Sua senha é: {st.session_state['users'][user]}")
        else:
            st.error("Usuário não encontrado")

    if st.button("Voltar"):
        st.session_state['tela'] = "login"
        st.rerun()


if not st.session_state['logado']:
    if st.session_state['tela'] == "login":
        tela_login()
    elif st.session_state['tela'] == "cadastro":
        tela_cadastro()
    elif st.session_state['tela'] == "recuperar":
        tela_recuperar()
