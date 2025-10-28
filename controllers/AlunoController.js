const Aluno = require('../models/Aluno');
const Avaliacao = require('../models/Avaliacao');
const Eixo = require('../models/Eixo');

class AlunoController {
    // Dashboard do aluno
    static async dashboard(req, res) {
        try {
            const alunoId = req.session.alunoId;
            const aluno = await Aluno.findById(alunoId);
            const professor = await aluno.getProfessor();

            res.render('aluno/dashboard', {
                aluno: aluno.toJSON(),
                professor: professor.toJSON(),
                title: 'Dashboard - Aluno'
            });
        } catch (error) {
            console.error('Erro ao carregar dashboard do aluno:', error);
            req.flash('error', 'Erro ao carregar dashboard');
            res.redirect('/login');
        }
    }

    // Página para definir senha (primeiro login)
    static async definirSenhaForm(req, res) {
        try {
            const alunoId = req.session.tempAlunoId;
            const alunoNome = req.session.tempAlunoNome;
            const alunoEmail = req.session.tempAlunoEmail;

            if (!alunoId || !alunoNome || !alunoEmail) {
                req.flash('error', 'Sessão expirada. Faça login novamente.');
                return res.redirect('/login');
            }

            res.render('aluno/definir-senha', {
                alunoNome,
                alunoEmail,
                title: 'Definir Senha'
            });
        } catch (error) {
            console.error('Erro ao carregar formulário de senha:', error);
            req.flash('error', 'Erro ao carregar formulário');
            res.redirect('/login');
        }
    }

    // Definir senha (primeiro login)
    static async definirSenha(req, res) {
        try {
            const alunoId = req.session.tempAlunoId;
            const { senha, confirmarSenha } = req.body;

            if (!senha || !confirmarSenha) {
                req.flash('error', 'Senha e confirmação são obrigatórias');
                return res.redirect('/aluno/definir-senha');
            }

            if (senha !== confirmarSenha) {
                req.flash('error', 'As senhas não coincidem');
                return res.redirect('/aluno/definir-senha');
            }

            if (senha.length < 6) {
                req.flash('error', 'A senha deve ter pelo menos 6 caracteres');
                return res.redirect('/aluno/definir-senha');
            }

            const aluno = await Aluno.findById(alunoId);
            if (!aluno) {
                req.flash('error', 'Aluno não encontrado');
                return res.redirect('/login');
            }

            await aluno.setPassword(senha);

            // Limpar sessão temporária e criar sessão normal
            req.session.tempAlunoId = null;
            req.session.tempAlunoNome = null;
            req.session.tempAlunoEmail = null;
            req.session.alunoId = aluno.id;
            req.session.isAluno = true;
            req.session.isProfessor = false;

            req.flash('success', 'Senha definida com sucesso!');
            res.redirect('/dashboard');
        } catch (error) {
            console.error('Erro ao definir senha:', error);
            req.flash('error', 'Erro ao definir senha');
            res.redirect('/aluno/definir-senha');
        }
    }

    // Selecionar sprint para avaliação
    static async selecionarSprint(req, res) {
        try {
            const alunoId = req.session.alunoId;
            const aluno = await Aluno.findById(alunoId);

            res.render('aluno/selecionar-sprint', {
                aluno: aluno.toJSON(),
                title: 'Selecionar Sprint'
            });
        } catch (error) {
            console.error('Erro ao carregar seleção de sprint:', error);
            req.flash('error', 'Erro ao carregar página');
            res.redirect('/dashboard');
        }
    }

    // Processar seleção de sprint
    static async processarSprint(req, res) {
        try {
            const alunoId = req.session.alunoId;
            const { sprint } = req.body;
            const aluno = await Aluno.findById(alunoId);

            if (!sprint || sprint < 1 || sprint > 5) {
                req.flash('error', 'Sprint deve ser entre 1 e 5');
                return res.redirect('/aluno/selecionar-sprint');
            }

            await aluno.updateSprintAtual(parseInt(sprint));
            req.flash('success', `Sprint ${sprint} selecionada com sucesso!`);
            res.redirect('/aluno/avaliar-colegas');
        } catch (error) {
            console.error('Erro ao processar sprint:', error);
            req.flash('error', 'Erro ao selecionar sprint');
            res.redirect('/aluno/selecionar-sprint');
        }
    }

    // Página de avaliação de colegas
    static async avaliarColegas(req, res) {
        try {
            const alunoId = req.session.alunoId;
            const aluno = await Aluno.findById(alunoId);
            const sprint = aluno.sprint_atual;
            
            const colegas = await aluno.getColegasEquipe(sprint);
            const eixos = await Eixo.findAll();
            
            const colegasComStatus = await Promise.all(
                colegas.map(async (colega) => {
                    const avaliacoesPorEixo = {};
                    let totalAvaliacoes = 0;
                    let avaliacoesCompletas = 0;
                    
                    for (const eixo of eixos) {
                        const jaAvaliou = await aluno.jaAvaliou(colega.id, sprint, eixo.id);
                        avaliacoesPorEixo[eixo.id] = jaAvaliou;
                        totalAvaliacoes++;
                        if (jaAvaliou) avaliacoesCompletas++;
                    }
                    
                    return {
                        ...colega.toJSON(),
                        avaliacoesPorEixo,
                        totalAvaliacoes,
                        avaliacoesCompletas,
                        percentualCompleto: Math.round((avaliacoesCompletas / totalAvaliacoes) * 100)
                    };
                })
            );

            res.render('aluno/avaliar-colegas', {
                aluno: aluno.toJSON(),
                colegas: colegasComStatus,
                eixos: eixos.map(eixo => eixo.toJSON()),
                sprint,
                title: `Avaliar Colegas - Sprint ${sprint}`
            });
        } catch (error) {
            console.error('Erro ao carregar colegas:', error);
            req.flash('error', 'Erro ao carregar colegas');
            res.redirect('/dashboard');
        }
    }

    // Página para avaliar um colega específico
    static async avaliarColegaForm(req, res) {
        try {
            const alunoId = req.session.alunoId;
            const colegaId = req.params.id;
            const aluno = await Aluno.findById(alunoId);
            const sprint = aluno.sprint_atual;
            const colega = await Aluno.findById(colegaId);
            const eixos = await Eixo.findAll();

            if (!colega) {
                req.flash('error', 'Colega não encontrado');
                return res.redirect('/aluno/avaliar-colegas');
            }

            const avaliacoesExistentes = {};
            for (const eixo of eixos) {
                const avaliacaoExistente = await Avaliacao.findByAvaliacao(alunoId, colegaId, sprint, eixo.id);
                avaliacoesExistentes[eixo.id] = avaliacaoExistente;
            }

            res.render('aluno/avaliar-colega', {
                aluno: aluno.toJSON(),
                colega: colega.toJSON(),
                eixos: eixos.map(eixo => eixo.toJSON()),
                avaliacoesExistentes,
                sprint,
                title: `Avaliar ${colega.nome}`
            });
        } catch (error) {
            console.error('Erro ao carregar formulário de avaliação:', error);
            req.flash('error', 'Erro ao carregar formulário');
            res.redirect('/aluno/avaliar-colegas');
        }
    }

    // Processar avaliação de colega
    static async processarAvaliacao(req, res) {
        try {
            const alunoId = req.session.alunoId;
            const colegaId = req.params.id;
            const aluno = await Aluno.findById(alunoId);
            const sprint = aluno.sprint_atual;
            const eixos = await Eixo.findAll();

            const colega = await Aluno.findById(colegaId);
            if (!colega) {
                req.flash('error', 'Colega não encontrado');
                return res.redirect('/aluno/avaliar-colegas');
            }

            let avaliacoesProcessadas = 0;
            let avaliacoesAtualizadas = 0;
            let avaliacoesCriadas = 0;

            for (const eixo of eixos) {
                const notaKey = `nota_${eixo.id}`;
                const feedbackKey = `feedback_${eixo.id}`;
                
                const nota = req.body[notaKey];
                const feedback = req.body[feedbackKey];

                if (nota !== undefined && nota !== '' && feedback && feedback.trim()) {
                    const notaInt = parseInt(nota);
                    
                    if (notaInt < 0 || notaInt > 3) {
                        req.flash('error', `Nota para ${eixo.nome} deve ser entre 0 e 3`);
                        continue;
                    }

                    const avaliacaoExistente = await Avaliacao.findByAvaliacao(alunoId, colegaId, sprint, eixo.id);

                    if (avaliacaoExistente) {
                        await Avaliacao.update(avaliacaoExistente.id, { nota: notaInt, feedback: feedback.trim() });
                        avaliacoesAtualizadas++;
                    } else {
                        await Avaliacao.create({
                            avaliador_id: alunoId,
                            avaliado_id: colegaId,
                            sprint: sprint,
                            eixo_id: eixo.id,
                            nota: notaInt,
                            feedback: feedback.trim()
                        });
                        avaliacoesCriadas++;
                    }
                    avaliacoesProcessadas++;
                }
            }

            if (avaliacoesProcessadas === 0) {
                req.flash('error', 'Nenhuma avaliação válida foi processada');
                return res.redirect(`/aluno/avaliar-colega/${colegaId}`);
            }

            let mensagem = `Avaliações de ${colega.nome} processadas com sucesso! `;
            if (avaliacoesCriadas > 0) mensagem += `${avaliacoesCriadas} criadas. `;
            if (avaliacoesAtualizadas > 0) mensagem += `${avaliacoesAtualizadas} atualizadas. `;
            
            req.flash('success', mensagem);
            res.redirect('/aluno/avaliar-colegas');
        } catch (error) {
            console.error('Erro ao processar avaliação:', error);
            req.flash('error', 'Erro ao processar avaliação');
            res.redirect(`/aluno/avaliar-colega/${req.params.id}`);
        }
    }

    // Página de resultados das avaliações
    static async resultadosAvaliacoes(req, res) {
        try {
            const alunoId = req.session.alunoId;
            const aluno = await Aluno.findById(alunoId);
            const sprint = aluno.sprint_atual;
            const avaliacoesRecebidas = await Avaliacao.getAvaliacoesRecebidas(alunoId, sprint);
            const estatisticas = await Avaliacao.getEstatisticas(alunoId, sprint);
            const eixos = await Eixo.findAll();

            const avaliacoesPorEixo = {};
            eixos.forEach(eixo => {
                avaliacoesPorEixo[eixo.id] = avaliacoesRecebidas.filter(av => av.eixo_id === eixo.id);
            });

            res.render('aluno/resultados-avaliacoes', {
                aluno: aluno.toJSON(),
                avaliacoesRecebidas,
                avaliacoesPorEixo,
                eixos: eixos.map(eixo => eixo.toJSON()),
                estatisticas,
                sprint,
                title: `Resultados - Sprint ${sprint}`
            });
        } catch (error) {
            console.error('Erro ao carregar resultados:', error);
            req.flash('error', 'Erro ao carregar resultados');
            res.redirect('/dashboard');
        }
    }
}

module.exports = AlunoController;
