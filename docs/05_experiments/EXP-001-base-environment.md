# EXP-001 — Base Environment

## Objetivo

Construir un entorno local reproducible para Prometheus que permita levantar y verificar los servicios base requeridos por la arquitectura inicial del sistema.

## Hipótesis técnica

Si se define un entorno basado en Docker Compose con PostgreSQL y RabbitMQ, entonces el proyecto dispondrá de una base estable, desacoplada y repetible para soportar el desarrollo incremental del pipeline orientado a eventos.

## Componentes involucrados

- Docker Compose
- PostgreSQL
- RabbitMQ
- Scripts de operación
- Variables de entorno

## Procedimiento

1. Crear archivo `.env` desde `.env.example`
2. Ejecutar `make up`
3. Esperar arranque de contenedores
4. Ejecutar `make check`
5. Verificar estado de salud de ambos servicios
6. Ejecutar `make down`

## Datos de entrada

- Archivo `docker-compose.yml`
- Archivo `.env`
- Scripts `up.sh`, `down.sh`, `check.sh`

## Resultados observados

Los servicios PostgreSQL y RabbitMQ se levantaron correctamente mediante Docker Compose. Ambos alcanzaron estado "healthy" según los healthchecks definidos.

## Evidencia

- Salida de `make up`
- Salida de `make check`
- Salida de `docker compose ps`

## Conclusión

Se valida que el entorno base es reproducible, desacoplado y estable, cumpliendo el criterio de aceptación de la fase inicial del proyecto.