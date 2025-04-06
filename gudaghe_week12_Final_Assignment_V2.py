# DSC 510
# Programming Assignment Week 12
# Author:Tushar Gudaghe
# Date: 05/30/2024

import socket
import requests

API_KEY = "918ea65d871d89c9cc6bce0c86b4f94c"
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"
GEO_API_URL = "http://api.openweathermap.org/geo/1.0/direct"
ZIP_URL = "http://api.openweathermap.org/geo/1.0/zip?"
COUNTRY_CODE = "US"


def get_weather_data(url, params):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except (requests.exceptions.RequestException, socket.gaierror) as e:
        print(f"Error: {e}")
        return None


def get_geolocation_zip(zip_code, country=COUNTRY_CODE):
    params = {"zip": f"{zip_code},{country}", "appid": API_KEY}
    data = get_weather_data(ZIP_URL, params)
    if data:
        lat = data.get("lat")
        lon = data.get("lon")
        name = data.get("name")
        country = data.get("country")
        return lon, lat, name, country
    else:
        return None, None, None, None


def get_geolocation_city(city_name, state=None, country=COUNTRY_CODE):
    params = {"q": f"{city_name},{state},{country}", "limit": 5, "appid": API_KEY}
    data = get_weather_data(GEO_API_URL, params)
    if data and isinstance(data, list) and len(data) > 0:
        lat = data[0].get('lat')
        lon = data[0].get('lon')
        state = data[0].get('state', '')
        name = data[0].get('name', '')
        return lat, lon, state, name
    return None, None, None, None


def get_weather(lat, lon):
    params = {"lat": lat, "lon": lon, "appid": API_KEY}
    return get_weather_data(WEATHER_API_URL, params)


# Below function converts temperature to Celsius
def kel_to_cel(k):
    return k - 273.15


# Below function converts temperature to Fahrenheit
def kel_to_fah(k):
    return k * 9 / 5 - 459.67


def display_weather(weather_data, temp_unit, state, name):
    # print(weather_data)
    if not weather_data:
        print("Failed to retrieve weather data.")
        return

    temp_units = {"C": "°C", "F": "°F", "K": "K"}

    temperature = weather_data["main"]["temp"]
    min_temp = weather_data["main"]["temp_min"]
    max_temp = weather_data["main"]["temp_max"]

    if temp_unit in temp_units:
        if temp_unit == "C":
            temperature, min_temp, max_temp = kel_to_cel(temperature), kel_to_cel(min_temp), kel_to_cel(max_temp)
        elif temp_unit == "F":
            temperature, min_temp, max_temp = kel_to_fah(temperature), kel_to_fah(min_temp), kel_to_fah(max_temp)
    else:
        print("Invalid temperature unit. Operation cancelled.")
        return

    print(50 * "*")
    print("Current Location:", name, ",", state, weather_data["sys"]["country"])
    print(f"Current temperature :{temperature:.2f}{temp_units.get(temp_unit)}")
    print("Current weather conditions:", weather_data["weather"][0]["description"].capitalize())
    print(f"Minimum temperature today: {min_temp:.2f}{temp_units.get(temp_unit)}")
    print(f"Maximum temperature today: {max_temp:.2f}{temp_units.get(temp_unit)}")
    print(f"Pressure level: {weather_data['main']['pressure']} hPa")
    print(f"Humidity level: {weather_data['main']['humidity']}%")
    print(50 * "*")


def main():
    print("\nWelcome to Open Weather API.\n")
    while True:
        choice = input("You can check weather by using below options.\nPlease Type: \n\na) \"1\" for Zip Code \n"
                       "b) \"2\" for City Name \nc) \"3\" to Exit \n\nYour input is: ").lower()

        if choice == "3":
            print("You opted to Exit. See you next time.")
            return

        elif choice == "2":
            city_name = input("Enter a city name located in US: ")
            if not city_name:
                print("You pressed Enter. Try again\n")
                continue
            state = input("Enter the state code: ")
            if not state:
                print("You pressed Enter. Try again\n")
                continue

            # Calling function to get latitude and longitude using city name details
            lat, lon, state, name = get_geolocation_city(city_name, state, COUNTRY_CODE)

            if lat is not None and lon is not None:
                weather_data = get_weather(lat, lon)  # calling function to get weather data
                if weather_data:
                    temp_unit = input("\nChoose unit for temperature \nType \"C\" for celsius \n"
                                      "Type \"F\" for Fahrenheit \nType \"K\" for Kelvin \n"
                                      "Press any key to exit operation \n\nYour input -> ").upper()
                    display_weather(weather_data, temp_unit, state, name)
                    while True:
                        user_input = input("\nWant to check weather for another location? "
                                           "Press \"Y\" or Press \"Q\" to quit.\n").lower()
                        if user_input == "y":
                            break
                        elif user_input == "q":
                            return
            else:
                print("Failed to retrieve location data. Due to invalid/missing details. Try again.\n")

        elif choice == "1":
            while True:
                zip_code = input(
                    "\nEnter a zip code of a location or \"M\" to return to main menu or \"Q\" to Quit: ").lower()
                if zip_code == "m":
                    break
                elif zip_code == "q":
                    return
                elif zip_code.isdigit():

                    # Calling function to get latitude and longitude using zip code details
                    lon, lat, state, name = get_geolocation_zip(zip_code, COUNTRY_CODE)
                    if lat is not None and lon is not None:
                        weather_data = get_weather(lat, lon)
                        if weather_data:
                            temp_unit = input("\nChoose unit for temperature \nType \"C\" for celsius \n"
                                              "Type \"F\" for Fahrenheit \nType \"K\" for Kelvin \n"
                                              "Press any key to exit operation \n\nYour input -> ").upper()

                            # calling function to display weather to user
                            display_weather(weather_data, temp_unit, state, name)

                            while True:
                                user_input = input("\nWant to check weather for another location? "
                                                   "Press \"Y\" or Press \"Q\" to quit\n").lower()
                                if user_input == "y":
                                    break
                                elif user_input == "q":
                                    return
                        break
                    else:
                        print("Failed to retrieve location data. Due to invalid/missing details. Try again.\n")
                else:
                    print("Zip Code must be numeric.")
        else:
            print("\nInvalid Input. Please try again.\n")


if __name__ == "__main__":
    main()
