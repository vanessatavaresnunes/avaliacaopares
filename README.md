# Sistema de Avaliação de Pares

Sistema web para avaliação de pares entre alunos, desenvolvido com Node.js, Express.js e SQLite.

## 🎯 Funcionalidades

- **Login de Professores Orientadores**: Acesso restrito para professores cadastrados
- **Login de Alunos**: Acesso para alunos cadastrados pelos professores
- **Primeiro Login de Alunos**: Sistema de definição de senha com dupla verificação no primeiro acesso
- **Gerenciamento de Alunos**: Professores podem cadastrar, editar e excluir alunos
- **Seleção de Turma e Grupo**: Dropdowns para turmas (T01-T30) e grupos (G1-G10)
- **Dashboard Personalizado**: Interface diferenciada para professores e alunos
- **Sistema de Sprints**: Avaliação por sprints (1 a 5) com seleção dinâmica
- **Avaliação de Colegas**: Sistema completo de avaliação entre pares de equipe
- **Busca Inteligente**: Encontra colegas da mesma turma, grupo e sprint
- **Sistema de Notas**: Avaliação de 0 a 3 com comentários obrigatórios
- **Resultados Detalhados**: Visualização de estatísticas e feedback recebido
- **Sistema de Eixos**: 3 eixos de avaliação com descrições detalhadas

## Estrutura do Projeto

```
avaliacaopares/
├── config/
│   └── db.js                 # Configuração do banco SQLite
├── controllers/
│   ├── AuthController.js     # Autenticação e middleware
│   ├── ProfessorController.js # Funcionalidades do professor
│   └── AlunoController.js    # Funcionalidades do aluno
├── models/
│   ├── Professor.js          # Modelo do Professor
│   ├── Aluno.js              # Modelo do Aluno
│   ├── Avaliacao.js          # Modelo da Avaliação
│   └── Eixo.js               # Modelo dos Eixos de Avaliação
├── views/
│   ├── layouts/
│   │   └── main.ejs          # Layout principal
│   ├── aluno/                # Views específicas do aluno
│   ├── professor/            # Views específicas do professor
│   ├── login.ejs             # Página de login
│   └── 404.ejs               # Página de erro 404
├── public/
│   ├── css/                  # Estilos CSS
│   └── js/                   # Scripts JavaScript
├── scripts/
│   ├── migrate.js            # Script de migração (limpo)
│   ├── init-db.js            # Script de inicialização (limpo)
│   └── create-professors.js  # Script para criar professores (no .gitignore)
├── database/
│   └── avaliacao_pares.db    # Banco de dados SQLite
├── package.json               # Dependências do projeto
├── server.js                  # Servidor Express principal
└── README.md                  # Este arquivo
```

## 🎯 Eixos de Avaliação

O sistema utiliza 3 eixos de avaliação baseados na metodologia do Inteli:

### 1. Entregas Reais
Avalia o cumprimento das entregas da sprint. Leva em consideração se os prazos foram respeitados, se os formatos estavam corretos e se os artefatos foram bem executados.

**Observações importantes:**
- GitHub: Verificar se o colega fez commits dentro do prazo
- Trello: Verificar se o colega cumpriu com as tarefas atribuídas
- Daily: Verificar se o colega foi atuante nas dailies

### 2. Valor Percebido
Avalia o impacto das entregas para o grupo durante a sprint. Deve levar em consideração o valor agregado para o projeto, se houve a geração de novas ideias e achados valiosos.

**Observações importantes:**
- GitHub: Verificar se o colega entregou algo que destravou uma etapa importante
- Trello: Verificar se as tarefas contribuíram significativamente para o avanço
- Daily: Verificar se o colega compartilhou ideias que ajudaram o grupo

### 3. Caixa de Ferramentas
Avalia o desenvolvimento técnico do aluno, verificando se a pessoa evoluiu e absorveu os conceitos técnicos, conseguindo aplicá-los na prática.

**Observações importantes:**
- GitHub: Verificar se o colega usou conceitos técnicos aprendidos
- Trello: Verificar se o colega assumiu tarefas técnicas mais desafiadoras
- Daily: Verificar se o colega demonstra domínio técnico

## 📦 Instalação

### Pré-requisitos
- Node.js (versão 14 ou superior)
- npm

### Instalação

1. **Clone o repositório:**
```bash
git clone <url-do-repositorio>
cd avaliacaopares
```

2. **Instale as dependências:**
```bash
npm install
```

3. **Inicialize o banco de dados:**
```bash
npm run init-db
```

4. **Inicie o servidor:**
```bash
npm start
```

5. **Acesse a aplicação:**
```
http://localhost:3000
```

## 🚀 Como Usar

### Para Professores:

1. **Login**: Use o email e senha do professor orientador
2. **Cadastrar Alunos**: 
   - Preencha nome e email do aluno
   - Selecione turma (T01-T30) e grupo (G1-G10)
   - O aluno será criado sem senha
3. **Gerenciar Alunos**: Edite ou exclua alunos através dos botões de ação
4. **Visualizar Avaliações**: Veja todas as avaliações por sprint

### Para Alunos:

1. **Primeiro Login**: 
   - Use apenas o email (deixe a senha em branco)
   - Será redirecionado para definir uma senha pessoal
   - **Dupla verificação**: Digite a senha duas vezes para confirmar
   - Indicadores visuais mostram se as senhas coincidem
   - Após definir a senha, terá acesso ao dashboard
2. **Login Normal**: Use email e senha definida anteriormente
3. **Dashboard**: Visualize seus dados e informações do professor orientador
4. **Avaliação de Pares**:
   - **Selecionar Sprint**: Escolha qual sprint (1-5) avaliar
   - **Avaliar Colegas**: Veja lista de colegas da mesma turma/grupo/sprint
   - **Dar Notas**: Avalie cada colega com nota de 0-3 e feedback por eixo
   - **Ver Resultados**: Visualize avaliações recebidas e estatísticas

## 🗄️ Banco de Dados

O sistema utiliza SQLite com as seguintes tabelas:

- **professores**: Dados dos professores orientadores
- **alunos**: Dados dos alunos com turma, grupo e sprint atual
- **eixos**: Eixos de avaliação com descrições e observações
- **avaliacoes**: Avaliações com nota (0-3) e feedback por eixo

## 🔐 Credenciais Padrão

### Professores Orientadores:
- **Email**: vanessa.nunes@prof.inteli.edu.br
- **Senha**: prof123

- **Email**: hermano.peixoto@prof.inteli.edu.br  
- **Senha**: prof123

> ⚠️ **IMPORTANTE**: Altere as senhas padrão após o primeiro login!

## 🛠️ Tecnologias Utilizadas

- **Node.js**: Runtime JavaScript
- **Express.js**: Framework web
- **SQLite**: Banco de dados
- **EJS**: Template engine
- **bcryptjs**: Criptografia de senhas
- **express-session**: Gerenciamento de sessões
- **connect-flash**: Mensagens flash
- **Bootstrap**: Framework CSS

## 📊 Sistema de Notas

- **0**: Não Atendeu
- **1**: Atendeu Parcialmente
- **2**: Atendeu Bem
- **3**: Atendeu Excelentemente

## 🔄 Fluxo de Avaliação

1. **Aluno faz login** → Dashboard atualizado
2. **Seleciona sprint** → Escolhe sprint 1-5
3. **Vê colegas de equipe** → Mesma turma + grupo + sprint
4. **Avalia cada colega** → Nota 0-3 + feedback por eixo
5. **Visualiza resultados** → Estatísticas e feedback recebido

## 🛡️ Segurança

- Senhas criptografadas com bcryptjs
- Sessões seguras com express-session
- Validações robustas no frontend e backend
- Controle de acesso por tipo de usuário
- Prevenção de avaliações duplicadas

## 📝 Scripts Disponíveis

- `npm start`: Inicia o servidor
- `npm run init-db`: Inicializa o banco de dados

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👥 Autores

- **Desenvolvido para**: Inteli - Instituto de Tecnologia e Liderança
- **Professores Orientadores**: Vanessa Nunes e Hermano Peixoto