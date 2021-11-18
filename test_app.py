from app import app

def test_default_route():
    response = app.test_client().get('/')

    assert response.status_code == 200