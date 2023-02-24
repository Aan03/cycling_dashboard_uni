import os
import pathlib
import secrets

basedir = os.path.abspath(os.path.dirname(__file__))
basedir_pathlib = pathlib.Path(__file__).parent
secret_key = secrets.token_urlsafe(16)

class Config(object):
    """Base config for all environments"""

    # Never put SECRET_KEY in GitHub for a deployed app!
    SECRET_KEY = ""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
        basedir, "flask_bp.db"
    )


class ProductionConfig(Config):
    """Production environment config"""

    pass


class DevelopmentConfig(Config):
    """Development environment config"""

    SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    """Test environment config"""

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + str(
        basedir_pathlib.joinpath("flask_bp", "data", "test_db.sqlite")
    )
    TESTING = True
    SQLALCHEMY_ECHO = True
