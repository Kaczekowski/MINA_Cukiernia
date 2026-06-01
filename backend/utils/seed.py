from sqlmodel import Session, select
from backend.db.session import engine
from backend.models.upgrade import Upgrade


UPGRADES = [
    Upgrade(
        name="Łyżka",
        description="Zwykła łyżka do mieszania",
        base_cost=50,
        cost_scaling=1.15,
        click_bonus=1.0,
        income_per_second=0.0,
        icon="🥄",
    ),
    Upgrade(
        name="Mikser",
        description="Elektryczny mikser",
        base_cost=125,
        cost_scaling=1.15,
        click_bonus=0.0,
        income_per_second=1.0,
        icon="🔌",
    ),
    Upgrade(
        name="Piekarnik",
        description="Nagrzany do 180°C",
        base_cost=400,
        cost_scaling=1.15,
        click_bonus=5.0,
        income_per_second=0.0,
        icon="🔥",
    ),
    Upgrade(
        name="Babcia",
        description="Babcia piecze całą dobę",
        base_cost=1000,
        cost_scaling=1.15,
        click_bonus=0.0,
        income_per_second=6.0,
        icon="👵",
    ),
    Upgrade(
        name="Ania Gotuje",
        description="Influencerka od wypieków",
        base_cost=3500,
        cost_scaling=1.15,
        click_bonus=50.0,
        income_per_second=0.0,
        icon="👩‍🍳",
    ),
    Upgrade(
        name="Cukiernik",
        description="Profesjonalny cukiernik",
        base_cost=10000,
        cost_scaling=1.15,
        click_bonus=0.0,
        income_per_second=100.0,
        icon="🎂",
    ),
    Upgrade(
        name="Linia Produkcyjna",
        description="Taśma ciast non-stop",
        base_cost=50000,
        cost_scaling=1.15,
        click_bonus=400.0,
        income_per_second=0.0,
        icon="🏭",
    ),
    Upgrade(
        name="Fabryka Ciast",
        description="Całodobowa fabryka",
        base_cost=400000,
        cost_scaling=1.15,
        click_bonus=0.0,
        income_per_second=1000.0,
        icon="🏗️",
    ),
    Upgrade(
        name="Korporacja Cukiernicza",
        description="Sieć cukierni na cały kraj",
        base_cost=1000000,
        cost_scaling=1.15,
        click_bonus=2000.0,
        income_per_second=0.0,
        icon="🏢",
    ),
    Upgrade(
        name="Ciasto-Bóstwo",
        description="Transcendentna moc wypieków",
        base_cost=2500000,
        cost_scaling=1.15,
        click_bonus=0.0,
        income_per_second=5000.0,
        icon="✨",
    ),
]


def seed_upgrades():
    with Session(engine) as db:
        existing = db.exec(select(Upgrade)).all()
        if existing:
            print("Upgrady już istnieją, pomijam seed.")
            return

        for upgrade in UPGRADES:
            db.add(upgrade)
        db.commit()
        print(f"Dodano {len(UPGRADES)} upgradów.")


if __name__ == "__main__":
    import backend.models.player  # noqa
    import backend.models.stats  # noqa
    import backend.models.upgrade  # noqa
    import backend.models.player_upgrade  # noqa
    from sqlmodel import SQLModel

    SQLModel.metadata.create_all(engine)
    seed_upgrades()
