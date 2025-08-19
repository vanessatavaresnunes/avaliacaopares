#!/usr/bin/env python3
"""
Script de instalação cross-platform para o Sistema de Avaliação de Pares.
Funciona em Windows, macOS e Linux.
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """Executa um comando e trata erros"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} concluído com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao {description.lower()}: {e}")
        print(f"   Comando: {command}")
        if e.stdout:
            print(f"   Saída: {e.stdout}")
        if e.stderr:
            print(f"   Erro: {e.stderr}")
        return False


def check_python_version():
    """Verifica se a versão do Python é compatível"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 ou superior é necessário!")
        print(f"   Versão atual: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detectado")
    return True


def install_dependencies():
    """Instala as dependências do projeto"""
    print("\n📦 Instalando dependências...")
    
    # Comando para instalar dependências
    install_cmd = f"{sys.executable} -m pip install -r requirements.txt"
    
    if not run_command(install_cmd, "Instalar dependências"):
        return False
    
    return True


def create_directories():
    """Cria diretórios necessários"""
    print("\n📁 Criando diretórios...")
    
    directories = ["dados", "data"]
    
    for directory in directories:
        try:
            Path(directory).mkdir(exist_ok=True)
            print(f"✅ Diretório '{directory}' criado/verificado")
        except Exception as e:
            print(f"❌ Erro ao criar diretório '{directory}': {e}")
            return False
    
    return True


def verify_installation():
    """Verifica se a instalação foi bem-sucedida"""
    print("\n🔍 Verificando instalação...")
    
    try:
        import streamlit
        import pandas
        import pyarrow
        import numpy
        import plotly
        print("✅ Todas as dependências foram instaladas corretamente!")
        return True
    except ImportError as e:
        print(f"❌ Erro ao importar dependência: {e}")
        return False


def main():
    """Função principal"""
    print("🚀 Sistema de Avaliação de Pares - Instalador Cross-Platform")
    print("=" * 60)
    
    # Verificar versão do Python
    if not check_python_version():
        sys.exit(1)
    
    # Criar diretórios
    if not create_directories():
        sys.exit(1)
    
    # Instalar dependências
    if not install_dependencies():
        sys.exit(1)
    
    # Verificar instalação
    if not verify_installation():
        sys.exit(1)
    
    print("\n🎉 Instalação concluída com sucesso!")
    print("\n📋 Próximos passos:")
    print("   1. Execute: streamlit run app.py")
    print("   2. Acesse: http://localhost:8501")
    print("\n💡 Dicas:")
    print("   - Para visualizar dados: streamlit run visualizador_mvc.py")
    print("   - Para parar o servidor: Ctrl+C")
    print("   - Para ajuda: python install.py --help")


if __name__ == "__main__":
    main()
