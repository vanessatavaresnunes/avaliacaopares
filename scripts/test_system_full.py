#!/usr/bin/env python3
"""
Teste funcional completo do sistema de avaliação
"""

import sys
import os
from pathlib import Path
import tempfile
import pandas as pd

# Adicionar src ao path para imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_user_model():
    """Testa o modelo de usuário"""
    print("=== Teste 1: Modelo de Usuario ===")
    
    try:
        from models.usuario import UsuarioModel
        
        usuario_model = UsuarioModel()
        
        # Testar carregamento de times
        times = usuario_model.obter_times()
        print(f"Times carregados: {len(times)}")
        
        if len(times) > 0:
            time_teste = times[0]
            print(f"Testando com time: {time_teste}")
            
            # Testar carregamento de alunos
            alunos = usuario_model.obter_alunos_por_time(time_teste)
            print(f"Alunos no time: {len(alunos)}")
            
            if len(alunos) > 0:
                aluno_teste = alunos[0]['nome']
                print(f"Testando login com: {aluno_teste}")
                
                # Testar login com senha correta
                login_ok = usuario_model.validar_senha(time_teste, aluno_teste, "123")
                if login_ok:
                    print("✓ Login funcionando!")
                    return True, time_teste, aluno_teste
                else:
                    print("✗ Login falhou!")
                    return False, None, None
            else:
                print("✗ Nenhum aluno encontrado!")
                return False, None, None
        else:
            print("✗ Nenhum time encontrado!")
            return False, None, None
            
    except Exception as e:
        print(f"✗ Erro no teste de usuario: {e}")
        return False, None, None

def test_avaliacao_controller(time_teste, aluno_teste):
    """Testa o controller de avaliação"""
    print("\n=== Teste 2: Controller de Avaliacao ===")
    
    try:
        from controllers.avaliacao_controller import AvaliacaoController
        
        controller = AvaliacaoController()
        
        # Simular sessão de login
        class MockSessionState:
            def __init__(self):
                self.data = {}
            
            def get(self, key, default=None):
                return self.data.get(key, default)
            
            def __setitem__(self, key, value):
                self.data[key] = value
            
            def __getitem__(self, key):
                return self.data[key]
        
        # Simular streamlit session_state
        import streamlit as st
        if not hasattr(st, 'session_state'):
            st.session_state = MockSessionState()
        
        # Fazer login
        login_resultado = controller.fazer_login(time_teste, aluno_teste, "123")
        if login_resultado:
            print("✓ Login pelo controller OK!")
            
            # Obter alunos para avaliar
            alunos_avaliar = controller.obter_alunos_para_avaliar()
            print(f"✓ Alunos para avaliar: {len(alunos_avaliar)}")
            
            # Obter eixos
            eixos = controller.obter_nomes_eixos()
            print(f"✓ Eixos carregados: {len(eixos)}")
            
            return True, controller, alunos_avaliar, eixos
        else:
            print("✗ Login pelo controller falhou!")
            return False, None, None, None
            
    except Exception as e:
        print(f"✗ Erro no teste do controller: {e}")
        return False, None, None, None

def test_avaliacao_creation(controller, alunos_avaliar, eixos):
    """Testa criação de avaliação completa"""
    print("\n=== Teste 3: Criacao de Avaliacao ===")
    
    try:
        # Inicializar avaliações para todos os alunos
        for aluno in alunos_avaliar:
            controller.inicializar_avaliacao_aluno(aluno)
        
        print("✓ Avaliações inicializadas")
        
        # Preencher dados de teste
        controller.preencher_dados_teste()
        print("✓ Dados de teste preenchidos")
        
        # Validar avaliações
        controller.validar_avaliacoes()
        print("✓ Validação executada")
        
        # Tentar salvar avaliações
        sucesso, mensagem = controller.salvar_avaliacoes()
        
        if sucesso:
            print(f"✓ Avaliações salvas: {mensagem}")
            return True
        else:
            print(f"✗ Falha ao salvar: {mensagem}")
            return False
            
    except Exception as e:
        print(f"✗ Erro na criação de avaliação: {e}")
        return False

def test_data_loading():
    """Testa carregamento de dados salvos"""
    print("\n=== Teste 4: Carregamento de Dados ===")
    
    try:
        from models.avaliacao import AvaliacaoModel
        
        avaliacao_model = AvaliacaoModel()
        
        # Tentar carregar dados
        df = avaliacao_model.carregar_dados()
        
        if not df.empty:
            print(f"✓ Dados carregados: {len(df)} registros")
            print(f"✓ Colunas: {list(df.columns)}")
            
            # Mostrar estatísticas
            estatisticas = avaliacao_model.obter_estatisticas(df)
            print(f"✓ Estatísticas: {estatisticas}")
            
            return True
        else:
            print("! Nenhum dado encontrado (normal se for primeira execução)")
            return True
            
    except Exception as e:
        print(f"✗ Erro no carregamento: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("TESTE FUNCIONAL COMPLETO DO SISTEMA")
    print("=" * 50)
    
    # Teste 1: Modelo de usuário
    user_ok, time_teste, aluno_teste = test_user_model()
    if not user_ok:
        print("\n✗ FALHA: Sistema de usuários não funciona!")
        return False
    
    # Teste 2: Controller
    controller_ok, controller, alunos_avaliar, eixos = test_avaliacao_controller(time_teste, aluno_teste)
    if not controller_ok:
        print("\n✗ FALHA: Controller não funciona!")
        return False
    
    # Teste 3: Criação de avaliação
    avaliacao_ok = test_avaliacao_creation(controller, alunos_avaliar, eixos)
    if not avaliacao_ok:
        print("\n✗ FALHA: Criação de avaliação não funciona!")
        return False
    
    # Teste 4: Carregamento de dados
    data_ok = test_data_loading()
    if not data_ok:
        print("\n✗ FALHA: Carregamento de dados não funciona!")
        return False
    
    print("\n" + "=" * 50)
    print("✓ TODOS OS TESTES PASSARAM!")
    print("✓ Sistema está funcionando corretamente!")
    print("=" * 50)
    return True

if __name__ == "__main__":
    # Verificar se estamos no diretório correto
    if not Path("data/alunos.json").exists():
        print("ERRO: Execute o script a partir do diretório raiz do projeto!")
        sys.exit(1)
    
    if main():
        print("\n🎉 Sistema pronto para uso!")
    else:
        print("\n💥 Sistema tem problemas que precisam ser corrigidos!")
        sys.exit(1)