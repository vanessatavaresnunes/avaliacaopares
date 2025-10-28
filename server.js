const express = require('express');
const session = require('express-session');
const flash = require('connect-flash');
const path = require('path');
const AuthController = require('./controllers/AuthController');
const ProfessorController = require('./controllers/ProfessorController');
const AlunoController = require('./controllers/AlunoController');

const app = express();
const PORT = process.env.PORT || 3000;

// Configuração do EJS
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Middleware
app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// Configuração da sessão
app.use(session({
    secret: 'avaliacao-pares-secret-key',
    resave: false,
    saveUninitialized: false,
    cookie: { secure: false, maxAge: 24 * 60 * 60 * 1000 } // 24 horas
}));

// Flash messages
app.use(flash());

// Middleware para disponibilizar flash messages em todas as views
app.use((req, res, next) => {
    res.locals.success_msg = req.flash('success');
    res.locals.error_msg = req.flash('error');
    next();
});

// Rotas públicas
app.get('/', (req, res) => {
    res.redirect('/login');
});

app.get('/login', (req, res) => {
    res.render('login', { title: 'Login' });
});

app.post('/login', async (req, res) => {
    const { tipo } = req.body;
    
    if (tipo === 'professor') {
        await AuthController.loginProfessor(req, res);
    } else if (tipo === 'aluno') {
        await AuthController.loginAluno(req, res);
    } else {
        req.flash('error', 'Tipo de usuário inválido');
        res.redirect('/login');
    }
});

// Rotas protegidas
app.get('/dashboard', AuthController.requireAuth, async (req, res) => {
    if (req.session.isProfessor) {
        await ProfessorController.dashboard(req, res);
    } else if (req.session.isAluno) {
        await AlunoController.dashboard(req, res);
    }
});

// Rotas do professor
app.get('/professor/cadastrar-aluno', AuthController.requireAuth, AuthController.requireProfessor, ProfessorController.cadastrarAlunoForm);
app.post('/professor/cadastrar-aluno', AuthController.requireAuth, AuthController.requireProfessor, ProfessorController.cadastrarAluno);
app.get('/professor/editar-aluno/:id', AuthController.requireAuth, AuthController.requireProfessor, ProfessorController.editarAlunoForm);
app.post('/professor/editar-aluno/:id', AuthController.requireAuth, AuthController.requireProfessor, ProfessorController.editarAluno);
app.post('/professor/deletar-aluno/:id', AuthController.requireAuth, AuthController.requireProfessor, ProfessorController.deletarAluno);
app.get('/professor/avaliacoes-sprint/:sprint', AuthController.requireAuth, AuthController.requireProfessor, ProfessorController.avaliacoesPorSprint);
app.get('/professor/estatisticas-gerais', AuthController.requireAuth, AuthController.requireProfessor, ProfessorController.estatisticasGerais);
// app.get('/professor/dashboard-calculos', AuthController.requireAuth, AuthController.requireProfessor, ProfessorController.dashboardCalculos);
// app.get('/professor/calculos-turma/:turma', AuthController.requireAuth, AuthController.requireProfessor, ProfessorController.calculosTurma);

// Rotas do aluno
app.get('/aluno/definir-senha', AlunoController.definirSenhaForm);
app.post('/aluno/definir-senha', AlunoController.definirSenha);
app.get('/aluno/selecionar-sprint', AuthController.requireAuth, AuthController.requireAluno, AlunoController.selecionarSprint);
app.post('/aluno/processar-sprint', AuthController.requireAuth, AuthController.requireAluno, AlunoController.processarSprint);
app.get('/aluno/avaliar-colegas', AuthController.requireAuth, AuthController.requireAluno, AlunoController.avaliarColegas);
app.get('/aluno/avaliar-colega/:id', AuthController.requireAuth, AuthController.requireAluno, AlunoController.avaliarColegaForm);
app.post('/aluno/processar-avaliacao/:id', AuthController.requireAuth, AuthController.requireAluno, AlunoController.processarAvaliacao);
app.get('/aluno/resultados-avaliacoes', AuthController.requireAuth, AuthController.requireAluno, AlunoController.resultadosAvaliacoes);

// Logout
app.post('/logout', AuthController.logout);

// Middleware para páginas não encontradas
app.use((req, res) => {
    res.status(404).render('404', { title: 'Página não encontrada' });
});

// Iniciar servidor
app.listen(PORT, () => {
    console.log(`Servidor rodando na porta ${PORT}`);
    console.log(`Acesse: http://localhost:${PORT}`);
});
