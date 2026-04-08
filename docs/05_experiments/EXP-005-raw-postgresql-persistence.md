# EXP-005 — Raw PostgreSQL Persistence

## Objetivo

Validar el almacenamiento persistente de eventos crudos SSH en PostgreSQL a partir del consumidor Python conectado a RabbitMQ.

## Hipótesis técnica

Si el consumidor Python valida correctamente los eventos y la persistencia está bien configurada, entonces una sesión SSH real deberá quedar almacenada como múltiples filas en `events_raw`.

## Componentes involucrados

- Honeypot SSH en Rust
- Exchange y queue en RabbitMQ
- Consumer Python
- PostgreSQL
- Tabla `events_raw`

## Procedimiento

1. Inicializar la base de datos
2. Ejecutar el consumer Python con persistencia
3. Generar tráfico SSH real
4. Consumir mensajes desde RabbitMQ
5. Insertar eventos validados en PostgreSQL
6. Verificar filas insertadas mediante consulta SQL

## Resultados observados

Se reconstruyeron sesiones SSH a partir de `events_raw` usando `session_id` y `event_sequence`. Para sesiones completas se calcularon variables temporales básicas, incluyendo `mean_dt`, `std_dt`, `burst_rate` y `temporal_entropy`.

## Problemas encontrados

Algunos eventos podían llegar y persistirse fuera de orden de consumo, pero el orden lógico fue preservado mediante `event_sequence`, lo que permitió reconstrucción correcta.

## Conclusión

La agregación por sesión y el modelado temporal básico quedaron operativos, dejando preparada la base para fingerprinting y análisis de anomalías.