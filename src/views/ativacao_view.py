"""
View para a tela de ativação e alteração de senha do aluno.
Responsável pela interface de primeiro acesso.
"""

import streamlit as st
from src.controllers.avaliacao_controller import AvaliacaoController


class AtivacaoView:
    """View responsável pela tela de ativação e troca de senha"""
    
    def __init__(self, controller: AvaliacaoController):
        self.controller = controller
    
    def renderizar(self):
        """Renderiza a tela de ativação e troca de senha"""
        st.title("🎓 Sistema de Avaliação de Pares")
        st.markdown("---")
        
        # Layout centralizado
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("### 🔐 Primeiro Acesso - Alteração de Senha")
            st.info("🔒 Esta é a sua primeira vez acessando o sistema. Por favor, altere sua senha padrão.")
            
            # Mostrar informações do usuário
            aluno_atual = st.session_state.get('aluno_atual', 'Aluno')
            time_atual = st.session_state.get('time_atual', 'Time')
            
            st.markdown(f"**Aluno:** {aluno_atual}")
            st.markdown(f"**Time:** {time_atual}")
            
            # Campos para nova senha
            st.markdown("#### Nova Senha")
            nova_senha = st.text_input(
                "Digite sua nova senha:",
                type="password",
                key="nova_senha"
            )
            
            confirmar_senha = st.text_input(
                "Confirme sua nova senha:",
                type="password",
                key="confirmar_senha"
            )
            
            # Botão de ativação
            col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
            with col_btn2:
                if st.button("✅ Ativar Conta", type="primary", use_container_width=True):
                    if not nova_senha:
                        st.error("❌ Por favor, digite uma nova senha.")
                    elif len(nova_senha) < 6:
                        st.error("❌ A senha deve ter pelo menos 6 caracteres.")
                    elif nova_senha != confirmar_senha:
                        st.error("❌ As senhas não coincidem. Por favor, verifique.")
                    else:
                        # Processar a ativação e mudança de senha
                        if self.controller.ativar_usuario(nova_senha):
                            st.success("✅ Conta ativada com sucesso! Sua senha foi alterada.")
                            st.info("🔄 Redirecionando para a tela principal...")
                            st.rerun()
                        else:
                            st.error("❌ Erro ao ativar conta. Por favor, tente novamente.")