import streamlit as st
import pandas as pd
from src.utils.supabase_storage import list_json_files_in_bucket, download_json_from_bucket
import json
from collections import defaultdict

st.set_page_config(page_title="Análise das Avaliações", layout="wide")

st.title("🔎 Análise das Avaliações de Pares")

# Carregar todos os arquivos de avaliações

# Listar arquivos do bucket Supabase

arquivos = list_json_files_in_bucket(prefix="aval_")
# st.info(f"Arquivos encontrados: {arquivos}")
if not arquivos:
    st.warning("Nenhum dado de avaliação encontrado no Supabase.")
    st.stop()


# Carregar dados em DataFrame
linhas = []
import tempfile
for arq in arquivos:
    if arq.startswith("avaliacoescompletas"):
        continue
    with tempfile.NamedTemporaryFile(delete=False, mode="w+b") as tmp:
        download_json_from_bucket(arq, tmp.name)
        tmp.seek(0)
        conteudo = tmp.read().decode("utf-8").strip()
    # st.info(f"Arquivo: {arq} | Conteúdo inicial: {conteudo[:200]}")
        if conteudo:
            for linha in conteudo.splitlines():
                linha = linha.strip()
                if linha:
                    try:
                        dado = json.loads(linha)
                        linhas.append(dado)
                    except Exception as e:
                        pass
if not linhas:
    st.warning("Nenhum dado de avaliação encontrado.")
    st.stop()
df = pd.DataFrame(linhas)

# Garantir colunas essenciais
for col in ["time", "sprint", "nome_avaliado", "eixo", "nota"]:
    if col not in df.columns:
        st.error(f"Coluna obrigatória ausente: {col}")
        st.stop()

grupos = sorted(df["time"].unique())
sprints = sorted(df["sprint"].unique())

for grupo in grupos:
    with st.expander(f"Grupo: {grupo}", expanded=False):
        df_grupo = df[df["time"] == grupo]
        for sprint in sprints:
            df_sprint = df_grupo[df_grupo["sprint"] == sprint]
            if df_sprint.empty:
                continue
            # Manter apenas a última avaliação de cada avaliador para cada avaliado/eixo
            df_sprint_sorted = df_sprint.sort_values("timestamp")
            df_sprint_last = df_sprint_sorted.groupby([
                "id_avaliador", "id_avaliado", "eixo"
            ], as_index=False).last()
            st.subheader(f"Sprint: {sprint}")
            alunos = sorted(df_sprint_last["nome_avaliado"].unique())
            eixos = sorted(df_sprint_last["eixo"].unique())
            # Montar tabela de somatórios
            dados = []
            for aluno in alunos:
                linha = {"Aluno": aluno}
                soma_total = 0
                for eixo in eixos:
                    soma = df_sprint_last[(df_sprint_last["nome_avaliado"] == aluno) & (df_sprint_last["eixo"] == eixo)]["nota"].sum()
                    linha[eixo] = soma
                    soma_total += soma
                linha["Total"] = soma_total
                dados.append(linha)
            df_result = pd.DataFrame(dados)
            df_result = df_result.sort_values("Aluno")
            # Calcular a nota conforme fórmula fornecida (1 casa decimal)
            if not df_result.empty:
                medias = df_result["Total"].mean()
                maior = df_result["Total"].max()
                menor = df_result["Total"].min()
                denominador = 0.6 * (maior - menor) if maior != menor else 1
                df_result["Nota"] = ((df_result["Total"] - medias) / denominador).round(1)
            st.dataframe(df_result, hide_index=True)

            # Exibir feedbacks recebidos por cada aluno em formato de tabela
            st.markdown("**Feedbacks recebidos por aluno (tabela):**")
            feedback_data = []
            for aluno in alunos:
                linha = {"Aluno": aluno}
                for eixo in eixos:
                    feedbacks = df_sprint_last[(df_sprint_last["nome_avaliado"] == aluno) & (df_sprint_last["eixo"] == eixo)]["feedback"].dropna().tolist()
                    # Junta múltiplos feedbacks, cada um com '- ' e quebra de linha
                    linha[eixo] = '\n'.join(f'- {fb}' for fb in feedbacks) if feedbacks else ""
                feedback_data.append(linha)
            df_feedback = pd.DataFrame(feedback_data)
            # Garante ordem das colunas: Aluno, eixo1, eixo2, eixo3
            # Ordena as colunas conforme desejado
            ordem_eixos = [
                "Entregas reais",
                "Valor Percebido",
                "Caixa de Ferramentas"
            ]
            colunas = ["Aluno"] + [eixo for eixo in ordem_eixos if eixo in df_feedback.columns]
            df_feedback = df_feedback[colunas]
            # Exibir a tabela de feedbacks com quebras de linha usando st.markdown
            def format_cell(text):
                if not text:
                    return ""
                return '<br>'.join(text.split('\n'))

            # Monta a tabela em HTML
            html = '<table border="1" style="border-collapse:collapse;width:100%">'
            # Cabeçalho
            html += '<tr>' + ''.join(f'<th>{col}</th>' for col in df_feedback.columns) + '</tr>'
            # Linhas
            for _, row in df_feedback.iterrows():
                html += '<tr>' + ''.join(f'<td>{format_cell(str(row[col]))}</td>' for col in df_feedback.columns) + '</tr>'
            html += '</table>'
            st.markdown(html, unsafe_allow_html=True)
