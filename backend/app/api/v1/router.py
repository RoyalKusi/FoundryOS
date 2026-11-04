from fastapi import APIRouter

from app.api.v1 import (
    approvals,
    agent_runs,
    charters,
    companies,
    documents,
    genesis,
    meetings,
    messages,
    roles,
    search,
    tasks,
    threads,
)

api_router = APIRouter()

api_router.include_router(genesis.router, prefix="/genesis", tags=["genesis"])
api_router.include_router(companies.router, prefix="/companies", tags=["companies"])
api_router.include_router(charters.router, prefix="/charters", tags=["charters"])
api_router.include_router(roles.router, prefix="/roles", tags=["roles"])
api_router.include_router(threads.router, prefix="/threads", tags=["threads"])
api_router.include_router(messages.router, prefix="/messages", tags=["messages"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(meetings.router, prefix="/meetings", tags=["meetings"])
api_router.include_router(approvals.router, prefix="/approvals", tags=["approvals"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(agent_runs.router, prefix="/agent_runs", tags=["agent_runs"])
