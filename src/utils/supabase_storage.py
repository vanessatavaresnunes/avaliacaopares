import os
import json
import hashlib
import tempfile
from typing import Dict, Optional, List
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()
SUPABASE_URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
SUPABASE_KEY = os.getenv("NEXT_PUBLIC_SUPABASE_PUBLISHABLE_DEFAULT_KEY")
BUCKET_NAME = os.getenv("BUCKET_NAME", "inteli_avaliacao_pares_sprint")
BUCKET_USERS = os.getenv("BUCKET_USERS", "usuarios_inteli")

def get_supabase_client():
    """Cria e retorna cliente Supabase"""
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def upload_json_to_bucket(file_path: str, bucket_path: str):
    """Faz upload de um arquivo local para o bucket do Supabase, deletando antes se já existir."""
    supabase = get_supabase_client()
    # Tenta deletar antes (ignora erro se não existir)
    try:
        supabase.storage.from_(BUCKET_NAME).remove([bucket_path])
    except Exception:
        pass
    with open(file_path, "rb") as f:
        data = f.read()
    supabase.storage.from_(BUCKET_NAME).upload(path=bucket_path, file=data)

def download_json_from_bucket(bucket_path: str, local_path: str):
    """Faz download de um arquivo do bucket do Supabase para o local."""
    supabase = get_supabase_client()
    res = supabase.storage.from_(BUCKET_NAME).download(bucket_path)
    with open(local_path, "wb") as f:
        f.write(res)

def list_json_files_in_bucket(prefix: str = ""):  # Ex: prefix="avaliacoes_"
    """Lista arquivos JSON no bucket que começam com determinado prefixo no nome."""
    supabase = get_supabase_client()
    files = supabase.storage.from_(BUCKET_NAME).list()
    return [f["name"] for f in files if f["name"].startswith(prefix) and f["name"].endswith(".json")]


# Funções específicas para gerenciamento de usuários
def gerar_hash_senha(senha: str) -> str:
    """Gera hash SHA-256 da senha"""
    return hashlib.sha256(senha.encode('utf-8')).hexdigest()



def carregar_usuario_do_bucket(nome_usuario: str) -> Optional[Dict]:
    """
    Carrega dados do usuário do bucket usuarios_inteli
    
    Args:
        nome_usuario: Nome do usuário
        
    Returns:
        Dicionário com dados do usuário ou None se não encontrado
    """
    try:
        # Nome do arquivo no bucket
        nome_arquivo = f"{nome_usuario.replace(' ', '_').lower()}.json"
        
        # Criar arquivo temporário para download
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as tmp_file:
            arquivo_temp = tmp_file.name
        
        # Download do bucket
        supabase = get_supabase_client()
        res = supabase.storage.from_(BUCKET_USERS).download(nome_arquivo)
        
        with open(arquivo_temp, "wb") as f:
            f.write(res)
        
        # Ler dados do arquivo
        with open(arquivo_temp, "r", encoding='utf-8') as f:
            dados_usuario = json.load(f)
        
        # Limpar arquivo temporário
        os.unlink(arquivo_temp)
        
        return dados_usuario
        
    except Exception as e:
        # Limpar arquivo temporário se houver erro
        try:
            if 'arquivo_temp' in locals():
                os.unlink(arquivo_temp)
        except:
            pass
        return None


def validar_senha_usuario(nome_usuario: str, senha: str) -> bool:
    """
    Valida senha do usuário
    
    Args:
        nome_usuario: Nome do usuário
        senha: Senha em texto plano
        
    Returns:
        True se senha estiver correta, False caso contrário
    """
    dados_usuario = carregar_usuario_do_bucket(nome_usuario)
    if not dados_usuario:
        return False
    
    # Verificar se usuário está ativo
    if not dados_usuario.get("ativo", True):
        return False
    
    # Comparar hash da senha
    senha_hash = gerar_hash_senha(senha)
    return dados_usuario.get("senha_hash") == senha_hash


def listar_usuarios_bucket() -> List[str]:
    """Mantido por compatibilidade; não utilizado pelo app principal."""
    try:
        supabase = get_supabase_client()
        files = supabase.storage.from_(BUCKET_USERS).list()
        usuarios = []
        for arquivo in files:
            if arquivo["name"].endswith(".json"):
                nome_usuario = arquivo["name"].replace(".json", "").replace("_", " ").title()
                usuarios.append(nome_usuario)
        return sorted(usuarios)
    except Exception:
        return []


def salvar_usuario_no_bucket(nome_usuario: str, email: str, senha: str, dados_extras: Dict = None) -> bool:
    """
    Salva/atualiza dados do usuário no bucket de usuários com hash da senha.

    Args:
        nome_usuario: Nome do usuário
        email: Email do usuário
        senha: Nova senha em texto plano (será hasheada)
        dados_extras: Campos adicionais para persistir (ex.: ativo, primeiro_acesso)

    Returns:
        True se salvou com sucesso, False caso contrário
    """
    try:
        senha_hash = gerar_hash_senha(senha)

        dados_usuario = {
            "nome": nome_usuario,
            "email": email,
            "senha_hash": senha_hash,
            "ativo": True,
        }
        if dados_extras:
            dados_usuario.update(dados_extras)

        # Criar arquivo temporário
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as tmp_file:
            json.dump(dados_usuario, tmp_file, ensure_ascii=False, indent=2)
            arquivo_temp = tmp_file.name

        nome_arquivo = f"{nome_usuario.replace(' ', '_').lower()}.json"

        supabase = get_supabase_client()
        # Remover existente (ignorar erro)
        try:
            supabase.storage.from_(BUCKET_USERS).remove([nome_arquivo])
        except Exception:
            pass
        # Upload
        with open(arquivo_temp, "rb") as f:
            data = f.read()
        supabase.storage.from_(BUCKET_USERS).upload(path=nome_arquivo, file=data)

        os.unlink(arquivo_temp)
        return True
    except Exception as e:
        print(f"Erro ao salvar usuário {nome_usuario}: {e}")
        try:
            if 'arquivo_temp' in locals():
                os.unlink(arquivo_temp)
        except Exception:
            pass
        return False
