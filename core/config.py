import os
import subprocess
from base64 import b64encode

from dotenv import load_dotenv


class Config(object):
    """Parent Configuration Class"""

    env_file = os.path.dirname(os.getcwd()) + "/.env"

    if not os.path.exists(env_file):
        env_file = os.path.join(os.path.abspath("."), ".env")
    key = b64encode(os.urandom(32)).decode("utf-8")

    with open(env_file, "r") as file:
        env_data = file.readlines()

    for line_number, line in enumerate(env_data):
        if line.startswith("APP_KEY="):
            line_split = line.split("=")
            if len(line_split) == 2:
                env_data[line_number] = "APP_KEY={0}\n".format(key)
            break

    with open(env_file, "w") as file:
        file.writelines(env_data)

    load_dotenv(env_file)

    # DB_DATABASE = os.getenv("DB_DATABASE")
    # DB_HOST = os.getenv("DB_HOST")
    # DB_PASSWORD = os.getenv("DB_PASSWORD")
    # DB_USERNAME = os.getenv("DB_USERNAME")
    # DB_PORT = int(os.getenv("DB_PORT"))

    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv("APP_KEY")

    # POSTGRES_INTERNAL = "{0}:{1}@{2}/{3}".format(
    #     DB_USERNAME, DB_PASSWORD, DB_HOST, DB_DATABASE
    # )
    # SQLALCHEMY_DATABASE_URI = "postgres+psycopg2://" + POSTGRES_INTERNAL
    # SQLALCHEMY_BINDS = {"readonly": "postgres+psycopg2://" + POSTGRES_INTERNAL}
    #
    # SQLALCHEMY_RECORD_QUERIES = True
    # SQLALCHEMY_ECHO = True


class DevelopmentConfig(Config):
    """Configurations for Development."""

    DEBUG = True


class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""

    TESTING = True
    # DB_DATABASE = "test_db"
    # POSTGRES_INTERNAL = f"{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{DB_DATABASE}"
    # SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_INTERNAL}"
    # SQLALCHEMY_BINDS = {"readonly": "postgresql://" + POSTGRES_INTERNAL}
    DEBUG = True


class StagingConfig(Config):
    """Configuration for Staging."""

    DEBUG = True


class ProductionConfig(Config):
    """Configuration for Production."""

    DEBUG = False
    TESTING = False


app_config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "staging": StagingConfig,
    "production": ProductionConfig,
}