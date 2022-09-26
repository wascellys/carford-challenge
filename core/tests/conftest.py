import pytest

from app import create_app, db
from core.models import Owner, Car


@pytest.fixture(scope="module")
def test_app():
    app = create_app
    app.config.from_object("app.config.Config")
    with app.app_context():
        yield app


@pytest.fixture(scope="module")
def test_database():
    db.create_all()
    yield db
    db.session.remove()
    db.drop_all()


@pytest.fixture(scope="module")
def add_owner():
    def _add_owner(name):
        owner = Owner(name=name)
        db.session.add(owner)
        db.session.commit()
        return owner

    return _add_owner

@pytest.fixture(scope="module")
def add_car():
    def _add_car(name, model, color, owner_id):
        car = Car(name=name, model=model, color=color, owner_id=owner_id)
        db.session.add(car)
        db.session.commit()
        return car

    return _add_car

