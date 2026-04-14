# EXP-009 — Anomaly Review V1

## Objetivo

Construir una capa de revisión explicable para sesiones marcadas como anómalas por el modelo `IsolationForest`.

## Hipótesis técnica

Si las sesiones anómalas presentan desviaciones claras respecto al baseline del dataset, entonces es posible identificar variables dominantes y generar explicaciones simples sin necesidad de SHAP en esta etapa.

## Componentes involucrados

- tabla `anomalies`
- tabla `session_features`
- script `anomaly_review.py`

## Procedimiento

1. Leer sesiones y scores de anomalía
2. Calcular medias globales del dataset
3. Comparar cada anomalía con el baseline
4. Rankear variables dominantes por desviación
5. Emitir resumen explicable por sesión

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

Incorporar explicabilidad más avanzada o construir una TUI mínima para visualizar sesiones, fingerprints y anomalías.