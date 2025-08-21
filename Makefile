# Makefile para o Sistema de Avaliação de Pares
# Automatiza tarefas comuns de desenvolvimento

.PHONY: help install install-dev test test-cov format lint type-check clean run run-viz

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

install-dev: ## Instala dependências de desenvolvimento
	$(PIP) install -e ".[dev]"

test: ## Executa testes unitários
	$(PYTHON) -m pytest tests/ -v

test-cov: ## Executa testes com cobertura
	$(PYTHON) -m pytest tests/ -v --cov=src --cov-report=html --cov-report=term

format: ## Formata código com Black
	$(PYTHON) scripts/format_code.py

lint: ## Verifica estilo do código com Flake8
	flake8 src/ tests/ --max-line-length=88 --ignore=E203,W503

type-check: ## Verifica tipos com MyPy
	mypy src/

quality: format lint type-check ## Executa todas as verificações de qualidade

run: ## Executa aplicativo principal (MVC)
	$(STREAMLIT) run app.py

run-viz: ## Executa visualizador (MVC)
	$(STREAMLIT) run visualizador_mvc.py

run-legacy: ## Executa aplicativo original
	$(STREAMLIT) run app.py

run-viz-legacy: ## Executa visualizador original
	$(STREAMLIT) run visualizar_dados.py

clean: ## Remove arquivos temporários e cache
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/

setup: install-dev ## Configura ambiente de desenvolvimento completo
	@echo "✅ Ambiente de desenvolvimento configurado!"

all: quality test-cov ## Executa todas as verificações e testes
	@echo "🎉 Todas as verificações passaram!"

# Comandos específicos para Windows
run-windows: ## Executa aplicativo no Windows
	run_app.bat

# Comandos de desenvolvimento
dev-setup: setup ## Configuração completa para desenvolvimento
	@echo "🚀 Ambiente pronto para desenvolvimento!"

dev-test: test-cov quality ## Testes e qualidade para desenvolvimento
	@echo "🧪 Testes e verificações concluídas!"

# Comandos de produção
prod-install: install ## Instalação para produção
	@echo "📦 Instalação de produção concluída!"

prod-run: run ## Execução em produção
	@echo "🚀 Aplicativo em execução!"
