import streamlit as st # type: ignore
import requests # type: ignore
import os
from dotenv import load_dotenv # type: ignore

# Load API Key from .env file
load_dotenv()
API_KEY = os.getenv("TOMORROW_API_KEY")

# Check if API_KEY is successfully loaded
if not API_KEY:
    st.error("❌ API Key is missing. Please add it in the .env file!")
else:
    # Custom CSS for a beautiful UI
    st.markdown("""
        <style>
            body {
                background: linear-gradient(to right, #9b59b6, #ff69b4); /* Purple to Pink gradient */
                color: white;
                font-family: 'Arial', sans-serif;
            }
            .stApp {
                background: linear-gradient(to right, #9b59b6, #ff69b4);
            }
            .main-title {
                font-size: 3rem;
                font-weight: bold;
                color: #ffcc00;
                text-align: center;
                margin-top: 50px;
            }
            .weather-box {
                background: rgba(255, 255, 255, 0.15);
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 4px 20px rgba(255, 255, 255, 0.3);
                text-align: center;
                margin-top: 30px;
                display: grid;
                grid-template-columns: 1fr 1fr 1fr;
                gap: 20px;
            }
            .metric-box {
                font-size: 1.5rem;
                font-weight: bold;
                color: #ffffff;
                padding: 15px;
                background-color: rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                box-shadow: 0 4px 10px rgba(255, 255, 255, 0.2);
                display: flex;
                justify-content: center;
                align-items: center;
                text-align: center;
            }
            .metric-box span {
                font-size: 1.2rem;
                color: #ffcc00;
            }
            .footer {
                text-align: center;
                font-size: 14px;
                margin-top: 50px;
                color: #ccc;
                font-weight: bold;
            }
            .input-box {
                margin-top: 20px;
                text-align: center;
            }
            .error-message {
                color: #ff4d4d;
                font-weight: bold;
            }
        </style>
    """, unsafe_allow_html=True)

    # Title
    st.markdown("<h1 class='main-title'>🌤️ Weather Insights</h1>", unsafe_allow_html=True)

    # Input Field for City
    city = st.text_input("📍 Enter City Name", "Karachi", placeholder="e.g., New York, London")

    # Fetch Weather Data Function
    def get_weather(city):
        url = f"https://api.tomorrow.io/v4/weather/realtime?location={city}&apikey={API_KEY}"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            return None

    # Display Weather Data
    if st.button("🔍 Get Weather"):
        if city:
            weather_data = get_weather(city)

            if weather_data:
                temp = weather_data['data']['values']['temperature']
                humidity = weather_data['data']['values']['humidity']
                wind_speed = weather_data['data']['values']['windSpeed']

                # Weather Box (using grid layout)
                st.markdown("<div class='weather-box'>", unsafe_allow_html=True)

                # Display Metrics in grid layout
                st.markdown(f"<div class='metric-box'>🌡️ <span>Temperature:</span> {temp}°C</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='metric-box'>💧 <span>Humidity:</span> {humidity}%</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='metric-box'>💨 <span>Wind Speed:</span> {wind_speed} km/h</div>", unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.markdown("<p class='error-message'>❌ City not found or API issue. Try again!</p>", unsafe_allow_html=True)
        else:
            st.markdown("<p class='error-message'>❌ Please enter a city name!</p>", unsafe_allow_html=True)

    # Footer
    st.markdown("<div class='footer'>Made with ❤️ by Asma Yaseen | Powered by Tomorrow.io</div>", unsafe_allow_html=True)
