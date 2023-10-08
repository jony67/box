from fastapi.testclient import TestClient
from backend.app.api import app
#from backend.settings import settings
# Отладка
from backend.settings_dev import settings

def test_answer():
    client = TestClient(app)
    result = client.get(settings.main_url)
    assert result.status_code == 200
    assert result.json() == {
        "status":"Ok"
    }