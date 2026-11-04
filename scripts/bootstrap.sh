#!/usr/bin/env bash
set -euo pipefail
echo "Bootstrapping FoundryOS..."
cp -n .env.example .env || true
echo "Installing backend deps..."
pip install -e backend[dev] || echo "pip install skipped (no venv)"
echo "docker compose up..."
docker compose up -d --build || echo "docker not available, using supabase local: supabase start"
echo "Done. Run ./scripts/smoke.sh (LLM_MODE=mock) and flutter run in app/"
