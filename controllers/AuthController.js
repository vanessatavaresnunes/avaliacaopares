const Professor = require('../models/Professor');
const Aluno = require('../models/Aluno');

class AuthController {
    // Login do professor
    static async loginProfessor(req, res) {
        try {
            const { email, senha } = req.body;

            if (!email || !senha) {
                req.flash('error', 'Email e senha são obrigatórios');
                return res.redirect('/login');
            }

            const professor = await Professor.findByEmail(email);
            if (!professor) {
                req.flash('error', 'Professor não encontrado');
                return res.redirect('/login');
            }

            const senhaValida = await professor.checkPassword(senha);
            if (!senhaValida) {
                req.flash('error', 'Senha incorreta');
                return res.redirect('/login');
            }

            req.session.professorId = professor.id;
            req.session.isProfessor = true;
            req.session.isAluno = false;

            req.flash('success', `Bem-vindo, Professor ${professor.nome}!`);
            res.redirect('/dashboard');
        } catch (error) {
            console.error('Erro no login do professor:', error);
            req.flash('error', 'Erro interno do servidor');
            res.redirect('/login');
        }
    }

    // Login do aluno
    static async loginAluno(req, res) {
        try {
            const { email, senha } = req.body;

            if (!email) {
                req.flash('error', 'Email é obrigatório');
                return res.redirect('/login');
            }

            const aluno = await Aluno.findByEmail(email);
            if (!aluno) {
                req.flash('error', 'Aluno não encontrado');
                return res.redirect('/login');
            }

            // Verificar se é primeiro login
            if (aluno.isFirstLogin()) {
                if (!senha) {
                    // Primeiro login - redirecionar para definir senha
                    req.session.tempAlunoId = aluno.id;
                    req.session.tempAlunoNome = aluno.nome;
                    req.session.tempAlunoEmail = aluno.email;
                    return res.redirect('/aluno/definir-senha');
                } else {
                    req.flash('error', 'Para primeiro login, deixe a senha em branco');
                    return res.redirect('/login');
                }
            } else {
                // Login normal
                if (!senha) {
                    req.flash('error', 'Senha é obrigatória');
                    return res.redirect('/login');
                }

                const senhaValida = await aluno.checkPassword(senha);
                if (!senhaValida) {
                    req.flash('error', 'Senha incorreta');
                    return res.redirect('/login');
                }

                req.session.alunoId = aluno.id;
                req.session.isAluno = true;
                req.session.isProfessor = false;

                req.flash('success', `Bem-vindo, ${aluno.nome}!`);
                res.redirect('/dashboard');
            }
        } catch (error) {
            console.error('Erro no login do aluno:', error);
            req.flash('error', 'Erro interno do servidor');
            res.redirect('/login');
        }
    }

    // Logout
    static logout(req, res) {
        req.session.destroy((err) => {
            if (err) {
                console.error('Erro ao fazer logout:', err);
            }
            res.redirect('/login');
        });
    }

    // Middleware para verificar autenticação
    static requireAuth(req, res, next) {
        if (req.session.professorId || req.session.alunoId) {
            next();
        } else {
            req.flash('error', 'Você precisa fazer login para acessar esta página');
            res.redirect('/login');
        }
    }

    // Middleware para verificar se é professor
    static requireProfessor(req, res, next) {
        if (req.session.isProfessor) {
            next();
        } else {
            req.flash('error', 'Acesso negado. Apenas professores podem acessar esta página');
            res.redirect('/dashboard');
        }
    }

    // Middleware para verificar se é aluno
    static requireAluno(req, res, next) {
        if (req.session.isAluno) {
            next();
        } else {
            req.flash('error', 'Acesso negado. Apenas alunos podem acessar esta página');
            res.redirect('/dashboard');
        }
    }

    // Dashboard baseado no tipo de usuário
    static async dashboard(req, res) {
        if (req.session.isProfessor) {
            const ProfessorController = require('./ProfessorController');
            await ProfessorController.dashboard(req, res);
        } else if (req.session.isAluno) {
            const AlunoController = require('./AlunoController');
            await AlunoController.dashboard(req, res);
        }
    }
}

module.exports = AuthController;