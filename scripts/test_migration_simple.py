#!/usr/bin/env python3
"""
Script simplificado para testar migração de usuários
"""

import json
import sys
import os
from pathlib import Path

# Adicionar src ao path para imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from utils.supabase_storage import salvar_usuario_no_bucket, carregar_usuario_do_bucket, validar_senha_usuario
    print("Imports OK")
except Exception as e:
    print(f"Erro no import: {e}")
    sys.exit(1)

def test_single_user():
    """Testa migração de um único usuário"""
    nome = "Gabriel Santos do Nascimento"
    email = "gabriel.santos.do.nascimento@inteli.edu.br"
    senha = "123"
    
    print(f"Testando usuário: {nome}")
    
    # Tentar salvar
    resultado = salvar_usuario_no_bucket(nome, email, senha, {"id": 10, "grupo": "Grupo 1"})
    
    if resultado:
        print("Usuário salvo com sucesso!")
        
        # Tentar carregar
        dados = carregar_usuario_do_bucket(nome)
        if dados:
            print(f"Usuário carregado: {dados['nome']} - {dados['email']}")
            
            # Testar validação de senha
            if validar_senha_usuario(nome, senha):
                print("Validação de senha OK!")
                return True
            else:
                print("ERRO: Validação de senha falhou!")
                return False
        else:
            print("ERRO: Não foi possível carregar usuário!")
            return False
    else:
        print("ERRO: Não foi possível salvar usuário!")
        return False

if __name__ == "__main__":
    print("Teste de Migracao - Usuario Unico")
    print("=" * 40)
    
    # Verificar se .env existe
    env_path = Path(__file__).parent.parent / ".env"
    if not env_path.exists():
        print("ERRO: Arquivo .env nao encontrado!")
        sys.exit(1)
    
    # Executar teste
    if test_single_user():
        print("\nTeste passou! Sistema funcionando.")
    else:
        print("\nTeste falhou! Há problemas no sistema.")
        sys.exit(1)