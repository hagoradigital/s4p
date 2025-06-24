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
INSERT INTO fabrica VALUES(1,'HD Tecnologia Ltda','12.345.678/0001-99','contato@tec.com','João Silva','(48) 99999-0001','Ativo','Tecnologia','Foco em software e automação.','2025-06-21 14:39:18.693819');
INSERT INTO fabrica VALUES(2,'HD Roupas Ltda','98.765.432/0001-11','contato@roupas.com','Maria Souza','(48) 98888-0002','Ativo','Roupas','Especializada em camisetas promocionais e uniformes.','2025-06-21 14:39:18.693822');
INSERT INTO fabrica VALUES(3,'HD Padaria Ltda','56.789.123/0001-44','contato@padaria.com','Carlos Lima','(48) 97777-0003','Ativo','Padaria','Foco em panificação artesanal.','2025-06-21 14:39:18.693822');
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
	senha_hash VARCHAR(128) NOT NULL, 
	funcao VARCHAR(20) NOT NULL, 
	ativo BOOLEAN, 
	created_at DATETIME, 
	fabrica_id INTEGER, 
	PRIMARY KEY (id), 
	UNIQUE (email), 
	FOREIGN KEY(fabrica_id) REFERENCES fabrica (id)
);
INSERT INTO usuario VALUES(1,'TecMA','antunes20@gmail.com','scrypt:32768:8:1$5qbrmmFhelrDIL9s$dbb123c62c44f65adfc39d3bd71d3ee2f215cdf76c7c389dba4f8e0fd73bca34b8d468a672427a76e4dccfb0e92122d04b1fcad1c9ed4915396c28352975234f','master',1,'2025-06-21 14:39:19.367534',1);
INSERT INTO usuario VALUES(2,'TecAD','admin@tec.com','scrypt:32768:8:1$OBsdZzpO7R2nEml8$16a10f8a20509e910c6507fe01f2ebfff51e14ae3c8c4a62d553c5e5600d1e79821931c7b5db1f28736d7f1bd5d497ceec6153f8db68a7d1af2c8ff98cc95e4a','admin',1,'2025-06-21 14:39:19.367538',1);
INSERT INTO usuario VALUES(3,'TecME','medio@tec.com','scrypt:32768:8:1$2RT8irrM96UvT7he$90fd0095ec386f281b66b4853dcbd78b8644cc6d736edcb1d8b519a70b97d04c68ae5ef66ecb51549067c2759ec02ce2d3df2685aee5b6f3931a3022c3853d9a','medio',1,'2025-06-21 14:39:19.367539',1);
INSERT INTO usuario VALUES(4,'TecSI','simples@tec.com','scrypt:32768:8:1$mF1UEpE1RCvFuJFa$35e5ca340e033327008f76da19da8b48543dbad8f697345b2f5e11011eac989c28cbcee8b2c5a471a2c945d209af7d13d4b2052514155eecea764c5aec2574e1','simples',1,'2025-06-21 14:39:19.367539',1);
INSERT INTO usuario VALUES(5,'RoupasAD','admin@roupas.com','scrypt:32768:8:1$CL1y3jmad9hqialz$17271ff60610f7b16efa95c5524693693ddbfc827f48ac1b036aceb6d3665da6fc7f163665329fab88d525d19be9362ca1c7a19230a66c217dfe5c6feecdff77','admin',1,'2025-06-21 14:39:19.367540',2);
INSERT INTO usuario VALUES(6,'RoupasME','medio@roupas.com','scrypt:32768:8:1$U0BkF2DwcQdT36ju$6d3cf9ad8f091627113c585e49713eec5797b01182f121df7d1ac0028c49f296eb06ee628f5183c63377fafcfc9aa7b20e05ef936058b1b2686060107b83e146','medio',1,'2025-06-21 14:39:19.367540',2);
INSERT INTO usuario VALUES(7,'PadariaAD','admin@padaria.com','scrypt:32768:8:1$5AjHOWX4ZoJFtAvp$88b1122308ae5beb1ad120f378eb8a83ba7d7f652169fd7c8324a96fc32b0b2a418ee3ad1486ab991a7a121f023c600b45f3c4f1baa8cc77c38d768a734dfc5d','admin',1,'2025-06-21 14:39:19.367541',3);
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
INSERT INTO cliente VALUES(1,'Padaria do Zezinho','','','','','','','','',NULL,'','','',1);
INSERT INTO cliente VALUES(2,'Clayton Antunes','Rodovia Baldicero Filomeno','995','','Florianópolis','SC','88064-000','22.222.222/2222-22','017.087.239-43',NULL,'(44) 44444-4444','(48) 9995-8058','antunes20@gmail.com',1);
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
INSERT INTO tipo_vestuario VALUES(4,'Avental',3);
INSERT INTO tipo_vestuario VALUES(5,'Corta-Vento',1);
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
INSERT INTO produto VALUES(1,'Camiseta Branca M',NULL,1,2,2,1,'ativo',10,30,100);
INSERT INTO produto VALUES(2,'Moletom Azul G',NULL,2,2,3,4,'ativo',20,60,50);
INSERT INTO produto VALUES(3,'Uniforme Técnico G',NULL,3,2,3,4,'ativo',15,45,30);
INSERT INTO produto VALUES(4,'Avental Branco M',NULL,4,3,2,1,'ativo',12,35,20);
INSERT INTO produto VALUES(5,'Corta-Vento Básico sem forro','',5,1,3,2,'ativo',0.11,1.11000000000000009,0);
INSERT INTO produto VALUES(6,'Corta-Vento Básico sem forro','',5,1,2,2,'ativo',0.0500000000000000027,0.0599999999999999977,0);
INSERT INTO produto VALUES(7,'Corta-Vento Básico sem forro','',5,1,1,2,'ativo',0.0599999999999999977,0.67000000000000004,0);
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
INSERT INTO pedido VALUES(1,1,1,1,'2025-06-23 01:00:45.686100',23.8999999999999985,'Em Análise',1);
INSERT INTO pedido VALUES(2,1,2,2,'2025-06-23 01:01:03.298084',43.6000000000000014,'Aprovado',1);
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
INSERT INTO estoque VALUES(1,2,1,100,'entrada','Estoque',1,'2025-06-21 14:39:19.409476',NULL,NULL,'Estoque inicial');
INSERT INTO estoque VALUES(2,2,2,50,'entrada','Estoque',1,'2025-06-21 14:39:19.409478',NULL,NULL,'Estoque inicial');
INSERT INTO estoque VALUES(3,2,3,30,'entrada','Estoque',1,'2025-06-21 14:39:19.409479',NULL,NULL,'Estoque inicial');
INSERT INTO estoque VALUES(4,3,4,20,'entrada','Estoque',1,'2025-06-21 14:39:19.409479',NULL,NULL,'Estoque inicial');
INSERT INTO estoque VALUES(5,1,5,11,'entrada','Estoque',1,'2025-06-21 14:52:41.876559',NULL,0.11,'');
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
