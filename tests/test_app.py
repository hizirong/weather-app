import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# def test_health_check(client):
#     """Test health check endpoint"""
#     response = client.get('/health')
#     assert response.status_code == 200
#     assert response.get_json() == {"status": "healthy"}

# def test_weather_endpoint(client, requests_mock):
#     """Test weather endpoint with mocked API response"""
#     # 完整的 mock response
#     mock_response = {
#         "main": {
#             "temp": 20,
#             "humidity": 50
#         },
#         "weather": [
#             {
#                 "description": "clear sky",
#                 "icon": "01d"
#             }
#         ],
#         "wind": {
#             "speed": 5.0
#         }
#     }

#     # 在测试环境中设置 API key
#     app.config['WEATHER_API_KEY'] = 'test_api_key'

#     # Mock the API call
#     requests_mock.get(
#         'http://api.openweathermap.org/data/2.5/weather',
#         json=mock_response,
#         complete_qs=False  # 不要求完全匹配 query string
#     )

#     response = client.get('/weather/taipei')
    
#     # 如果失敗，印出錯誤訊息
#     if response.status_code != 200:
#         print(response.get_json())
    
#     assert response.status_code == 200
#     data = response.get_json()
#     assert data['city'] == 'taipei'
#     assert data['temperature'] == 20
#     assert data['description'] == 'clear sky'
#     assert data['humidity'] == 50
#     assert data['wind_speed'] == 5.0
#     assert data['icon'] == '01d'

def test_forecast_endpoint(client, requests_mock):
    """Test forecast endpoint with mocked API response"""
    # 完整的 mock response
    mock_response = {
        "list": [
            {
                "dt_txt": "2023-01-01 12:00:00",
                "main": {
                    "temp": 20,
                    "humidity": 50
                },
                "weather": [
                    {
                        "description": "clear sky",
                        "icon": "01d"
                    }
                ]
            },
            {
                "dt_txt": "2023-01-02 12:00:00",
                "main": {
                    "temp": 22,
                    "humidity": 55
                },
                "weather": [
                    {
                        "description": "few clouds",
                        "icon": "02d"
                    }
                ]
            }
        ]
    }

    # 在测试环境中设置 API key
    app.config['WEATHER_API_KEY'] = 'test_api_key'

    # Mock the API call
    requests_mock.get(
        'http://api.openweathermap.org/data/2.5/forecast',
        json=mock_response,
        complete_qs=False
    )

    response = client.get('/forecast/taipei')
    
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) > 0
    assert 'date' in data[0]
    assert 'temp' in data[0]
    assert 'humidity' in data[0]

def test_historical_endpoint(client, requests_mock):
    """Test historical endpoint with mocked API response"""
    # 使用跟当前天气相同的 mock 数据，因为我们的历史数据是基于当前天气生成的
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

    # 在测试环境中设置 API key
    app.config['WEATHER_API_KEY'] = 'test_api_key'

    # Mock the API call
    requests_mock.get(
        'http://api.openweathermap.org/data/2.5/weather',
        json=mock_response,
        complete_qs=False
    )

    response = client.get('/historical/taipei')
    
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 7  # 过去7天
    assert 'date' in data[0]
    assert 'temp' in data[0]
    assert 'humidity' in data[0]