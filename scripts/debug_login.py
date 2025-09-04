#!/usr/bin/env python3
"""
Debug detalhado do sistema de login
"""

import sys
import os
from pathlib import Path

# Adicionar src ao path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def debug_login():
    """Debug detalhado do login"""
    print("DEBUG DO SISTEMA DE LOGIN")
    print("=" * 40)
    
    try:
        from src.models.usuario import UsuarioModel
        
        user_model = UsuarioModel()
        print("✓ UsuarioModel criado")
        
        # Verificar dados carregados
        print(f"Times: {user_model.obter_times()}")
        
        primeiro_time = "Grupo 1"
        alunos = user_model.obter_alunos_por_time(primeiro_time)
        print(f"Alunos no {primeiro_time}: {len(alunos)}")
        
        if len(alunos) > 0:
            primeiro_aluno = alunos[0]['nome']
            print(f"Primeiro aluno: {primeiro_aluno}")
            print(f"Dados do aluno: {alunos[0]}")
            
            # Testar validacao de aluno
            aluno_valido = user_model.validar_aluno(primeiro_time, primeiro_aluno)
            print(f"Aluno válido no time? {aluno_valido}")
            
            if aluno_valido:
                print("\nTestando senha...")
                
                # Testar diretamente o método validar_senha com debug
                try:
                    print("Tentando validar senha...")
                    resultado = user_model.validar_senha(primeiro_time, primeiro_aluno, "123")
                    print(f"Resultado da validação: {resultado}")
                except Exception as e:
                    print(f"Erro na validação: {e}")
                    import traceback
                    traceback.print_exc()
            else:
                print("ERRO: Aluno não é válido no time!")
        else:
            print("ERRO: Nenhum aluno encontrado!")
            
    except Exception as e:
        print(f"ERRO GERAL: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_login()