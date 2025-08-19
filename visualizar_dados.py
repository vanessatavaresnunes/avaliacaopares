import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(
    page_title="Visualizador de Avaliações",
    page_icon="📈",
    layout="wide"
)

from config import CONFIG

def carregar_dados():
    """Carrega os dados de avaliação salvos"""
    arquivo_consolidado = f'{CONFIG["diretorio_dados"]}/avaliacoes_consolidadas.json'
    
    if os.path.exists(arquivo_consolidado):
        return pd.read_json(arquivo_consolidado, orient='records', lines=True)
    else:
        return pd.DataFrame()

def main():
    st.title("📈 Visualizador de Avaliações")
    st.markdown("---")
    
    # Carregar dados
    df = carregar_dados()
    
    if df.empty:
        st.warning("Nenhum dado de avaliação encontrado. Execute o aplicativo principal primeiro.")
        return
    
    # Informações gerais
    st.markdown("### 📊 Resumo Geral")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total de Avaliações", len(df))
    
    with col2:
        st.metric("Alunos Avaliadores", df['aluno_avaliador'].nunique())
    
    with col3:
        st.metric("Times", df['time'].nunique())
    
    with col4:
        st.metric("Período", f"{df['timestamp'].min()[:8]} a {df['timestamp'].max()[:8]}")
    
    st.markdown("---")
    
    # Filtros
    st.markdown("### 🔍 Filtros")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        times = ['Todos'] + list(df['time'].unique())
        time_filtro = st.selectbox("Filtrar por Time:", times)
    
    with col2:
        avaliadores = ['Todos'] + list(df['aluno_avaliador'].unique())
        avaliador_filtro = st.selectbox("Filtrar por Avaliador:", avaliadores)
    
    with col3:
        eixos = ['Todos'] + list(df['eixo'].unique())
        eixo_filtro = st.selectbox("Filtrar por Eixo:", eixos)
    
    # Aplicar filtros
    df_filtrado = df.copy()
    
    if time_filtro != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['time'] == time_filtro]
    
    if avaliador_filtro != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['aluno_avaliador'] == avaliador_filtro]
    
    if eixo_filtro != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['eixo'] == eixo_filtro]
    
    st.markdown("---")
    
    # Análise por eixo
    st.markdown("### 📊 Análise por Eixo")
    
    if not df_filtrado.empty:
        # Média por eixo
        media_por_eixo = df_filtrado.groupby('eixo')['nota'].agg(['mean', 'count']).round(2)
        media_por_eixo.columns = ['Média', 'Quantidade']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Média de Notas por Eixo:**")
            st.dataframe(media_por_eixo, use_container_width=True)
        
        with col2:
            st.markdown("**Distribuição de Notas:**")
            # Gráfico de barras da distribuição
            import plotly.express as px
            
            fig = px.histogram(
                df_filtrado, 
                x='nota', 
                color='eixo',
                title='Distribuição de Notas por Eixo',
                nbins=4
            )
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Análise por aluno
    st.markdown("### 👥 Análise por Aluno")
    
    if not df_filtrado.empty:
        # Média por aluno avaliado
        media_por_aluno = df_filtrado.groupby('aluno_avaliado')['nota'].agg(['mean', 'count']).round(2)
        media_por_aluno.columns = ['Média', 'Quantidade de Avaliações']
        media_por_aluno = media_por_aluno.sort_values('Média', ascending=False)
        
        st.dataframe(media_por_aluno, use_container_width=True)
    
    st.markdown("---")
    
    # Feedbacks
    st.markdown("### 💬 Feedbacks")
    
    if not df_filtrado.empty:
        # Mostrar feedbacks não vazios
        feedbacks = df_filtrado[df_filtrado['feedback'].str.strip() != '']
        
        if not feedbacks.empty:
            for _, row in feedbacks.head(10).iterrows():
                with st.expander(f"Feedback de {row['aluno_avaliador']} para {row['aluno_avaliado']} ({row['eixo']})"):
                    st.write(f"**Nota:** {row['nota']}")
                    st.write(f"**Feedback:** {row['feedback']}")
                    st.write(f"**Data:** {row['timestamp']}")
        else:
            st.info("Nenhum feedback textual encontrado.")
    
    st.markdown("---")
    
    # Dados completos
    st.markdown("### 📋 Dados Completos")
    
    if not df_filtrado.empty:
        st.dataframe(df_filtrado, use_container_width=True)
        
        # Botão para download
        csv = df_filtrado.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"avaliacoes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
