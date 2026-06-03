from pydantic import BaseModel


class ClickOut(BaseModel):
    money: float
    total_clicks: int
    cookies_per_second: float

    model_config = {"from_attributes": True}


class TickOut(BaseModel):
    money: float
    cookies_per_second: float

    model_config = {"from_attributes": True}


class BuyUpgradeIn(BaseModel):
    upgrade_id: int


class BuyUpgradeOut(BaseModel):
    success: bool
    money: float
    upgrade_id: int
    new_quantity: int
    next_cost: float
    cookies_per_second: float

    model_config = {"from_attributes": True}


class UpgradeOut(BaseModel):
    id: int
    name: str
    description: str
    icon: str
    base_cost: float
    cost_scaling: float
    income_per_second: float
    click_bonus: float
    current_cost: float
    quantity: int

    model_config = {"from_attributes": True}
