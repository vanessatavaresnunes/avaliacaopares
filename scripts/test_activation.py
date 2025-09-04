#!/usr/bin/env python3
"""
Teste especifico da logica de ativacao de usuarios
Verifica se a ativacao funciona corretamente apos as mudancas
"""

import sys
import os
from pathlib import Path
import json
import tempfile
import shutil

# Adicionar src ao path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_activation_logic():
    """Testa logica de ativacao de usuarios"""
    print("TESTE DE LOGICA DE ATIVACAO DE USUARIOS")
    print("=" * 50)
    
    try:
        # Criar dados temporarios para teste
        temp_dir = tempfile.mkdtemp()
        print(f"Usando diretorio temporario: {temp_dir}")
        
        # Criar arquivo de alunos de teste com usuario ativo e inativo
        test_alunos = {
            "Teste": [
                {
                    "nome": "Usuario Ativo",
                    "id": 100,
                    "ativo": True
                },
                {
                    "nome": "Usuario Inativo", 
                    "id": 101,
                    "ativo": False
                },
                {
                    "nome": "Usuario Sem Campo Ativo",
                    "id": 102
                }
            ]
        }
        
        alunos_path = Path(temp_dir) / "alunos.json"
        with open(alunos_path, 'w', encoding='utf-8') as f:
            json.dump(test_alunos, f, ensure_ascii=False, indent=2)
        
        # Criar arquivos de configuracao basicos
        config_data = {"nota_minima": 0, "nota_maxima": 3}
        config_path = Path(temp_dir) / "config.json"
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config_data, f)
        
        eixos_data = [{"nome": "Teste", "descricao": "Eixo teste"}]
        eixos_path = Path(temp_dir) / "eixos.json"
        with open(eixos_path, 'w', encoding='utf-8') as f:
            json.dump(eixos_data, f)
        
        print("OK: Arquivos de teste criados")
        
        # Importar e testar modelo
        from src.models.usuario import UsuarioModel
        
        # Criar modelo com diretorio temporario
        usuario_model = UsuarioModel(diretorio_config=temp_dir)
        print("OK: Modelo de usuario criado")
        
        # Teste 1: Usuario ativo deve fazer login
        print("\n--- Teste 1: Usuario Ativo ---")
        resultado = usuario_model.validar_senha("Teste", "Usuario Ativo", "123")
        if resultado:
            print("OK: Usuario ativo pode fazer login")
        else:
            print("ERRO: Usuario ativo nao conseguiu fazer login")
            return False
        
        # Teste 2: Usuario inativo nao deve fazer login
        print("\n--- Teste 2: Usuario Inativo ---")
        resultado = usuario_model.validar_senha("Teste", "Usuario Inativo", "123")
        if not resultado:
            print("OK: Usuario inativo foi bloqueado corretamente")
        else:
            print("ERRO: Usuario inativo conseguiu fazer login quando nao deveria")
            return False
        
        # Teste 3: Usuario sem campo 'ativo' deve ser considerado ativo por padrao
        print("\n--- Teste 3: Usuario Sem Campo Ativo (Padrao) ---")
        resultado = usuario_model.validar_senha("Teste", "Usuario Sem Campo Ativo", "123")
        if resultado:
            print("OK: Usuario sem campo 'ativo' foi considerado ativo por padrao")
        else:
            print("ERRO: Usuario sem campo 'ativo' foi bloqueado incorretamente")
            return False
        
        # Teste 4: Usuario inexistente nao deve fazer login
        print("\n--- Teste 4: Usuario Inexistente ---")
        resultado = usuario_model.validar_senha("Teste", "Usuario Inexistente", "123")
        if not resultado:
            print("OK: Usuario inexistente foi bloqueado corretamente")
        else:
            print("ERRO: Usuario inexistente conseguiu fazer login")
            return False
        
        # Teste 5: Time inexistente nao deve permitir login
        print("\n--- Teste 5: Time Inexistente ---")
        resultado = usuario_model.validar_senha("Time Inexistente", "Usuario Ativo", "123")
        if not resultado:
            print("OK: Time inexistente foi bloqueado corretamente")
        else:
            print("ERRO: Time inexistente permitiu login")
            return False
        
        # Teste 6: Senha incorreta nao deve permitir login
        print("\n--- Teste 6: Senha Incorreta ---")
        resultado = usuario_model.validar_senha("Teste", "Usuario Ativo", "senha_errada")
        if not resultado:
            print("OK: Senha incorreta foi bloqueada corretamente")
        else:
            print("ERRO: Senha incorreta permitiu login")
            return False
        
        print("\n" + "=" * 50)
        print("TODOS OS TESTES DE ATIVACAO PASSARAM!")
        print("Sistema de ativacao funciona corretamente")
        
        return True
        
    except Exception as e:
        print(f"ERRO no teste de ativacao: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Limpar arquivos temporarios
        if 'temp_dir' in locals():
            try:
                shutil.rmtree(temp_dir)
                print(f"Diretorio temporario removido: {temp_dir}")
            except:
                pass

def test_integration_activation():
    """Testa ativacao no sistema real"""
    print("\nTESTE DE ATIVACAO NO SISTEMA REAL")
    print("=" * 50)
    
    try:
        from src.models.usuario import UsuarioModel
        
        usuario_model = UsuarioModel()
        print("OK: Modelo carregado com dados reais")
        
        # Obter primeiro usuario de cada grupo para teste
        times = usuario_model.obter_times()
        print(f"Times encontrados: {times}")
        
        for time in times[:2]:  # Testar apenas 2 primeiros times
            alunos = usuario_model.obter_alunos_por_time(time)
            if alunos:
                primeiro_aluno = alunos[0]
                nome_aluno = primeiro_aluno['nome']
                
                print(f"\n--- Testando {nome_aluno} do {time} ---")
                
                # Verificar status de ativacao
                ativo = primeiro_aluno.get('ativo', True)  # Padrao: ativo
                print(f"Status de ativacao: {'Ativo' if ativo else 'Inativo'}")
                
                # Tentar login
                resultado = usuario_model.validar_senha(time, nome_aluno, "123")
                
                if ativo and resultado:
                    print("OK: Usuario ativo conseguiu fazer login")
                elif not ativo and not resultado:
                    print("OK: Usuario inativo foi bloqueado")
                elif ativo and not resultado:
                    print("AVISO: Usuario ativo foi bloqueado (pode ser problema de validacao)")
                elif not ativo and resultado:
                    print("ERRO: Usuario inativo conseguiu fazer login")
                    return False
        
        print("\nTeste de ativacao no sistema real concluido com sucesso")
        return True
        
    except Exception as e:
        print(f"ERRO no teste de ativacao real: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = True
    
    # Executar teste isolado
    if not test_activation_logic():
        success = False
    
    # Executar teste no sistema real
    if not test_integration_activation():
        success = False
    
    if success:
        print("\n" + "=" * 60)
        print("CONCLUSAO: Sistema de ativacao esta funcionando corretamente!")
        print("A logica de ativacao nao foi quebrada pelas mudancas.")
        print("Usuarios ativos podem fazer login, inativos sao bloqueados.")
    else:
        print("\n" + "=" * 60)
        print("PROBLEMA: Ha falhas no sistema de ativacao!")
        sys.exit(1)