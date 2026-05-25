from pydantic import BaseModel


class SaveIn(BaseModel):
    money: float
    total_clicks: int
    cookies_per_second: float
    total_money_earned: float = 0.0
    total_upgrades_bought: int = 0
    play_time_seconds: int = 0


class StatsOut(BaseModel):
    total_money_earned: float
    total_upgrades_bought: int
    play_time_seconds: int

    model_config = {"from_attributes": True}


class SaveOut(BaseModel):
    id: int
    money: float
    total_clicks: int
    cookies_per_second: float
    stats: StatsOut | None = None

    model_config = {"from_attributes": True}


class ResetOut(BaseModel):
    message: str
