import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()
SUPABASE_URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
SUPABASE_KEY = os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY")
BUCKET_NAME = os.getenv("BUCKET_NAME", "avaliacaopares")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def upload_json_to_bucket(file_path: str, bucket_path: str):
    """Faz upload de um arquivo local para o bucket do Supabase, deletando antes se já existir."""
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
    res = supabase.storage.from_(BUCKET_NAME).download(bucket_path)
    with open(local_path, "wb") as f:
        f.write(res)

def list_json_files_in_bucket(prefix: str = ""):  # Ex: prefix="avaliacoes_"
    """Lista arquivos JSON no bucket com determinado prefixo."""
    files = supabase.storage.from_(BUCKET_NAME).list(path=prefix)
    return [f["name"] for f in files if f["name"].endswith(".json")]
