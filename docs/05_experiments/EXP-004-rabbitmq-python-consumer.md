# EXP-004 — RabbitMQ to Python Consumer Validation

## Objetivo

Validar el tramo del pipeline distribuido desde el honeypot Rust hacia RabbitMQ y desde RabbitMQ hacia el consumidor Python con validación Pydantic.

## Hipótesis técnica

Si el publisher Rust publica eventos estructurados al exchange `prometheus.events` y una cola enlazada los enruta correctamente, entonces el consumidor Python deberá recibirlos y validarlos sin ambigüedad.

## Componentes involucrados

- Honeypot SSH en Rust
- Publisher AMQP
- RabbitMQ exchange `prometheus.events`
- Queue `prometheus.events.queue`
- Consumer Python
- Modelo Pydantic `PrometheusEvent`

## Procedimiento

1. Ejecutar el honeypot Rust
2. Generar tráfico SSH real
3. Publicar eventos al exchange RabbitMQ
4. Enrutar mensajes a la cola enlazada
5. Ejecutar consumidor Python
6. Validar mensajes consumidos con Pydantic

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

Persistir eventos crudos en PostgreSQL desde el consumidor Python.