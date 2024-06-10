import folium
import requests

from bs4 import BeautifulSoup


def single_map(user_location: str) -> None:
    """
    Creates a map centered on the specified location and saves it as an HTML file.

    :param user_location: The name of the location to center the map on.
    :return: None: This function does not return any value.

    Functionality:
    1. Constructs a URL for the Wikipedia page of the specified location.
    2. Sends a GET request to fetch the Wikipedia page.
    3. Parses the HTML response to extract the latitude and longitude coordinates.
    4. Creates a folium map centered on the extracted coordinates.
    5. Adds a marker to the map at the specified location.
    6. Saves the map as an HTML file named after the location.

    Example usage:
    single_map("Warsaw")

    Expected behavior:
    An HTML file named "Warsaw.html" will be created, displaying a map centered on Warsaw with a marker.

    Notes:
    - The function relies on the Wikipedia page structure to extract coordinates, so it may fail if the page structure changes.
    - Ensure that the `requests` and `BeautifulSoup` libraries are installed.
    - There is no error handling for cases where the location is not found or the coordinates are not present.
    """
    url: str = f'https://pl.wikipedia.org/wiki/{user_location}'
    response = requests.get(url)
    response_html = BeautifulSoup(response.text, 'html.parser')

    latitude: str = response_html.select('.latitude')[1].text.replace(",", ".")
    longitude: str = response_html.select('.longitude')[1].text.replace(",", ".")

    my_map = folium.Map(location=[latitude, longitude], zoom_start=11)
    folium.Marker(location=[latitude, longitude], popup=f"{user_location}").add_to(my_map)
    my_map.save(f'./{user_location}.html')


def full_map(users: str) -> None:
    """
    Creates a map with markers for the locations of all users and saves it as an HTML file.

    :param users: A list of dictionaries, where each dictionary represents a user and contains the key 'location'.
    :return: None: This function does not return any value.

    Functionality:
    1. Initializes a folium map centered on a default location.
    2. Iterates over the list of users to extract each user's location.
    3. For each user, constructs a URL for the Wikipedia page of their location.
    4. Sends a GET request to fetch the Wikipedia page.
    5. Parses the HTML response to extract the latitude and longitude coordinates.
    6. Adds the extracted coordinates to a list and places a marker on the map for each location.
    7. Saves the map as an HTML file named "common_map.html".

    Example usage:
    users_list = [
        {"name": "John", "surname": "Doe", "posts": 5, "location": "Warsaw"},
        {"name": "Anna", "surname": "Smith", "posts": 12, "location": "London"}
    ]
    full_map(users_list)

    Expected behavior:
    An HTML file named "common_map.html" will be created, displaying a map with markers for Warsaw and London.

    Notes:
    - The function relies on the Wikipedia page structure to extract coordinates, so it may fail if the page structure changes.
    - Ensure that the `requests` and `BeautifulSoup` libraries are installed.
    - There is no error handling for cases where a location is not found or the coordinates are not present.
    - The map is initially centered on [52, 21] with a zoom level of 8.
    """

    coords: list = []
    my_map = folium.Map(location=[52, 21], zoom_start=8)
    for user in users:
        url: str = f"https://pl.wikipedia.org/wiki/{user['location']}"
        response = requests.get(url)
        response_html = BeautifulSoup(response.text, 'html.parser')
        latitude: str = response_html.select('.latitude')[1].text.replace(",", ".")
        longitude: str = response_html.select('.longitude')[1].text.replace(",", ".")
        coords.append([latitude, longitude])
        for pair_of_coords in coords:
            folium.Marker(location=pair_of_coords).add_to(my_map)

        my_map.save(f'./common_map.html')
