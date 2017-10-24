def get_engine():
    import config

    from sqlalchemy import create_engine

    return create_engine("sqlite:///%s" % config.DB, echo=False)


def create_db():
    from sql.models import Base

    engine = get_engine()

    Base.metadata.create_all(engine)


def get_session():
    from sqlalchemy.orm import sessionmaker
    session = sessionmaker(bind=get_engine())
    return session()
