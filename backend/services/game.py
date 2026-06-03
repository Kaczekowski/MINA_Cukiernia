from sqlmodel import Session, select

from backend.models.player import Player
from backend.models.player_upgrade import PlayerUpgrade
from backend.models.upgrade import Upgrade
from backend.services.save import get_or_create_player


def get_click_value(player: Player, db: Session) -> float:
    """Bazowa wartość kliknięcia to 1, plus bonusy z ulepszeń."""
    base = 1.0
    upgrades = db.exec(
        select(PlayerUpgrade).where(PlayerUpgrade.player_id == player.id)
    ).all()
    bonus = 0.0

    for player_upgrade in upgrades:
        upgrade = db.get(Upgrade, player_upgrade.upgrade_id)
        if upgrade is not None:
            bonus += upgrade.click_bonus * player_upgrade.quantity

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


def handle_tick(db: Session):
    """Dodaje automatyczny przychód wynikający z CPS."""
    player = get_or_create_player(db)
    player.money += player.cookies_per_second
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
    """Przelicza cookies_per_second na podstawie wszystkich ulepszeń gracza."""
    all_upgrades = db.exec(
        select(PlayerUpgrade).where(PlayerUpgrade.player_id == player.id)
    ).all()

    merged = {pu.upgrade_id: pu.quantity for pu in all_upgrades}
    merged[updated.upgrade_id] = updated.quantity

    total = 0.0
    for upgrade_id, quantity in merged.items():
        upgrade = db.get(Upgrade, upgrade_id)
        if upgrade:
            total += upgrade.income_per_second * quantity
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
    for upgrade in upgrades:
        quantity = owned.get(upgrade.id, 0)
        result.append(
            {
                "id": upgrade.id,
                "name": upgrade.name,
                "description": upgrade.description,
                "icon": upgrade.icon,
                "base_cost": upgrade.base_cost,
                "cost_scaling": upgrade.cost_scaling,
                "income_per_second": upgrade.income_per_second,
                "click_bonus": upgrade.click_bonus,
                "current_cost": compute_upgrade_cost(upgrade, quantity),
                "quantity": quantity,
            }
        )
    return result
