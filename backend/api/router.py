from fastapi import APIRouter
from backend.api.enpoints.save import router as save_router

router = APIRouter()
router.include_router(save_router)
