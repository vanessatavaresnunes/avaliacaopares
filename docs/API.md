# Documentação da API - Sistema de Avaliação de Pares

## Visão Geral

Esta documentação descreve a API do Sistema de Avaliação de Pares, implementado seguindo o padrão MVC (Model-View-Controller).

## Estrutura do Projeto

```
src/
├── models/           # Modelos de dados
├── controllers/      # Controllers
├── views/           # Views
└── __init__.py
```

## Models

### AvaliacaoModel

Responsável por gerenciar dados de avaliação.

#### Métodos Principais

- `salvar_avaliacoes(aluno_avaliador, time, avaliacoes) -> str`
- `carregar_dados() -> pd.DataFrame`
- `validar_notas(notas, num_alunos) -> bool`
- `validar_avaliacoes_completas(avaliacoes, alunos_time) -> Dict[str, bool]`
- `obter_estatisticas(df) -> Dict`

### UsuarioModel

Responsável por gerenciar dados de usuários e configurações.

#### Métodos Principais

- `obter_times() -> List[str]`
- `obter_alunos_por_time(time) -> List[str]`
- `obter_alunos_time_excluindo(time, aluno_excluir) -> List[str]`
- `obter_eixos() -> List[str]`
- `obter_configuracao() -> Configuracao`
- `validar_time(time) -> bool`
- `validar_aluno(time, aluno) -> bool`

## Controllers

### AvaliacaoController

Coordena a lógica de negócio entre models e views.

#### Métodos Principais

- `inicializar_sessao()`
- `fazer_login(time, aluno) -> bool`
- `fazer_logout()`
- `obter_dados_usuario_atual() -> Tuple[str, str]`
- `obter_alunos_para_avaliar() -> List[str]`
- `inicializar_avaliacao_aluno(aluno)`
- `atualizar_nota(aluno, eixo_index, nota)`
- `atualizar_feedback(aluno, feedback)`
- `validar_avaliacoes() -> Dict[str, bool]`
- `salvar_avaliacoes() -> Tuple[bool, str]`
- `obter_estatisticas_avaliacoes() -> Dict`
- `obter_dados_filtrados(time_filtro, avaliador_filtro, eixo_filtro) -> pd.DataFrame`

## Views

### LoginView

Interface de autenticação.

#### Métodos Principais

- `renderizar()`
- `mostrar_mensagem_erro(mensagem)`
- `mostrar_mensagem_sucesso(mensagem)`

### AvaliacaoView

Interface de avaliação de pares.

#### Métodos Principais

- `renderizar()`
- `_renderizar_sidebar()`
- `_renderizar_matriz_avaliacao(alunos_time)`
- `_renderizar_validacao_notas(alunos_time)`
- `_renderizar_botao_salvar()`

### VisualizacaoView

Interface de visualização de dados.

#### Métodos Principais

- `renderizar()`
- `_renderizar_resumo_geral(df)`
- `_renderizar_filtros(df) -> pd.DataFrame`
- `_renderizar_analise_eixo(df)`
- `_renderizar_analise_aluno(df)`
- `_renderizar_feedbacks(df)`
- `_renderizar_dados_completos(df)`

## Estruturas de Dados

### Avaliacao

```python
@dataclass
class Avaliacao:
    timestamp: str
    aluno_avaliador: str
    time: str
    aluno_avaliado: str
    eixo: str
    nota: int
    feedback: str
```

### Configuracao

```python
@dataclass
class Configuracao:
    nota_minima: int
    nota_maxima: int
    diretorio_dados: str
```

## Fluxo de Dados

1. **Login**: Usuário seleciona time e aluno
2. **Avaliação**: Usuário avalia colegas em 3 eixos
3. **Validação**: Sistema valida se soma das notas = número de colegas + 1
4. **Salvamento**: Dados são salvos em formato JSON
5. **Visualização**: Dados podem ser analisados e exportados

## Validações

### Notas
- Cada eixo deve ter soma igual ao número de colegas + 1
- Notas devem estar entre `nota_minima` e `nota_maxima`
- Feedback textual é obrigatório

### Usuários
- Time deve existir no sistema
- Aluno deve pertencer ao time selecionado
- Usuário não pode avaliar a si mesmo

## Armazenamento

### Formato
- **JSON**: Formato eficiente para dados tabulares
- **Estrutura**: Cada linha representa uma avaliação individual
- **Consolidação**: Arquivo individual + arquivo consolidado

### Campos
- `timestamp`: Data e hora da avaliação
- `aluno_avaliador`: Quem fez a avaliação
- `time`: Time do avaliador
- `aluno_avaliado`: Quem foi avaliado
- `eixo`: Eixo de avaliação
- `nota`: Nota atribuída
- `feedback`: Comentário textual

## Exemplos de Uso

### Inicializar Sistema
```python
from src.controllers.avaliacao_controller import AvaliacaoController

controller = AvaliacaoController()
controller.inicializar_sessao()
```

### Fazer Login
```python
sucesso = controller.fazer_login("Time A", "João Silva")
if sucesso:
    print("Login realizado com sucesso!")
```

### Obter Dados
```python
alunos = controller.obter_alunos_para_avaliar()
estatisticas = controller.obter_estatisticas_avaliacoes()
```

### Salvar Avaliações
```python
sucesso, mensagem = controller.salvar_avaliacoes()
if sucesso:
    print("Avaliações salvas!")
else:
    print(f"Erro: {mensagem}")
```

## Tratamento de Erros

O sistema inclui tratamento robusto de erros:

- **Validação de entrada**: Verifica dados antes do processamento
- **Tratamento de exceções**: Captura e reporta erros adequadamente
- **Feedback ao usuário**: Mensagens claras sobre problemas
- **Recuperação**: Sistema continua funcionando após erros

## Performance

### Otimizações
- **JSON**: Formato eficiente para leitura/escrita
- **Lazy loading**: Dados carregados sob demanda
- **Caching**: Sessão mantém dados temporários
- **Filtros**: Consultas otimizadas para visualização

### Limitações
- Dados mantidos em memória durante sessão
- Sem persistência de sessão entre reinicializações
- Interface síncrona (Streamlit)

## Extensibilidade

O sistema foi projetado para ser facilmente extensível:

- **Novos eixos**: Adicionar em `UsuarioModel.eixos`
- **Novos times**: Adicionar em `UsuarioModel.alunos`
- **Novas validações**: Implementar em `AvaliacaoModel`
- **Novas visualizações**: Criar novas views
- **Novos formatos**: Implementar novos models de armazenamento
