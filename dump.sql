PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    tipo TEXT NOT NULL,
    fabrica_id INTEGER,
    FOREIGN KEY (fabrica_id) REFERENCES fabrica(id)
);
INSERT INTO user VALUES(1,'admin@sgp.com','senha123','admin_master',NULL);
INSERT INTO user VALUES(2,'admin@hagora.com','senha123','admin_fabrica',1);
INSERT INTO user VALUES(3,'admin@hdroupas.com','senha123','admin_fabrica',2);
CREATE TABLE permissao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    acao TEXT NOT NULL,
    permitido BOOLEAN NOT NULL DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES user(id)
);
CREATE TABLE IF NOT EXISTS "OLD_produto_estoque_movimento" (
	id INTEGER NOT NULL, 
	produto_id INTEGER NOT NULL, 
	tamanho VARCHAR(5) NOT NULL, 
	cor VARCHAR(30) NOT NULL, 
	quantidade INTEGER NOT NULL, 
	quantidade_consumida INTEGER, 
	tipo_movimento VARCHAR(10) NOT NULL, 
	status_estoque VARCHAR(20) NOT NULL, 
	data_movimento DATETIME, 
	usuario_id INTEGER NOT NULL, 
	referencia_entrada_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(produto_id) REFERENCES produto (id), 
	FOREIGN KEY(usuario_id) REFERENCES usuario (id), 
	FOREIGN KEY(referencia_entrada_id) REFERENCES "OLD_produto_estoque_movimento" (id)
);
CREATE TABLE fabrica (
	id INTEGER NOT NULL, 
	nome VARCHAR(100) NOT NULL, 
	cnpj VARCHAR(20), 
	email VARCHAR(120), 
	responsavel VARCHAR(100), 
	celular VARCHAR(20), 
	status VARCHAR(10), 
	tipo VARCHAR(50), 
	observacao TEXT, 
	created_at DATETIME, 
	PRIMARY KEY (id)
);
INSERT INTO fabrica VALUES(1,'HD Tecnologia Ltda','12.345.678/0001-99','contato@hd.com.br','Clayton Antunes','(48) 99958-0587','Ativo','Tecnologia','Foco em software e automação.','2025-06-24 00:49:44.536288');
INSERT INTO fabrica VALUES(2,'HD Roupas Ltda','98.765.432/0001-11','contato@roupas.com.br','Magda Renata','(48) 98484-0587','Ativo','Roupas','Especializada em camisetas promocionais e uniformes.','2025-06-24 00:49:44.536292');
CREATE TABLE tamanho (
	id INTEGER NOT NULL, 
	descricao VARCHAR(10) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (descricao)
);
INSERT INTO tamanho VALUES(1,'P');
INSERT INTO tamanho VALUES(2,'M');
INSERT INTO tamanho VALUES(3,'G');
INSERT INTO tamanho VALUES(4,'GG');
INSERT INTO tamanho VALUES(5,'G1');
INSERT INTO tamanho VALUES(6,'G2');
INSERT INTO tamanho VALUES(7,'G3');
CREATE TABLE cor (
	id INTEGER NOT NULL, 
	descricao VARCHAR(50) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (descricao)
);
INSERT INTO cor VALUES(1,'Branco');
INSERT INTO cor VALUES(2,'Preto');
INSERT INTO cor VALUES(3,'Vermelho');
INSERT INTO cor VALUES(4,'Azul');
INSERT INTO cor VALUES(5,'Verde');
INSERT INTO cor VALUES(6,'Amarelo');
INSERT INTO cor VALUES(7,'Cinza');
CREATE TABLE usuario (
	id INTEGER NOT NULL, 
	nome VARCHAR(100) NOT NULL, 
	email VARCHAR(120) NOT NULL, 
	senha_hash VARCHAR(256) NOT NULL, 
	funcao VARCHAR(20) NOT NULL, 
	ativo BOOLEAN, 
	created_at DATETIME, 
	fabrica_id INTEGER, 
	PRIMARY KEY (id), 
	UNIQUE (email), 
	FOREIGN KEY(fabrica_id) REFERENCES fabrica (id)
);
INSERT INTO usuario VALUES(1,'TecMA','antunes20@gmail.com','pbkdf2:sha256:260000$CM3HMIJwj8J5ln0j$84a84abef58ebe9ec6866da608c458dc1a8842fd43919476c21e811257cd6798','master',1,'2025-06-24 00:49:45.084695',1);
INSERT INTO usuario VALUES(2,'TecAD','admin@tec.com','pbkdf2:sha256:260000$CXQO1o2rPQHH7ZmY$86857a05abd3d05119a08e423ef9c4ac4ee31ad4abc33fb163e5a0ee08f1694d','admin',1,'2025-06-24 00:49:45.084701',1);
INSERT INTO usuario VALUES(3,'TecME','medio@tec.com','pbkdf2:sha256:260000$jxf92gtZswXG7FMo$2b8c1173650a09e15628529f44d5f28548a264a1d726c383fc6e0add6d81f17a','medio',1,'2025-06-24 00:49:45.084701',1);
INSERT INTO usuario VALUES(5,'RoupasAD','admin@roupas.com','pbkdf2:sha256:260000$MJrvQvOxp32fWm2L$6b0cab0a8e4aa06f7d78a5bfccf894abf99e801c7851aa8a80b76cdadc349a1a','admin',1,'2025-06-24 00:49:45.084702',2);
INSERT INTO usuario VALUES(6,'RoupasME','medio@roupas.com','pbkdf2:sha256:260000$fefSEueysH8mIiyh$c4b0cf5a8783db0533c8005ba6c81cf9587c0d5396ab44322864738cb796ae17','medio',1,'2025-06-24 00:49:45.084703',2);
INSERT INTO usuario VALUES(7,'aaaaa','aaaa@ddd.bom','pbkdf2:sha256:260000$KfQYLAO07XShHOoE$941c676413040f522164c27968a0ad509c10e338cc0e433bfcb03e083f477c0d','master',1,'2025-06-24 20:25:11.052252',1);
INSERT INTO usuario VALUES(8,'bbbbb1','bbb1@bbb.com','pbkdf2:sha256:260000$uytC50lpMq1nMJUn$370e21e10cec5ddbd5431fa9e271ebce496f3035177f03ffdc96356045392e3f','simples',0,'2025-06-24 20:25:51.863615',2);
CREATE TABLE cliente (
	id INTEGER NOT NULL, 
	nome VARCHAR(120) NOT NULL, 
	endereco VARCHAR(150), 
	numero VARCHAR(20), 
	complemento VARCHAR(100), 
	cidade VARCHAR(100), 
	uf VARCHAR(2), 
	cep VARCHAR(10), 
	cnpj VARCHAR(18), 
	cpf VARCHAR(14), 
	responsavel VARCHAR(100), 
	celular VARCHAR(20), 
	telefone VARCHAR(20), 
	email VARCHAR(120), 
	fabrica_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(fabrica_id) REFERENCES fabrica (id)
);
CREATE TABLE tipo_vestuario (
	id INTEGER NOT NULL, 
	nome VARCHAR(100) NOT NULL, 
	fabrica_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(fabrica_id) REFERENCES fabrica (id)
);
INSERT INTO tipo_vestuario VALUES(1,'Camiseta',2);
INSERT INTO tipo_vestuario VALUES(2,'Moletom',2);
INSERT INTO tipo_vestuario VALUES(3,'Uniforme',2);
INSERT INTO tipo_vestuario VALUES(4,'Avental',2);
CREATE TABLE produto (
	id INTEGER NOT NULL, 
	nome VARCHAR(120) NOT NULL, 
	descricao TEXT, 
	tipo_id INTEGER NOT NULL, 
	fabrica_id INTEGER NOT NULL, 
	tamanho_id INTEGER NOT NULL, 
	cor_id INTEGER NOT NULL, 
	status VARCHAR(20) NOT NULL, 
	valor_compra NUMERIC(10, 2) NOT NULL, 
	valor_venda NUMERIC(10, 2) NOT NULL, 
	saldo_estoque INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(tipo_id) REFERENCES tipo_vestuario (id), 
	FOREIGN KEY(fabrica_id) REFERENCES fabrica (id), 
	FOREIGN KEY(tamanho_id) REFERENCES tamanho (id), 
	FOREIGN KEY(cor_id) REFERENCES cor (id)
);
CREATE TABLE pedido (
	id INTEGER NOT NULL, 
	fabrica_id INTEGER NOT NULL, 
	numero INTEGER NOT NULL, 
	cliente_id INTEGER NOT NULL, 
	data DATETIME, 
	valor_frete FLOAT NOT NULL, 
	status VARCHAR(20) NOT NULL, 
	usuario_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(fabrica_id) REFERENCES fabrica (id), 
	FOREIGN KEY(cliente_id) REFERENCES cliente (id), 
	FOREIGN KEY(usuario_id) REFERENCES usuario (id)
);
CREATE TABLE estoque (
	id INTEGER NOT NULL, 
	fabrica_id INTEGER NOT NULL, 
	produto_id INTEGER NOT NULL, 
	quantidade INTEGER NOT NULL, 
	tipo_movimento VARCHAR(10) NOT NULL, 
	status_estoque VARCHAR(20), 
	usuario_id INTEGER NOT NULL, 
	data_movimento DATETIME, 
	referencia_entrada_id INTEGER, 
	valor_unitario FLOAT, 
	local_compra TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(fabrica_id) REFERENCES fabrica (id), 
	FOREIGN KEY(produto_id) REFERENCES produto (id), 
	FOREIGN KEY(usuario_id) REFERENCES usuario (id)
);
CREATE TABLE pedido_item (
	id INTEGER NOT NULL, 
	pedido_id INTEGER NOT NULL, 
	produto_id INTEGER NOT NULL, 
	quantidade INTEGER NOT NULL, 
	informacao VARCHAR(100), 
	PRIMARY KEY (id), 
	FOREIGN KEY(pedido_id) REFERENCES pedido (id), 
	FOREIGN KEY(produto_id) REFERENCES produto (id)
);
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('user',3);
COMMIT;
