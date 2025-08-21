#!/usr/bin/env python3
"""
Script para executar testes do projeto.
Inclui testes unitários, cobertura e verificação de qualidade de código.
"""

import subprocess
import sys
import os


def run_command(command, description):
    """Executa um comando e mostra o resultado"""
    print(f"\n{'='*50}")
    print(f"Executando: {description}")
    print(f"Comando: {command}")
    print('='*50)
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.stdout:
        print("Saída:")
        print(result.stdout)
    
    if result.stderr:
        print("Erros:")
        print(result.stderr)
    
    if result.returncode != 0:
        print(f"❌ Falha: {description}")
        return False
    else:
        print(f"✅ Sucesso: {description}")
        return True


def main():
    """Função principal do script"""
    print("🧪 Executando testes e verificações de qualidade...")
    
    # Verificar se estamos no diretório correto
    if not os.path.exists("src"):
        print("❌ Erro: Execute este script no diretório raiz do projeto")
        sys.exit(1)
    
    success = True
    
    # Executar testes unitários
    success &= run_command(
        "python -m pytest tests/ -v --cov=src --cov-report=html --cov-report=term",
        "Testes unitários com cobertura"
    )
    
    # Verificar formatação do código
    success &= run_command(
        "black --check src/ tests/",
        "Verificação de formatação (Black)"
    )
    
    # Verificar estilo do código
    success &= run_command(
        "flake8 src/ tests/ --max-line-length=88 --ignore=E203,W503",
        "Verificação de estilo (Flake8)"
    )
    
    # Verificar tipos (se mypy estiver disponível)
    try:
        success &= run_command(
            "mypy src/",
            "Verificação de tipos (MyPy)"
        )
    except FileNotFoundError:
        print("⚠️  MyPy não encontrado. Pule a verificação de tipos.")
    
    # Resumo final
    print(f"\n{'='*50}")
    if success:
        print("🎉 Todos os testes e verificações passaram!")
        print("📊 Relatório de cobertura disponível em: htmlcov/index.html")
    else:
        print("❌ Alguns testes ou verificações falharam.")
        print("🔧 Corrija os problemas antes de continuar.")
    
    print('='*50)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
