-- 1. Crear la tabla para el Perfil de usuarios
create table if not exists perfil_usuario (
   id_cliente                              INT PRIMARY KEY,
   edad                                    NUMERIC,
   dispositivos_registrados                NUMERIC,
   porcentaje_uso_app_movil                NUMERIC,
   cantidad_perfiles_creados               NUMERIC,
   interacciones_mensuales_soporte         NUMERIC,
   distancia_promedio_red_km               NUMERIC
);


COPY perfil_usuario()
FROM '/docker-entrypoint-initdb.d/perfil_usuarios.csv'
DELIMITER ','
CSV HEADER;