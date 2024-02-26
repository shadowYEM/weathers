import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# API key for weather API
api_key = "5a4110f3bdff4af6918144642232109"
base_url = "http://api.weatherapi.com/v1/"
# Function to get current weather

# Function to get current weather
def get_weather(city: str):
    complete_url = f"{base_url}current.json?key={api_key}&q={city}"
    response = requests.get(complete_url)
    data = response.json()
    print(data)  # Print the data for debugging purposes
    temperature = data["current"]["temp_c"]
    description = data["current"]["condition"]["text"]
    return temperature, description

# Function to get weather forecast
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

# Dictionary of Arab countries and their provinces
arab_countries = {
     "Yemen": ["Sana'a (governorate)","'Adan","'Amran","Al Bayda'","Al Hudaydah","Al Jawf","Al Mahrah","Al Mahwit","Amanat al 'Asimah","Dhamar","Hadhramaut","Hajjah","Ibb","Lahij","Ma'rib","Raymah","Sa'dah","Shabwah","Socotra Island","Ta'izz"],
    "Saudi Arabia": ["Riyadh","Jeddah", "'Asir", "Al Bahah", "Al Jawf", "Al Madinah al Munawwarah", "Al-Qassim", "Eastern Province", "Ha'il", "Jazan", "Makkah al Mukarramah", "Najran", "Northern Borders", "Tabuk"],
    "Egypt": ["Cairo", "Alexandria", "Ismailia", "Aswan", "Asyut", "Luxor", "Port Said", "Suez", "El-Mahalla El-Kubra", "El Mansoura", "Tanta", "As-Suways", "Al-Minya", "Faiyum", "Zagazig", "Damanhur", "Al-Fashn", "Qena", "Sohag", "Hurghada", "Banha", "Arish", "Marsa Matruh", "Kafr El Sheikh", "Damietta", "Giza", "Beni Suef", "Shibin El Kom", "Mallawi", "Kafr El Dawwar", "Bilbais", "Marsa Alam", "Desouk", "Idfu", "Mit Ghamr", "Al-Arish", "Abu Kabir", "El Tor", "Sheikh Zuweid", "Qalyub", "Akhmim", "Dekernes", "Al-Hamidiyya", "Samalut", "Al-Qanayat", "Al-Qantara", "Ras Gharib", "Al-Balyana", "Al-Ibrahimiyah", "Al-Matariyah", "Al-Qusiyah", "Al-Sharqia", "Al-Waqf", "Dahab", "El Badari", "El Qoseir", "Faqous", "Isna", "Mansoura", "Minya", "New Cairo", "Rafah", "Safaga", "Siwa Oasis", "Tamiya", "Zifta"],
    "Ethiopia": ["Addis Ababa", "Harar", "Hawassa", "Dire Dawa", "Adama", "Bahir Dar", "Assela", "Gonder", "Shashamane", "Mek'ele", "Aksum", "Asosa", "Hosaena", "Adigrat", "Dessie", "Jijiga", "Arba Minch", "Agaro", "Bishoftu", "Areka", "Bonga", "Adwa", "Debre Tabor", "Kombolcha", "Gambela", "Jimma", "Debre Markos", "Ambo", "Gimbi", "Waliso", "Fiche", "Goba", "Yigra Alem", "Alaba Kulito", "Boditi", "Finote Selam", "Butajira", "Metu Zuria", "Nekemte", "Sodo", "Mizan Teferi"],
    "Iraq": ["Baghdad", "Basra", "Mosul", "Erbil", "Kirkuk", "Najaf", "Sulaymaniyah", "Duhok", "Ramadi", "Fallujah", "Tikrit", "Karbala", "Hilla", "Nasiriyah", "Samawah", "Kut", "Diwaniyah", "Kufa", "Al Hillah", "Baqubah"],
    "Jordan": ["Amman", "Zarqa", "Irbid", "Aqaba", "Madaba", "Jerash", "Ma'an", "Mafraq", "Sahab", "Karak", "Tafilah", "Azraq", "Aydoun", "Qasr Al-Hallabat", "Al-Jafr", "Al-Mudawwara", "Al-Ramtha", "Al-Salt", "Jarash", "Al-Mazar Al-Janubi"],
    "Kuwait": ["Kuwait City", "Al Ahmadi", "Hawalli", "Salwa", "Salmiya", "Jahra", "Sabah Al-Salem", "Al-Farwaniyah", "Al-Jahra", "Mubarak Al-Kabeer", "Ahmadi", "Fahaheel", "Wafra", "Qurain", "Abdullah Al-Salem", "Adan", "Al-Qurain"],
    "United Arab Emirates": ["Abu Dhabi", "Dubai", "Sharjah", "Ajman", "Ras Al Khaimah", "Fujairah", "Umm Al Quwain", "Al Ain", "Khor Fakkan", "Dibba Al-Fujairah", "Dibba Al-Hisn", "Hatta", "Kalba", "Madinat Zayed", "Mirbah", "Ruwais", "Liwa Oasis", "Jebel Ali"],
    "Kuwait": ["Kuwait City", "Al Ahmadi", "Hawalli", "Salwa", "Salmiya", "Jahra", "Sabah Al-Salem", "Al-Farwaniyah", "Al-Jahra", "Mubarak Al-Kabeer", "Ahmadi", "Fahaheel", "Wafra", "Qurain", "Abdullah Al-Salem", "Adan", "Al-Qurain"],
    "Lebanon": ["Beirut", "Tripoli", "Sidon", "Tyre", "Jounieh", "Zahle", "Nabatieh", "Batroun", "Baalbek", "Jbeil", "Byblos", "Chouf", "Aley", "Keserwan", "Metn", "Baabda", "Marjeyoun", "Akkar", "Bsharri", "Zgharta"],
    "Oman": ["Muscat", "Salalah", "Sohar", "Nizwa", "Ibri", "Sur", "Khasab", "Bahla", "Rustaq", "Al Buraimi", "Ibra", "Saham", "Adam", "Yanqul", "Bidbid", "Al Khaburah", "Shinas", "Al Hamra", "Izki", "Barka"],
    "Qatar": ["Doha", "Al Rayyan", "Umm Salal", "Al Wakrah", "Al Khor", "Al Daayen", "Mesaieed", "Al Shahaniya", "Al Sheehaniya", "Al Ruwais", "Al Wukair", "Al Gharafa", "Al Jasra", "Al Khuwayr", "Al Thakhira", "Dukhan", "Lusail", "Madinat Al-Shamal", "Mesaimeer", "Ras Laffan"],
    "Bahrain": ["Manama", "Muharraq", "Isa Town", "Riffa", "Hamad Town", "Sitra", "Jidhafs", "Al-Malikiyah", "Adliya", "Sanabis", "Juffair", "Sar", "Budaiya", "Al-Hidd", "Diplomatic Area", "Ma'ameer", "Zinj", "Seef", "Awali", "Tubli"],
    "Syria": ["Damascus", "Aleppo", "Homs", "Latakia", "Hama", "Deir ez-Zor", "Raqqa", "Idlib", "Tartus", "As-Suwayda", "Al-Hasakah", "Daraa", "Dayr Hafir", "Al-Bab", "Manbij", "Al-Thawrah", "Darayya", "Tadmur", "Tafas", "Al-Qusayr"],
    "Tunisia": ["Tunis", "Sfax", "Sousse", "Kairouan", "Bizerte", "Gabes", "Ariana", "Gafsa", "La Marsa", "El Mourouj", "Kasserine", "Monastir", "Nabeul", "Ben Arous", "Zarzis", "Beja", "Mahdia", "Sidi Bouzid", "Menzel Bourguiba", "Siliana"],
    "Algeria": ["Algiers", "Oran", "Constantine", "Annaba", "Blida", "Batna", "Djelfa", "Sétif", "Sidi Bel Abbès", "Biskra", "Tébessa", "Chlef", "Tiaret", "Guelma", "Béchar", "Tlemcen", "Béjaïa", "Skikda", "Mostaganem", "El Oued"],
    "Morocco": ["Casablanca", "Rabat", "Fes", "Marrakesh", "Agadir", "Tangier", "Meknes", "Oujda", "Kenitra", "Tétouan", "Safi", "Mohammedia", "El Jadida", "Beni Mellal", "Nador", "Khouribga", "Taza", "Settat", "Larache", "Khemisset"],
    "Libya": ["Tripoli", "Benghazi", "Misrata", "Tarhuna", "Al Bayda", "Zawiya", "Zliten", "Sabha", "Ajdabiya", "Tobruk", "Sirte", "Derna", "Murzuk", "Ghat", "Gharyan", "Al Khums", "Az Zintan", "Mizdah", "Zaltan", "Bani Walid"],
    "Sudan": ["Khartoum", "Omdurman", "Nyala", "Port Sudan", "Kassala", "Al-Ubayyid", "Kosti", "Wad Madani", "El Fasher", "El Geneina", "Ad-Damazin", "Gedaref", "Zalingei", "Sennar", "Rabak", "El Obeid", "Kadugli", "Ed Daein", "Khartoum North", "En Nuhud"],
    "Palestine": ["Jerusalem", "Gaza", "Hebron", "Nablus", "Bethlehem", "Ramallah", "Jenin", "Tulkarm", "Qalqilya", "Beit Jala", "Beit Sahour", "Al-Bireh", "Khan Yunis", "Rafah", "Tubas", "Salfit"],
    "Djibouti": ["Djibouti", "Ali Sabieh", "Dikhil", "Tadjoura", "Obock", "Arta", "Holhol", "Dorra", "Galafi", "Loyada", "Balho", "Goubetto", "Mouloud", "Assa-Gueyla", "Goda", "Ali Adde", "Oued'Alimini", "Gulbaley", "Haramous", "Tewa"],
    "Mauritania": ["Nouakchott", "Nouadhibou", "Kiffa", "Zouerate", "Rosso", "Atar", "Tidjikja", "Kaédi", "Selibaby", "Aleg", "Akjoujt", "Boghé", "Bir Moghrein", "Boutilimit", "Timbedra", "Néma", "Tichit", "Ayoun El Atrous", "Aoujeft", "Guérou"],
    # Add more countries and provinces here...
}

# Display current weather
st.title("Current Weather")
country1 = st.selectbox("Select a country:", list(arab_countries.keys()), key="country1")
province1 = st.selectbox("Select a province:", arab_countries[country1], key="province1")

temperature, description = get_weather(province1)
st.write(f"The current temperature in {province1} is {temperature}°C and the weather condition is {description}.")

# Display weather forecast
dates, temperatures = get_forecast(province1, 1)
fig = px.line(x=dates, y=temperatures, labels={"x": "Time", "y": "Temperature (°C)"})
st.plotly_chart(fig)

# Display weather forecast
st.title("Weather Forecast")
country2 = st.selectbox("Select a country:", list(arab_countries.keys()), key="country2")
province2 = st.selectbox("Select a province:", arab_countries[country2], key="province2")
days = st.slider("Select the number of days:", 1, 10, 2)

dates, temperatures = get_forecast(province2, days)

fig = px.line(x=dates, y=temperatures, labels={"x": "Date", "y": "Temperature (°C)"})
st.plotly_chart(fig)

# data = {"Date": dates, "Temperature (°C)": temperatures}
# df = pd.DataFrame(data)

# col1, col2, col3 = st.columns([1, 2, 1])
# with col2:
#     st.table(df)

# Create a DataFrame from the forecast data
data = {"Date": dates, "Temperature (°C)": temperatures}
df = pd.DataFrame(data)

# Display the forecast data in a table
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.dataframe(df)
