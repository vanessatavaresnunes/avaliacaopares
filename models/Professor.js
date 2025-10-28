const db = require('../config/db');
const bcrypt = require('bcryptjs');

class Professor {
    constructor(data) {
        this.id = data.id;
        this.nome = data.nome;
        this.email = data.email;
        this.senha = data.senha;
        this.created_at = data.created_at;
    }


    // Método para buscar professor por email
    static async findByEmail(email) {
        return new Promise((resolve, reject) => {
            const sql = 'SELECT id, nome, email, senha, created_at FROM professores WHERE email = ?';
            db.get(sql, [email], (err, row) => {
                if (err) {
                    reject(err);
                } else if (row) {
                    resolve(new Professor(row));
                } else {
                    resolve(null);
                }
            });
        });
    }

    // Método para buscar professor por ID
    static async findById(id) {
        return new Promise((resolve, reject) => {
            const sql = 'SELECT id, nome, email, senha, created_at FROM professores WHERE id = ?';
            db.get(sql, [id], (err, row) => {
                if (err) {
                    reject(err);
                } else if (row) {
                    resolve(new Professor(row));
                } else {
                    resolve(null);
                }
            });
        });
    }

    // Método para verificar senha
    async checkPassword(password) {
        return bcrypt.compare(password, this.senha);
    }

    // Método para atualizar senha
    async updatePassword(newPassword) {
        return new Promise((resolve, reject) => {
            bcrypt.hash(newPassword, 10, (err, hashedPassword) => {
                if (err) {
                    reject(err);
                    return;
                }

                const sql = 'UPDATE professores SET senha = ? WHERE id = ?';
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

    // Método para obter todos os alunos do professor
    async getAlunos() {
        const Aluno = require('./Aluno');
        return Aluno.findByProfessor(this.id);
    }

    // Método para obter dados sem senha (para segurança)
    toJSON() {
        const { senha, ...professorData } = this;
        return professorData;
    }
}

module.exports = Professor;
