def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "POS API is running"}


def test_openapi_available(client):
    response = client.get("/openapi.json")
    assert response.status_code == 200
