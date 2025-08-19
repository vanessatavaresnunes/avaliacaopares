@echo off
echo Instalando dependencias...
pip install -r requirements.txt

echo.
echo Iniciando o aplicativo de avaliacao de pares...
echo.
streamlit run app.py

pause
