from db.session import engine, Base
from models import user  # import all your models so they're registered
from models import event
from models import shared_access
from models import EventHistory


def init():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created!")


if __name__ == "__main__":
    init()
