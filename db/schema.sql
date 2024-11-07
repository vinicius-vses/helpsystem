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

INSERT INTO usuarios (nome, sobrenome, id_departamento, email, senha) VALUES ('João', 'Silva', 1, 'joao.silva@empresa.com', 'senha123');
INSERT INTO usuarios (nome, sobrenome, id_departamento, email, senha) VALUES ('Marcos', 'Oliveira', 2, 'maria.oliveira@empresa.com', 'senha456');
INSERT INTO usuarios (nome, sobrenome, id_departamento, email, senha) VALUES ('Lucas', 'Santos', 3, 'carlos.santos@empresa.com', 'senha789');

INSERT INTO departamentos (nome, descricao) VALUES ('Revenue', 'Departamento de Receita');
INSERT INTO departamentos (nome, descricao) VALUES ('Previdência', 'Departamento de Previdência');
INSERT INTO departamentos (nome, descricao) VALUES ('Estratégia e Performance', 'Departamento de Estratégia e Performance');
INSERT INTO departamentos (nome, descricao) VALUES ('Estratégias Quantitativas', 'Departamento de Estratégias Quantitativas');
INSERT INTO departamentos (nome, descricao) VALUES ('FP&A', 'Departamento de FP&A');
INSERT INTO departamentos (nome, descricao) VALUES ('Open Finance', 'Departamento de Open Finance');
INSERT INTO departamentos (nome, descricao) VALUES ('Arquitetura Mobile', 'Departamento de Arquitetura Mobile');
INSERT INTO departamentos (nome, descricao) VALUES ('Gestão de Ativos', 'Departamento de Gestão de Ativos');
INSERT INTO departamentos (nome, descricao) VALUES ('Comunidade e Colaboração', 'Departamento de Comunidade e Colaboração');
INSERT INTO departamentos (nome, descricao) VALUES ('Outro', 'Outro departamento');

INSERT INTO categorias (nome, descricao) VALUES ('Conta e Cadastro', 'Questões relacionadas à conta e cadastro de usuários');
INSERT INTO categorias (nome, descricao) VALUES ('Pagamentos e Faturamento', 'Dúvidas e problemas com pagamentos e faturamento');
INSERT INTO categorias (nome, descricao) VALUES ('Configurações e Preferências', 'Configurações e preferências de usuário');
INSERT INTO categorias (nome, descricao) VALUES ('Técnico e Solução de Problemas', 'Soluções para problemas técnicos');
INSERT INTO categorias (nome, descricao) VALUES ('Segurança e Privacidade', 'Questões de segurança e privacidade de dados');
INSERT INTO categorias (nome, descricao) VALUES ('Funcionalidades e Recursos', 'Funcionalidades e recursos disponíveis');
INSERT INTO categorias (nome, descricao) VALUES ('Suporte e Atendimento ao Cliente', 'Atendimento ao cliente e suporte');
INSERT INTO categorias (nome, descricao) VALUES ('Integrações e APIs', 'Integrações e uso de APIs');
INSERT INTO categorias (nome, descricao) VALUES ('Feedback e Sugestões', 'Feedback e sugestões de usuários');
INSERT INTO categorias (nome, descricao) VALUES ('Comunidade e Colaboração', 'Comunidade e colaboração entre usuários');
INSERT INTO categorias (nome, descricao) VALUES ('Documentação e Tutoriais', 'Documentação e tutoriais para usuários');
INSERT INTO categorias (nome, descricao) VALUES ('Atualizações e Novidades', 'Novidades e atualizações do sistema');
INSERT INTO categorias (nome, descricao) VALUES ('Políticas e Termos de Uso', 'Informações sobre políticas e termos de uso');
INSERT INTO categorias (nome, descricao) VALUES ('Outro', 'Outras categorias não especificadas');

INSERT INTO solicitacoes (id_usuario, id_categoria, titulo, descricao, status) VALUES (1, 1, 'Computador não liga', 'Meu computador não está ligando.', 0);
INSERT INTO solicitacoes (id_usuario, id_categoria, titulo, descricao, status) VALUES (2, 2, 'Erro no sistema', 'Erro ao tentar acessar o sistema financeiro.', 0);
INSERT INTO solicitacoes (id_usuario, id_categoria, titulo, descricao, status) VALUES (3, 3, 'Solicitação de reembolso', 'Preciso de um reembolso para despesas de viagem.', 0);

INSERT INTO respostas (id_solicitacao, id_usuario, resposta, pontos) VALUES (1, 2, 'Verifique se o cabo de energia está conectado.', 5);
INSERT INTO respostas (id_solicitacao, id_usuario, resposta, pontos) VALUES (2, 1, 'Tente reiniciar o sistema e limpar o cache.', 3);
INSERT INTO respostas (id_solicitacao, id_usuario, resposta, pontos) VALUES (3, 2, 'Envie a documentação para o setor financeiro.', 4);

INSERT INTO ranking (id_usuario, pontos_totais, nivel_proatividade) VALUES (1, 10, 1);
INSERT INTO ranking (id_usuario, pontos_totais, nivel_proatividade) VALUES (2, 12, 2);
INSERT INTO ranking (id_usuario, pontos_totais, nivel_proatividade) VALUES (3, 8, 1);
