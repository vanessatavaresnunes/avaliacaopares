"""
Controller para gerenciar a lógica de negócio das avaliações.
Responsável por coordenar entre modelos e views.
"""

from typing import Dict, List, Optional, Tuple
import streamlit as st
from src.models.avaliacao import AvaliacaoModel
from src.models.usuario import UsuarioModel


class AvaliacaoController:
    """Controller responsável por gerenciar a lógica de avaliações"""
    
    def __init__(self):
        self.avaliacao_model = AvaliacaoModel()
        self.usuario_model = UsuarioModel()
    
    def inicializar_sessao(self):
        """Inicializa a sessão do Streamlit se necessário"""
        if 'avaliacoes_temp' not in st.session_state:
            st.session_state.avaliacoes_temp = {}
        
        if 'logado' not in st.session_state:
            st.session_state.logado = False

        if 'validation_messages' not in st.session_state:
            st.session_state.validation_messages = {
                'soma_notas': {'is_valid': True, 'messages': [], 'details': {}},
                'notas_individuais': {'is_valid': True, 'messages': []},
                'feedbacks_preenchidos': {'is_valid': True, 'messages': []},
                'feedbacks_unicos': {'is_valid': True, 'messages': []},
                'conteudo_feedbacks': {'is_valid': True, 'messages': []}
            }
    
    def fazer_login(self, time: str, aluno: str, senha: str) -> bool:
        """
        Realiza o login do usuário
        
        Args:
            time: Nome do time
            aluno: Nome do aluno
            senha: Senha do aluno
            
        Returns:
            True se login bem-sucedido, False caso contrário
        """
        if self.usuario_model.validar_time(time) and \
           self.usuario_model.validar_aluno(time, aluno) and \
           self.usuario_model.validar_senha(time, aluno, senha):
            st.session_state.logado = True
            st.session_state.aluno_atual = aluno
            st.session_state.aluno_id_atual = self.usuario_model.obter_id_aluno(aluno)
            st.session_state.time_atual = time
            
            # Verificar se é primeiro acesso
            st.session_state.primeiro_acesso = self.usuario_model.verificar_primeiro_acesso(aluno)
            
            return True
        return False
    
    def fazer_logout(self):
        """Realiza o logout do usuário"""
        st.session_state.logado = False
        if 'aluno_atual' in st.session_state:
            del st.session_state.aluno_atual
        if 'aluno_id_atual' in st.session_state:
            del st.session_state.aluno_id_atual
        if 'time_atual' in st.session_state:
            del st.session_state.time_atual
        if 'avaliacoes_temp' in st.session_state:
            del st.session_state.avaliacoes_temp
        if 'primeiro_acesso' in st.session_state:
            del st.session_state.primeiro_acesso
    
    def ativar_usuario(self, nova_senha: str) -> bool:
        """
        Ativa o usuário e altera sua senha no primeiro acesso
        
        Args:
            nova_senha: Nova senha do usuário
            
        Returns:
            True se ativado com sucesso, False caso contrário
        """
        aluno_atual = st.session_state.get('aluno_atual')
        if not aluno_atual:
            return False
            
        # Alterar senha e marcar como ativo
        sucesso = self.usuario_model.alterar_senha_usuario(aluno_atual, nova_senha)
        if sucesso:
            # Atualizar flag de primeiro acesso
            st.session_state.primeiro_acesso = False
        return sucesso
    
    def esta_logado(self) -> bool:
        """
        Verifica se o usuário está logado
        
        Returns:
            True se logado, False caso contrário
        """
        return st.session_state.get('logado', False)
    
    def obter_dados_usuario_atual(self) -> Tuple[int, str]:
        """
        Obtém dados do usuário atualmente logado
        
        Returns:
            Tupla com (id_aluno, time)
        """
        return st.session_state.aluno_id_atual, st.session_state.time_atual
    
    def obter_alunos_para_avaliar(self) -> List[Dict[str, any]]:
        """
        Obtém lista de alunos que podem ser avaliados pelo usuário atual
        
        Returns:
            Lista de alunos do mesmo time (excluindo o próprio)
        """
        aluno_atual, time_atual = st.session_state.aluno_atual, st.session_state.time_atual
        return self.usuario_model.obter_alunos_time_excluindo(time_atual, aluno_atual)
    
    def inicializar_avaliacao_aluno(self, aluno: Dict[str, any]):
        """
        Inicializa a estrutura de avaliação para um aluno
        
        Args:
            aluno: Dicionário com dados do aluno
        """
        aluno_id = aluno['id']
        if aluno_id not in st.session_state.avaliacoes_temp:
            nomes_eixos = self.obter_nomes_eixos()
            st.session_state.avaliacoes_temp[aluno_id] = {
                'notas': [0] * len(nomes_eixos),
                'feedbacks': [''] * len(nomes_eixos)
            }
    
    def atualizar_nota(self, aluno_id: int, eixo_index: int):
        """
        Atualiza a nota de um aluno em um eixo específico
        
        Args:
            aluno_id: ID do aluno
            eixo_index: Índice do eixo (0-2)
        """
        key = f"nota_{aluno_id}_{eixo_index}"
        nota = st.session_state[key]
        if aluno_id in st.session_state.avaliacoes_temp:
            st.session_state.avaliacoes_temp[aluno_id]['notas'][eixo_index] = nota
        self.validar_avaliacoes()
    
    def atualizar_feedback(self, aluno_id: int, eixo_index: int):
        """
        Atualiza o feedback de um aluno para um eixo específico
        
        Args:
            aluno_id: ID do aluno
            eixo_index: Índice do eixo
        """
        key = f"feedback_{aluno_id}_{eixo_index}"
        feedback = st.session_state[key]
        if aluno_id in st.session_state.avaliacoes_temp:
            st.session_state.avaliacoes_temp[aluno_id]['feedbacks'][eixo_index] = feedback
        self.validar_avaliacoes()
    
    def validar_avaliacoes(self) -> Dict[str, any]:
        """
        Valida todas as avaliações atuais.

        Returns:
            Dicionário com os resultados de cada validação.
        """
        alunos_time = self.obter_alunos_para_avaliar()
        nomes_eixos = self.obter_nomes_eixos()
        config = self.obter_configuracao()

        # Garante que a avaliação temporária exista para todos os alunos
        for aluno in alunos_time:
            self.inicializar_avaliacao_aluno(aluno)

        num_integrantes_grupo = len(alunos_time) + 1

        # Initialize validation messages structure
        st.session_state.validation_messages = {
            'soma_notas': {'is_valid': True, 'messages': [], 'details': {}},
            'notas_individuais': {'is_valid': True, 'messages': []},
            'feedbacks_preenchidos': {'is_valid': True, 'messages': []},
            'feedbacks_unicos': {'is_valid': True, 'messages': []},
            'conteudo_feedbacks': {'is_valid': True, 'messages': []}
        }

        # Perform validations
        validacoes = self.avaliacao_model.validar_avaliacoes(
            st.session_state.avaliacoes_temp,
            [aluno['id'] for aluno in alunos_time],
            nomes_eixos,
            config,
            num_integrantes_grupo
        )

        # Store messages based on validation results
        # Validação da soma de notas por eixo
        soma_notas_validas_geral = True
        for eixo, detalhes in validacoes['soma_notas'].items():
            st.session_state.validation_messages['soma_notas']['details'][eixo] = { # Store details for each axis
                'soma_atual': detalhes['soma_atual'],
                'soma_esperada': detalhes['soma_esperada']
            }
            if not detalhes['valido']:
                soma_notas_validas_geral = False
                diferenca = detalhes['soma_atual'] - detalhes['soma_esperada']
                if diferenca > 0:
                    st.session_state.validation_messages['soma_notas']['messages'].append(
                        f"A soma das notas para o eixo '{eixo}' excedeu em {diferenca} ponto(s). Soma atual: {detalhes['soma_atual']}, Esperado: {detalhes['soma_esperada']}."
                    )
                else:
                    st.session_state.validation_messages['soma_notas']['messages'].append(
                        f"A soma das notas para o eixo '{eixo}' está faltando {-diferenca} ponto(s). Soma atual: {detalhes['soma_atual']}, Esperado: {detalhes['soma_esperada']}."
                    )
        st.session_state.validation_messages['soma_notas']['is_valid'] = soma_notas_validas_geral

        # Validação de notas individuais
        if not validacoes['notas_individuais']:
            st.session_state.validation_messages['notas_individuais']['is_valid'] = False
            st.session_state.validation_messages['notas_individuais']['messages'].append(
                "Pelo menos uma nota excede o valor máximo permitido ou a regra N/2."
            )

        # Validação de preenchimento de feedbacks
        if not validacoes['feedbacks_preenchidos']:
            st.session_state.validation_messages['feedbacks_preenchidos']['is_valid'] = False
            st.session_state.validation_messages['feedbacks_preenchidos']['messages'].append(
                "Todos os campos de feedback devem ser preenchidos."
            )

        # Validação de feedbacks únicos
        if not validacoes['feedbacks_unicos']:
            st.session_state.validation_messages['feedbacks_unicos']['is_valid'] = False
            st.session_state.validation_messages['feedbacks_unicos']['messages'].append(
                "Os feedbacks para um mesmo aluno não podem ser iguais."
            )

        # Validação de conteúdo de feedbacks
        if not validacoes['conteudo_feedbacks']:
            st.session_state.validation_messages['conteudo_feedbacks']['is_valid'] = False
            st.session_state.validation_messages['conteudo_feedbacks']['messages'].append(
                "Os feedbacks devem conter pelo menos duas palavras e não podem conter emojis ou caracteres especiais."
            )
        
        return validacoes

    def preencher_dados_teste(self):
        """Preenche o formulário com dados de teste."""
        alunos_time = self.obter_alunos_para_avaliar()
        nomes_eixos = self.obter_nomes_eixos()
        num_alunos = len(alunos_time)
        pontos_totais = num_alunos + 1

        for i_eixo, eixo in enumerate(nomes_eixos):
            # Distribui 1 ponto para cada aluno, e o restante para o último
            pontos = [1] * num_alunos
            pontos[-1] = pontos_totais - (num_alunos - 1)
            for idx, aluno in enumerate(alunos_time):
                self.inicializar_avaliacao_aluno(aluno)
                st.session_state.avaliacoes_temp[aluno['id']]['notas'][i_eixo] = pontos[idx]
                st.session_state.avaliacoes_temp[aluno['id']]['feedbacks'][i_eixo] = f"Feedback para {aluno['nome']} no {eixo}. Teste automatizado."
        self.validar_avaliacoes()
    
    def salvar_avaliacoes(self) -> Tuple[bool, str]:
        """
        Salva as avaliações atuais.

        Returns:
            Tupla com (sucesso, mensagem).
        """
        try:
            # Validar antes de salvar
            validacoes = self.validar_avaliacoes()
            mensagens_erro = []

            # Checar soma das notas
            eixos_soma_invalidos = [
                eixo for eixo, detalhes in validacoes['soma_notas'].items()
                if not detalhes.get('valido', False)
            ]
            if eixos_soma_invalidos:
                mensagens_erro.append(
                    f"A soma das notas para os eixos {', '.join(eixos_soma_invalidos)} está incorreta."
                )

            # Checar notas individuais
            if not validacoes['notas_individuais']:
                mensagens_erro.append("Uma ou mais notas excedem o valor máximo permitido.")

            # Checar preenchimento dos feedbacks
            if not validacoes['feedbacks_preenchidos']:
                mensagens_erro.append("Todos os campos de feedback devem ser preenchidos.")

            # Checar feedbacks únicos
            if not validacoes['feedbacks_unicos']:
                mensagens_erro.append("Os feedbacks para um mesmo aluno não podem ser iguais.")

            # Checar conteúdo dos feedbacks
            if not validacoes['conteudo_feedbacks']:
                mensagens_erro.append("Os feedbacks não podem conter emojis ou caracteres especiais.")

            if mensagens_erro:
                return False, "\n".join(mensagens_erro)

            # Salvar avaliações
            aluno_id_atual, time_atual = self.obter_dados_usuario_atual()
            sprint_atual = st.session_state.sprint_atual
            nomes_eixos = self.obter_nomes_eixos()
            nome_avaliador = self.usuario_model.obter_nome_aluno(aluno_id_atual)
            arquivo = self.avaliacao_model.salvar_avaliacoes(
                aluno_id_atual, time_atual, sprint_atual, st.session_state.avaliacoes_temp, nomes_eixos, nome_avaliador
            )

            # Limpar dados temporários
            del st.session_state.avaliacoes_temp

            return True, f"Avaliações salvas com sucesso! Arquivo: {arquivo}"

        except Exception as e:
            return False, f"Erro ao salvar: {str(e)}"
    
    def obter_estatisticas_avaliacoes(self) -> Dict:
        """
        Obtém estatísticas das avaliações salvas
        
        Returns:
            Dicionário com estatísticas
        """
        df = self.avaliacao_model.carregar_dados()
        return self.avaliacao_model.obter_estatisticas(df)
    
    def obter_dados_filtrados(self, time_filtro: str = None, 
                            avaliador_filtro: int = None, 
                            eixo_filtro: str = None) -> 'pd.DataFrame':
        """
        Obtém dados filtrados para visualização
        
        Args:
            time_filtro: Filtro por time
            avaliador_filtro: Filtro por id do avaliador
            eixo_filtro: Filtro por eixo
            
        Returns:
            DataFrame filtrado
        """
        df = self.avaliacao_model.carregar_dados()
        
        if df.empty:
            return df
        
        if time_filtro and time_filtro != 'Todos':
            df = df[df['time'] == time_filtro]
        
        if avaliador_filtro and avaliador_filtro != 'Todos':
            df = df[df['id_avaliador'] == avaliador_filtro]
        
        if eixo_filtro and eixo_filtro != 'Todos':
            df = df[df['eixo'] == eixo_filtro]
        
        return df
    
    def obter_configuracao(self):
        """Obtém configurações do sistema"""
        return self.usuario_model.obter_configuracao()
    
    def obter_eixos(self) -> List[Dict[str, any]]:
        """Obtém lista de eixos de avaliação com nome, descrição e observações"""
        return self.usuario_model.obter_eixos()
    
    def obter_nomes_eixos(self) -> List[str]:
        """Obtém lista apenas com os nomes dos eixos de avaliação"""
        return self.usuario_model.obter_nomes_eixos()
    
    def obter_descricao_eixo(self, nome_eixo: str) -> str:
        """Obtém a descrição de um eixo específico"""
        return self.usuario_model.obter_descricao_eixo(nome_eixo)
    
    def obter_observacoes_eixo(self, nome_eixo: str) -> List[str]:
        """Obtém as observações de um eixo específico"""
        return self.usuario_model.obter_observacoes_eixo(nome_eixo)
    
    def obter_times(self) -> List[str]:
        """Obtém lista de times disponíveis"""
        return self.usuario_model.obter_times()
    
    def obter_alunos_por_time(self, time: str) -> List[str]:
        """Obtém lista de alunos de um time"""
        return self.usuario_model.obter_alunos_por_time(time)
