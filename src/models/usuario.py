"""
Modelo de dados para usuários e configurações do sistema.
Responsável por gerenciar dados de alunos, times e configurações.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
import unicodedata


@dataclass
class Configuracao:
    """Classe que representa as configurações do sistema"""
    nota_minima: int
    nota_maxima: int
    diretorio_dados: str


class UsuarioModel:
    """Modelo responsável por gerenciar dados de usuários e configurações"""
    
    def __init__(self, diretorio_config: str = "data"):
        """
        Inicializa o modelo carregando dados dos arquivos JSON
        
        Args:
            diretorio_config: Diretório onde estão os arquivos de configuração
        """
        self.diretorio_config = diretorio_config
        self.alunos = self._carregar_alunos()
        self.eixos = self._carregar_eixos()
        self.config = self._carregar_configuracao()
    
    def _carregar_alunos(self) -> Dict[str, List[Dict[str, str]]]:
        """Carrega dados dos alunos do arquivo JSON"""
        try:
            caminho_arquivo = Path(self.diretorio_config) / "alunos.json"
            with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                return json.load(arquivo)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Erro ao carregar alunos.json: {e}")
            return {}

    def validar_senha(self, time: str, aluno: str, senha: str) -> bool:
        """
        Valida a senha de um aluno
        
        Args:
            time: Nome do time
            aluno: Nome do aluno
            senha: Senha a ser verificada
            
        Returns:
            True se a senha estiver correta, False caso contrário
        """
        if time in self.alunos:
            for a in self.alunos[time]:
                if a['nome'] == aluno and a['senha'] == senha:
                    return True
        return False
    
    def _carregar_eixos(self) -> List[Dict[str, any]]:
        """Carrega eixos de avaliação do arquivo JSON"""
        try:
            caminho_arquivo = Path(self.diretorio_config) / "eixos.json"
            with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                eixos_data = json.load(arquivo)
                for eixo in eixos_data:
                    eixo['nome'] = unicodedata.normalize('NFC', eixo['nome'])
                    eixo['descricao'] = unicodedata.normalize('NFC', eixo['descricao'])
                    if 'observacoes' in eixo:
                        eixo['observacoes'] = [unicodedata.normalize('NFC', obs) for obs in eixo['observacoes']]
                return eixos_data
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Erro ao carregar eixos.json: {e}")
            return []
    
    def _carregar_configuracao(self) -> Dict:
        """Carrega configurações do sistema do arquivo JSON"""
        try:
            caminho_arquivo = Path(self.diretorio_config) / "config.json"
            with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                return json.load(arquivo)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Erro ao carregar config.json: {e}")
            return {"nota_minima": 0, "nota_maxima": 3, "diretorio_dados": "dados"}
    
    def obter_times(self) -> List[str]:
        """Retorna lista de times disponíveis"""
        return list(self.alunos.keys())
    
    def obter_alunos_por_time(self, time: str) -> List[Dict[str, any]]:
        """
        Retorna lista de alunos de um time específico
        
        Args:
            time: Nome do time
            
        Returns:
            Lista de dicionários de alunos do time
        """
        return self.alunos.get(time, [])
    
    def obter_alunos_time_excluindo(self, time: str, aluno_excluir: str) -> List[Dict[str, any]]:
        """
        Retorna lista de alunos de um time excluindo um aluno específico
        
        Args:
            time: Nome do time
            aluno_excluir: Nome do aluno a ser excluído
            
        Returns:
            Lista de alunos do time sem o aluno excluído
        """
        alunos_time = self.obter_alunos_por_time(time)
        return [aluno for aluno in alunos_time if aluno['nome'] != aluno_excluir]
    
    def obter_aluno_por_nome(self, nome_aluno: str) -> Optional[Dict[str, any]]:
        """
        Retorna os dados de um aluno pelo nome.

        Args:
            nome_aluno: Nome do aluno a ser buscado.

        Returns:
            Dicionário com os dados do aluno ou None se não encontrado.
        """
        for time in self.alunos.values():
            for aluno in time:
                if unicodedata.normalize('NFC', aluno['nome']) == unicodedata.normalize('NFC', nome_aluno):
                    return aluno
        return None

    def obter_aluno_por_id(self, id_aluno: int) -> Optional[Dict[str, any]]:
        """
        Retorna os dados de um aluno pelo ID.

        Args:
            id_aluno: ID do aluno a ser buscado.

        Returns:
            Dicionário com os dados do aluno ou None se não encontrado.
        """
        for time in self.alunos.values():
            for aluno in time:
                if aluno['id'] == id_aluno:
                    return aluno
        return None

    def obter_id_aluno(self, nome_aluno: str) -> Optional[int]:
        """
        Retorna o ID de um aluno pelo nome.

        Args:
            nome_aluno: Nome do aluno.

        Returns:
            ID do aluno ou None se não encontrado.
        """
        aluno = self.obter_aluno_por_nome(nome_aluno)
        return aluno['id'] if aluno else None

    def obter_nome_aluno(self, id_aluno: int) -> Optional[str]:
        """
        Retorna o nome de um aluno pelo ID.

        Args:
            id_aluno: ID do aluno.

        Returns:
            Nome do aluno ou None se não encontrado.
        """
        aluno = self.obter_aluno_por_id(id_aluno)
        return aluno['nome'] if aluno else None

    def obter_eixos(self) -> List[Dict[str, any]]:
        """Retorna lista de eixos de avaliação com nome, descrição e observações"""
        return self.eixos.copy()
    
    def obter_nomes_eixos(self) -> List[str]:
        """Retorna lista apenas com os nomes dos eixos de avaliação"""
        return [eixo["nome"] for eixo in self.eixos]
    
    def obter_descricao_eixo(self, nome_eixo: str) -> str:
        """
        Retorna a descrição de um eixo específico
        
        Args:
            nome_eixo: Nome do eixo
            
        Returns:
            Descrição do eixo ou string vazia se não encontrado
        """
        for eixo in self.eixos:
            if unicodedata.normalize('NFC', eixo["nome"]) == unicodedata.normalize('NFC', nome_eixo):
                return eixo["descricao"]
        return ""
    
    def obter_observacoes_eixo(self, nome_eixo: str) -> List[str]:
        """
        Retorna as observações de um eixo específico
        
        Args:
            nome_eixo: Nome do eixo
            
        Returns:
            Lista de observações do eixo ou lista vazia se não encontrado
        """
        for eixo in self.eixos:
            if unicodedata.normalize('NFC', eixo["nome"]) == unicodedata.normalize('NFC', nome_eixo):
                return eixo.get("observacoes", [])
        return []
    
    def obter_configuracao(self) -> Dict:
        """Retorna configurações do sistema"""
        return self.config
    
    def validar_time(self, time: str) -> bool:
        """
        Valida se um time existe
        
        Args:
            time: Nome do time
            
        Returns:
            True se o time existe, False caso contrário
        """
        return time in self.alunos
    
    def validar_aluno(self, time: str, aluno: str) -> bool:
        """
        Valida se um aluno pertence a um time
        
        Args:
            time: Nome do time
            aluno: Nome do aluno
            
        Returns:
            True se o aluno pertence ao time, False caso contrário
        """
        if time in self.alunos:
            return any(unicodedata.normalize('NFC', a['nome']) == unicodedata.normalize('NFC', aluno) for a in self.alunos[time])
        return False
