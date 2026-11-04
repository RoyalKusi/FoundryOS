"""HR Productivity Engine (B5 squad) — weekly Workforce Report + propose_role_change."""
from __future__ import annotations
import structlog
logger = structlog.get_logger(__name__)

async def assess_productivity(company_id: str) -> dict:
    # Mock metrics — in prod: compute from tasks/agent_runs/kpi_snapshots
    return {
        "company_id": company_id,
        "period": "2026-W18",
        "metrics": {"throughput": 12, "on_time": 0.85, "kpi_movement": 0.12, "approval_accept": 0.9},
        "roles": [{"role_id": "ops-1", "health": "green"}, {"role_id": "sales-1", "health": "amber"}],
        "proposals": [],
    }

async def workforce_report(company_id: str) -> dict:
    report = await assess_productivity(company_id)
    logger.info("workforce_report", company_id=company_id, health=report["metrics"])
    return report
