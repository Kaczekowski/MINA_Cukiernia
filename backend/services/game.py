from sqlmodel import Session, select

from backend.models.player import Player
from backend.models.player_upgrade import PlayerUpgrade
from backend.models.upgrade import Upgrade
from backend.services.save import get_or_create_player


def get_click_value(player: Player, db: Session) -> float:
    """Bazowa wartość kliknięcia to 1, plus bonusy z ulepszeni."""
    base = 1.0
    upgrades = db.exec(
        select(PlayerUpgrade).where(PlayerUpgrade.player_id == player.id)
    ).all()
    bonus = sum(
        db.get(Upgrade, pu.upgrade_id).click_bonus * pu.quantity
        for pu in upgrades
        if db.get(Upgrade, pu.upgrade_id) is not None
    )
    return base + bonus


def handle_click(db: Session):
    player = get_or_create_player(db)
    click_value = get_click_value(player, db)
    player.money += click_value
    player.total_clicks += 1
    db.add(player)
    db.commit()
    db.refresh(player)
    return player


def compute_upgrade_cost(upgrade: Upgrade, quantity: int) -> float:
    """Cena rośnie wykładniczo: base_cost * scaling ^ quantity."""
    return upgrade.base_cost * (upgrade.cost_scaling**quantity)


def buy_upgrade(db: Session, upgrade_id: int):
    player = get_or_create_player(db)

    upgrade = db.get(Upgrade, upgrade_id)
    if upgrade is None:
        raise ValueError(f"Upgrade {upgrade_id} nie istnieje")

    player_upgrade = db.exec(
        select(PlayerUpgrade).where(
            PlayerUpgrade.player_id == player.id,
            PlayerUpgrade.upgrade_id == upgrade_id,
        )
    ).first()

    current_qty = player_upgrade.quantity if player_upgrade else 0
    cost = compute_upgrade_cost(upgrade, current_qty)

    if player.money < cost:
        return {
            "success": False,
            "money": player.money,
            "upgrade_id": upgrade_id,
            "new_quantity": current_qty,
            "next_cost": cost,
            "cookies_per_second": player.cookies_per_second,
        }

    player.money -= cost

    if player_upgrade:
        player_upgrade.quantity += 1
    else:
        player_upgrade = PlayerUpgrade(
            player_id=player.id, upgrade_id=upgrade_id, quantity=1
        )

    player.cookies_per_second = _recalc_cps(player, db, player_upgrade)

    db.add(player)
    db.add(player_upgrade)
    db.commit()
    db.refresh(player)
    db.refresh(player_upgrade)

    next_cost = compute_upgrade_cost(upgrade, player_upgrade.quantity)

    return {
        "success": True,
        "money": player.money,
        "upgrade_id": upgrade_id,
        "new_quantity": player_upgrade.quantity,
        "next_cost": next_cost,
        "cookies_per_second": player.cookies_per_second,
    }


def _recalc_cps(player: Player, db: Session, updated: PlayerUpgrade) -> float:
    """Przelicza cookies_per_second na podstawie wszystkich ulepszeni gracza."""
    all_upgrades = db.exec(
        select(PlayerUpgrade).where(PlayerUpgrade.player_id == player.id)
    ).all()

    # Podmień zaktualizowany rekord w liście (przed commitem)
    merged = {pu.upgrade_id: pu.quantity for pu in all_upgrades}
    merged[updated.upgrade_id] = updated.quantity

    total = 0.0
    for uid, qty in merged.items():
        upg = db.get(Upgrade, uid)
        if upg:
            total += upg.income_per_second * qty
    return total


def list_upgrades(db: Session):
    player = get_or_create_player(db)
    upgrades = db.exec(select(Upgrade)).all()

    owned = {
        pu.upgrade_id: pu.quantity
        for pu in db.exec(
            select(PlayerUpgrade).where(PlayerUpgrade.player_id == player.id)
        ).all()
    }

    result = []
    for upg in upgrades:
        qty = owned.get(upg.id, 0)
        result.append(
            {
                "id": upg.id,
                "name": upg.name,
                "description": upg.description,
                "icon": upg.icon,
                "base_cost": upg.base_cost,
                "cost_scaling": upg.cost_scaling,
                "income_per_second": upg.income_per_second,
                "click_bonus": upg.click_bonus,
                "current_cost": compute_upgrade_cost(upg, qty),
                "quantity": qty,
            }
        )
    return result
