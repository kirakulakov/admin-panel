from typing import Generator

import pytest
from starlette.testclient import TestClient

from src.api.app import app
from src.core.config import settings, Settings


@pytest.fixture(scope="session")
def _override_settings() -> settings:
    overrided_settings = Settings(_env_file='.env_test')

    for key, value in overrided_settings.model_dump().items():
        setattr(settings, key, value)

    return settings


@pytest.fixture(scope="session")
def _settings(_override_settings) -> settings:
    return settings


@pytest.fixture(scope="session")
def _app(_settings) -> app:
    return app


@pytest.fixture(scope="session")
def client(_app) -> Generator:
    with TestClient(_app) as client:
        yield client
