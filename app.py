"""
Aplicativo principal do Sistema de Avaliação de Pares.
Implementado seguindo o padrão MVC (Model-View-Controller).
"""

import streamlit as st
from src.controllers.avaliacao_controller import AvaliacaoController
from src.views.login_view import LoginView
from src.views.avaliacao_view import AvaliacaoView
from src.views.ativacao_view import AtivacaoView


def configurar_pagina():
    """Configura as configurações da página Streamlit"""
    st.set_page_config(
        page_title="Sistema de Avaliação de Pares",
        page_icon="📊",
        layout="wide"
    )


def main():
    """Função principal do aplicativo"""
    # Configurar página
    configurar_pagina()
    
    # Inicializar controller
    controller = AvaliacaoController()
    controller.inicializar_sessao()
    
    # Verificar se o usuário está logado
    if not controller.esta_logado():
        # Mostrar tela de login
        login_view = LoginView(controller)
        login_view.renderizar()
    else:
        # Verificar se é o primeiro acesso
        if st.session_state.get('primeiro_acesso', False):
            # Mostrar tela de ativação
            ativacao_view = AtivacaoView(controller)
            ativacao_view.renderizar()
        else:
            # Mostrar tela de avaliação
            avaliacao_view = AvaliacaoView(controller)
            avaliacao_view.renderizar()


if __name__ == "__main__":
    main()
