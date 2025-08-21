"""
Visualizador de dados do Sistema de Avaliação de Pares.
Implementado seguindo o padrão MVC (Model-View-Controller).
"""

import streamlit as st
from src.controllers.avaliacao_controller import AvaliacaoController
from src.views.visualizacao_view import VisualizacaoView


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
    
    # Mostrar tela de visualização
    visualizacao_view = VisualizacaoView(controller)
    visualizacao_view.renderizar()


if __name__ == "__main__":
    main()
