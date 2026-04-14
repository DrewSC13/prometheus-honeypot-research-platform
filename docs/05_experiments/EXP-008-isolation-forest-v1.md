# EXP-008 — Isolation Forest V1

## Objetivo

Aplicar detección de anomalías no supervisada sobre `session_features` ya enriquecidas con temporalidad básica.

## Hipótesis técnica

Si las sesiones contienen diferencias significativas en ritmo, duración e intensidad, entonces un modelo Isolation Forest debería asignar scores distintos y marcar algunas sesiones como más raras que otras.

## Componentes involucrados

- `session_features`
- `StandardScaler`
- `IsolationForest`
- tabla `anomalies`

## Procedimiento

1. Seleccionar features v2
2. Normalizar con `StandardScaler`
3. Entrenar `IsolationForest`
4. Calcular `anomaly_score`
5. Persistir resultados en `anomalies`

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

Añadir interpretabilidad y análisis manual de las sesiones más raras.