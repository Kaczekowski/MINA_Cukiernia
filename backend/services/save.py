from datetime import datetime, timezone

from backend.models.player import Player
from backend.models.player_upgrade import PlayerUpgrade
from backend.models.stats import Stats
from sqlmodel import Session, select


def get_or_create_player(db: Session):
    player = db.exec(select(Player)).first()

    if player:
        return player

    player = Player()

    db.add(player)
    db.commit()
    db.refresh(player)

    stats = Stats(player_id=player.id)

    db.add(stats)
    db.commit()

    return player


def get_stats(db: Session):
    return db.exec(select(Stats)).first()


def read_save(db: Session):
    player = get_or_create_player(db)
    stats = get_stats(db)
    return player, stats


def save_game(db: Session, data):
    player = get_or_create_player(db)

    player.money = data.money
    player.total_clicks = data.total_clicks
    player.cookies_per_second = data.cookies_per_second

    db.add(player)

    stats = get_stats(db)
    if stats is None:
        stats = Stats(player_id=player.id)

    stats.total_money_earned = data.total_money_earned
    stats.total_upgrades_bought = data.total_upgrades_bought
    stats.play_time_seconds = data.play_time_seconds
    stats.last_save = datetime.now(timezone.utc)

    db.add(stats)
    db.commit()
    db.refresh(player)

    return player, stats


def reset_save(db: Session):
    player = db.exec(select(Player)).first()

    if player:
        stats = get_stats(db)
        if stats:
            db.delete(stats)
            db.commit()

        upgrades = db.exec(
            select(PlayerUpgrade).where(PlayerUpgrade.player_id == player.id)
        ).all()
        for upgrade in upgrades:
            db.delete(upgrade)
        db.commit()

        db.delete(player)
        db.commit()

    new_player = Player()
    db.add(new_player)
    db.commit()
    db.refresh(new_player)

    new_stats = Stats(player_id=new_player.id)
    db.add(new_stats)

    db.commit()

    return {"message": "reset"}
