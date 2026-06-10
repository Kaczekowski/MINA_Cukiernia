import pytest
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine, delete
from starlette.testclient import TestClient

import backend.db.session as db_module
import backend.utils.seed as seed_module
from backend.db.session import get_db
from backend.main import app
from backend.models.player import Player
from backend.models.player_upgrade import PlayerUpgrade
from backend.models.stats import Stats
from backend.utils.seed import seed_upgrades

_test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


def _override_get_db():
    with Session(_test_engine) as session:
        yield session


@pytest.fixture(scope="session")
def client():
    original_db_engine = db_module.engine
    original_seed_engine = seed_module.engine

    db_module.engine = _test_engine
    seed_module.engine = _test_engine

    SQLModel.metadata.create_all(_test_engine)
    seed_upgrades()

    app.dependency_overrides[get_db] = _override_get_db
    yield TestClient(app, raise_server_exceptions=False)

    app.dependency_overrides.clear()
    SQLModel.metadata.drop_all(_test_engine)
    db_module.engine = original_db_engine
    seed_module.engine = original_seed_engine


@pytest.fixture(autouse=True)
def clean_db():
    with Session(_test_engine) as session:
        session.exec(delete(PlayerUpgrade))
        session.exec(delete(Stats))
        session.exec(delete(Player))
        session.commit()
