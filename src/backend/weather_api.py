"""
Weather API Integration Module
Fetches real-time weather data from OpenWeatherMap
"""

import requests
import os
from typing import Dict, Optional, Tuple
from dotenv import load_dotenv

load_dotenv()
from datetime import datetime, timedelta
import json


class WeatherAPIClient:
    """Client for OpenWeatherMap API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize weather API client
        
        Args:
            api_key: OpenWeatherMap API key (get free at openweathermap.org)
        """
        self.api_key = api_key or os.environ.get('OPENWEATHER_API_KEY')
        
        # Fallback to Streamlit Secrets for cloud deployment
        if not self.api_key:
            try:
                import streamlit as st
                if 'OPENWEATHER_API_KEY' in st.secrets:
                    self.api_key = st.secrets['OPENWEATHER_API_KEY']
                    print("✅ Weather API key loaded from st.secrets")
            except Exception:
                pass

        self.base_url = "https://api.openweathermap.org/data/2.5"
        
        # Cache to avoid hitting rate limits
        self._cache = {}
        self._cache_duration = timedelta(minutes=10)  # Cache for 10 minutes
        
        if not self.api_key:
            print("⚠️  Warning: No API key provided. Using demo mode.")
            print("   Get free API key at: https://openweathermap.org/api")
            self.demo_mode = True
        else:
            self.demo_mode = False
            print("✅ Weather API client initialized")
    
    def get_current_weather(self, city: str, country_code: str = "IN") -> Dict:
        """
        Get current weather for a city
        
        Args:
            city: City name (e.g., "Lucknow")
            country_code: Country code (default: "IN" for India)
            
        Returns:
            Weather data dictionary
        """
        # Check cache first
        cache_key = f"{city}_{country_code}"
        if cache_key in self._cache:
            cached_data, cache_time = self._cache[cache_key]
            if datetime.now() - cache_time < self._cache_duration:
                print(f"📦 Using cached data for {city}")
                return cached_data
        
        if self.demo_mode:
            demo = self._get_demo_weather(city)
            # Cache demo data the same way real data is cached
            self._cache[cache_key] = (demo, datetime.now())
            return demo
        
        try:
            # Build API URL
            url = f"{self.base_url}/weather"
            params = {
                'q': f"{city},{country_code}",
                'appid': self.api_key,
                'units': 'metric'  # Celsius
            }
            
            print(f"🌐 Fetching weather data for {city}...")
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Weather data retrieved for {city}")
                
                # Cache the result
                self._cache[cache_key] = (data, datetime.now())
                
                return data
            elif response.status_code == 401:
                print("❌ Invalid API key. Using demo mode.")
                self.demo_mode = True
                return self._get_demo_weather(city)
            else:
                print(f"⚠️  API error {response.status_code}. Using demo data.")
                return self._get_demo_weather(city)
                
        except Exception as e:
            print(f"⚠️  Error fetching weather: {e}. Using demo data.")
            return self._get_demo_weather(city)
    
    def get_coordinates(self, city: str, country_code: str = "IN") -> Tuple[float, float]:
        """
        Get coordinates for a city
        
        Returns:
            (latitude, longitude)
        """
        weather = self.get_current_weather(city, country_code)
        
        if 'coord' in weather:
            return weather['coord']['lat'], weather['coord']['lon']
        
        # Default coordinates for major Indian cities
        city_coords = {
            'lucknow': (26.8467, 80.9462),
            'delhi': (28.6139, 77.2090),
            'mumbai': (19.0760, 72.8777),
            'kolkata': (22.5726, 88.3639),
            'chennai': (13.0827, 80.2707),
            'bangalore': (12.9716, 77.5946),
            'hyderabad': (17.3850, 78.4867),
            'ahmedabad': (23.0225, 72.5714),
            'pune': (18.5204, 73.8567),
            'varanasi': (25.3176, 82.9739)
        }
        
        city_lower = city.lower()
        return city_coords.get(city_lower, (26.8467, 80.9462))  # Default to Lucknow
    
    def _get_demo_weather(self, city: str) -> Dict:
        """Generate deterministic demo weather data.
        
        Values are seeded by city name + current hour so they stay
        stable across refreshes within the same hour.
        """
        import random as _rng
        import hashlib

        # Seed: city (case-insensitive) + date + hour → stable per hour
        now = datetime.now()
        seed_str = f"{city.lower()}_{now.strftime('%Y%m%d%H')}"
        seed = int(hashlib.md5(seed_str.encode()).hexdigest(), 16) % (2**32)
        gen = _rng.Random(seed)

        demo_data = {
            'coord': {'lat': 26.8467, 'lon': 80.9462},
            'weather': [
                {
                    'id': 500,
                    'main': 'Rain',
                    'description': 'moderate rain'
                }
            ],
            'main': {
                'temp': round(gen.uniform(20, 35), 1),
                'feels_like': round(gen.uniform(20, 35), 1),
                'temp_min': round(gen.uniform(18, 30), 1),
                'temp_max': round(gen.uniform(25, 38), 1),
                'pressure': round(gen.uniform(1000, 1020), 1),
                'humidity': round(gen.uniform(40, 90), 1)
            },
            'wind': {
                'speed': round(gen.uniform(2, 15), 1),
                'deg': gen.randint(0, 360)
            },
            'rain': {
                '1h': round(gen.uniform(0, 25), 1)
            },
            'dt': int(now.timestamp()),
            'name': city
        }
        
        return demo_data
    
    def transform_to_features(self, weather_data: Dict, city: str) -> Dict:
        """
        Transform weather API data to model features
        
        Args:
            weather_data: Raw weather data from API
            city: City name
            
        Returns:
            Dictionary with 12 model features
        """
        print(f"\n🔄 Transforming weather data for {city}...")
        
        # Extract weather data
        main = weather_data.get('main', {})
        wind = weather_data.get('wind', {})
        rain = weather_data.get('rain', {})
        
        # Get rainfall (if available)
        rainfall_1h = rain.get('1h', 0.0)  # Rain in last hour
        rainfall_24h = rainfall_1h * 24  # Estimate for 24h (simplified)
        
        # Temperature and humidity
        temperature = main.get('temp', 25.0)
        humidity = main.get('humidity', 70.0)
        
        # Wind speed (convert m/s to km/h)
        wind_speed_ms = wind.get('speed', 5.0)
        wind_speed_kmh = wind_speed_ms * 3.6
        
        # Current month
        month = datetime.now().month
        
        # Estimated/default values for features not in weather API
        # In production, these would come from additional APIs or sensors
        
        # Estimate river level based on recent rainfall
        # (Simplified model - in production, use actual river gauge data)
        if rainfall_24h > 150:
            river_level = 9.0 + (rainfall_24h - 150) / 50
        elif rainfall_24h > 80:
            river_level = 6.0 + (rainfall_24h - 80) / 30
        elif rainfall_24h > 40:
            river_level = 4.0 + (rainfall_24h - 40) / 20
        else:
            river_level = 2.5 + rainfall_24h / 20
        
        river_level = min(river_level, 14.0)  # Cap at realistic max
        
        # Estimate soil moisture from rainfall and humidity
        base_moisture = humidity * 0.6  # Base from humidity
        rain_moisture = min(rainfall_24h * 0.5, 40)  # Additional from rain
        soil_moisture = min(base_moisture + rain_moisture, 98.0)
        
        # Get coordinates for distance estimation
        lat, lon = self.get_coordinates(city)
        
        # Estimate elevation (simplified - in production, use elevation API)
        elevation_map = {
            'lucknow': 123.0,
            'delhi': 216.0,
            'mumbai': 14.0,
            'kolkata': 9.0,
            'chennai': 7.0,
            'bangalore': 920.0,
            'hyderabad': 542.0,
            'varanasi': 80.8,
            'patna': 53.0,
            'ahmedabad': 53.0
        }
        elevation = elevation_map.get(city.lower(), 150.0)
        
        # Estimate distance to river (simplified)
        # In production, use geospatial database
        distance_to_river = 3.0  # Default 3km
        
        # Build feature dictionary
        features = {
            'rainfall_mm': round(rainfall_24h, 2),
            'rainfall_7day_avg': round(rainfall_24h * 0.7, 2),  # Estimate
            'rainfall_intensity': round(rainfall_1h, 2),
            'river_level_m': round(river_level, 2),
            'river_level_change': round(rainfall_1h * 0.15, 2),  # Estimate from rain
            'soil_moisture_percent': round(soil_moisture, 2),
            'elevation_m': round(elevation, 2),
            'temperature_celsius': round(temperature, 2),
            'humidity_percent': round(humidity, 2),
            'wind_speed_kmh': round(wind_speed_kmh, 2),
            'distance_to_river_km': round(distance_to_river, 2),
            'month': month
        }
        
        print("✅ Features extracted:")
        print(f"   Rainfall: {features['rainfall_mm']} mm")
        print(f"   Temperature: {features['temperature_celsius']}°C")
        print(f"   Humidity: {features['humidity_percent']}%")
        print(f"   Estimated River Level: {features['river_level_m']} m")
        
        return features


def test_weather_api():
    """Test the weather API client"""
    
    print("\n" + "="*70)
    print(" "*20 + "🌦️  WEATHER API TEST")
    print("="*70 + "\n")
    
    # Initialize client
    client = WeatherAPIClient()
    
    # Test cities
    cities = ["Lucknow", "Mumbai", "Delhi"]
    
    for city in cities:
        print(f"\n{'='*70}")
        print(f"Testing: {city}")
        print("="*70)
        
        # Get weather
        weather = client.get_current_weather(city)
        
        # Display raw weather
        print(f"\n📊 Raw Weather Data:")
        if 'main' in weather:
            print(f"   Temperature: {weather['main']['temp']:.1f}°C")
            print(f"   Humidity: {weather['main']['humidity']}%")
        if 'wind' in weather:
            print(f"   Wind Speed: {weather['wind']['speed']:.1f} m/s")
        if 'rain' in weather:
            print(f"   Rain (1h): {weather['rain'].get('1h', 0)} mm")
        
        # Transform to features
        features = client.transform_to_features(weather, city)
        
        print(f"\n🎯 Model Features:")
        for key, value in features.items():
            print(f"   {key}: {value}")
    
    print("\n" + "="*70)
    print("✅ Weather API test complete!")
    print("="*70 + "\n")


if __name__ == "__main__":
    test_weather_api()

