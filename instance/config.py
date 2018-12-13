# /instance/config.py

import os


class Config(object):
    """Parent configuration class."""
    DEBUG = True
    SECRET = os.getenv('SECRET')


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True
    db_url = os.getenv('DATABASE_URL')


class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    DEBUG = True
    TESTING = True
    testdb_url = os.getenv('TESTDATABASE_URL')


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
}
