"""Configuration - replaces appsettings.json, appsettings.Development.json and
the ASPNETCORE_ENVIRONMENT switch from Properties/launchSettings.json."""
import os


class Config:
    # "Production" settings (appsettings.json); ASP.NET Core also defaults to Production
    DEBUG = False
    TESTING = False
    LOG_LEVEL = "INFO"
    # Key for the anti-forgery (CSRF) token. ASP.NET Core generates its Data Protection
    # key automatically; here we read it from the environment or generate one per process.
    SECRET_KEY = os.environ.get("SECRET_KEY") or os.urandom(32)
    WTF_CSRF_ENABLED = True


class DevelopmentConfig(Config):
    # appsettings.Development.json
    DEBUG = True
    LOG_LEVEL = "DEBUG"


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False


CONFIGS = {
    "Production": Config,
    "Development": DevelopmentConfig,
    "Testing": TestingConfig,
}


def get_config(env_name=None):
    # APP_ENV plays the role of ASPNETCORE_ENVIRONMENT
    return CONFIGS[env_name or os.environ.get("APP_ENV", "Production")]
