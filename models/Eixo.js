const db = require('../config/db');

class Eixo {
    constructor(data) {
        this.id = data.id;
        this.nome = data.nome;
        this.descricao = data.descricao;
        this.observacoes = data.observacoes ? JSON.parse(data.observacoes) : [];
        this.ordem = data.ordem;
        this.created_at = data.created_at;
    }

    // Método para buscar todos os eixos
    static async findAll() {
        return new Promise((resolve, reject) => {
            const sql = 'SELECT id, nome, descricao, observacoes, ordem, created_at FROM eixos ORDER BY ordem ASC';
            db.all(sql, [], (err, rows) => {
                if (err) {
                    reject(err);
                } else {
                    resolve(rows.map(row => new Eixo(row)));
                }
            });
        });
    }

    // Método para buscar eixo por ID
    static async findById(id) {
        return new Promise((resolve, reject) => {
            const sql = 'SELECT id, nome, descricao, observacoes, ordem, created_at FROM eixos WHERE id = ?';
            db.get(sql, [id], (err, row) => {
                if (err) {
                    reject(err);
                } else if (row) {
                    resolve(new Eixo(row));
                } else {
                    resolve(null);
                }
            });
        });
    }

    // Método para buscar eixo por nome
    static async findByNome(nome) {
        return new Promise((resolve, reject) => {
            const sql = 'SELECT id, nome, descricao, observacoes, ordem, created_at FROM eixos WHERE nome = ?';
            db.get(sql, [nome], (err, row) => {
                if (err) {
                    reject(err);
                } else if (row) {
                    resolve(new Eixo(row));
                } else {
                    resolve(null);
                }
            });
        });
    }

    // Método para obter dados sem informações sensíveis
    toJSON() {
        return {
            id: this.id,
            nome: this.nome,
            descricao: this.descricao,
            observacoes: this.observacoes,
            ordem: this.ordem,
            created_at: this.created_at
        };
    }
}

module.exports = Eixo;
