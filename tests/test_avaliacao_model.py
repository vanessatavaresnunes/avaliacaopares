"""
Testes unitários para o modelo de avaliação.
Demonstra boas práticas de testes e cobertura de código.
"""

import unittest
import tempfile
import os
import pandas as pd
from unittest.mock import patch
from src.models.avaliacao import AvaliacaoModel, Avaliacao


class TestAvaliacaoModel(unittest.TestCase):
    """Testes para a classe AvaliacaoModel"""
    
    def setUp(self):
        """Configuração inicial para cada teste"""
        self.temp_dir = tempfile.mkdtemp()
        self.model = AvaliacaoModel(diretorio_dados=self.temp_dir)
    
    def tearDown(self):
        """Limpeza após cada teste"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_criar_diretorio_se_nao_existe(self):
        """Testa criação de diretório quando não existe"""
        novo_dir = os.path.join(self.temp_dir, "novo_diretorio")
        model = AvaliacaoModel(diretorio_dados=novo_dir)
        
        self.assertTrue(os.path.exists(novo_dir))
    
    def test_validar_notas_valido(self):
        """Testa validação de notas válidas"""
        notas = [1, 2, 1]  # Soma = 4, num_alunos = 3
        resultado = self.model.validar_notas(notas, 3)
        self.assertTrue(resultado)
    
    def test_validar_notas_invalido(self):
        """Testa validação de notas inválidas"""
        notas = [1, 1, 1]  # Soma = 3, num_alunos = 3 (deveria ser 4)
        resultado = self.model.validar_notas(notas, 3)
        self.assertFalse(resultado)
    
    def test_validar_avaliacoes_completas(self):
        """Testa validação de avaliações completas"""
        avaliacoes = {
            'Aluno1': {'notas': [1, 1, 1], 'feedbacks': ['', '', '']},
            'Aluno2': {'notas': [1, 1, 1], 'feedbacks': ['', '', '']},
            'Aluno3': {'notas': [1, 1, 1], 'feedbacks': ['', '', '']}
        }
        alunos_time = ['Aluno1', 'Aluno2', 'Aluno3']
        
        resultado = self.model.validar_avaliacoes_completas(avaliacoes, alunos_time)
        
        # Todas as avaliações devem ser inválidas (soma = 3, deveria ser 4)
        self.assertFalse(all(resultado.values()))
    
    def test_obter_estatisticas_dados_vazios(self):
        """Testa obtenção de estatísticas com dados vazios"""
        df = pd.DataFrame()
        estatisticas = self.model.obter_estatisticas(df)
        
        self.assertEqual(estatisticas['total_avaliacoes'], 0)
        self.assertEqual(estatisticas['alunos_avaliadores'], 0)
        self.assertEqual(estatisticas['times'], 0)
        self.assertEqual(estatisticas['periodo'], 'N/A')
    
    def test_obter_estatisticas_com_dados(self):
        """Testa obtenção de estatísticas com dados"""
        dados = {
            'timestamp': ['20231201_120000', '20231201_120001'],
            'aluno_avaliador': ['João', 'Maria'],
            'time': ['Time A', 'Time A'],
            'aluno_avaliado': ['Pedro', 'Ana'],
            'eixo': ['Colaboração', 'Responsabilidade'],
            'nota': [2, 3],
            'feedback': ['Bom trabalho', 'Excelente']
        }
        df = pd.DataFrame(dados)
        
        estatisticas = self.model.obter_estatisticas(df)
        
        self.assertEqual(estatisticas['total_avaliacoes'], 2)
        self.assertEqual(estatisticas['alunos_avaliadores'], 2)
        self.assertEqual(estatisticas['times'], 1)
        self.assertIn('20231201', estatisticas['periodo'])


class TestAvaliacao(unittest.TestCase):
    """Testes para a classe Avaliacao"""
    
    def test_criar_avaliacao(self):
        """Testa criação de uma avaliação"""
        avaliacao = Avaliacao(
            timestamp="20231201_120000",
            aluno_avaliador="João",
            time="Time A",
            aluno_avaliado="Maria",
            eixo="Colaboração",
            nota=3,
            feedback="Excelente trabalho em equipe"
        )
        
        self.assertEqual(avaliacao.timestamp, "20231201_120000")
        self.assertEqual(avaliacao.aluno_avaliador, "João")
        self.assertEqual(avaliacao.time, "Time A")
        self.assertEqual(avaliacao.aluno_avaliado, "Maria")
        self.assertEqual(avaliacao.eixo, "Colaboração")
        self.assertEqual(avaliacao.nota, 3)
        self.assertEqual(avaliacao.feedback, "Excelente trabalho em equipe")


if __name__ == '__main__':
    unittest.main()
