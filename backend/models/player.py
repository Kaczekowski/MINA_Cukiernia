from sqlmodel import SQLModel, Field


class Player(SQLModel, table=True):
    __tablename__ = "player"

    id: int | None = Field(default=None, primary_key=True)

    money: float = 0.0
    total_clicks: int = 0
    cookies_per_second: float = 0.0
