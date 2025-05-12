import streamlit as st
import requests
import os
from dotenv import load_dotenv

# --- Configuration ---
load_dotenv()
API_KEY = os.getenv("TOMORROW_API_KEY", "dbc942c987794e424cb288ccd90af48d")  # Fallback to test key

# --- UI Styling ---
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #9b59b6, #ff69b4);
            color: white;
        }
        .main-title {
            font-size: 2.5rem;
            font-weight: 800;
            text-align: center;
            margin: 1rem 0;
            background: linear-gradient(90deg, #ffcc00, #ff9500);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .weather-box {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1.5rem 0;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        .metric-box {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 1rem;
            border-radius: 10px;
            background: rgba(255, 255, 255, 0.15);
            margin: 0.5rem;
        }
        .metric-icon {
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }
        .metric-value {
            font-size: 1.8rem;
            font-weight: 700;
            color: #ffcc00;
        }
        .metric-label {
            font-size: 1rem;
            opacity: 0.8;
        }
        .stButton>button {
            background: linear-gradient(90deg, #9b59b6, #ff69b4);
            color: white;
            border: none;
            border-radius: 25px;
            padding: 0.5rem 2rem;
            font-size: 1rem;
        }
        .stTextInput>div>div>input {
            background: rgba(255,255,255,0.2);
            color: black;
            border: 1px solid rgba(255,255,255,0.3);
        }
    </style>
""", unsafe_allow_html=True)

# --- App Layout ---
st.markdown("<h1 class='main-title'>🌤️ Weather Insights</h1>", unsafe_allow_html=True)

city = st.text_input("📍 Enter City Name", "Karachi", 
                    placeholder="e.g., New York, London",
                    key="city_input")

# --- Weather Data Fetching ---
@st.cache_data(ttl=3600, show_spinner="Fetching weather data...")
def get_weather(city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"⚠️ Error: {str(e)}")
        return None

# --- Main App Logic ---
if st.button("🔍 Get Weather", use_container_width=True):
    if not city.strip():
        st.warning("Please enter a city name")
    elif not API_KEY:
        st.error("API key missing! Add it to .env file")
    else:
        weather_data = get_weather(city)
        
        if weather_data:
            try:
                # Extract weather data
                temp = weather_data['main']['temp']
                humidity = weather_data['main']['humidity']
                wind_speed = weather_data['wind']['speed']
                weather_desc = weather_data['weather'][0]['description'].title()
                icon_code = weather_data['weather'][0]['icon']
                
                # Weather icons mapping
                icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
                
                # Display weather data
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"""
                        <div class="metric-box">
                            <img src="{icon_url}" width="60">
                            <div class="metric-value">{temp}°C</div>
                            <div class="metric-label">Temperature</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                        <div class="metric-box">
                            <div class="metric-icon">💧</div>
                            <div class="metric-value">{humidity}%</div>
                            <div class="metric-label">Humidity</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                        <div class="metric-box">
                            <div class="metric-icon">💨</div>
                            <div class="metric-value">{wind_speed} km/h</div>
                            <div class="metric-label">Wind Speed</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                st.markdown(f"""
                    <div style="text-align: center; margin-top: 1rem; font-size: 1.2rem;">
                        Current conditions: <strong>{weather_desc}</strong>
                    </div>
                """, unsafe_allow_html=True)
                
            except KeyError as e:
                st.error(f"Data parsing error: {str(e)}")
        else:
            st.error("Failed to fetch weather data. Please try again.")

# --- Footer ---
st.markdown("""
    <div style="text-align: center; margin-top: 3rem; color: rgba(255,255,255,0.6);">
        Made with ❤️ using Streamlit | Data from OpenWeatherMap
    </div>
""", unsafe_allow_html=True)