# LOCAL SETUP

## Objetivo

Definir el procedimiento local mínimo para levantar el entorno base reproducible de Prometheus.

## Requisitos

- Git instalado
- Docker instalado
- Docker Compose Plugin disponible mediante `docker compose`

## Variables de entorno

Crear el archivo `.env` a partir de la plantilla:

```bash
cp .env.example .env