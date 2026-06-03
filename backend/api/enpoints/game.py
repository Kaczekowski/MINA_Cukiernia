from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from backend.db.session import get_db
from backend.schemas.game import BuyUpgradeOut, ClickOut, TickOut, UpgradeOut
from backend.services import game as game_service

router = APIRouter(prefix="/game", tags=["game"])


@router.post("/click", response_model=ClickOut)
def click(db: Session = Depends(get_db)):
    player = game_service.handle_click(db)
    return ClickOut(
        money=player.money,
        total_clicks=player.total_clicks,
        cookies_per_second=player.cookies_per_second,
    )


@router.post("/tick", response_model=TickOut)
def tick(db: Session = Depends(get_db)):
    player = game_service.handle_tick(db)
    return TickOut(
        money=player.money,
        cookies_per_second=player.cookies_per_second,
    )


@router.post("/buy/{upgrade_id}", response_model=BuyUpgradeOut)
def buy_upgrade(upgrade_id: int, db: Session = Depends(get_db)):
    try:
        result = game_service.buy_upgrade(db, upgrade_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return BuyUpgradeOut(**result)


@router.get("/upgrades", response_model=list[UpgradeOut])
def list_upgrades(db: Session = Depends(get_db)):
    return game_service.list_upgrades(db)
