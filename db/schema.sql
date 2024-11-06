CREATE TABLE usuarios (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    sobrenome TEXT NOT NULL,
    id_departamento INTEGER,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    FOREIGN KEY (id_departamento) REFERENCES departamentos(id_departamento)
);

CREATE TABLE categorias (
    id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    descricao TEXT
);

CREATE TABLE departamentos (
    id_departamento INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    descricao TEXT
);

CREATE TABLE solicitacoes (
    id_solicitacao INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    id_categoria INTEGER NOT NULL,
    titulo TEXT NOT NULL,
    descricao TEXT,
    status INTEGER DEFAULT 0 CHECK (status IN (0, 1)), -- 0 = Não Resolvida, 1 = Resolvida
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    data_resolucao DATETIME,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria)
);

CREATE TABLE respostas (
    id_resposta INTEGER PRIMARY KEY AUTOINCREMENT,
    id_solicitacao INTEGER NOT NULL,
    id_usuario INTEGER NOT NULL,
    resposta TEXT NOT NULL,
    data_resposta DATETIME DEFAULT CURRENT_TIMESTAMP,
    pontos INTEGER DEFAULT 0,
    FOREIGN KEY (id_solicitacao) REFERENCES solicitacoes(id_solicitacao),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

CREATE TABLE ranking (
    id_usuario INTEGER PRIMARY KEY,
    pontos_totais INTEGER DEFAULT 0,
    nivel_proatividade INTEGER DEFAULT 0,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

CREATE TRIGGER atualizar_pontuacao_apos_resposta
AFTER INSERT ON respostas
FOR EACH ROW
BEGIN
    UPDATE ranking
    SET pontos_totais = pontos_totais + NEW.pontos
    WHERE id_usuario = NEW.id_usuario;
END;
