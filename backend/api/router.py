from fastapi import APIRouter
from backend.api.enpoints.save import router as save_router
from backend.api.enpoints.game import router as game_router

router = APIRouter()
router.include_router(save_router)
router.include_router(game_router)
