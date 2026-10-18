import pytest

from config import Config, DevelopmentConfig, TestingConfig, get_config

# --- choosing the configuration ---

def test_production_config_by_name():
    assert get_config("Production") == Config


def test_development_config_by_name():
    assert get_config("Development") == DevelopmentConfig


def test_testing_config_by_name():
    assert get_config("Testing") == TestingConfig


def test_config_is_read_from_app_env(monkeypatch):
    monkeypatch.setenv("APP_ENV", "Development")
    assert get_config() == DevelopmentConfig


def test_default_config_is_production(monkeypatch):
    monkeypatch.delenv("APP_ENV", raising=False)
    assert get_config() == Config


def test_unknown_config_name_is_an_error():
    with pytest.raises(KeyError):
        get_config("Staging")


# --- settings in each configuration ---

def test_production_has_debug_off():
    assert Config.DEBUG is False


def test_production_has_csrf_on():
    assert Config.WTF_CSRF_ENABLED is True


def test_production_has_a_secret_key():
    assert Config.SECRET_KEY


def test_testing_has_csrf_off():
    assert TestingConfig.WTF_CSRF_ENABLED is False
