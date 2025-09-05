"""
Visualizador de dados do Sistema de Avaliação de Pares.
Implementado seguindo o padrão MVC (Model-View-Controller).

Agora protegido por login estático (uso docente).
"""

import os
import streamlit as st
from dotenv import load_dotenv
from src.views.visualizacao_view import VisualizacaoView

from src.controllers.avaliacao_controller import AvaliacaoController

# Carrega variáveis do .env
load_dotenv()

# Credenciais do dashboard do professor via .env
ADMIN_USERNAME = os.getenv("PROFESSOR_EMAIL", "")
ADMIN_PASSWORD = os.getenv("PROFESSOR_PASSWORD", "")


def configurar_pagina():
    """Configura as configurações da página Streamlit"""
    st.set_page_config(
        page_title="Visualizador de Avaliações",
        page_icon="📈",
        layout="wide"
    )


def main():
    """Função principal do visualizador"""
    # Configurar página
    configurar_pagina()
    
    # Inicializar controller
    controller = AvaliacaoController()

    # Estado de autenticação do visualizador
    if 'viz_logado' not in st.session_state:
        st.session_state.viz_logado = False

    if not st.session_state.viz_logado:
        # Tela de login simples
        st.title("🔐 Login do Professor")
        st.markdown("Insira suas credenciais para acessar o visualizador de avaliações.")

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if not ADMIN_USERNAME or not ADMIN_PASSWORD:
                st.warning("Credenciais não configuradas. Defina PROFESSOR_EMAIL e PROFESSOR_PASSWORD no arquivo .env.")
            usuario = st.text_input("Usuário", key="viz_user")
            senha = st.text_input("Senha", type="password", key="viz_pass")
            entrar = st.button("Entrar", type="primary")

            if entrar:
                if usuario == ADMIN_USERNAME and senha == ADMIN_PASSWORD:
                    st.session_state.viz_logado = True
                    st.success("Acesso concedido.")
                    st.rerun()
                else:
                    st.error("Credenciais inválidas.")
        return

    # Header e botão de logout quando autenticado
    st.sidebar.success("Acesso: Professor")
    if st.sidebar.button("Sair"):
        st.session_state.viz_logado = False
        st.session_state.pop('viz_user', None)
        st.session_state.pop('viz_pass', None)
        st.rerun()

    # Mostrar tela de visualização
    visualizacao_view = VisualizacaoView(controller)
    visualizacao_view.renderizar()


if __name__ == "__main__":
    main()
