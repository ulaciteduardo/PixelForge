import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from main import app, db
from models import User
from werkzeug.security import generate_password_hash
from datetime import date

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["WTF_CSRF_ENABLED"] = False

    with app.app_context():
        db.drop_all()
        db.create_all()

        # Crear usuario de prueba
        user = User(
            username="testuser",
            email="test@test.com",
            password_hash=generate_password_hash("1234"),
            fecha_nacimiento=date(2000, 1, 1),
            cambio_contrasennia=False,
            estado=True
        )
        db.session.add(user)
        db.session.commit()

        yield app.test_client()

        db.session.remove()
        db.drop_all()