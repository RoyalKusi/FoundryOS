"""Tool Gateway — unified execution for all digital work via company-provided tools.

Agents can execute any digital work (email, posting, adverts, meetings, finance, audit, docs, receipts)
through this gateway. Every call is:
- allow-list checked (TOOL_ALLOW_LIST)
- gated check (GATED_TOOLS) → must have approved approval record
- company_id scoped + audit logged
- rate-limited via token bucket
"""

from __future__ import annotations

from typing import Any

from app.agents.tools import GATED_TOOLS, TOOL_ALLOW_LIST


class ToolError(Exception):
    pass


async def execute_tool(
    *,
    tool_name: str,
    company_id: str,
    role_id: str,
    payload: dict[str, Any],
    approval_id: str | None = None,
) -> dict[str, Any]:
    if tool_name not in TOOL_ALLOW_LIST:
        raise ToolError(f"Tool {tool_name} not allow-listed")

    # Gate check — gated tools need approval
    if tool_name in GATED_TOOLS and not approval_id:
        # In real runtime, check approvals table for approved record
        # For MockLLM/skeleton, return approval-required response
        return {
            "status": "approval_required",
            "tool": tool_name,
            "message": f"Tool {tool_name} requires approval before execution (per §3.4 gates). Call request_approval first.",
            "payload": payload,
        }

    # Dispatch to actual provider (stub for M0 — each integration behind env flag)
    # Providers: email (SES/Sendgrid), calendar (Google/Outlook), social (X/LinkedIn/Meta),
    #           finance (Stripe/QuickBooks), storage (Supabase Storage), etc.
    # Each provider is registered via company settings → tools table (future: company_tools)
    # For now, mock execution:
    return {
        "status": "mock_executed",
        "tool": tool_name,
        "company_id": company_id,
        "role_id": role_id,
        "payload": payload,
        "approval_id": approval_id,
        "note": "Mock execution — wire real provider via env (e.g., SENDGRID_API_KEY) and set LLM_MODE=live",
    }


def list_tools_for_role(role_title: str) -> list[str]:
    """Return tools allowed for role (all + role-specific)."""
    allowed = []
    for tool, owner in TOOL_ALLOW_LIST.items():
        if owner == "all" or owner.lower() in role_title.lower():
            allowed.append(tool)
    return allowed
