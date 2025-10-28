const db = require('../config/db');

class Avaliacao {
    constructor(data) {
        this.id = data.id;
        this.avaliador_id = data.avaliador_id;
        this.avaliado_id = data.avaliado_id;
        this.sprint = data.sprint;
        this.eixo_id = data.eixo_id;
        this.nota = data.nota;
        this.feedback = data.feedback;
        this.created_at = data.created_at;
    }

    // Método para criar nova avaliação
    static async create(avaliacaoData) {
        return new Promise((resolve, reject) => {
            const { avaliador_id, avaliado_id, sprint, eixo_id, nota, feedback } = avaliacaoData;
            const sql = 'INSERT INTO avaliacoes (avaliador_id, avaliado_id, sprint, eixo_id, nota, feedback) VALUES (?, ?, ?, ?, ?, ?)';
            
            db.run(sql, [avaliador_id, avaliado_id, sprint, eixo_id, nota, feedback], function(err) {
                if (err) {
                    reject(err);
                } else {
                    resolve(new Avaliacao({
                        id: this.lastID,
                        avaliador_id,
                        avaliado_id,
                        sprint,
                        eixo_id,
                        nota,
                        feedback,
                        created_at: new Date()
                    }));
                }
            });
        });
    }

    // Método para atualizar avaliação existente
    static async update(id, avaliacaoData) {
        return new Promise((resolve, reject) => {
            const { nota, feedback } = avaliacaoData;
            const sql = 'UPDATE avaliacoes SET nota = ?, feedback = ? WHERE id = ?';
            
            db.run(sql, [nota, feedback, id], function(err) {
                if (err) {
                    reject(err);
                } else {
                    resolve(this.changes > 0);
                }
            });
        });
    }

    // Método para buscar avaliação específica
    static async findByAvaliacao(avaliador_id, avaliado_id, sprint, eixo_id) {
        return new Promise((resolve, reject) => {
            const sql = 'SELECT id, avaliador_id, avaliado_id, sprint, eixo_id, nota, feedback, created_at FROM avaliacoes WHERE avaliador_id = ? AND avaliado_id = ? AND sprint = ? AND eixo_id = ?';
            db.get(sql, [avaliador_id, avaliado_id, sprint, eixo_id], (err, row) => {
                if (err) {
                    reject(err);
                } else if (row) {
                    resolve(new Avaliacao(row));
                } else {
                    resolve(null);
                }
            });
        });
    }

    // Método para buscar todas as avaliações de um aluno em uma sprint
    static async findByAvaliadorSprint(avaliador_id, sprint) {
        return new Promise((resolve, reject) => {
            const sql = `
                SELECT a.*, e.nome as eixo_nome, al.nome as avaliado_nome
                FROM avaliacoes a
                JOIN eixos e ON a.eixo_id = e.id
                JOIN alunos al ON a.avaliado_id = al.id
                WHERE a.avaliador_id = ? AND a.sprint = ?
                ORDER BY e.ordem, al.nome
            `;
            db.all(sql, [avaliador_id, sprint], (err, rows) => {
                if (err) {
                    reject(err);
                } else {
                    resolve(rows);
                }
            });
        });
    }

    // Método para buscar avaliações recebidas por um aluno
    static async getAvaliacoesRecebidas(alunoId, sprint) {
        return new Promise((resolve, reject) => {
            const sql = `
                SELECT a.*, e.nome as eixo_nome, al.nome as avaliador_nome
                FROM avaliacoes a
                JOIN eixos e ON a.eixo_id = e.id
                JOIN alunos al ON a.avaliador_id = al.id
                WHERE a.avaliado_id = ? AND a.sprint = ?
                ORDER BY e.ordem, al.nome
            `;
            db.all(sql, [alunoId, sprint], (err, rows) => {
                if (err) {
                    reject(err);
                } else {
                    resolve(rows);
                }
            });
        });
    }

    // Método para obter estatísticas de um aluno em uma sprint
    static async getEstatisticas(alunoId, sprint) {
        return new Promise((resolve, reject) => {
            const sql = `
                SELECT 
                    AVG(nota) as media_nota,
                    COUNT(id) as total_avaliacoes,
                    MIN(nota) as menor_nota,
                    MAX(nota) as maior_nota
                FROM avaliacoes
                WHERE avaliado_id = ? AND sprint = ?
            `;
            db.get(sql, [alunoId, sprint], (err, row) => {
                if (err) {
                    reject(err);
                } else {
                    resolve(row);
                }
            });
        });
    }

    // Método para validar soma das notas por eixo
    static async validarSomaNotasPorEixo(avaliador_id, sprint, eixo_id, nota) {
        return new Promise((resolve, reject) => {
            const sql = `
                SELECT SUM(nota) as soma_atual
                FROM avaliacoes
                WHERE avaliador_id = ? AND sprint = ? AND eixo_id = ?
            `;
            db.get(sql, [avaliador_id, sprint, eixo_id], (err, row) => {
                if (err) {
                    reject(err);
                } else {
                    const somaAtual = (row.soma_atual || 0) + nota;
                    resolve(somaAtual);
                }
            });
        });
    }

    // Método para obter dados sem informações sensíveis
    toJSON() {
        return {
            id: this.id,
            avaliador_id: this.avaliador_id,
            avaliado_id: this.avaliado_id,
            sprint: this.sprint,
            eixo_id: this.eixo_id,
            nota: this.nota,
            feedback: this.feedback,
            created_at: this.created_at
        };
    }
}

module.exports = Avaliacao;