import streamlit as st
import pandas as pd
import requests
import plotly.express as px

api_key = "d189e6e5c1734d2e803221317230706"
base_url = "http://api.weatherapi.com/v1/"

def get_weather(city: str):
    complete_url = f"{base_url}current.json?key={api_key}&q={city}"
    response = requests.get(complete_url)
    data = response.json()
    print(data)  # Print the data for debugging purposes
    temperature = data["current"]["temp_c"]
    description = data["current"]["condition"]["text"]
    return temperature, description

def get_forecast(city: str, days: int):
    complete_url = f"{base_url}forecast.json?key={api_key}&q={city}&days={days}&hourly=1"
    response = requests.get(complete_url)
    data = response.json()
    forecast_days = data["forecast"]["forecastday"]
    dates = []
    temperatures = []
    for day in forecast_days:
        for hour in day["hour"]:
            dates.append(hour["time"])
            temperatures.append(hour["temp_c"])
    return dates, temperatures

arab_countries = {
     "Yemen": ["Sana'a","'Adan","'Amran","Al Bayda'","Al Hudaydah","Al Jawf","Al Mahrah","Al Mahwit","Amanat al 'Asimah","Dhamar","Hadhramaut","Hajjah","Ibb","Lahij","Ma'rib","Raymah","Sa'dah","Sana'a (governorate)","Shabwah","Socotra Island","Ta'izz"],
    "Saudi Arabia": ["Riyadh","Jeddah", "'Asir", "Al Bahah", "Al Jawf", "Al Madinah al Munawwarah", "Al-Qassim", "Eastern Province", "Ha'il", "Jazan", "Makkah al Mukarramah", "Najran", "Northern Borders", "Tabuk"],
    "Egypt": ["Cairo", "Alexandria", "Ismailia", "Aswan", "Asyut", "Luxor"],
}

st.title("Current Weather")
country1 = st.selectbox("Select a country:", list(arab_countries.keys()), key="country1")
province1 = st.selectbox("Select a province:", arab_countries[country1], key="province1")

temperature, description = get_weather(province1)
st.write(f"The current temperature in {province1} is {temperature}°C and the weather condition is {description}.")


dates, temperatures = get_forecast(province1, 1)
fig = px.line(x=dates, y=temperatures, labels={"x": "Time", "y": "Temperature (°C)"})
st.plotly_chart(fig)

st.title("Weather Forecast")
country2 = st.selectbox("Select a country:", list(arab_countries.keys()), key="country2")
province2 = st.selectbox("Select a province:", arab_countries[country2], key="province2")
days = st.slider("Select the number of days:", 1, 10, 1)

dates, temperatures = get_forecast(province2, days)

fig = px.line(x=dates, y=temperatures, labels={"x": "Date", "y": "Temperature (°C)"})
st.plotly_chart(fig)

data = {"Date": dates, "Temperature (°C)": temperatures}
df = pd.DataFrame(data)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.table(df)

# Example usage of the get_forecast function
# city = "Riyadh"
# dates, temperatures = get_forecast(city, 1)
# plot_temperatures(dates, temperatures)


