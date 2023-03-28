import os
import pathlib

basedir = os.path.abspath(os.path.dirname(__file__))
basedir_pathlib = pathlib.Path(__file__).parent

class Config(object):
    """Base config for all environments"""
    # Never put SECRET_KEY in GitHub for a deployed app!

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