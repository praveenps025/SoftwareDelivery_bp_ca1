import pytest

from config import Config, DevelopmentConfig, TestingConfig, get_config


@pytest.mark.parametrize("name, expected", [
    ("Production", Config),
    ("Development", DevelopmentConfig),
    ("Testing", TestingConfig),
])
def test_get_config_by_name(name, expected):
    assert get_config(name) is expected


def test_get_config_reads_app_env(monkeypatch):
    monkeypatch.setenv("APP_ENV", "Development")
    assert get_config() is DevelopmentConfig


def test_get_config_defaults_to_production(monkeypatch):
    monkeypatch.delenv("APP_ENV", raising=False)
    assert get_config() is Config


def test_unknown_environment_raises():
    with pytest.raises(KeyError):
        get_config("Staging")


def test_production_is_safe():
    assert Config.DEBUG is False and Config.WTF_CSRF_ENABLED is True
    assert Config.SECRET_KEY


def test_testing_disables_csrf_only_for_tests():
    assert TestingConfig.TESTING is True and TestingConfig.WTF_CSRF_ENABLED is False
