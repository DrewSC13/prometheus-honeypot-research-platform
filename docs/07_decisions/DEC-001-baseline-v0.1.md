# DEC-001 — Baseline v0.1

## Contexto

Se ha alcanzado un estado estable del sistema con:

- Honeypot SSH funcional
- Emisión de eventos estructurados
- Pipeline RabbitMQ operativo
- Validación con Pydantic
- Persistencia en PostgreSQL (events_raw)
- Reconstrucción de sesiones SSH
- Generación de features iniciales (session_features)

## Decisión

Se congela este estado como baseline experimental reproducible bajo la versión:

v0.1-baseline

## Justificación

Este punto representa el primer sistema completo funcional del pipeline.

Permite:

- reproducibilidad experimental
- comparación con versiones futuras
- validación de mejoras en modelado temporal y fingerprinting

## Impacto

Todas las mejoras futuras deberán compararse contra este baseline.