import os
import requests
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Wether Dashboard", layout="wide")

try:
    key = st.secrets["API_KEY"]
except Exception:
    key = os.getenv("API_KEY")

if not key:
    st.error("API key missing. Add it to Streamlit secrets or environment variables.")
    st.stop()
st.title("Live Weather Dashboard")
def weather_fetch(city , cc = ""):

    location = f"{city},{cc}" if cc else city 
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": location,
        "appid": key,
        "units": "metric"
    }
    response = requests.get(url,params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        try:
            error_data = response.json()
            error_message = error_data.get("message", "Unknown API error")
        except ValueError:
             error_message = "Could not parse error response"
        
        st.error(f"Status code : {response.status_code} , {error_message}")
        st.warning("Try another city")
        return None
city = st.text_input("Enter the City name:","London")
cc = st.text_input("Enter country code(optional):")
weather = weather_fetch(city,cc)

if weather:
    c_name = weather["name"]
    temp = weather["main"]["temp"],"°C"
    feel = weather["main"]["feels_like"], "°C"
    hum = weather["main"]["humidity"], "%"
    condi =  weather["weather"][0]["description"]
    wind_s = weather["wind"]["speed"], "m/s"
  
    icon_url = f"http://openweathermap.org/img/wn/{weather['weather'][0]['icon']}@2x.png"
    st.title(f"Live Weather in {c_name}")
    col1, col2 = st.columns([1, 4])
    with col1:
         st.markdown(f"<h3 style='font-size: 19px; font-weight: bold;'> {condi}</h3>", unsafe_allow_html=True)
       
    with col2:
        st.image(icon_url, width=40)
    col_a, col_b, col_c, col_d = st.columns(4)
    col_a.metric("🌡️Temperature:",f"{temp[0]} °C")
    col_b.metric("🫠Feels like:",f"{feel[0]} °C")
    col_c.metric("💧Humidity:",f"{hum[0]} %")
    col_d.metric("💨Wind speed:",f"{wind_s[0]} m/s")


def fetch_7_day_history(city, cc=""):
    """
    Fetch the last 7 days of maximum temperatures using the Open-Meteo geocoding + forecast APIs.
    """
    query = f"{city},{cc}" if cc else city

    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    geo_params = {
        "name": query,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    geo_response = requests.get(geo_url, params=geo_params, timeout=15)
    if geo_response.status_code != 200:
        st.error(f"Failed to resolve city coordinates: {geo_response.status_code}")
        return None

    try:
        geo_data = geo_response.json()
    except ValueError:
        st.error("The geocoding service returned a non-JSON response.")
        return None

    results = geo_data.get("results") or []
    if not results:
        st.warning("City not found. Try a different city or add a valid country code.")
        return None

    location = results[0]
    lat = location.get("latitude")
    lon = location.get("longitude")

    if lat is None or lon is None:
        st.warning("Location coordinates were not returned for this city.")
        return None

    forecast_url = "https://api.open-meteo.com/v1/forecast"
    forecast_params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_max",
        "past_days": 7,
        "forecast_days": 0,
        "timezone": "auto"
    }

    response = requests.get(forecast_url, params=forecast_params, timeout=15)
    if response.status_code != 200:
        st.error(f"Failed to fetch historical data: {response.status_code}")
        return None

    try:
        data = response.json()
    except ValueError:
        st.error("The historical-weather service returned a non-JSON response.")
        return None

    daily_data = data.get("daily", {})
    if not daily_data.get("time"):
        st.warning("No historical weather data was returned for this location.")
        return None

    df = pd.DataFrame({
        "Date": pd.to_datetime(daily_data.get("time")),
        "Max Temp (°C)": daily_data.get("temperature_2m_max")
    })

    return df.set_index("Date")

st.subheader("7-Day Temperature Trend")

df_history = fetch_7_day_history(city, cc)

if df_history is not None:
    st.line_chart(df_history)

