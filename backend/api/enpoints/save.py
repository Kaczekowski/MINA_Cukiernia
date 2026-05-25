from fastapi import APIRouter, Depends
from sqlmodel import Session

from backend.db.session import get_db
from backend.schemas.save import SaveIn, SaveOut, StatsOut, ResetOut
from backend.services import save as save_service

router = APIRouter(prefix="/save", tags=["save"])


@router.get("/", response_model=SaveOut)
def read_save(db: Session = Depends(get_db)):
    player, stats = save_service.read_save(db)
    return SaveOut(
        id=player.id,
        money=player.money,
        total_clicks=player.total_clicks,
        cookies_per_second=player.cookies_per_second,
        stats=stats,
    )


@router.post("/", response_model=SaveOut)
def save_game(data: SaveIn, db: Session = Depends(get_db)):
    player, stats = save_service.save_game(db, data)
    return SaveOut(
        id=player.id,
        money=player.money,
        total_clicks=player.total_clicks,
        cookies_per_second=player.cookies_per_second,
        stats=stats,
    )


@router.delete("/reset", response_model=ResetOut)
def reset_save(db: Session = Depends(get_db)):
    return save_service.reset_save(db)


@router.get("/stats", response_model=StatsOut)
def read_stats(db: Session = Depends(get_db)):
    return save_service.get_stats(db)
