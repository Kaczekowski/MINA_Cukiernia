from sqlmodel import SQLModel, Field


class Upgrade(SQLModel, table=True):
    __tablename__ = "upgrade"

    id: int | None = Field(default=None, primary_key=True)

    name: str
    description: str = ""

    base_cost: float
    cost_scaling: float = 1.15

    income_per_second: float = 0.0
    click_bonus: float = 0.0

    icon: str = "👵"
