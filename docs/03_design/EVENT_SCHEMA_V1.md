# EVENT_SCHEMA_V1

## 1. Propósito

Este documento define el contrato formal de eventos `event_schema_v1` para el sistema Prometheus.

Su propósito es establecer un lenguaje común, estable y reproducible entre los componentes de captura implementados en Rust y los componentes analíticos implementados en Python.

## 2. Rol del contrato dentro del sistema

El contrato de eventos constituye la base de interoperabilidad del pipeline orientado a eventos:

Honeypot SSH/HTTP → RabbitMQ → Consumer Python → PostgreSQL → Agregación → Fingerprinting → ML → TUI

Sin un contrato estable, no es posible garantizar validación consistente, persistencia reproducible ni reconstrucción correcta de sesiones.

## 3. Principios de diseño

### 3.1 Estabilidad estructural
Todos los eventos comparten un envoltorio común con campos obligatorios bien definidos.

### 3.2 Especialización semántica
El contenido de `payload` depende del `event_type`.

### 3.3 Versionado explícito
Cada evento incluye el campo `schema_version`, cuyo valor actual es `event_schema_v1`.

### 3.4 Correlación reproducible
El campo `session_id` es obligatorio para permitir reconstrucción de sesiones y unidades analíticas.

### 3.5 Trazabilidad técnica
El campo `metadata` conserva información operativa útil sin alterar el significado principal del evento.

## 4. Campos obligatorios del contrato

| Campo | Tipo | Descripción |
|---|---|---|
| schema_version | string | Versión explícita del contrato |
| event_id | uuid string | Identificador único del evento |
| timestamp | ISO 8601 string | Marca temporal del evento |
| protocol | string | Protocolo observado |
| source_ip | string | IP de origen |
| source_port | integer | Puerto de origen |
| destination_port | integer | Puerto destino |
| session_id | uuid string | Identificador de correlación de sesión |
| event_sequence | integer | Secuencia incremental del evento |
| event_type | string | Tipo semántico del evento |
| payload | object | Carga útil específica del evento |
| metadata | object | Metadatos técnicos |

## 5. Catálogo inicial de eventos SSH

El catálogo inicial SSH, alineado con la fase temprana del proyecto, es:

- `ssh.session_start`
- `ssh.auth_attempt`
- `ssh.auth_result`
- `ssh.connection_closed`

El esquema también contempla eventos futuros:

- `ssh.command_input`
- `ssh.command_executed`
- `ssh.session_end`

## 6. Semántica de eventos iniciales

### 6.1 `ssh.session_start`
Representa el inicio observado de una conexión SSH.

### 6.2 `ssh.auth_attempt`
Representa un intento de autenticación e incluye credenciales o método observado.

### 6.3 `ssh.auth_result`
Representa el resultado del intento de autenticación.

### 6.4 `ssh.connection_closed`
Representa el cierre de conexión, independientemente de autenticación exitosa o no.

## 7. Reglas de validación

1. Todo evento debe incluir `schema_version = event_schema_v1`.
2. Todo evento debe incluir `session_id`.
3. `event_sequence` debe iniciar en 1 y crecer de forma incremental dentro de la sesión.
4. `protocol` debe ser coherente con `event_type`.
5. `payload` debe respetar la estructura definida para el `event_type`.
6. `timestamp` debe emitirse en formato ISO 8601 con zona horaria.
7. `event_id` y `session_id` deben ser UUID válidos.

## 8. Decisiones de diseño

### 8.1 Uso de envoltorio común
Se adopta una estructura uniforme para simplificar emisión, validación, persistencia y análisis.

### 8.2 Separación entre `payload` y `metadata`
`payload` contiene significado analítico; `metadata` contiene trazabilidad técnica.

### 8.3 Versionado en el evento
Aunque el archivo del contrato ya posee versión, se replica esa información dentro del evento persistido para soportar trazabilidad histórica.

## 9. Relación con etapas posteriores

El contrato `event_schema_v1` habilita directamente:

- validación Pydantic en Python,
- persistencia en `events_raw`,
- reconstrucción de sesiones por `session_id`,
- cálculo de features,
- modelado temporal,
- fingerprinting.

## 10. Limitaciones de v1

- El catálogo HTTP aún no está operacionalmente detallado.
- No se imponen restricciones semánticas profundas sobre todos los campos de `metadata`.
- Los eventos avanzados de comandos SSH quedan definidos, pero no necesariamente implementados en la primera iteración del sensor.

## 11. Evolución futura

Toda modificación incompatible deberá producir una nueva versión del contrato, por ejemplo:

- `event_schema_v2`

La versión v1 debe preservarse para compatibilidad histórica y reproducibilidad experimental.