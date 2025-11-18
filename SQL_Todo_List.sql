-- create database todo_list

create table usuario(
id_usuario serial primary key,
nome varchar(255) not null,
email varchar(255) not null unique,
senha varchar(255) not null,
idade int
);

create table tarefa(
id_tarefas serial primary key,
titulo varchar(255) not null,
descricao varchar(255),
completa boolean default false,
id_usuario INT REFERENCES usuario(id_usuario) ON DELETE CASCADE
);