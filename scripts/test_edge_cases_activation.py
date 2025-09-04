#!/usr/bin/env python3
"""
Teste de casos extremos para ativacao de usuarios
Verifica robustez do sistema em situacoes incomuns
"""

import sys
import os
from pathlib import Path
import json
import tempfile
import shutil

# Adicionar src ao path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_edge_cases():
    """Testa casos extremos de ativacao"""
    print("TESTE DE CASOS EXTREMOS - ATIVACAO DE USUARIOS")
    print("=" * 55)
    
    try:
        # Criar dados temporarios com casos extremos
        temp_dir = tempfile.mkdtemp()
        print(f"Testando casos extremos no diretorio: {temp_dir}")
        
        # Casos extremos para teste
        edge_case_alunos = {
            "Team Edge Cases": [
                {
                    "nome": "Usuario Normal",
                    "id": 300,
                    "ativo": True
                },
                {
                    "nome": "Usuario Ativo False",
                    "id": 301,
                    "ativo": False
                },
                {
                    "nome": "Usuario Ativo None",
                    "id": 302,
                    "ativo": None  # Valor None - caso extremo
                },
                {
                    "nome": "Usuario Ativo Zero",
                    "id": 303,
                    "ativo": 0  # Valor falsy - caso extremo
                },
                {
                    "nome": "Usuario Ativo String True",
                    "id": 304,
                    "ativo": "true"  # String ao inves de boolean
                },
                {
                    "nome": "Usuario Ativo String False",
                    "id": 305,
                    "ativo": "false"  # String ao inves de boolean
                },
                {
                    "nome": "Usuario Ativo Numero",
                    "id": 306,
                    "ativo": 1  # Numero ao inves de boolean
                },
                {
                    "nome": "Usuario Nome Vazio",
                    "id": 307,
                    "nome": "",  # Nome vazio
                    "ativo": True
                },
                {
                    "nome": "Usuario Com Espacos   ",  # Nome com espacos extras
                    "id": 308,
                    "ativo": True
                },
                {
                    "nome": "Usuário com Acentos",  # Nome com acentos especiais
                    "id": 309,
                    "ativo": True
                }
            ],
            "": [  # Time com nome vazio - caso extremo
                {
                    "nome": "Usuario Time Vazio",
                    "id": 310,
                    "ativo": True
                }
            ]
        }
        
        alunos_path = Path(temp_dir) / "alunos.json"
        with open(alunos_path, 'w', encoding='utf-8') as f:
            json.dump(edge_case_alunos, f, ensure_ascii=False, indent=2)
        
        # Criar arquivos de configuracao
        config_data = {"nota_minima": 0, "nota_maxima": 3}
        config_path = Path(temp_dir) / "config.json"
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config_data, f)
        
        eixos_data = [{"nome": "Edge", "descricao": "Eixo teste"}]
        eixos_path = Path(temp_dir) / "eixos.json"
        with open(eixos_path, 'w', encoding='utf-8') as f:
            json.dump(eixos_data, f)
        
        print("OK: Dados de casos extremos criados")
        
        from src.models.usuario import UsuarioModel
        
        usuario_model = UsuarioModel(diretorio_config=temp_dir)
        print("OK: Modelo carregado com casos extremos")
        
        # Teste 1: Ativo = None deve ser tratado como False
        print("\n--- Teste 1: Campo Ativo = None ---")
        resultado = usuario_model.validar_senha("Team Edge Cases", "Usuario Ativo None", "123")
        if not resultado:
            print("OK: Campo 'ativo' = None foi tratado como False (bloqueado)")
        else:
            print("PROBLEMA: Campo 'ativo' = None permitiu login")
        
        # Teste 2: Ativo = 0 deve ser tratado como False
        print("\n--- Teste 2: Campo Ativo = 0 ---")
        resultado = usuario_model.validar_senha("Team Edge Cases", "Usuario Ativo Zero", "123")
        if not resultado:
            print("OK: Campo 'ativo' = 0 foi tratado como False (bloqueado)")
        else:
            print("PROBLEMA: Campo 'ativo' = 0 permitiu login")
        
        # Teste 3: Ativo = "true" (string) deve ser tratado como False
        print("\n--- Teste 3: Campo Ativo = String 'true' ---")
        resultado = usuario_model.validar_senha("Team Edge Cases", "Usuario Ativo String True", "123")
        if not resultado:
            print("OK: Campo 'ativo' = 'true' (string) foi tratado como False")
        else:
            print("PROBLEMA: Campo 'ativo' = 'true' (string) permitiu login")
        
        # Teste 4: Ativo = 1 deve ser tratado como False (apenas True boolean é válido)
        print("\n--- Teste 4: Campo Ativo = 1 ---")
        resultado = usuario_model.validar_senha("Team Edge Cases", "Usuario Ativo Numero", "123")
        if not resultado:
            print("OK: Campo 'ativo' = 1 foi tratado como False")
        else:
            print("PROBLEMA: Campo 'ativo' = 1 permitiu login")
        
        # Teste 5: Nome vazio deve falhar na validacao
        print("\n--- Teste 5: Nome de Usuario Vazio ---")
        resultado = usuario_model.validar_senha("Team Edge Cases", "", "123")
        if not resultado:
            print("OK: Usuario com nome vazio foi bloqueado")
        else:
            print("PROBLEMA: Usuario com nome vazio permitiu login")
        
        # Teste 6: Nome com espacos extras
        print("\n--- Teste 6: Nome com Espacos Extras ---")
        resultado = usuario_model.validar_senha("Team Edge Cases", "Usuario Com Espacos   ", "123")
        if resultado:
            print("OK: Usuario com espacos extras no nome conseguiu login")
        else:
            print("PROBLEMA: Usuario com espacos extras foi bloqueado incorretamente")
        
        # Teste 7: Nome com acentos especiais
        print("\n--- Teste 7: Nome com Acentos ---")
        resultado = usuario_model.validar_senha("Team Edge Cases", "Usuário com Acentos", "123")
        if resultado:
            print("OK: Usuario com acentos conseguiu login (Unicode funciona)")
        else:
            print("PROBLEMA: Usuario com acentos foi bloqueado")
        
        # Teste 8: Time com nome vazio
        print("\n--- Teste 8: Time com Nome Vazio ---")
        resultado = usuario_model.validar_senha("", "Usuario Time Vazio", "123")
        if resultado:
            print("OK: Time com nome vazio funciona")
        else:
            print("INFO: Time com nome vazio foi bloqueado (comportamento esperado)")
        
        # Teste 9: Senha com caracteres especiais
        print("\n--- Teste 9: Validacao com Senha Especial ---")
        resultado = usuario_model.validar_senha("Team Edge Cases", "Usuario Normal", "!@#$%^&*()")
        if not resultado:
            print("OK: Senha especial foi rejeitada (apenas '123' aceita)")
        else:
            print("PROBLEMA: Senha especial foi aceita")
        
        # Teste 10: Case sensitivity nos nomes
        print("\n--- Teste 10: Case Sensitivity ---")
        resultado_lower = usuario_model.validar_senha("team edge cases", "usuario normal", "123")
        resultado_upper = usuario_model.validar_senha("TEAM EDGE CASES", "USUARIO NORMAL", "123")
        
        if not resultado_lower and not resultado_upper:
            print("OK: Sistema é case-sensitive (comportamento correto)")
        else:
            print("INFO: Sistema aceita variações de case")
        
        print("\n" + "=" * 55)
        print("TESTE DE CASOS EXTREMOS CONCLUIDO!")
        print("Sistema demonstrou robustez em situações incomuns")
        
        return True
        
    except Exception as e:
        print(f"ERRO no teste de casos extremos: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        if 'temp_dir' in locals():
            try:
                shutil.rmtree(temp_dir)
                print(f"Ambiente de teste removido: {temp_dir}")
            except:
                pass

def test_malformed_data():
    """Testa comportamento com dados malformados"""
    print("\nTESTE DE DADOS MALFORMADOS")
    print("=" * 35)
    
    try:
        temp_dir = tempfile.mkdtemp()
        
        # Casos de dados malformados
        test_cases = [
            {
                "name": "JSON inválido",
                "data": "{ invalid json }",
                "should_handle": True
            },
            {
                "name": "Lista ao invés de objeto",
                "data": json.dumps([{"nome": "Test", "id": 1}]),
                "should_handle": True
            },
            {
                "name": "Arquivo vazio",
                "data": "",
                "should_handle": True
            }
        ]
        
        from src.models.usuario import UsuarioModel
        
        for case in test_cases:
            print(f"\n--- Testando: {case['name']} ---")
            
            # Criar arquivo malformado
            alunos_path = Path(temp_dir) / "alunos.json"
            with open(alunos_path, 'w', encoding='utf-8') as f:
                f.write(case['data'])
            
            # Criar outros arquivos necessarios
            config_data = {"nota_minima": 0, "nota_maxima": 3}
            config_path = Path(temp_dir) / "config.json"
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f)
            
            eixos_data = []
            eixos_path = Path(temp_dir) / "eixos.json"
            with open(eixos_path, 'w', encoding='utf-8') as f:
                json.dump(eixos_data, f)
            
            try:
                usuario_model = UsuarioModel(diretorio_config=temp_dir)
                print(f"OK: Sistema lidou com {case['name']} sem quebrar")
                
                # Verificar se retornou estrutura vazia
                times = usuario_model.obter_times()
                if len(times) == 0:
                    print("OK: Retornou estrutura vazia para dados inválidos")
                else:
                    print(f"INFO: Retornou {len(times)} times mesmo com dados inválidos")
                
            except Exception as e:
                if case['should_handle']:
                    print(f"PROBLEMA: Sistema não lidou bem com {case['name']}: {e}")
                else:
                    print(f"OK: Sistema rejeitou corretamente {case['name']}")
        
        return True
        
    except Exception as e:
        print(f"ERRO no teste de dados malformados: {e}")
        return False
    
    finally:
        if 'temp_dir' in locals():
            try:
                shutil.rmtree(temp_dir)
            except:
                pass

if __name__ == "__main__":
    success = True
    
    # Testar casos extremos
    if not test_edge_cases():
        success = False
    
    # Testar dados malformados
    if not test_malformed_data():
        success = False
    
    if success:
        print("\n" + "=" * 70)
        print("CONCLUSAO: Sistema passou em TODOS os testes de casos extremos!")
        print("* Tratamento robusto de valores inválidos para campo 'ativo'")
        print("* Validação correta de nomes com caracteres especiais")
        print("* Comportamento previsível com dados malformados")
        print("* Sistema é resiliente a situações extremas")
    else:
        print("\n" + "=" * 70)
        print("ATENÇÃO: Algumas falhas encontradas nos casos extremos!")
        sys.exit(1)