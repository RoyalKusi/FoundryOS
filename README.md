# FoundryOS — Company Operating System

> Founder → Charter → Org of digital employees → Meetings → Execution Plan. Runs with `LLM_MODE=mock` (no keys) or real Baseten keys.

## Run in <15 min

### Logo
New branding in `docs/branding/LOGO.md` + SVGs in `app/assets/branding/`. Generate PNGs:

```bash
pip install Pillow
python3 scripts/generate_logo.py
python3 scripts/build_icons.py   # creates mipmap + AppIcon set
```

### Quick build APK (one command)

```bash
chmod +x scripts/setup_android.sh
./scripts/setup_android.sh       # generates logo, creates android scaffold if missing, builds APK
# APK at app/build/app/outputs/flutter-apk/app-debug.apk
adb install -r app/build/app/outputs/flutter-apk/app-debug.apk
```

Or manual:

```bash
git clone <repo> && cd FoundryOS
cp .env.example .env          # set BASETEN_API_KEY for live, or keep LLM_MODE=mock
docker compose up --build     # API http://localhost:8000/docs, Redis, worker
# In another terminal:
cd app && flutter pub get && flutter run   # 5-tab shell: Home, Messages, Schedule, Approvals, Company
# Or without docker:
pip install -e backend[dev] && uvicorn app.main:app --reload --app-dir backend
pytest backend/tests -q       # mock LLM, no key needed
./scripts/smoke.sh            # M0 smoke: health, MockLLM charter, migration, flutter
```

CI also builds APK on every push: check Actions → *Build APK + Logo* → download `foundryos-debug-apk`.


- **Backend:** `LLM_MODE=mock` default — gateway returns deterministic charter/resolutions, 1024-dim embeddings, token accounting. Set `LLM_MODE=live` + Baseten keys for real inference.
- **Frontend:** `APP_USE_FAKE_API=true` for FakeApi (no backend) per WS-E.
- **Supabase:** `supabase start` if you have CLI; otherwise `supabase/migrations/00001_initial.sql` has 14 tables + pgvector 1024 + RLS.
- **CI:** `flutter analyze`, `flutter test`, `ruff`, `mypy --strict`, `pytest`, `evals` (recall@8 ≥0.85) on every push.

## Docs

- `docs/MASTER_PROMPT.md` — source of truth (§5 design, §6 Flutter, §7 Backend, §11 M0–M7)
- `docs/STATE.md` — current milestone (M0 Foundation), cycle plan, decisions, risks (kept <300 lines)
- `docs/CONTRACTS.md` — API endpoints, realtime channels, shared enums (WS-A frozen v1)
- `docs/adr/` — ADRs (stack, multitenancy, gateway, milestones)
- `.clinerules/` — standards/design/workflow summaries for Cline

## Architecture

Flutter 5-tab app → FastAPI Core API (REST+SSE) → arq+Redis workers → Supabase Postgres pgvector + Baseten LLM (Maverick/Scout + BGE-M3 + Whisper). Every table `company_id` + RLS, agents via DB only.

See `docs/STATE.md` for progress and `scripts/bootstrap.sh` for full setup.

