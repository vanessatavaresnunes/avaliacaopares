from src.models.usuario import UsuarioModel
"""
Modelo de dados para avaliações de pares.
Responsável pela estrutura de dados e validações.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path
import pandas as pd
import os
import unicodedata


@dataclass
class Avaliacao:
    """Classe que representa uma avaliação individual"""
    timestamp: str
    id_avaliador: int
    time: str
    id_avaliado: int
    eixo: str
    nota: int
    feedback: str


class AvaliacaoModel:
    """Modelo responsável por gerenciar os dados de avaliação"""
    
    def __init__(self, diretorio_dados: str = "dados"):
        self.diretorio_dados = diretorio_dados
        self._criar_diretorio_se_nao_existe()
        self.usuario_model = UsuarioModel()
    
    def _criar_diretorio_se_nao_existe(self):
        """Cria o diretório de dados se não existir"""
        Path(self.diretorio_dados).mkdir(parents=True, exist_ok=True)
    
    def salvar_avaliacoes(self, id_avaliador: int, time: str, sprint: str, 
                         avaliacoes: Dict, nomes_eixos: List[str], nome_avaliador: str) -> str:
        """
        Salva as avaliações em arquivo json
        
        Args:
            id_avaliador: ID do aluno que fez a avaliação
            time: Time do avaliador
            sprint: Sprint que está sendo avaliada
            avaliacoes: Dicionário com as avaliações
            nomes_eixos: Lista com os nomes dos eixos de avaliação
            
        Returns:
            Caminho do arquivo salvo
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Preparar dados para salvar
        dados_para_salvar = []
        for id_avaliado, notas in avaliacoes.items():
            nome_avaliado = self.usuario_model.obter_nome_aluno(id_avaliado)
            for i, nome_eixo in enumerate(nomes_eixos):
                feedback_normalizado = unicodedata.normalize('NFC', notas['feedbacks'][i])
                dados_para_salvar.append({
                    'timestamp': timestamp,
                    'sprint': sprint,
                    'id_avaliador': id_avaliador,
                    'nome_avaliador': nome_avaliador,
                    'time': time,
                    'id_avaliado': id_avaliado,
                    'nome_avaliado': nome_avaliado,
                    'eixo': nome_eixo,
                    'nota': notas['notas'][i],
                    'feedback': feedback_normalizado
                })
        
        df = pd.DataFrame(dados_para_salvar)
        
        # Salvar arquivo individual
        arquivo = Path(self.diretorio_dados) / f'avaliacoes_{timestamp}.json'
        df.to_json(str(arquivo), orient='records', lines=True, force_ascii=False)
        
        # Salvar arquivo consolidado
        self._salvar_arquivo_consolidado(df)
        
        return arquivo
    
    def _salvar_arquivo_consolidado(self, df_novo: pd.DataFrame):
        """Salva ou atualiza o arquivo consolidado"""
        arquivo_consolidado = Path(self.diretorio_dados) / 'avaliacoescompletas_consolidadas.json'
        
        if arquivo_consolidado.exists():
            df_existente = pd.read_json(str(arquivo_consolidado), orient='records', lines=True, encoding='utf-8')
            df_consolidado = pd.concat([df_existente, df_novo], ignore_index=True)
        else:
            df_consolidado = df_novo
        
        df_consolidado.to_json(str(arquivo_consolidado), orient='records', lines=True, force_ascii=False)
    
    def carregar_dados(self) -> pd.DataFrame:
        """
        Carrega todos os dados de avaliação
        
        Returns:
            DataFrame com todos os dados ou DataFrame vazio se não existir
        """
        arquivo_consolidado = Path(self.diretorio_dados) / 'avaliacoescompletas_consolidadas.json'
        
        if arquivo_consolidado.exists():
            return pd.read_json(str(arquivo_consolidado), orient='records', lines=True, encoding='utf-8')
        else:
            return pd.DataFrame()
    
    def validar_soma_notas_por_eixo(self, avaliacoes: Dict, ids_alunos_time: List[int], nomes_eixos: List[str]) -> Dict[str, Dict[str, any]]:
        """
        Valida se a soma das notas de cada eixo é igual ao esperado, e retorna detalhes.

        Args:
            avaliacoes: Dicionário com as avaliações.
            ids_alunos_time: Lista de IDs de alunos do time.
            nomes_eixos: Lista com os nomes dos eixos.

        Returns:
            Dicionário com o status de validação para cada eixo, incluindo soma atual e esperada.
        """
        resultados = {}
        num_alunos = len(ids_alunos_time)
        pontos_esperados = num_alunos + 1
        for i, nome_eixo in enumerate(nomes_eixos):
            soma_notas_atual = sum(avaliacoes[id_aluno]['notas'][i] for id_aluno in ids_alunos_time)
            resultados[nome_eixo] = {
                'valido': (soma_notas_atual == pontos_esperados),
                'soma_atual': soma_notas_atual,
                'soma_esperada': pontos_esperados
            }
        return resultados

    def validar_notas_individuais(self, avaliacoes: Dict, ids_alunos_time: List[int], nomes_eixos: List[str], nota_maxima: int, num_integrantes_grupo: int) -> bool:
        """
        Valida se as notas individuais não excedem o valor máximo e a regra N/2.

        Args:
            avaliacoes: Dicionário com as avaliações.
            ids_alunos_time: Lista de IDs de alunos do time.
            nomes_eixos: Lista com os nomes dos eixos.
            nota_maxima: Nota máxima permitida.
            num_integrantes_grupo: Número total de integrantes do grupo (N).

        Returns:
            True se todas as notas são válidas, False caso contrário.
        """
        max_nota_n_div_2 = int(num_integrantes_grupo / 2)
        for id_aluno in ids_alunos_time:
            for i in range(len(nomes_eixos)):
                nota = avaliacoes[id_aluno]['notas'][i]
                if nota > nota_maxima or nota > max_nota_n_div_2:
                    return False
        return True

    def validar_preenchimento_feedbacks(self, avaliacoes: Dict, ids_alunos_time: List[int], nomes_eixos: List[str]) -> bool:
        """
        Valida se todos os campos de feedback foram preenchidos.

        Args:
            avaliacoes: Dicionário com as avaliações.
            ids_alunos_time: Lista de IDs de alunos do time.
            nomes_eixos: Lista com os nomes dos eixos.

        Returns:
            True se todos os feedbacks foram preenchidos, False caso contrário.
        """
        for id_aluno in ids_alunos_time:
            for i in range(len(nomes_eixos)):
                feedback_content = avaliacoes[id_aluno]['feedbacks'][i]
                if feedback_content is None or not feedback_content.strip():
                    return False
        return True

    def validar_feedbacks_unicos(self, avaliacoes: Dict, ids_alunos_time: List[int], nomes_eixos: List[str]) -> bool:
        """
        Valida se os feedbacks para um mesmo aluno são únicos.

        Args:
            avaliacoes: Dicionário com as avaliações.
            ids_alunos_time: Lista de IDs de alunos do time.
            nomes_eixos: Lista com os nomes dos eixos.

        Returns:
            True se os feedbacks são únicos, False caso contrário.
        """
        for id_aluno in ids_alunos_time:
            feedbacks_aluno = [unicodedata.normalize('NFC', avaliacoes[id_aluno]['feedbacks'][i]).strip() for i in range(len(nomes_eixos))]
            if len(feedbacks_aluno) != len(set(feedbacks_aluno)):
                return False
        return True

    def validar_conteudo_feedbacks(self, avaliacoes: Dict, ids_alunos_time: List[int], nomes_eixos: List[str]) -> bool:
        """
        Valida se os feedbacks não contêm caracteres inválidos (ex: emojis) e se contêm mais de uma palavra.

        Args:
            avaliacoes: Dicionário com as avaliações.
            ids_alunos_time: Lista de IDs de alunos do time.
            nomes_eixos: Lista com os nomes dos eixos.

        Returns:
            True se o conteúdo dos feedbacks é válido, False caso contrário.
        """
        import re
        # Expressão regular para detectar emojis
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "]+",
            flags=re.UNICODE,
        )
        # Expressão regular para verificar se há pelo menos duas palavras
        two_words_pattern = re.compile(r"\b\w+\b(?:\s+\b\w+\b){1,}")

        for id_aluno in ids_alunos_time:
            for i in range(len(nomes_eixos)):
                feedback = unicodedata.normalize('NFC', avaliacoes[id_aluno]['feedbacks'][i])
                if emoji_pattern.search(feedback):
                    return False
                if not two_words_pattern.search(feedback):
                    return False
        return True

    def validar_avaliacoes(self, avaliacoes: Dict, ids_alunos_time: List[int], nomes_eixos: List[str], config: Dict, num_integrantes_grupo: int) -> Dict[str, any]:
        """
        Executa todas as validações e retorna um dicionário com os resultados.

        Args:
            avaliacoes: Dicionário com as avaliações.
            ids_alunos_time: Lista de IDs de alunos do time.
            nomes_eixos: Lista com os nomes dos eixos.
            config: Dicionário de configuração.

        Returns:
            Dicionário com os resultados de cada validação.
        """
        resultados = {}

        # Validação da soma das notas por eixo
        resultados['soma_notas'] = self.validar_soma_notas_por_eixo(avaliacoes, ids_alunos_time, nomes_eixos)

        # Validação de notas individuais
        resultados['notas_individuais'] = self.validar_notas_individuais(avaliacoes, ids_alunos_time, nomes_eixos, config['nota_maxima'], num_integrantes_grupo)

        # Validação de preenchimento de feedbacks
        resultados['feedbacks_preenchidos'] = self.validar_preenchimento_feedbacks(avaliacoes, ids_alunos_time, nomes_eixos)

        # Validação de feedbacks únicos
        resultados['feedbacks_unicos'] = self.validar_feedbacks_unicos(avaliacoes, ids_alunos_time, nomes_eixos)

        # Validação de conteúdo de feedbacks
        resultados['conteudo_feedbacks'] = self.validar_conteudo_feedbacks(avaliacoes, ids_alunos_time, nomes_eixos)
        
        return resultados
    
    def obter_estatisticas(self, df: pd.DataFrame) -> Dict:
        """
        Calcula estatísticas dos dados de avaliação
        
        Args:
            df: DataFrame com os dados
            
        Returns:
            Dicionário com estatísticas
        """
        if df.empty:
            return {
                'total_avaliacoes': 0,
                'alunos_avaliadores': 0,
                'times': 0,
                'periodo': 'N/A'
            }
        
        return {
            'total_avaliacoes': len(df),
            'alunos_avaliadores': df['id_avaliador'].nunique(),
            'times': df['time'].nunique(),
            'periodo': f"{df['timestamp'].min()[:8]} a {df['timestamp'].max()[:8]}"
        }
