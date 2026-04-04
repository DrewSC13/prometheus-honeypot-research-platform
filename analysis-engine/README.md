# Analysis Engine

Motor analítico inicial de Prometheus.

## Responsabilidades iniciales

- Validación de eventos contra el contrato lógico del sistema
- Deserialización de ejemplos
- Base para agregación, features y fingerprinting

## Entorno

Crear entorno virtual e instalar dependencias:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt