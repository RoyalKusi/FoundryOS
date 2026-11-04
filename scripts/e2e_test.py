#!/usr/bin/env python3
"""FoundryOS E2E Test — structure + contracts + UI + mock flow"""
import sys
from pathlib import Path
ROOT = Path(__file__).parent.parent
PASS=FAIL=TOTAL=0
def check(name, fn):
    global PASS, FAIL, TOTAL
    TOTAL+=1
    print(f"\n▶ {name}")
    try:
        fn(); print(f"  ✅ PASS: {name}"); PASS+=1
    except Exception as e:
        print(f"  ❌ FAIL: {name} — {e}"); FAIL+=1

def test_structure():
    req=["app/pubspec.yaml","app/lib/main.dart","app/lib/router.dart","app/lib/widgets/app_logo.dart","app/assets/branding/foundry_logo_primary.svg","backend/app/main.py","backend/app/llm/gateway.py","supabase/migrations/00001_initial.sql","docs/CONTRACTS.md"]
    for f in req: assert (ROOT/f).exists(), f"Missing {f}"

def test_pubspec():
    c=(ROOT/"app/pubspec.yaml").read_text()
    assert "foundryos_app" in c and "go_router" in c and "flutter_launcher_icons" in c

def test_tokens():
    c=(ROOT/"app/lib/theme/app_colors.dart").read_text()
    assert "0xFF4F46E5" in c and "0xFF7C74FF" in c

def test_logo():
    s=(ROOT/"app/assets/branding/foundry_logo_primary.svg").read_text()
    assert "<svg" in s and "#4F46E5" in s and "linearGradient" in s

def test_router():
    r=(ROOT/"app/lib/router.dart").read_text()
    assert r.count("StatefulShellBranch")==5 and "/company" in r

def test_gateway():
    g=(ROOT/"backend/app/llm/gateway.py").read_text()
    assert "MockLLM" in g and "1024" in g

def test_contracts():
    c=(ROOT/"docs/CONTRACTS.md").read_text()
    assert "/genesis" in c and "idea" in c

def test_models():
    d=ROOT/"backend/app/db/models"
    for m in ["company.py","charter.py","role.py","thread.py","message.py","task.py","approval.py"]:
        assert (d/m).exists()
        assert "company_id" in (d/m).read_text() or "CompanyScoped" in (d/m).read_text()

def test_migration():
    s=(ROOT/"supabase/migrations/00001_initial.sql").read_text()
    assert "1024" in s and "company_id" in s

def test_ci():
    assert "flutter build apk" in (ROOT/".github/workflows/build-apk.yml").read_text()

def test_screens():
    for kw in ["Good morning, Founder","Welcome to FoundryOS"]:
        found=any(kw in f.read_text() for f in (ROOT/"app/lib/features").rglob("*.dart"))
        assert found, kw

def test_security():
    assert "JWT" in (ROOT/"backend/app/core/security.py").read_text() or "jwt" in (ROOT/"backend/app/core/security.py").read_text().lower()

if __name__=="__main__":
    print("="*50); print("FoundryOS E2E Test")
    for n,f in [("Structure",test_structure),("Pubspec",test_pubspec),("Tokens",test_tokens),("Logo SVG",test_logo),("Router 5-tab",test_router),("Gateway Mock",test_gateway),("Contracts",test_contracts),("DB Models",test_models),("Migration",test_migration),("CI",test_ci),("Screens",test_screens),("Security",test_security)]:
        check(n,f)
    print(f"\nResults: {PASS}/{TOTAL} passed, {FAIL} failed")
    if FAIL==0: print("✅ All E2E passed")
    sys.exit(FAIL)
