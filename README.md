# Sistema de Avaliação de Pares

Um aplicativo Streamlit para avaliação de pares em equipes, onde cada aluno avalia seus colegas de time em 3 eixos diferentes.

**🔄 Versão 2.0 - Reescrita com padrão MVC e boas práticas de programação**

## 🏗️ Arquitetura

O projeto foi reescrito seguindo o padrão **MVC (Model-View-Controller)** e boas práticas de programação:

- **📁 Models**: Estrutura de dados e regras de negócio
- **🎮 Controllers**: Lógica de coordenação entre models e views
- **👁️ Views**: Interface do usuário e apresentação
- **🧪 Tests**: Testes unitários e de integração
- **🔧 Scripts**: Ferramentas de desenvolvimento

## Funcionalidades

- 🔐 **Tela de Login**: Seleção de time e aluno
- 📊 **Matriz de Avaliação**: Interface para avaliar colegas em 3 eixos
- 📋 **Descrições Detalhadas**: Cada eixo inclui descrição e lista de observações específicas
- ✅ **Validação Automática**: Garante que a soma das notas seja igual ao número de colegas + 1
- 💬 **Feedback Textual**: Campo para comentários sobre cada colega
- 💾 **Salvamento em JSON**: Dados salvos em formato eficiente
- 📈 **Relatórios**: Arquivos individuais e consolidados
- ⚙️ **Configuração Flexível**: Eixos, alunos e configurações via arquivos JSON

## Eixos de Avaliação

O sistema agora utiliza configurações baseadas em JSON para maior flexibilidade:

### Eixos Atuais
1. **Entregas reais**: Avalia o cumprimento das entregas da sprint
2. **Valor Percebido**: Avalia o impacto das entregas para o grupo
3. **Caixa de Ferramentas**: Avalia o desenvolvimento técnico do aluno

### Configuração via JSON
- `data/alunos.json`: Lista de alunos organizados por grupos
- `data/eixos.json`: Definição dos eixos com descrições e observações
- `data/config.json`: Configurações do sistema (notas mín/máx, diretório)

Cada eixo inclui:
- **Descrição detalhada** do que avaliar
- **Lista de observações** específicas para verificar (GitHub, Trello, Daily, etc.)

## 📦 Instalação

### 🖥️ Instalação Cross-Platform (Recomendada)

**Windows, macOS e Linux:**

```bash
# Opção 1: Script automático
python install.py

# Opção 2: Instalação manual
pip install -r requirements.txt
```

### 🔧 Instalação Manual por Sistema

**Windows:**
```cmd
# CMD ou PowerShell
python -m pip install -r requirements.txt
```

**macOS/Linux:**
```bash
# Terminal
pip3 install -r requirements.txt
# ou
python3 -m pip install -r requirements.txt
```

### 📋 Pré-requisitos
- Python 3.8 ou superior
- pip (geralmente vem com Python)

### Estrutura do Projeto
```
AvaliacaoParesv2/
├── src/                    # Código fonte principal
│   ├── models/            # Modelos de dados
│   ├── controllers/       # Controllers
│   ├── views/            # Views (interfaces)
│   └── utils/            # Utilitários (Supabase)
├── data/                  # Configurações em JSON
│   ├── alunos.json       # Lista de alunos por grupos
│   ├── eixos.json        # Definição dos eixos
│   └── config.json       # Configurações do sistema
├── tests/                 # Testes unitários
├── scripts/              # Scripts de desenvolvimento
├── docs/                 # Documentação da API
├── dados/                # Dados salvos (criado automaticamente)
├── app.py                # Aplicativo principal (MVC)
├── visualizador_mvc.py   # Visualizador (MVC)
└── requirements.txt      # Dependências
```

## 🧪 Testes

### Executar Testes

**Comando básico:**
```bash
python -m pytest tests/ -v
```

**Com cobertura de código:**
```bash
python -m pytest tests/ -v --cov=src --cov-report=html --cov-report=term
```

<!-- Removido: script de qualidade completo -->

### Relatórios
- **Terminal**: Exibe cobertura diretamente
- **HTML**: Relatório detalhado em `htmlcov/index.html`
- **Qualidade**: Script roda testes + formatação + style check

### Estrutura dos Testes
- `test_avaliacao_model.py`: Testes do modelo de avaliação
- `test_analise_calculo.py`: Testes de cálculos matemáticos

## 🚀 Como Usar

### 🖥️ Cross-Platform (Recomendado)

**Windows, macOS e Linux:**

```bash
# Aplicativo principal
streamlit run app.py

# Visualizador de dados
streamlit run visualizador_mvc.py
```

### Docker Compose
- Somente o sistema (alunos) `app.py`:
```bash
docker compose -f docker-compose.app.yml up --build
# porta padrão: 8501 (configurável via APP_PORT)
```
- Somente o painel de análises (professora):
```bash
docker compose -f docker-compose.viz.yml up --build
# porta padrão: 8502 (configurável via VIZ_PORT)
```

### 🔧 Comandos por Sistema

**Windows:**
```cmd
# CMD ou PowerShell
streamlit run app.py
```

**macOS/Linux:**
```bash
# Terminal
streamlit run app.py
# ou
python -m streamlit run app.py
```

### 🌐 Acesso
- **URL:** http://localhost:8501
- **Porta padrão:** 8501
- **Para parar:** Ctrl+C no terminal

### 📱 Compatibilidade
- **Navegadores:** Chrome, Firefox, Safari, Edge
- **Dispositivos:** Desktop, tablet, mobile (responsivo)

## 🔧 Troubleshooting

### Problemas Comuns

**❌ "pip não é reconhecido" (Windows)**
```cmd
# Instale o Python do site oficial: https://python.org
# Ou use:
python -m pip install -r requirements.txt
```

**❌ "Permission denied" (macOS/Linux)**
```bash
# Use sudo ou instale para usuário:
pip install --user -r requirements.txt
```

**❌ "Porta 8501 já em uso"**
```bash
# Use outra porta:
streamlit run app.py --server.port 8502
```

**❌ "Erro de encoding"**
```bash
# Defina encoding UTF-8:
export PYTHONIOENCODING=utf-8  # Linux/macOS
set PYTHONIOENCODING=utf-8     # Windows
```

### 🆘 Suporte
- **Python:** 3.8+
- **Sistemas:** Windows 10+, macOS 10.14+, Ubuntu 18.04+
- **Memória:** Mínimo 4GB RAM

3. **Tela de Login**:
   - Selecione seu time
   - Selecione seu nome
   - Clique em "Entrar"

4. **Tela de Avaliação**:
   - Para cada colega, atribua notas de 0 a 3 em cada eixo
   - Escreva um feedback textual
   - **Importante**: A soma das notas de cada eixo deve ser igual ao número de colegas + 1
   - Clique em "Salvar Avaliações"

## Estrutura de Dados

Os dados são salvos em dois formatos:

1. **Arquivo Individual**: `dados/avaliacoes_YYYYMMDD_HHMMSS.parquet`
2. **Arquivo Consolidado**: `dados/avaliacoes_consolidadas.parquet`

### Campos Salvos

- `timestamp`: Data e hora da avaliação
- `aluno_avaliador`: Nome do aluno que fez a avaliação
- `time`: Time do avaliador
- `aluno_avaliado`: Nome do aluno avaliado
- `eixo`: Eixo de avaliação (Entregas reais, Valor Percebido, Caixa de Ferramentas)
- `nota`: Nota atribuída (0-3)
- `feedback`: Comentário textual específico para cada eixo

## ⚙️ Personalização

### Versão MVC
Para personalizar a lista de alunos, edite o arquivo `src/models/usuario.py`:

```python
def __init__(self):
    self.alunos = {
        "Time A": ["Seu Nome", "Colega 1", "Colega 2", "Colega 3"],
        "Time B": ["Outro Nome", "Outro Colega 1", "Outro Colega 2"],
        # Adicione mais times conforme necessário
    }
    
    self.eixos = ["Colaboração", "Responsabilidade", "Comunicação"]
    
    self.config = Configuracao(
        nota_minima=0,
        nota_maxima=3,
        diretorio_dados="dados"
    )
```

### Versão Original
Para personalizar a lista de alunos, edite o arquivo `config.py`:

```python
ALUNOS = {
    "Time A": ["Seu Nome", "Colega 1", "Colega 2", "Colega 3"],
    "Time B": ["Outro Nome", "Outro Colega 1", "Outro Colega 2"],
    # Adicione mais times conforme necessário
}

# Você também pode modificar os eixos de avaliação
EIXOS = ["Colaboração", "Responsabilidade", "Comunicação"]

# E as configurações do sistema
CONFIG = {
    "nota_minima": 0,
    "nota_maxima": 3,
    "diretorio_dados": "dados"
}
```

## Validação de Notas

O sistema garante que:
- Cada eixo tenha exatamente `(número de colegas + 1)` pontos distribuídos
- As notas sejam de 0 a 3
- Todas as avaliações tenham feedback textual

## 📊 Visualização de Dados

### Versão MVC (Recomendada)
```bash
streamlit run visualizador_mvc.py
```

### Versão Original
```bash
streamlit run visualizar_dados.py
```

Este aplicativo permite:
- Visualizar resumos estatísticos
- Filtrar dados por time, avaliador ou eixo
- Ver gráficos de distribuição de notas
- Exportar dados para CSV
- Visualizar feedbacks textuais

## 🧪 Desenvolvimento e Testes

### Executar Testes
```bash
# Executar todos os testes
<!-- Removido: script de qualidade completo -->

# Executar apenas testes unitários
python -m pytest tests/ -v

# Executar com cobertura
python -m pytest tests/ --cov=src --cov-report=html
```

### Formatar Código
```bash
# Formatar automaticamente
python scripts/format_code.py

# Verificar formatação
black --check src/ tests/
```

### Verificar Qualidade
```bash
# Verificar estilo
flake8 src/ tests/

# Verificar tipos
mypy src/
```

## 🏗️ Tecnologias Utilizadas

### Frontend
- **Streamlit**: Interface web interativa

### Backend
- **Pandas**: Manipulação e análise de dados
- **PyArrow**: Formato JSON para armazenamento eficiente
- **NumPy**: Operações numéricas

### Visualização
- **Plotly**: Gráficos interativos

### Desenvolvimento
- **Pytest**: Framework de testes
- **Black**: Formatação de código
- **Flake8**: Verificação de estilo
- **MyPy**: Verificação de tipos
