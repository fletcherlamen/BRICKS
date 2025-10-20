#!/bin/bash
# Quick coverage generation script
# Runs tests in parallel and generates coverage report

echo "🚀 Running fast coverage analysis..."

cd /app

# Run tests with minimal output, parallel execution
pytest \
  --cov=app \
  --cov-report=json \
  --cov-report=term-missing:skip-covered \
  --tb=no \
  -q \
  -n auto \
  --maxfail=5 \
  --timeout=10 \
  2>&1 | grep -E "passed|failed|TOTAL"

# Generate summary
if [ -f coverage.json ]; then
    python3 -c "
import json
with open('coverage.json') as f:
    data = json.load(f)
    total = data['totals']
    print(f'\n📊 COVERAGE SUMMARY')
    print(f'   Lines Covered: {total[\"covered_lines\"]}/{total[\"num_statements\"]}')
    print(f'   Coverage: {total[\"percent_covered\"]:.1f}%')
    print(f'   Target: 80%')
    print(f'   Gap: {80 - total[\"percent_covered\"]:.1f}%')
"
fi

echo "✅ Coverage report generated: coverage.json"

