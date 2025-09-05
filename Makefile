# Makefile para o Sistema de Avaliação de Pares
# Automatiza tarefas comuns de desenvolvimento

.PHONY: help install test test-cov format clean run run-viz

# Variáveis
PYTHON = python
PIP = pip
STREAMLIT = streamlit

# Comandos principais
help: ## Mostra esta ajuda
	@echo "Sistema de Avaliação de Pares - Comandos disponíveis:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Instala dependências básicas
	$(PIP) install -r requirements.txt

test: ## Executa testes unitários
	$(PYTHON) -m pytest tests/ -v

test-cov: ## Executa testes com cobertura
	$(PYTHON) -m pytest tests/ -v --cov=src --cov-report=html --cov-report=term

format: ## Formata código com Black (se disponível)
	$(PYTHON) scripts/format_code.py || true

run: ## Executa aplicativo principal (MVC)
	$(STREAMLIT) run app.py

run-viz: ## Executa visualizador (MVC)
	$(STREAMLIT) run visualizador_mvc.py

clean: ## Remove arquivos temporários e cache
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/

all: test-cov ## Executa testes com cobertura
	@echo "🎉 Testes concluídos!"

# Comandos específicos para Windows
run-windows: ## Executa aplicativo no Windows
	run_app.bat
