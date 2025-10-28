const Professor = require('../models/Professor');
const Aluno = require('../models/Aluno');
const Avaliacao = require('../models/Avaliacao');
const Eixo = require('../models/Eixo');

class ProfessorController {
    // Dashboard do professor
    static async dashboard(req, res) {
        try {
            const professorId = req.session.professorId;
            const professor = await Professor.findById(professorId);
            const alunos = await professor.getAlunos();

            const alunosPorSprint = {};
            for (let sprint = 1; sprint <= 5; sprint++) {
                alunosPorSprint[sprint] = alunos.filter(aluno => aluno.sprint_atual === sprint);
            }

            res.render('professor/dashboard', {
                professor: professor.toJSON(),
                alunos: alunos.map(aluno => aluno.toJSON()),
                alunosPorSprint,
                title: 'Dashboard - Professor'
            });
        } catch (error) {
            console.error('Erro ao carregar dashboard do professor:', error);
            req.flash('error', 'Erro ao carregar dashboard');
            res.redirect('/login');
        }
    }

    // Formulário para cadastrar aluno
    static async cadastrarAlunoForm(req, res) {
        try {
            const professorId = req.session.professorId;
            const professor = await Professor.findById(professorId);

            res.render('professor/cadastrar-aluno', {
                professor: professor.toJSON(),
                title: 'Cadastrar Aluno'
            });
        } catch (error) {
            console.error('Erro ao carregar formulário de cadastro:', error);
            req.flash('error', 'Erro ao carregar formulário');
            res.redirect('/dashboard');
        }
    }

    // Cadastrar aluno
    static async cadastrarAluno(req, res) {
        try {
            const professorId = req.session.professorId;
            const { nome, email, turma, grupo } = req.body;

            if (!nome || !email || !turma || !grupo) {
                req.flash('error', 'Todos os campos são obrigatórios');
                return res.redirect('/professor/cadastrar-aluno');
            }

            const alunoData = {
                nome,
                email,
                turma,
                grupo,
                professor_id: professorId
            };

            await Aluno.create(alunoData);
            req.flash('success', 'Aluno cadastrado com sucesso!');
            res.redirect('/dashboard');
        } catch (error) {
            console.error('Erro ao cadastrar aluno:', error);
            if (error.message.includes('UNIQUE constraint failed')) {
                req.flash('error', 'Já existe um aluno com este email');
            } else {
                req.flash('error', 'Erro ao cadastrar aluno');
            }
            res.redirect('/professor/cadastrar-aluno');
        }
    }

    // Formulário para editar aluno
    static async editarAlunoForm(req, res) {
        try {
            const professorId = req.session.professorId;
            const alunoId = req.params.id;
            const professor = await Professor.findById(professorId);
            const aluno = await Aluno.findById(alunoId);

            if (!aluno || aluno.professor_id !== professorId) {
                req.flash('error', 'Aluno não encontrado');
                return res.redirect('/dashboard');
            }

            res.render('professor/editar-aluno', {
                professor: professor.toJSON(),
                aluno: aluno.toJSON(),
                title: 'Editar Aluno'
            });
        } catch (error) {
            console.error('Erro ao carregar formulário de edição:', error);
            req.flash('error', 'Erro ao carregar formulário');
            res.redirect('/dashboard');
        }
    }

    // Editar aluno
    static async editarAluno(req, res) {
        try {
            const professorId = req.session.professorId;
            const alunoId = req.params.id;
            const { nome, email, turma, grupo } = req.body;

            if (!nome || !email || !turma || !grupo) {
                req.flash('error', 'Todos os campos são obrigatórios');
                return res.redirect(`/professor/editar-aluno/${alunoId}`);
            }

            const aluno = await Aluno.findById(alunoId);
            if (!aluno || aluno.professor_id !== professorId) {
                req.flash('error', 'Aluno não encontrado');
                return res.redirect('/dashboard');
            }

            const alunoData = {
                nome,
                email,
                turma,
                grupo
            };

            await aluno.update(alunoData);
            req.flash('success', 'Aluno atualizado com sucesso!');
            res.redirect('/dashboard');
        } catch (error) {
            console.error('Erro ao editar aluno:', error);
            if (error.message.includes('UNIQUE constraint failed')) {
                req.flash('error', 'Já existe um aluno com este email');
            } else {
                req.flash('error', 'Erro ao editar aluno');
            }
            res.redirect(`/professor/editar-aluno/${req.params.id}`);
        }
    }

    // Deletar aluno
    static async deletarAluno(req, res) {
        try {
            const professorId = req.session.professorId;
            const alunoId = req.params.id;

            const aluno = await Aluno.findById(alunoId);
            if (!aluno || aluno.professor_id !== professorId) {
                req.flash('error', 'Aluno não encontrado');
                return res.redirect('/dashboard');
            }

            await aluno.delete();
            req.flash('success', 'Aluno deletado com sucesso!');
            res.redirect('/dashboard');
        } catch (error) {
            console.error('Erro ao deletar aluno:', error);
            req.flash('error', 'Erro ao deletar aluno');
            res.redirect('/dashboard');
        }
    }

    // Visualizar avaliações por sprint
    static async avaliacoesPorSprint(req, res) {
        try {
            const professorId = req.session.professorId;
            const sprint = req.params.sprint || 1;
            const professor = await Professor.findById(professorId);
            const alunos = await professor.getAlunos();
            const eixos = await Eixo.findAll();

            const avaliacoes = [];
            for (const aluno of alunos) {
                const avaliacoesRecebidas = await Avaliacao.getAvaliacoesRecebidas(aluno.id, parseInt(sprint));
                const avaliacoesFeitas = await aluno.getAvaliacoesFeitas(parseInt(sprint));
                
                avaliacoesRecebidas.forEach(av => { av.aluno_avaliado = aluno.toJSON(); });
                avaliacoesFeitas.forEach(av => { av.aluno_avaliador = aluno.toJSON(); });

                avaliacoes.push({
                    aluno: aluno.toJSON(),
                    avaliacoesRecebidas,
                    avaliacoesFeitas,
                    estatisticas: await Avaliacao.getEstatisticas(aluno.id, parseInt(sprint))
                });
            }

            res.render('professor/avaliacoes-sprint', {
                professor: professor.toJSON(),
                avaliacoes,
                eixos: eixos.map(eixo => eixo.toJSON()),
                sprint: parseInt(sprint),
                title: `Avaliações - Sprint ${sprint}`
            });
        } catch (error) {
            console.error('Erro ao carregar avaliações:', error);
            req.flash('error', 'Erro ao carregar avaliações');
            res.redirect('/dashboard');
        }
    }

    // Visualizar estatísticas gerais
    static async estatisticasGerais(req, res) {
        try {
            const professorId = req.session.professorId;
            const professor = await Professor.findById(professorId);
            const alunos = await professor.getAlunos();

            // Estatísticas por sprint
            const estatisticasPorSprint = {};
            for (let sprint = 1; sprint <= 5; sprint++) {
                const alunosNaSprint = alunos.filter(aluno => aluno.sprint_atual === sprint);
                estatisticasPorSprint[sprint] = {
                    totalAlunos: alunosNaSprint.length,
                    avaliacoesCompletas: 0,
                    avaliacoesPendentes: 0,
                    mediaGeral: 0
                };

                let totalNotas = 0;
                let totalAvaliacoes = 0;

                for (const aluno of alunosNaSprint) {
                    const estatisticas = await Avaliacao.getEstatisticas(aluno.id, sprint);
                    if (estatisticas.total_avaliacoes > 0) {
                        estatisticasPorSprint[sprint].avaliacoesCompletas++;
                        totalNotas += estatisticas.media_notas * estatisticas.total_avaliacoes;
                        totalAvaliacoes += estatisticas.total_avaliacoes;
                    } else {
                        estatisticasPorSprint[sprint].avaliacoesPendentes++;
                    }
                }

                if (totalAvaliacoes > 0) {
                    estatisticasPorSprint[sprint].mediaGeral = (totalNotas / totalAvaliacoes).toFixed(1);
                }
            }

            res.render('professor/estatisticas-gerais', {
                professor: professor.toJSON(),
                estatisticasPorSprint,
                title: 'Estatísticas Gerais'
            });
        } catch (error) {
            console.error('Erro ao carregar estatísticas:', error);
            req.flash('error', 'Erro ao carregar estatísticas');
            res.redirect('/dashboard');
        }
    }
}

module.exports = ProfessorController;
