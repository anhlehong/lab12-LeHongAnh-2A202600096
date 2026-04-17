#!/bin/bash
source /home/anhle/vinuni/week_03/Day12/day12_ha-tang-cloud_va_deployment/01-localhost-vs-production/develop/.venv/bin/activate
cd /home/anhle/vinuni/week_03/Day12/day12_ha-tang-cloud_va_deployment/05-scaling-reliability/production
fuser -k 8000/tcp || true
python app.py > app.log 2>&1 &
PID=$!
sleep 5
echo "Running test_stateless.py..."
python test_stateless.py
echo "Stopping app..."
kill -TERM $PID
wait $PID || true
echo "App logs:"
cat app.log
