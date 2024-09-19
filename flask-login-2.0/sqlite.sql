create table usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    matricula INTEGER NOT NULL,
    email TEXT NOT NULL,
    senha TEXT NOT NULL
);

create table exercicios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    descricao TEXT NOT NULL,
    usuario INTEGER,
    FOREIGN KEY(usuario) REFERENCES usuarios(id)
);
