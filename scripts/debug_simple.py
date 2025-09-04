#!/usr/bin/env python3
"""
Debug simples do sistema de login
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
        print("OK: UsuarioModel criado")
        
        # Verificar dados carregados
        times = user_model.obter_times()
        print(f"Times: {times}")
        
        primeiro_time = "Grupo 1"
        alunos = user_model.obter_alunos_por_time(primeiro_time)
        print(f"Alunos no {primeiro_time}: {len(alunos)}")
        
        if len(alunos) > 0:
            primeiro_aluno = alunos[0]['nome']
            print(f"Primeiro aluno: {primeiro_aluno}")
            print(f"Dados do aluno: {alunos[0]}")
            
            # Testar validacao de aluno
            aluno_valido = user_model.validar_aluno(primeiro_time, primeiro_aluno)
            print(f"Aluno valido no time? {aluno_valido}")
            
            if aluno_valido:
                print("Testando senha...")
                
                # Importar função de validação do Supabase
                from src.utils.supabase_storage import validar_senha_usuario
                
                # Testar diretamente a função do Supabase
                try:
                    print("Testando Supabase diretamente...")
                    supabase_ok = validar_senha_usuario(primeiro_aluno, "123")
                    print(f"Supabase resultado: {supabase_ok}")
                except Exception as e:
                    print(f"Erro no Supabase: {e}")
                
                # Testar método do modelo
                try:
                    print("Testando metodo do modelo...")
                    resultado = user_model.validar_senha(primeiro_time, primeiro_aluno, "123")
                    print(f"Resultado da validacao: {resultado}")
                except Exception as e:
                    print(f"Erro na validacao: {e}")
            else:
                print("ERRO: Aluno nao e valido no time!")
        else:
            print("ERRO: Nenhum aluno encontrado!")
            
    except Exception as e:
        print(f"ERRO GERAL: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_login()