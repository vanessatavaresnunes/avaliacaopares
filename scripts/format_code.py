#!/usr/bin/env python3
"""
Script para formatar código do projeto.
Aplica formatação automática usando Black.
"""

import subprocess
import sys
import os


def main():
    """Função principal do script"""
    print("🎨 Formatando código do projeto...")
    
    # Verificar se estamos no diretório correto
    if not os.path.exists("src"):
        print("❌ Erro: Execute este script no diretório raiz do projeto")
        sys.exit(1)
    
    # Formatar código com Black
    print("📝 Aplicando formatação com Black...")
    result = subprocess.run(
        "black src/ tests/",
        shell=True,
        capture_output=True,
        text=True
    )
    
    if result.stdout:
        print("Arquivos formatados:")
        print(result.stdout)
    
    if result.stderr:
        print("Erros:")
        print(result.stderr)
    
    if result.returncode == 0:
        print("✅ Código formatado com sucesso!")
    else:
        print("❌ Erro ao formatar código")
        sys.exit(1)


if __name__ == "__main__":
    main()
