#!/usr/bin/env python3
"""
Script para migrar usuários do arquivo local alunos.json para o bucket usuarios_inteli do Supabase
"""

import json
import sys
import os
from pathlib import Path

# Adicionar src ao path para imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils.supabase_storage import salvar_usuario_no_bucket, carregar_usuario_do_bucket


def gerar_email_padrao(nome: str) -> str:
    """
    Gera um email padrão baseado no nome do aluno
    
    Args:
        nome: Nome completo do aluno
        
    Returns:
        Email no formato nome.sobrenome@inteli.edu.br
    """
    nome_normalizado = nome.lower()
    nome_normalizado = nome_normalizado.replace(" ", ".")
    nome_normalizado = nome_normalizado.replace("ã", "a").replace("ç", "c").replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
    return f"{nome_normalizado}@inteli.edu.br"


def migrar_usuarios():
    """
    Migra todos os usuários do arquivo alunos.json para o Supabase
    """
    # Caminho para o arquivo alunos.json (usar backup com senhas)
    caminho_alunos = Path(__file__).parent.parent / "data" / "alunos_backup.json"
    
    if not caminho_alunos.exists():
        print(f"* Arquivo {caminho_alunos} não encontrado!")
        return False
    
    try:
        # Carregar dados dos alunos
        with open(caminho_alunos, 'r', encoding='utf-8') as arquivo:
            dados_alunos = json.load(arquivo)
        
        print("*� Iniciando migração de usuários para o Supabase...")
        
        usuarios_migrados = 0
        usuarios_existentes = 0
        erros = 0
        
        # Processar cada grupo
        for nome_grupo, alunos in dados_alunos.items():
            print(f"\n*� Processando {nome_grupo}:")
            
            for aluno in alunos:
                nome = aluno['nome']
                senha = aluno['senha']
                id_aluno = aluno['id']
                
                # Verificar se usuário já existe no Supabase
                usuario_existente = carregar_usuario_do_bucket(nome)
                
                if usuario_existente:
                    print(f"  **  {nome} - já existe no Supabase")
                    usuarios_existentes += 1
                    continue
                
                # Gerar email padrão
                email = gerar_email_padrao(nome)
                
                # Dados extras do usuário
                dados_extras = {
                    "id": id_aluno,
                    "grupo": nome_grupo,
                    "data_migração": "2024-01-01"  # Data da migração
                }
                
                # Salvar no Supabase
                sucesso = salvar_usuario_no_bucket(nome, email, senha, dados_extras)
                
                if sucesso:
                    print(f"  * {nome} - migrado com sucesso")
                    usuarios_migrados += 1
                else:
                    print(f"  * {nome} - erro na migração")
                    erros += 1
        
        # Resumo da migração
        print(f"\n*� Resumo da migração:")
        print(f"  * Usuários migrados: {usuarios_migrados}")
        print(f"  **  Usuários já existentes: {usuarios_existentes}")
        print(f"  * Erros: {erros}")
        
        if erros == 0:
            print("\n*� Migração concluída com sucesso!")
            return True
        else:
            print(f"\n**  Migração concluída com {erros} erro(s)")
            return False
            
    except Exception as e:
        print(f"* Erro durante a migração: {e}")
        return False


def verificar_migracao():
    """
    Verifica se a migração foi bem-sucedida listando usuários do bucket
    """
    try:
        from utils.supabase_storage import listar_usuarios_bucket
        
        usuarios = listar_usuarios_bucket()
        print(f"\n*� Verificação: {len(usuarios)} usuários encontrados no bucket:")
        
        for usuario in usuarios:
            print(f"  - {usuario}")
            
    except Exception as e:
        print(f"* Erro na verificação: {e}")


if __name__ == "__main__":
    print("*� Script de Migração de Usuários para Supabase")
    print("=" * 50)
    
    # Verificar se o arquivo .env existe
    env_path = Path(__file__).parent.parent / ".env"
    if not env_path.exists():
        print("* Arquivo .env não encontrado!")
        print("Certifique-se de que as variáveis de ambiente estão configuradas:")
        print("- NEXT_PUBLIC_SUPABASE_URL")
        print("- NEXT_PUBLIC_SUPABASE_PUBLISHABLE_DEFAULT_KEY")
        print("- BUCKET_USERS")
        sys.exit(1)
    
    # Executar migração
    sucesso = migrar_usuarios()
    
    if sucesso:
        # Verificar migração
        verificar_migracao()
        print("\n✨ Processo concluído!")
    else:
        print("\n*� Processo falhou!")
        sys.exit(1)