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

Pendiente de ejecución.

## Evidencia

Pendiente de ejecución.

## Problemas encontrados

Pendiente de ejecución.

## Correcciones aplicadas

Pendiente de ejecución.

## Conclusión

Pendiente de ejecución.

## Siguiente paso

Reconstruir sesiones SSH a partir de `session_id` y `event_sequence`.