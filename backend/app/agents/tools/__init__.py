"""Agent tools registry — extensible digital work via company-provided tools.

All digital work goes through allow-listed tools; gated side-effects require approval.
Per §13 Always: approval gate for any external action; never bypass company_id/RLS.
"""

TOOL_ALLOW_LIST: dict[str, str] = {
    # Core — all roles (internal work, no external side effect)
    "search_knowledge": "all",
    "create_task": "all",
    "update_task": "all",
    "post_message": "all",
    "request_approval": "all",
    "draft_document": "all",
    "schedule_meeting": "all",
    "read_kpis": "all",
    "read_calendar": "all",
    # Communication — drafting is free, sending requires approval gate
    "draft_email": "all",
    "send_email": "all",  # gated: requires approval record
    "draft_post": "all",
    "publish_post": "all",  # gated
    "send_message_external": "all",  # gated
    # Documents & files — generation free, sending external gated
    "generate_document": "all",
    "send_document": "all",  # gated: receipts, invoices, contracts, etc.
    "upload_file": "all",
    # Calendar & meetings — arranging is free, external invite gated
    "create_calendar_event": "all",
    "invite_attendees": "all",  # gated
    "arrange_meeting": "all",
    # Adverts & marketing — drafting free, publishing gated + spend gate
    "draft_advert": "all",
    "draft_campaign": "Sales & Marketing",
    "publish_campaign": "Sales & Marketing",  # gated + spend
    "publish_advert": "all",  # gated + spend
    "build_lead_list": "Sales & Marketing",
    # Finance — drafting free, any spend/send/audit gated
    "build_budget": "Finance",
    "forecast_cashflow": "Finance",
    "create_invoice": "Finance",
    "send_invoice": "Finance",  # gated
    "create_receipt": "Finance",
    "send_receipt": "Finance",  # gated
    "run_audit": "Finance",  # internal but sensitive
    "record_transaction": "Finance",
    # HR & Ops
    "assess_productivity": "HR",
    "propose_role_change": "HR",
    "audit_workload": "all",
    # Generic extensible hook — any company-provided tool via Tool Gateway
    # e.g., slack_post, notion_create, hubspot_update, etc. Registered dynamically
    # and validated against this allow-list + approval gates at runtime.
    "call_company_tool": "all",  # gated if tool side-effect == external/spend/delete
}

# Tools that ALWAYS require approval before execution (non-negotiable §3.4 gates)
# Note: request_approval itself is NOT gated — it is the gate enforcer (AUDIT-P2-02 fix).
GATED_TOOLS = {
    "send_email",
    "publish_post",
    "send_message_external",
    "send_document",
    "invite_attendees",
    "publish_campaign",
    "publish_advert",
    "send_invoice",
    "send_receipt",
    "record_transaction",
    "create_calendar_event",  # if external attendees — runtime checks attendee list
    "call_company_tool",  # dynamically checked: if tool metadata says external/spend/delete -> gated
    "propose_role_change",
    "build_budget",  # if triggers spend — runtime checks payload.spend=true
}

# Tool categories for UI/docs
TOOL_CATEGORIES = {
    "core": ["search_knowledge", "create_task", "update_task", "post_message", "request_approval", "draft_document", "schedule_meeting", "read_kpis", "read_calendar"],
    "communication": ["draft_email", "send_email", "draft_post", "publish_post", "send_message_external"],
    "documents": ["generate_document", "send_document", "upload_file"],
    "calendar": ["create_calendar_event", "invite_attendees", "arrange_meeting"],
    "marketing": ["draft_advert", "draft_campaign", "publish_campaign", "publish_advert", "build_lead_list"],
    "finance": ["build_budget", "forecast_cashflow", "create_invoice", "send_invoice", "create_receipt", "send_receipt", "run_audit", "record_transaction"],
    "hr_ops": ["assess_productivity", "propose_role_change", "audit_workload"],
    "extensible": ["call_company_tool"],
}
