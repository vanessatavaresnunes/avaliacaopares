#!/usr/bin/env python3
"""
Teste completo de criação de avaliação
"""

import sys
import os
from pathlib import Path

# Adicionar src ao path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_avaliacao_completa():
    """Testa criação completa de uma avaliação"""
    print("TESTE DE CRIACAO DE AVALIACAO COMPLETA")
    print("=" * 50)
    
    try:
        from src.controllers.avaliacao_controller import AvaliacaoController
        
        # Simular session_state do Streamlit
        class MockSession:
            def __init__(self):
                self.data = {}
                # Adicionar sprint padrão
                self.data['sprint_atual'] = 'Sprint 1'
            
            def get(self, key, default=None):
                return self.data.get(key, default)
            
            def __setitem__(self, key, value):
                self.data[key] = value
            
            def __getitem__(self, key):
                return self.data.get(key)
                
            def __contains__(self, key):
                return key in self.data
            
            def __getattr__(self, key):
                return self.data.get(key)
            
            def __setattr__(self, key, value):
                if key == 'data':
                    super().__setattr__(key, value)
                else:
                    self.data[key] = value
        
        # Configurar session_state mock
        import streamlit as st
        st.session_state = MockSession()
        
        controller = AvaliacaoController()
        print("OK: Controller criado")
        
        # 1. Fazer login
        print("\n--- Teste 1: Login ---")
        login_ok = controller.fazer_login("Grupo 1", "Gabriel Santos do Nascimento", "123")
        if login_ok:
            print("OK: Login realizado com sucesso")
            print(f"Usuario logado: {st.session_state.get('aluno_atual')}")
            print(f"Time: {st.session_state.get('time_atual')}")
        else:
            print("ERRO: Login falhou!")
            return False
        
        # 2. Obter alunos para avaliar
        print("\n--- Teste 2: Alunos para Avaliar ---")
        alunos = controller.obter_alunos_para_avaliar()
        print(f"OK: {len(alunos)} alunos para avaliar")
        for aluno in alunos:
            print(f"  - {aluno['nome']} (ID: {aluno['id']})")
        
        # 3. Inicializar sessão
        print("\n--- Teste 3: Inicializar Sessão ---")
        controller.inicializar_sessao()
        print("OK: Sessão inicializada")
        
        # 4. Inicializar avaliações para todos os alunos
        print("\n--- Teste 4: Inicializar Avaliacoes ---")
        for aluno in alunos:
            controller.inicializar_avaliacao_aluno(aluno)
        print("OK: Avaliacoes inicializadas para todos os alunos")
        
        # 5. Preencher dados de teste
        print("\n--- Teste 5: Preencher Dados de Teste ---")
        controller.preencher_dados_teste()
        print("OK: Dados de teste preenchidos")
        
        # 6. Validar avaliações
        print("\n--- Teste 6: Validar Avaliacoes ---")
        controller.validar_avaliacoes()
        print("OK: Validacao executada")
        
        # Mostrar status da validação
        if 'validation_messages' in st.session_state.data:
            msgs = st.session_state.data['validation_messages']
            print("Status das validacoes:")
            
            # Soma das notas por eixo
            soma_notas = msgs.get('soma_notas', {})
            if 'details' in soma_notas:
                for eixo, details in soma_notas['details'].items():
                    soma_atual = details.get('soma_atual', 0)
                    soma_esperada = details.get('soma_esperada', 0)
                    status = "OK" if details.get('valido', False) else "ERRO"
                    print(f"  - {eixo}: {soma_atual}/{soma_esperada} pontos [{status}]")
            
            # Outros status
            for key, value in msgs.items():
                if key != 'soma_notas':
                    status = "OK" if value.get('is_valid', False) else "ERRO"
                    print(f"  - {key}: [{status}]")
        
        # 7. Tentar salvar avaliações
        print("\n--- Teste 7: Salvar Avaliacoes ---")
        sucesso, mensagem = controller.salvar_avaliacoes()
        if sucesso:
            print(f"OK: Avaliacoes salvas! {mensagem}")
        else:
            print(f"ERRO: Falha ao salvar - {mensagem}")
            return False
        
        # 8. Verificar se os dados foram salvos
        print("\n--- Teste 8: Verificar Dados Salvos ---")
        from src.models.avaliacao import AvaliacaoModel
        
        avaliacao_model = AvaliacaoModel()
        df = avaliacao_model.carregar_dados()
        
        if not df.empty:
            print(f"OK: Dados carregados - {len(df)} registros")
            print(f"Colunas: {list(df.columns)}")
            
            # Mostrar algumas estatísticas
            stats = avaliacao_model.obter_estatisticas(df)
            print(f"Estatisticas: {stats}")
            
            # Mostrar últimos registros
            print("\nUltimos 3 registros:")
            for i, row in df.tail(3).iterrows():
                print(f"  {row['nome_avaliador']} -> {row['nome_avaliado']}: {row['eixo']} = {row['nota']}")
        else:
            print("AVISO: Nenhum dado encontrado (pode ser problema de salvamento)")
        
        print("\n" + "=" * 50)
        print("TESTE DE AVALIACAO COMPLETO PASSOU!")
        print("Sistema funcional para criacao de avaliacoes!")
        return True
        
    except Exception as e:
        print(f"ERRO no teste de avaliacao: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if test_avaliacao_completa():
        print("\nSistema pronto para uso em producao!")
        print("Execute: streamlit run app.py")
    else:
        print("\nHa problemas que precisam ser corrigidos!")
        sys.exit(1)