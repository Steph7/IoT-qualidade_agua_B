#!/bin/bash
# Ativa o ambiente virtual
source /venv/bin/activate

# Roda o primeiro script em segundo plano
python /venv/src/data_processor_agua_v2.py &

# Roda o segundo script
python /venv/src/data_collector_agua_v2.py
