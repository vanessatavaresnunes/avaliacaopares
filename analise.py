import streamlit as st
import pandas as pd
from src.utils.supabase_storage import list_json_files_in_bucket, download_json_from_bucket
import json
from collections import defaultdict

st.set_page_config(page_title="Análise das Avaliações", layout="wide")

st.title("🔎 Análise das Avaliações de Pares")

# Carregar todos os arquivos de avaliações

# Listar arquivos do bucket Supabase
arquivos = list_json_files_in_bucket(prefix="avaliacoes_")
if not arquivos:
    st.warning("Nenhum dado de avaliação encontrado no Supabase.")
    st.stop()

# Carregar dados em DataFrame
linhas = []
import tempfile
for arq in arquivos:
    with tempfile.NamedTemporaryFile(delete=False, mode="w+b") as tmp:
        download_json_from_bucket(arq, tmp.name)
        tmp.seek(0)
        for linha in tmp:
            linha = linha.decode("utf-8").strip()
            if linha:
                try:
                    linhas.append(json.loads(linha))
                except Exception:
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
    st.header(f"Grupo: {grupo}")
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
        # Tabela detalhada: avaliações feitas por cada avaliador
        st.markdown("**Avaliações feitas por cada avaliador:**")
        colunas_detalhe = ["nome_avaliador", "nome_avaliado", "eixo", "nota", "feedback"]
        st.dataframe(df_sprint_last[colunas_detalhe].sort_values(["nome_avaliador", "nome_avaliado", "eixo"]), hide_index=True)
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
