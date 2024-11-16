from flask import Flask, jsonify, render_template, request
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# 新增前端頁面路由
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather/<city>')
def get_weather(city):
    api_key = os.getenv('WEATHER_API_KEY')
    if not api_key:
        return jsonify({"error": "API key not configured"}), 500
        
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # 會引發例外如果狀態碼不是 200
        data = response.json()
        
        weather_data = {
            "city": city,
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "icon": data["weather"][0]["icon"]
        }
        return jsonify(weather_data)
    except requests.exceptions.RequestException as e:
        print(f"API Request Error: {str(e)}")  # 加入日誌
        return jsonify({"error": "Error fetching weather data"}), 500
    except KeyError as e:
        print(f"Data Parsing Error: {str(e)}")  # 加入日誌
        return jsonify({"error": "Error parsing weather data"}), 500
    except Exception as e:
        print(f"Unexpected Error: {str(e)}")  # 加入日誌
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)