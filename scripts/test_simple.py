#!/usr/bin/env python3
"""
Teste simples para verificar se os imports funcionam
"""

import sys
import os
from pathlib import Path

# Adicionar src ao path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_imports():
    """Testa se todos os imports funcionam"""
    print("Testando imports...")
    
    try:
        from src.models.usuario import UsuarioModel
        print("OK: UsuarioModel")
    except Exception as e:
        print(f"ERRO: UsuarioModel - {e}")
        return False
        
    try:
        from src.controllers.avaliacao_controller import AvaliacaoController
        print("OK: AvaliacaoController")
    except Exception as e:
        print(f"ERRO: AvaliacaoController - {e}")
        return False
        
    try:
        from src.models.avaliacao import AvaliacaoModel
        print("OK: AvaliacaoModel")
    except Exception as e:
        print(f"ERRO: AvaliacaoModel - {e}")
        return False
        
    return True

def test_user_system():
    """Testa o sistema de usuário"""
    print("\nTestando sistema de usuario...")
    
    try:
        from src.models.usuario import UsuarioModel
        
        user_model = UsuarioModel()
        
        # Testar carregamento de times
        times = user_model.obter_times()
        print(f"Times encontrados: {times}")
        
        if len(times) == 0:
            print("ERRO: Nenhum time encontrado!")
            return False
            
        # Testar primeiro time
        primeiro_time = times[0]
        alunos = user_model.obter_alunos_por_time(primeiro_time)
        print(f"Alunos no {primeiro_time}: {len(alunos)} alunos")
        
        if len(alunos) == 0:
            print("ERRO: Nenhum aluno encontrado!")
            return False
            
        # Testar login
        primeiro_aluno = alunos[0]['nome']
        print(f"Testando login: {primeiro_aluno}")
        
        # Teste com senha correta
        login_ok = user_model.validar_senha(primeiro_time, primeiro_aluno, "123")
        if login_ok:
            print("OK: Login funcionando!")
        else:
            print("ERRO: Login falhou!")
            return False
            
        # Teste com senha incorreta
        login_fail = user_model.validar_senha(primeiro_time, primeiro_aluno, "senhaerrada")
        if not login_fail:
            print("OK: Rejeicao de senha incorreta funcionando!")
        else:
            print("ERRO: Sistema aceitou senha incorreta!")
            return False
            
        return True
        
    except Exception as e:
        print(f"ERRO no sistema de usuario: {e}")
        return False

def test_controller():
    """Testa o controller"""
    print("\nTestando controller...")
    
    try:
        from src.controllers.avaliacao_controller import AvaliacaoController
        
        controller = AvaliacaoController()
        print("OK: Controller criado")
        
        # Testar métodos básicos
        times = controller.obter_times()
        print(f"OK: Times obtidos - {len(times)} times")
        
        eixos = controller.obter_nomes_eixos()
        print(f"OK: Eixos obtidos - {eixos}")
        
        return True
        
    except Exception as e:
        print(f"ERRO no controller: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("TESTE SIMPLES DO SISTEMA")
    print("=" * 30)
    
    # Teste 1: Imports
    if not test_imports():
        print("\nFALHA: Problemas nos imports!")
        return False
    
    # Teste 2: Sistema de usuário
    if not test_user_system():
        print("\nFALHA: Sistema de usuario com problemas!")
        return False
        
    # Teste 3: Controller
    if not test_controller():
        print("\nFALHA: Controller com problemas!")
        return False
    
    print("\n" + "=" * 30)
    print("TODOS OS TESTES PASSARAM!")
    print("Sistema basico esta funcionando!")
    return True

if __name__ == "__main__":
    # Verificar diretório
    current_dir = Path.cwd()
    print(f"Diretorio atual: {current_dir}")
    
    if not (current_dir / "data" / "alunos.json").exists():
        print("AVISO: alunos.json nao encontrado, alguns testes podem falhar")
    
    if main():
        print("\nSistema pronto para testes manuais!")
        print("Execute: streamlit run app.py")
    else:
        print("\nCorreja os problemas antes de continuar!")
        sys.exit(1)