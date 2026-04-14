# EXP-007 — Basic Fingerprinting V1

## Objetivo

Construir una primera representación compacta del comportamiento de cada sesión SSH a partir de `session_features`.

## Hipótesis técnica

Si las features estadísticas, estructurales y temporales ya fueron calculadas correctamente, entonces es posible combinarlas en un `fp_vector` reproducible y asignar etiquetas interpretables preliminares.

## Componentes involucrados

- `session_features`
- Script `build_fingerprints.py`
- Columnas `fp_vector` y `fingerprint_label`

## Procedimiento

1. Leer filas de `session_features`
2. Construir vector numérico ordenado
3. Asignar etiqueta preliminar por reglas
4. Persistir `fp_vector` y `fingerprint_label`

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

Realizar EDA sobre `session_features` y `fp_vector` antes de aplicar modelos de anomalía.