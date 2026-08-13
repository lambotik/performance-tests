import os
import pytest

from performance_tests.clients.http.helpers import HTTPClientHelpers


@pytest.fixture
def api_helper():
    """Фикстура создаёт экземпляр HTTPClientHelpers и закрывает его после теста."""
    base_url = os.getenv("API_BASE_URL", "http://localhost:8003")
    api = HTTPClientHelpers(base_url=base_url)
    yield api
    api.close()