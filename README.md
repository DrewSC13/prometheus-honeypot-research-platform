# Prometheus Honeypot Research Platform

Prometheus es una plataforma de investigación aplicada en ciberseguridad orientada al modelado temporal y fingerprinting del comportamiento atacante a partir de eventos capturados por honeypots.

## Objetivo general

Diseñar e implementar un sistema de honeypot orientado a eventos que modele el comportamiento atacante mediante representaciones temporales y fingerprints dinámicos, permitiendo su análisis, comparación, agrupamiento e interpretación en un entorno controlado.

## Alcance inicial

- Honeypot SSH mínimo en Rust
- Arquitectura orientada a eventos
- RabbitMQ como broker de mensajería
- Motor analítico en Python
- Persistencia en PostgreSQL
- TUI en tiempo real
- Modelado temporal y fingerprinting
- Detección de anomalías e interpretabilidad

## Estructura del repositorio

```text
.
├── honeypot-rust/
├── analysis-engine/
├── tui/
├── schemas/
├── docker/
├── scripts/
├── docs/
└── tests/

```

## Estado actual

Fase 1: base reproducible del proyecto.

Documentación base
docs/01_research/ → fundamento científico
docs/02_architecture/ → arquitectura general
docs/03_design/ → diseño técnico y contratos
docs/05_experiments/ → evidencia experimental
docs/07_decisions/ → decisiones arquitectónicas (ADR)
Regla de desarrollo

No se abre una nueva etapa si la anterior no es estable, demostrable y entendible.

Próximos pasos
Definir entorno reproducible con Docker Compose
Levantar PostgreSQL y RabbitMQ
Definir contrato de eventos v1
Implementar honeypot SSH mínimo
Construir pipeline de captura a persistencia

---

## Paso 7: definir la estrategia Git desde ahora

### Ramas
Usa esta convención:

- `main` → estable
- `develop` → integración
- `feat/...` → nuevas funcionalidades
- `fix/...` → correcciones
- `docs/...` → documentación
- `research/...` → análisis, experimentos o documentos metodológicos

### Ejemplos
```bash
git checkout -b develop
git checkout -b docs/bootstrap-project-structure
git checkout -b feat/docker-base-services
git checkout -b docs/event-schema-v1
```

## Inicio rápido
```bash
    1. Copiar variables de entorno:
        cp .env.example .env
    2. Levantar servicios base:
        make up
    3. Verificar estado:
        make check
    4. Ver logs:
        make logs
    5. Apagar entorno:
        make down
```

### PostgreSQL
- Host: `localhost`
- Puerto: definido por `POSTGRES_PORT` en `.env`
- Base de datos: definida por `POSTGRES_DB`
- Usuario: definido por `POSTGRES_USER`

### RabbitMQ
- AMQP: localhost:5672
- Management UI: http://localhost:15672
- Usuario: prometheus
- Contraseña: prometheus_dev_password

### Documentación
- docs/01_research/ → fundamento científico
- docs/02_architecture/ → arquitectura general
- docs/03_design/ → diseño técnico y contratos
- docs/04_setup/ → instalación y entorno local
- docs/05_experiments/ → evidencia experimental
- docs/07_decisions/ → decisiones arquitectónicas (ADR)
