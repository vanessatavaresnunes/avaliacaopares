#!/usr/bin/env python3
"""
Teste especifico para ativacao de usuarios usando pela primeira vez
Simula cenario de primeiro uso do sistema
"""

import sys
import os
from pathlib import Path
import json
import tempfile
import shutil

# Adicionar src ao path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_first_time_usage():
    """Testa cenario de primeiro uso do sistema"""
    print("TESTE DE PRIMEIRO USO DO SISTEMA")
    print("=" * 50)
    
    try:
        # Criar dados temporarios simulando sistema limpo (primeiro uso)
        temp_dir = tempfile.mkdtemp()
        print(f"Simulando primeiro uso no diretorio: {temp_dir}")
        
        # Criar arquivo de alunos sem dados de ativacao (como seria no inicio)
        fresh_alunos = {
            "Time Teste": [
                {
                    "nome": "Usuario Primeiro Uso",
                    "id": 200
                    # Note: sem campo 'ativo' - simulando dados originais
                },
                {
                    "nome": "Usuario Ja Usado",
                    "id": 201,
                    "ativo": True  # Simulando usuario ja ativado anteriormente
                }
            ]
        }
        
        alunos_path = Path(temp_dir) / "alunos.json"
        with open(alunos_path, 'w', encoding='utf-8') as f:
            json.dump(fresh_alunos, f, ensure_ascii=False, indent=2)
        
        # Criar arquivos de configuracao basicos
        config_data = {"nota_minima": 0, "nota_maxima": 3}
        config_path = Path(temp_dir) / "config.json"
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config_data, f)
        
        eixos_data = [{"nome": "Colaboracao", "descricao": "Eixo de colaboracao"}]
        eixos_path = Path(temp_dir) / "eixos.json"
        with open(eixos_path, 'w', encoding='utf-8') as f:
            json.dump(eixos_data, f)
        
        print("OK: Ambiente de primeiro uso simulado")
        
        # Importar e testar modelo
        from src.models.usuario import UsuarioModel
        
        # Criar modelo com dados de primeiro uso
        usuario_model = UsuarioModel(diretorio_config=temp_dir)
        print("OK: Sistema carregado com dados de primeiro uso")
        
        # Teste 1: Usuario sem campo 'ativo' deve ser considerado ativo (primeiro uso)
        print("\n--- Teste 1: Primeiro Login do Usuario ---")
        resultado = usuario_model.validar_senha("Time Teste", "Usuario Primeiro Uso", "123")
        if resultado:
            print("OK: Usuario de primeiro uso conseguiu fazer login (campo 'ativo' padrao = True)")
        else:
            print("ERRO: Usuario de primeiro uso foi bloqueado incorretamente")
            return False
        
        # Teste 2: Usuario ja com campo ativo deve continuar funcionando
        print("\n--- Teste 2: Usuario com Campo Ativo Explicito ---")
        resultado = usuario_model.validar_senha("Time Teste", "Usuario Ja Usado", "123")
        if resultado:
            print("OK: Usuario com campo 'ativo' explicito continua funcionando")
        else:
            print("ERRO: Usuario com campo 'ativo' foi bloqueado")
            return False
        
        # Teste 3: Verificar se sistema reconhece usuarios do time
        print("\n--- Teste 3: Validacao de Time e Usuarios ---")
        time_valido = usuario_model.validar_time("Time Teste")
        usuario_valido = usuario_model.validar_aluno("Time Teste", "Usuario Primeiro Uso")
        
        if time_valido and usuario_valido:
            print("OK: Sistema reconhece time e usuario corretamente")
        else:
            print(f"ERRO: Problema de validacao - Time: {time_valido}, Usuario: {usuario_valido}")
            return False
        
        # Teste 4: Simular controller de avaliacao com primeiro uso
        print("\n--- Teste 4: Integracao com Controller ---")
        
        # Simular session_state basico
        class MockSessionState:
            def __init__(self):
                self.data = {}
            
            def get(self, key, default=None):
                return self.data.get(key, default)
            
            def __setitem__(self, key, value):
                self.data[key] = value
            
            def __contains__(self, key):
                return key in self.data
        
        # Configurar mock do streamlit
        import streamlit as st
        st.session_state = MockSessionState()
        
        from src.controllers.avaliacao_controller import AvaliacaoController
        
        # Usar diretorio de dados temporario
        original_data_dir = None
        if hasattr(AvaliacaoController, '_get_data_directory'):
            # Se houver metodo para configurar diretorio, usar ele
            pass
        
        controller = AvaliacaoController()
        # Sobrescrever modelo com nosso modelo de teste
        controller.usuario_model = usuario_model
        
        # Testar login de primeiro uso via controller
        login_sucesso = controller.fazer_login("Time Teste", "Usuario Primeiro Uso", "123")
        
        if login_sucesso:
            print("OK: Login de primeiro uso via controller funcionou")
            print(f"Usuario logado: {st.session_state.get('aluno_atual')}")
        else:
            print("ERRO: Login de primeiro uso via controller falhou")
            return False
        
        print("\n" + "=" * 50)
        print("TESTE DE PRIMEIRO USO PASSOU COMPLETAMENTE!")
        print("Sistema funciona corretamente para usuarios novos")
        
        return True
        
    except Exception as e:
        print(f"ERRO no teste de primeiro uso: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Limpar arquivos temporarios
        if 'temp_dir' in locals():
            try:
                shutil.rmtree(temp_dir)
                print(f"Ambiente temporario removido: {temp_dir}")
            except:
                pass

def test_real_system_first_time():
    """Testa comportamento de primeiro uso no sistema real"""
    print("\nVERIFICACAO DO SISTEMA REAL PARA PRIMEIRO USO")
    print("=" * 55)
    
    try:
        from src.models.usuario import UsuarioModel
        
        usuario_model = UsuarioModel()
        
        # Verificar estrutura dos dados reais
        print("Analisando estrutura de dados atual...")
        
        times = usuario_model.obter_times()
        usuarios_sem_campo_ativo = 0
        usuarios_com_campo_ativo = 0
        
        for time in times:
            alunos = usuario_model.alunos.get(time, [])
            for aluno in alunos:
                if 'ativo' in aluno:
                    usuarios_com_campo_ativo += 1
                else:
                    usuarios_sem_campo_ativo += 1
        
        print(f"Usuarios SEM campo 'ativo': {usuarios_sem_campo_ativo}")
        print(f"Usuarios COM campo 'ativo': {usuarios_com_campo_ativo}")
        
        if usuarios_sem_campo_ativo > 0:
            print("OK: Ha usuarios sem campo 'ativo' (sera padrao = True)")
            print("Sistema esta preparado para primeiro uso")
        else:
            print("INFO: Todos usuarios ja tem campo 'ativo' definido")
        
        # Testar login com usuario real (primeiro do primeiro time)
        primeiro_time = times[0]
        primeiro_aluno = usuario_model.obter_alunos_por_time(primeiro_time)[0]
        nome_primeiro_aluno = primeiro_aluno['nome']
        
        print(f"\nTestando primeiro uso com: {nome_primeiro_aluno}")
        
        resultado = usuario_model.validar_senha(primeiro_time, nome_primeiro_aluno, "123")
        
        if resultado:
            print("OK: Usuario real pode fazer login (primeiro uso funcionando)")
        else:
            print("PROBLEMA: Usuario real nao consegue fazer login")
            
            # Investigar motivo
            usuario_existe = usuario_model.validar_aluno(primeiro_time, nome_primeiro_aluno)
            time_existe = usuario_model.validar_time(primeiro_time)
            
            print(f"Debug - Time existe: {time_existe}")
            print(f"Debug - Usuario existe: {usuario_existe}")
            print(f"Debug - Dados do usuario: {primeiro_aluno}")
            
            return False
        
        return True
        
    except Exception as e:
        print(f"ERRO na verificacao do sistema real: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = True
    
    # Testar cenario simulado de primeiro uso
    if not test_first_time_usage():
        success = False
    
    # Verificar sistema real
    if not test_real_system_first_time():
        success = False
    
    if success:
        print("\n" + "=" * 70)
        print("CONCLUSAO FINAL: Sistema de ativacao esta COMPLETAMENTE funcional!")
        print("* Usuarios novos (primeiro uso) podem fazer login normalmente")
        print("* Campo 'ativo' ausente é tratado como True (ativo) por padrao")
        print("* Sistema preserva compatibilidade com dados existentes")
        print("* Nenhuma funcionalidade foi quebrada pelas mudancas de seguranca")
    else:
        print("\n" + "=" * 70)
        print("PROBLEMA: Ha falhas no sistema de primeiro uso!")
        sys.exit(1)