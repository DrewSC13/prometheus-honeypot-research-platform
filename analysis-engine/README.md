# Analysis Engine

Motor analítico inicial de Prometheus.

## Responsabilidades iniciales

- Validación de eventos contra el contrato lógico del sistema
- Deserialización de ejemplos
- Consumo de eventos desde RabbitMQ
- Persistencia cruda en PostgreSQL
- Base para agregación, features y fingerprinting

## Entorno

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

## Fingerprinting v1

```bash
python -m app.fingerprinting.build_fingerprints