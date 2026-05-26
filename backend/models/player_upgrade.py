from sqlmodel import SQLModel, Field


class PlayerUpgrade(SQLModel, table=True):
    __tablename__ = "player_upgrade"

    id: int | None = Field(default=None, primary_key=True)

    player_id: int = Field(foreign_key="player.id")
    upgrade_id: int = Field(foreign_key="upgrade.id")

    quantity: int = 1
