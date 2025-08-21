"""
Views do Sistema de Avaliação de Pares.
Responsáveis pela interface do usuário e apresentação dos dados.
"""

from .login_view import LoginView
from .avaliacao_view import AvaliacaoView
from .visualizacao_view import VisualizacaoView

__all__ = ['LoginView', 'AvaliacaoView', 'VisualizacaoView']
