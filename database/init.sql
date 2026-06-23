-- 1. Crear la tabla para el Perfil de usuarios
create table if not exists perfil_usuario (
   id_usuario            varchar(50) primary key,
   edad                  INT,
   genero                varchar(20),
   pais                  varchar(50),
   dispositivo_principal varchar(50),
   fecha_registro        date
);


COPY perfil_usuario(id_usuario,edad,genero,pais,dispositivo_principal,fecha_registro)
FROM '/docker-entrypoint-initdb.d/perfil_cliente.csv'
DELIMITER ','
CSV HEADER;