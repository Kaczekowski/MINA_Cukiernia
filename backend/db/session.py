from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = "sqlite:///./cukiernia.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def get_db():
    with Session(engine) as session:
        yield session


def init_db():
    import backend.models.player  # noqa: F401
    import backend.models.stats  # noqa: F401
    import backend.models.upgrade  # noqa: F401
    import backend.models.player_upgrade  # noqa: F401

    SQLModel.metadata.create_all(engine)
