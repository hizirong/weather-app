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
    mock_response = {
        "main": {
            "temp": 20,
            "humidity": 50
        },
        "weather": [
            {
                "description": "clear sky",
                "icon": "01d"
            }
        ],
        "wind": {
            "speed": 5.0
        }
    }

    # 修正：使用具體的 URL pattern
    requests_mock.get(
        "http://api.openweathermap.org/data/2.5/weather?q=taipei&appid=*&units=metric",
        json=mock_response
    )
    
    response = client.get('/weather/taipei')
    assert response.status_code == 200
    
    data = response.get_json()
    assert "city" in data
    assert "temperature" in data
    assert "description" in data
    assert "humidity" in data
    assert "wind_speed" in data
    assert "icon" in data