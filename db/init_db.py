from db.session import engine, Base
from models import user
from models import event
from models import shared_access
from models import event_history


def init():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created!")


if __name__ == "__main__":
    init()
