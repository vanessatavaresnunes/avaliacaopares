"""
Modelos de dados do Sistema de Avaliação de Pares.
Responsáveis pela estrutura de dados e regras de negócio.
"""

from .avaliacao import AvaliacaoModel, Avaliacao
from .usuario import UsuarioModel, Configuracao

__all__ = ['AvaliacaoModel', 'Avaliacao', 'UsuarioModel', 'Configuracao']
