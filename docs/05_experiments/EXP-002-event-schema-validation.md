# EXP-002 — Event Schema Validation

## Objetivo

Validar programáticamente los ejemplos del contrato `event_schema_v1` mediante modelos Pydantic en Python.

## Hipótesis técnica

Si el contrato formal fue definido correctamente, entonces los eventos válidos deberán ser aceptados y los eventos inválidos deberán fallar de forma consistente bajo validación tipada.

## Componentes involucrados

- `schemas/events/event_schema_v1.json`
- ejemplos JSON de `schemas/examples/`
- modelo Pydantic en `analysis-engine/app/models/event_models.py`
- script validador `analysis-engine/app/validators/validate_examples.py`

## Procedimiento

1. Crear entorno virtual en `analysis-engine`
2. Instalar Pydantic
3. Ejecutar script de validación
4. Verificar aceptación de ejemplos válidos
5. Verificar rechazo de ejemplo inválido

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

Preparar el proyecto Rust del honeypot SSH mínimo y emitir eventos JSON a consola.