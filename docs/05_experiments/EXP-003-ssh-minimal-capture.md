## Resultados observados

El honeypot SSH aceptó conexiones reales y generó eventos estructurados alineados con `event_schema_v1`.

Se observaron eventos:

- ssh.session_start
- ssh.auth_attempt
- ssh.auth_result
- ssh.connection_closed

## Evidencia

Salida de consola del honeypot durante conexión SSH local.

## Conclusión

Se valida que el sensor SSH es capaz de producir eventos consistentes, estructurados y compatibles con el contrato definido, habilitando la siguiente fase de integración con el broker de mensajería.