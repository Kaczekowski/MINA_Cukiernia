from sqlmodel import SQLModel, Field
from datetime import datetime, timezone


class Stats(SQLModel, table=True):
    __tablename__ = "stats"

    id: int | None = Field(default=None, primary_key=True)

    player_id: int = Field(foreign_key="player.id")

    total_money_earned: float = 0.0
    total_upgrades_bought: int = 0
    play_time_seconds: int = 0

    last_save: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
