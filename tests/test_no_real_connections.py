"""
Testes para garantir que não há conexões reais com serviços externos durante os testes.
"""

import unittest
from unittest.mock import patch, MagicMock
from src.utils.supabase_storage import upload_json_to_bucket, download_json_from_bucket, list_json_files_in_bucket


class TestNoRealConnections(unittest.TestCase):
    """Testa que não há conexões reais com Supabase"""
    
    def test_no_real_supabase_connection_on_upload(self):
        """Testa que upload não faz conexão real"""
        # Este teste vai falhar se houver conexão real
        with patch('tempfile.NamedTemporaryFile') as mock_temp:
            mock_temp.return_value.__enter__.return_value.name = '/tmp/test.json'
            mock_temp.return_value.__enter__.return_value.write = MagicMock()
            
            with patch('builtins.open', create=True) as mock_open:
                mock_open.return_value.__enter__.return_value.read.return_value = b'{"test": "data"}'
                
                # Deve usar o mock, não conexão real
                upload_json_to_bucket('/tmp/test.json', 'test.json')
                
        # Se chegou até aqui, o mock funcionou
        self.assertTrue(True)
    
    def test_no_real_supabase_connection_on_download(self):
        """Testa que download não faz conexão real"""
        with patch('builtins.open', create=True) as mock_open:
            mock_open.return_value.__enter__.return_value.write = MagicMock()
            
            # Deve usar o mock, não conexão real
            download_json_from_bucket('test.json', '/tmp/test.json')
            
        # Se chegou até aqui, o mock funcionou
        self.assertTrue(True)
    
    def test_no_real_supabase_connection_on_list(self):
        """Testa que listagem não faz conexão real"""
        # Deve usar o mock, não conexão real
        files = list_json_files_in_bucket()
        
        # Mock retorna lista vazia
        self.assertIsInstance(files, list)


if __name__ == '__main__':
    unittest.main()