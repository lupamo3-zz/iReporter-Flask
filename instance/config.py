# /instance/config.py

import os


class Config(object):
    """Parent configuration class."""
    DEBUG = True
    SECRET = os.getenv('SECRET')


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True


class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/test_db'
    DEBUG = True


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
}
