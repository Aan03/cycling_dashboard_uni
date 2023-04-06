import os
import pathlib
import secrets

basedir = os.path.abspath(os.path.dirname(__file__))
basedir_pathlib = pathlib.Path(__file__).parent

secret_key = secrets.token_urlsafe(16)
print("\nSecret key for session:\n" + secret_key + "\n")


class Config:
    """Base config for all environments"""
    # Never put SECRET_KEY in GitHub for a deployed app!
    SECRET_KEY = secret_key
    SQLALCHEMY_DATABASE_URI = (
        'sqlite:///' + os.path.join(basedir, "data/cycle_parking.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    JSONIFY_PRETTYPRINT_REGULAR = True


class TestConfig(Config):
    """Test environment config"""
    SQLALCHEMY_DATABASE_URI = (
        'sqlite:///' + os.path.join(basedir_pathlib.parent, "tests/test.db")
    )
    TESTING = True
    SQLALCHEMY_ECHO = True


class TestSeleniumConfig(Config):
    """Test environment config"""
    SQLALCHEMY_DATABASE_URI = (
        'sqlite:///' + os.path.join(basedir_pathlib.parent,
                                    "tests/test_selenium.db")
    )
    TESTING = True
    SQLALCHEMY_ECHO = True
