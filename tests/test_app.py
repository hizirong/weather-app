import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}

def test_weather_endpoint(client, requests_mock):
    """Test weather endpoint with mocked API response"""
    # Mock the external API call
    mock_response = {
        "main": {"temp": 20, "humidity": 50},
        "weather": [{"description": "clear sky"}]
    }
    requests_mock.get("http://api.openweathermap.org/data/2.5/weather", json=mock_response)
    
    response = client.get('/weather/taipei')
    assert response.status_code == 200
    data = response.get_json()
    assert "temperature" in data
    assert "description" in data