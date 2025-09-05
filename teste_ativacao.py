"""
Script de teste para verificar a funcionalidade de primeiro acesso e alteração de senha.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from src.models.usuario import UsuarioModel
from src.utils.supabase_storage import salvar_usuario_no_bucket, carregar_usuario_do_bucket

def test_first_access():
    """Testa a funcionalidade de primeiro acesso"""
    print("=== Teste de Primeiro Acesso ===")
    
    # Criar um modelo de usuário
    usuario_model = UsuarioModel()
    
    # Testar com um aluno existente
    time = "Grupo 1"
    aluno = "Gabriel Santos do Nascimento"
    
    print(f"Testando aluno: {aluno}")
    print(f"Time: {time}")
    
    # Verificar se o aluno existe
    if usuario_model.validar_aluno(time, aluno):
        print("✓ Aluno válido")
    else:
        print("✗ Aluno inválido")
        return
    
    # Verificar se é primeiro acesso (deve ser True inicialmente)
    primeiro_acesso = usuario_model.verificar_primeiro_acesso(aluno)
    print(f"Primeiro acesso: {primeiro_acesso}")
    
    # Testar login com senha padrão
    senha_padrao = "123"
    if usuario_model.validar_senha(time, aluno, senha_padrao):
        print("✓ Login com senha padrão funcionou")
    else:
        print("✗ Login com senha padrão falhou")
    
    # Testar alteração de senha
    nova_senha = "nova_senha_segura_123"
    if usuario_model.alterar_senha_usuario(aluno, nova_senha):
        print("✓ Alteração de senha funcionou")
    else:
        print("✗ Alteração de senha falhou")
        return
    
    # Verificar se não é mais primeiro acesso
    primeiro_acesso = usuario_model.verificar_primeiro_acesso(aluno)
    print(f"Primeiro acesso após alteração: {primeiro_acesso}")
    
    # Testar login com nova senha
    if usuario_model.validar_senha(time, aluno, nova_senha):
        print("✓ Login com nova senha funcionou")
    else:
        print("✗ Login com nova senha falhou")
    
    # Testar login com senha antiga (deve falhar)
    if usuario_model.validar_senha(time, aluno, senha_padrao):
        print("✗ Login com senha antiga funcionou (não deveria)")
    else:
        print("✓ Login com senha antiga falhou (como esperado)")
    
    print("=== Fim do Teste ===")

if __name__ == "__main__":
    test_first_access()