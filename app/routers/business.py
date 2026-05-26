from fastapi import APIRouter, Depends

from app.dependencies import require_permission

router = APIRouter(prefix="/business", tags=["business"])


@router.get("/documents")
async def get_documents(_=Depends(require_permission("documents:read"))) -> list:
    return [{"id": 1, "name": "Document 1"}]


@router.get("/reports")
async def get_reports(_=Depends(require_permission("reports:read"))) -> list:
    return [{"id": 1, "name": "Report 1"}]


@router.get("/orders")
async def get_orders(_=Depends(require_permission("orders:read"))) -> list:
    return [{"id": 1, "name": "Order 1"}]
