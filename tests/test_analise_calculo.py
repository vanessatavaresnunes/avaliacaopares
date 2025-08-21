import pandas as pd
import pytest

def test_calculo_total_e_nota():
    # Dados simulados (alunos x eixos)
    dados = [
        {"Aluno": "Gabriel Santos do Nascimento", "Eixo1": 18, "Eixo2": 17, "Eixo3": 17},
        {"Aluno": "Giacomo Zema Matizonkas", "Eixo1": 2, "Eixo2": 2, "Eixo3": 1},
        {"Aluno": "Iasmim Santos Silva de Jesus", "Eixo1": 6, "Eixo2": 7, "Eixo3": 8},
        {"Aluno": "Lucas Matheus Nunes", "Eixo1": 6, "Eixo2": 7, "Eixo3": 8},
        {"Aluno": "Renan Sabino dos Reis", "Eixo1": 14, "Eixo2": 10, "Eixo3": 13},
        {"Aluno": "Thalyta da Silva Viana", "Eixo1": 10, "Eixo2": 11, "Eixo3": 8},
        {"Aluno": "Vinicius dos Reis Savian", "Eixo1": 0, "Eixo2": 1, "Eixo3": 2},
        {"Aluno": "Vinicius Maciel Flor", "Eixo1": 8, "Eixo2": 9, "Eixo3": 7},
    ]
    df = pd.DataFrame(dados)
    df["Total"] = df[["Eixo1", "Eixo2", "Eixo3"]].sum(axis=1)
    # Cálculo da nota
    media = df["Total"].mean()
    maior = df["Total"].max()
    menor = df["Total"].min()
    denominador = 0.6 * (maior - menor) if maior != menor else 1
    df["Nota"] = ((df["Total"] - media) / denominador).round(1)

    # Valores esperados
    totais_esperados = [52, 5, 21, 21, 37, 29, 3, 24]
    notas_esperadas = [1.0, -0.6, -0.1, -0.1, 0.4, 0.2, -0.7, 0.0]

    assert df["Total"].tolist() == totais_esperados, f"Totais incorretos: {df['Total'].tolist()}"
    assert all(abs(a-b) < 0.01 for a, b in zip(df["Nota"], notas_esperadas)), f"Notas incorretas: {df['Nota'].tolist()}"
