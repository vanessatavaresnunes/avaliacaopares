"""
View para a tela de visualização de dados do aplicativo.
Responsável pela interface de análise e relatórios.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from src.controllers.avaliacao_controller import AvaliacaoController


class VisualizacaoView:
    """View responsável pela tela de visualização de dados"""
    
    def __init__(self, controller: AvaliacaoController):
        self.controller = controller
    
    def renderizar(self):
        """Renderiza a tela de visualização"""
        st.title("📈 Visualizador de Avaliações")
        st.markdown("---")
        
        # Carregar dados
        df = self.controller.avaliacao_model.carregar_dados()
        
        if df.empty:
            st.warning("Nenhum dado de avaliação encontrado. Execute o aplicativo principal primeiro.")
            return
        
        # Resumo geral
        self._renderizar_resumo_geral(df)
        
        # Filtros
        df_filtrado = self._renderizar_filtros(df)
        
        # Análise por eixo
        self._renderizar_analise_eixo(df_filtrado)
        
        # Análise por aluno
        self._renderizar_analise_aluno(df_filtrado)
        
        # Feedbacks
        self._renderizar_feedbacks(df_filtrado)
        
        # Dados completos
        self._renderizar_dados_completos(df_filtrado)
    
    def _renderizar_resumo_geral(self, df: pd.DataFrame):
        """Renderiza o resumo geral dos dados"""
        st.markdown("### 📊 Resumo Geral")
        
        estatisticas = self.controller.obter_estatisticas_avaliacoes()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total de Avaliações", estatisticas['total_avaliacoes'])
        
        with col2:
            st.metric("Alunos Avaliadores", estatisticas['alunos_avaliadores'])
        
        with col3:
            st.metric("Times", estatisticas['times'])
        
        with col4:
            st.metric("Período", estatisticas['periodo'])
    
    def _renderizar_filtros(self, df: pd.DataFrame) -> pd.DataFrame:
        """Renderiza os filtros e retorna dados filtrados"""
        st.markdown("### 🔍 Filtros")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            times = ['Todos'] + list(df['time'].unique())
            time_filtro = st.selectbox("Filtrar por Time:", times)
        
        with col2:
            import pandas as pd
            ids_avaliadores = pd.unique(df['id_avaliador'].dropna())
            nomes_avaliadores = {}
            for id_ in ids_avaliadores:
                try:
                    id_int = int(id_)
                except Exception:
                    id_int = id_
                nome = self.controller.usuario_model.obter_nome_aluno(id_int)
                if not nome or not isinstance(nome, str):
                    nome = f"ID {id_int}"
                nomes_avaliadores[nome] = id_int

            opcoes_avaliador = ['Todos'] + sorted(list(nomes_avaliadores.keys()), key=lambda x: x or "")
            avaliador_selecionado = st.selectbox("Filtrar por Avaliador:", opcoes_avaliador)
            id_avaliador_filtro = nomes_avaliadores.get(avaliador_selecionado)

        with col3:
            eixos = ['Todos'] + list(df['eixo'].unique())
            eixo_filtro = st.selectbox("Filtrar por Eixo:", eixos)
        
        # Aplicar filtros
        df_filtrado = self.controller.obter_dados_filtrados(
            time_filtro, id_avaliador_filtro, eixo_filtro
        )
        
        return df_filtrado
    
    def _renderizar_analise_eixo(self, df: pd.DataFrame):
        """Renderiza a análise por eixo"""
        st.markdown("### 📊 Análise por Eixo")
        
        if df.empty:
            st.info("Nenhum dado encontrado com os filtros aplicados.")
            return
        
        # Média por eixo
        media_por_eixo = df.groupby('eixo')['nota'].agg(['mean', 'count']).round(2)
        media_por_eixo.columns = ['Média', 'Quantidade']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Média de Notas por Eixo:**")
            st.dataframe(media_por_eixo, use_container_width=True)
        
        with col2:
            st.markdown("**Distribuição de Notas:**")
            self._renderizar_grafico_distribuicao(df)
    
    def _renderizar_grafico_distribuicao(self, df: pd.DataFrame):
        """Renderiza gráfico de distribuição de notas"""
        try:
            import plotly.express as px
            
            fig = px.histogram(
                df, 
                x='nota', 
                color='eixo',
                title='Distribuição de Notas por Eixo',
                nbins=4
            )
            st.plotly_chart(fig, use_container_width=True)
        except ImportError:
            st.warning("Plotly não está disponível. Instale com: pip install plotly")
    
    def _renderizar_analise_aluno(self, df: pd.DataFrame):
        """Renderiza a análise por aluno"""
        st.markdown("### 👥 Análise por Aluno")
        
        if df.empty:
            st.info("Nenhum dado encontrado com os filtros aplicados.")
            return
        
        # Média por aluno avaliado
        media_por_aluno = df.groupby('id_avaliado')['nota'].agg(['mean', 'count']).round(2)
        media_por_aluno.columns = ['Média', 'Quantidade de Avaliações']
        media_por_aluno.index = media_por_aluno.index.map(lambda id_: self.controller.usuario_model.obter_nome_aluno(id_))
        media_por_aluno = media_por_aluno.sort_values('Média', ascending=False)
        
        st.dataframe(media_por_aluno, use_container_width=True)
    
    def _renderizar_feedbacks(self, df: pd.DataFrame):
        """Renderiza a seção de feedbacks"""
        st.markdown("### 💬 Feedbacks")
        
        if df.empty:
            st.info("Nenhum dado encontrado com os filtros aplicados.")
            return
        
        # Mostrar feedbacks não vazios
        feedbacks = df[df['feedback'].str.strip() != '']
        
        if not feedbacks.empty:
            for _, row in feedbacks.head(10).iterrows():
                nome_avaliador = self.controller.usuario_model.obter_nome_aluno(row['id_avaliador'])
                nome_avaliado = self.controller.usuario_model.obter_nome_aluno(row['id_avaliado'])
                with st.expander(f"Feedback de {nome_avaliador} para {nome_avaliado} ({row['eixo']})"):
                    st.write(f"**Nota:** {row['nota']}")
                    st.write(f"**Feedback:** {row['feedback']}")
                    st.write(f"**Data:** {row['timestamp']}")
        else:
            st.info("Nenhum feedback textual encontrado.")
    
    def _renderizar_dados_completos(self, df: pd.DataFrame):
        """Renderiza os dados completos"""
        st.markdown("### 📋 Dados Completos")
        
        if df.empty:
            st.info("Nenhum dado encontrado com os filtros aplicados.")
            return
        
        st.dataframe(df, use_container_width=True)
        
        # Botão para download
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"avaliacoes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
