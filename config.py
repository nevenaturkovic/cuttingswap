import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "hard to guess string"
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.googlemail.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", "587"))
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "true").lower() in [
        "true",
        "on",
        "1",
    ]
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    CUTTINGSWAP_MAIL_SUBJECT_PREFIX = "[CuttingSwap]"
    CUTTINGSWAP_MAIL_SENDER = "CuttingSwap Admin <cuttingswap@example.com>"
    CUTTINGSWAP_ADMIN = os.environ.get("CUTTINGSWAP_ADMIN")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CUTTINGSWAP_POSTS_PER_PAGE = 20
    CUTTINGSWAP_FOLLOWERS_PER_PAGE = 50
    CUTTINGSWAP_COMMENTS_PER_PAGE = 30
    MAX_CONTENT_LENGTH = (
        int(os.environ.get("MAX_CONTENT_LENGTH"))
        if os.environ.get("MAX_CONTENT_LENGTH")
        else 15 * 1024 * 1024
    )
    UPLOAD_EXTENSIONS = (
        set(os.environ.get("UPLOAD_EXTENSIONS").split(";"))
        if os.environ.get("UPLOAD_EXTENSIONS")
        else {
            ".jpg",
            ".jpeg",
            ".png",
            ".gif",
        }
    )
    UPLOAD_PATH = os.environ.get("UPLOAD_PATH") or "uploads"

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DEV_DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "data-dev.sqlite")


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("TEST_DATABASE_URL") or "sqlite://"
    )


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "data.sqlite")


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
