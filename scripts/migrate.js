const sqlite3 = require('sqlite3').verbose();
const path = require('path');

// Caminho do banco de dados
const dbPath = path.join(__dirname, 'database', 'avaliacao_pares.db');

console.log('🔄 Iniciando migração do banco de dados...');

// Criar diretório database se não existir
const fs = require('fs');
const dbDir = path.join(__dirname, 'database');
if (!fs.existsSync(dbDir)) {
    fs.mkdirSync(dbDir, { recursive: true });
    console.log('📁 Diretório database criado');
}

// Conectar ao banco
const db = new sqlite3.Database(dbPath, (err) => {
    if (err) {
        console.error('❌ Erro ao conectar com o banco de dados:', err.message);
        process.exit(1);
    } else {
        console.log('✅ Conectado ao banco de dados SQLite');
    }
});

// Habilitar foreign keys
db.run('PRAGMA foreign_keys = ON');

// Função para criar tabelas
function createTables() {
    return new Promise((resolve, reject) => {
        console.log('📋 Criando tabelas...');

        const createProfessoresTable = `
            CREATE TABLE IF NOT EXISTS professores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        `;

        const createAlunosTable = `
            CREATE TABLE IF NOT EXISTS alunos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                senha TEXT,
                turma TEXT NOT NULL,
                grupo TEXT NOT NULL,
                sprint_atual INTEGER DEFAULT 1,
                professor_id INTEGER NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (professor_id) REFERENCES professores (id)
            )
        `;

        const createEixosTable = `
            CREATE TABLE IF NOT EXISTS eixos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT UNIQUE NOT NULL,
                descricao TEXT NOT NULL,
                observacoes TEXT,
                ordem INTEGER DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        `;

        const createAvaliacoesTable = `
            CREATE TABLE IF NOT EXISTS avaliacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                avaliador_id INTEGER NOT NULL,
                avaliado_id INTEGER NOT NULL,
                sprint INTEGER NOT NULL,
                eixo_id INTEGER NOT NULL,
                nota INTEGER NOT NULL CHECK (nota >= 0 AND nota <= 3),
                feedback TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (avaliador_id) REFERENCES alunos (id),
                FOREIGN KEY (avaliado_id) REFERENCES alunos (id),
                FOREIGN KEY (eixo_id) REFERENCES eixos (id),
                UNIQUE(avaliador_id, avaliado_id, sprint, eixo_id)
            )
        `;

        db.serialize(() => {
            db.run(createProfessoresTable, (err) => {
                if (err) {
                    console.error('❌ Erro ao criar tabela professores:', err);
                    reject(err);
                    return;
                }
                console.log('✅ Tabela professores criada');
            });

            db.run(createAlunosTable, (err) => {
                if (err) {
                    console.error('❌ Erro ao criar tabela alunos:', err);
                    reject(err);
                    return;
                }
                console.log('✅ Tabela alunos criada');
            });

            db.run(createEixosTable, (err) => {
                if (err) {
                    console.error('❌ Erro ao criar tabela eixos:', err);
                    reject(err);
                    return;
                }
                console.log('✅ Tabela eixos criada');
            });

            db.run(createAvaliacoesTable, (err) => {
                if (err) {
                    console.error('❌ Erro ao criar tabela avaliacoes:', err);
                    reject(err);
                    return;
                }
                console.log('✅ Tabela avaliacoes criada');
                resolve();
            });
        });
    });
}

// Função para inserir eixos iniciais
async function insertInitialEixos() {
    console.log('📊 Inserindo eixos de avaliação...');

    const eixos = [
        {
            nome: "Entregas reais",
            descricao: "Avalia o cumprimento das entregas da sprint. Leva em consideração se os prazos foram respeitados, se os formatos estavam corretos e se os artefatos foram bem executados.",
            observacoes: JSON.stringify([
                "GitHub: Verificar se o colega fez commits dentro do prazo",
                "GitHub: Verificar se o colega dez entregas funcionais",
                "GitHub: Verificar se o colega seguiu padrões de projeto, nomeou corretamente os PRs",
                "Trello: Verificar se o colega cumpriu com as tarefas atribuídas a ele e elas foram finalizadas no prazo.",
                "Daily: Verificar se o colega foi atuante nas dailies, se posicionando sobre o que foi feito e o que vai fazer.",
                "Daily: Verificar se o colega participa ativamente das dailies contribuindo para a gestão diária e a condução do projeto."
            ]),
            ordem: 1
        },
        {
            nome: "Valor Percebido",
            descricao: "Avalia o impacto das entregas para o grupo durante a sprint. Deve levar em consideração o valor agregado para o projeto, se houve a geração de novas ideias e achados valiosos para o parceiro e se o trabalho contribuiu para um avanço nos resultados esperados.",
            observacoes: JSON.stringify([
                "GitHub: Verificar se o colega entregou algo que destravou uma etapa importante do projeto.",
                "GitHub: Verificar se o item de informação / código entregue agregou valor ao projeto/sistema (ex: documentações relevantes, modelagens relevantes, novas funcionalidades, correções críticas, ganho de performance).",
                "Trello: Verificar se as tarefas atribuídas ao colega contribuíram significativamente para o avanço do grupo ou para entregas mais complexas.",
                "Daily: Verificar se o colega compartilhou ideias ou sugestões que ajudaram o grupo a resolver problemas ou tomar decisões.",
                "Daily: Verificar se o colega trouxe aprendizados, achados ou validações que contribuíram para o parceiro ou para a visão do produto.",
                "Horário de desenvolvimento: Verificar se o colega ajudou outros membros do grupo a finalizar tarefas ou superar obstáculos durante os horários coletivos."
            ]),
            ordem: 2
        },
        {
            nome: "Caixa de Ferramentas",
            descricao: "Avalia o desenvolvimento técnico do aluno, verificando se a pessoa evoluiu e absorveu os conceitos técnicos, conseguindo aplicá-los na prática (afinal, estamos em uma faculdade de tecnologia).",
            observacoes: JSON.stringify([
                "GitHub: Verificar se o colega usou conceitos técnicos aprendidos no módulo (ex: bibliotecas novas, estruturação correta do código, uso de boas práticas).",
                "GitHub: Verificar se houve evolução técnica ao longo do tempo (ex: começou com pequenos ajustes e passou a contribuir com partes mais complexas).",
                "Trello: Verificar se o colega assumiu tarefas técnicas mais desafiadoras ou complexas.",
                "Daily: Verificar se o colega demonstra domínio técnico ao explicar o que está desenvolvendo.",
                "Daily: Verificar se o colega compartilha aprendizados técnicos com o grupo ou propõe soluções com base nos conteúdos aprendidos.",
                "Horário de desenvolvimento: Verificar se o colega aproveitou os momentos de trabalho para experimentar ferramentas e consolidar o aprendizado técnico na prática."
            ]),
            ordem: 3
        }
    ];

    for (const eixo of eixos) {
        try {
            await new Promise((resolve, reject) => {
                const sql = 'INSERT OR IGNORE INTO eixos (nome, descricao, observacoes, ordem) VALUES (?, ?, ?, ?)';
                db.run(sql, [eixo.nome, eixo.descricao, eixo.observacoes, eixo.ordem], function(err) {
                    if (err) {
                        reject(err);
                    } else {
                        if (this.changes > 0) {
                            console.log(`✅ Eixo "${eixo.nome}" inserido`);
                        } else {
                            console.log(`ℹ️  Eixo "${eixo.nome}" já existe`);
                        }
                        resolve();
                    }
                });
            });
        } catch (error) {
            console.error(`❌ Erro ao inserir eixo "${eixo.nome}":`, error);
        }
    }
}

// Função principal
async function migrate() {
    try {
        await createTables();
        await insertInitialEixos();
        
        console.log('\n🎉 Migração concluída com sucesso!');
        console.log('📋 Tabelas criadas:');
        console.log('   - professores (vazia)');
        console.log('   - alunos (vazia)');
        console.log('   - eixos (com dados iniciais)');
        console.log('   - avaliacoes (vazia)');
        console.log('\n⚠️  IMPORTANTE:');
        console.log('   - Execute "npm run create-professors" para criar os professores');
        console.log('   - As tabelas estão vazias e prontas para uso');
        
    } catch (error) {
        console.error('❌ Erro durante a migração:', error);
        process.exit(1);
    } finally {
        db.close((err) => {
            if (err) {
                console.error('❌ Erro ao fechar banco:', err.message);
            } else {
                console.log('🔒 Conexão com banco fechada');
            }
        });
    }
}

// Executar migração
migrate();
