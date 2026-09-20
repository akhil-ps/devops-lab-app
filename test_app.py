from app import app

def test_home():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert response.json["status"] == "healthy"

def test_health():
    client = app.test_client()
    response = client.get('/healthz')
    assert response.status_code == 200
    assert response.json["status"] == "ok"
