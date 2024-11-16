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
    # 修正 mock response 格式
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

    # 確保 URL 完全匹配，包含 query parameters
    requests_mock.get(
        requests_mock.ANY,  # 這樣可以匹配任何 URL
        json=mock_response
    )
    
    response = client.get('/weather/taipei')
    assert response.status_code == 200
    
    data = response.get_json()
    expected_fields = ["city", "temperature", "description", "humidity", "wind_speed", "icon"]
    for field in expected_fields:
        assert field in data