const db = require('../config/db');
const bcrypt = require('bcryptjs');

class Aluno {
    constructor(data) {
        this.id = data.id;
        this.nome = data.nome;
        this.email = data.email;
        this.senha = data.senha;
        this.turma = data.turma;
        this.grupo = data.grupo;
        this.sprint_atual = data.sprint_atual || 1;
        this.professor_id = data.professor_id;
        this.created_at = data.created_at;
    }

    // Método para criar um novo aluno
    static async create(alunoData) {
        return new Promise((resolve, reject) => {
            const { nome, email, turma, grupo, professor_id } = alunoData;
            
            // Inserir aluno sem senha (primeira vez)
            const sql = 'INSERT INTO alunos (nome, email, senha, turma, grupo, sprint_atual, professor_id) VALUES (?, ?, NULL, ?, ?, 1, ?)';
            db.run(sql, [nome, email, turma, grupo, professor_id], function(err) {
                if (err) {
                    reject(err);
                } else {
                    resolve(new Aluno({
                        id: this.lastID,
                        nome,
                        email,
                        senha: null,
                        turma,
                        grupo,
                        sprint_atual: 1,
                        professor_id,
                        created_at: new Date()
                    }));
                }
            });
        });
    }

    // Método para buscar aluno por email
    static async findByEmail(email) {
        return new Promise((resolve, reject) => {
            const sql = 'SELECT id, nome, email, senha, turma, grupo, sprint_atual, professor_id, created_at FROM alunos WHERE email = ?';
            db.get(sql, [email], (err, row) => {
                if (err) {
                    reject(err);
                } else if (row) {
                    resolve(new Aluno(row));
                } else {
                    resolve(null);
                }
            });
        });
    }

    // Método para buscar aluno por ID
    static async findById(id) {
        return new Promise((resolve, reject) => {
            const sql = 'SELECT id, nome, email, senha, turma, grupo, sprint_atual, professor_id, created_at FROM alunos WHERE id = ?';
            db.get(sql, [id], (err, row) => {
                if (err) {
                    reject(err);
                } else if (row) {
                    resolve(new Aluno(row));
                } else {
                    resolve(null);
                }
            });
        });
    }

    // Método para buscar alunos por professor
    static async findByProfessor(professorId) {
        return new Promise((resolve, reject) => {
            const sql = 'SELECT id, nome, email, senha, turma, grupo, sprint_atual, professor_id, created_at FROM alunos WHERE professor_id = ? ORDER BY nome';
            db.all(sql, [professorId], (err, rows) => {
                if (err) {
                    reject(err);
                } else {
                    resolve(rows.map(row => new Aluno(row)));
                }
            });
        });
    }

    // Método para verificar senha
    async checkPassword(password) {
        if (!this.senha) {
            return false; // Aluno ainda não definiu senha
        }
        return bcrypt.compare(password, this.senha);
    }

    // Método para verificar se é primeiro login
    isFirstLogin() {
        return !this.senha;
    }

    // Método para definir senha (primeiro login)
    async setPassword(password) {
        return new Promise((resolve, reject) => {
            bcrypt.hash(password, 10, (err, hashedPassword) => {
                if (err) {
                    reject(err);
                    return;
                }

                const sql = 'UPDATE alunos SET senha = ? WHERE id = ?';
                db.run(sql, [hashedPassword, this.id], function(err) {
                    if (err) {
                        reject(err);
                    } else {
                        this.senha = hashedPassword;
                        resolve(this);
                    }
                }.bind(this));
            });
        });
    }

    // Método para obter o professor do aluno
    async getProfessor() {
        const Professor = require('./Professor').Professor;
        return Professor.findById(this.professor_id);
    }

    // Método para obter dados sem senha (para segurança)
    toJSON() {
        const { senha, ...alunoData } = this;
        return alunoData;
    }

    // Método para atualizar dados do aluno
    async update(updateData) {
        return new Promise((resolve, reject) => {
            const { nome, email, turma, grupo } = updateData;
            const sql = 'UPDATE alunos SET nome = ?, email = ?, turma = ?, grupo = ? WHERE id = ?';
            
            db.run(sql, [nome, email, turma, grupo, this.id], function(err) {
                if (err) {
                    reject(err);
                } else {
                    // Atualizar os dados locais
                    this.nome = nome;
                    this.email = email;
                    this.turma = turma;
                    this.grupo = grupo;
                    resolve(this);
                }
            }.bind(this));
        });
    }

    // Método para deletar aluno
    async delete() {
        return new Promise((resolve, reject) => {
            const sql = 'DELETE FROM alunos WHERE id = ?';
            db.run(sql, [this.id], function(err) {
                if (err) {
                    reject(err);
                } else {
                    resolve(true);
                }
            });
        });
    }

    // Método para buscar colegas de equipe (mesma turma, mesmo grupo, mesma sprint)
    async getColegasEquipe(sprint) {
        return new Promise((resolve, reject) => {
            const sql = `
                SELECT id, nome, email, senha, turma, grupo, sprint_atual, professor_id, created_at 
                FROM alunos 
                WHERE turma = ? AND grupo = ? AND sprint_atual = ? AND id != ?
                ORDER BY nome
            `;
            db.all(sql, [this.turma, this.grupo, sprint, this.id], (err, rows) => {
                if (err) {
                    reject(err);
                } else {
                    resolve(rows.map(row => new Aluno(row)));
                }
            });
        });
    }

    // Método para buscar TODOS os colegas de equipe (mesma turma e grupo) - para professor
    async getTodosColegasEquipe() {
        return new Promise((resolve, reject) => {
            const sql = `
                SELECT id, nome, email, senha, turma, grupo, sprint_atual, professor_id, created_at 
                FROM alunos
                WHERE turma = ? AND grupo = ? AND id != ?
                ORDER BY sprint_atual, nome
            `;
            db.all(sql, [this.turma, this.grupo, this.id], (err, rows) => {
                if (err) {
                    reject(err);
                } else {
                    resolve(rows.map(row => new Aluno(row)));
                }
            });
        });
    }

    // Método para atualizar sprint atual
    async updateSprintAtual(novaSprint) {
        return new Promise((resolve, reject) => {
            const sql = 'UPDATE alunos SET sprint_atual = ? WHERE id = ?';
            db.run(sql, [novaSprint, this.id], function(err) {
                if (err) {
                    reject(err);
                } else {
                    this.sprint_atual = novaSprint;
                    resolve(this);
                }
            }.bind(this));
        });
    }

    // Método para verificar se já avaliou um colega em um eixo específico
    async jaAvaliou(avaliadoId, sprint, eixoId) {
        return new Promise((resolve, reject) => {
            const sql = 'SELECT id FROM avaliacoes WHERE avaliador_id = ? AND avaliado_id = ? AND sprint = ? AND eixo_id = ?';
            db.get(sql, [this.id, avaliadoId, sprint, eixoId], (err, row) => {
                if (err) {
                    reject(err);
                } else {
                    resolve(!!row);
                }
            });
        });
    }

    // Método para obter avaliações feitas pelo aluno
    async getAvaliacoesFeitas(sprint) {
        return new Promise((resolve, reject) => {
            const sql = `
                SELECT a.*, e.nome as eixo_nome, al.nome as avaliado_nome 
                FROM avaliacoes a 
                JOIN eixos e ON a.eixo_id = e.id
                JOIN alunos al ON a.avaliado_id = al.id 
                WHERE a.avaliador_id = ? AND a.sprint = ?
                ORDER BY e.ordem, al.nome
            `;
            db.all(sql, [this.id, sprint], (err, rows) => {
                if (err) {
                    reject(err);
                } else {
                    resolve(rows);
                }
            });
        });
    }
}

module.exports = Aluno;
