import folium
import requests
import pandas as pd
import maidenhead
from geopy.geocoders import Nominatim

# Function to get latitude and longitude of a city
def get_coordinates(city):
    geolocator = Nominatim(user_agent="geo_query")
    location = geolocator.geocode(city)
    return (location.latitude, location.longitude) if location else None

# Function to get OSRM route
def get_route(cities):
    coords = [get_coordinates(city) for city in cities]
    coords = [c for c in coords if c]  # Remove any None values

    if len(coords) < 2:
        print("Error: Not enough valid city coordinates.")
        return []

    coord_str = ";".join(f"{lon},{lat}" for lat, lon in coords)
    osrm_url = f"http://router.project-osrm.org/route/v1/driving/{coord_str}?overview=full&geometries=geojson"
    response = requests.get(osrm_url)

    if response.status_code == 200:
        route_data = response.json()
        if route_data["routes"]:
            return route_data["routes"][0]["geometry"]["coordinates"]
    return []

# Function to get six-character Maidenhead grid square
def get_grid_square(lat, lon):
    return maidenhead.to_maiden(lat, lon, precision=6)[:6]  # Extract first six characters

# Get cities along the route
cities = ["Minneapolis, MN", "Sioux City, IA", "Omaha, NE", "Lincoln, NE"]
route = get_route(cities)

if route:
    print("Route successfully retrieved!")

    # Convert route waypoints to six-character Maidenhead grid squares
    route_grids = set(get_grid_square(lat, lon) for lon, lat in route)

    # Load CSV with latitude and longitude data
    df = pd.read_csv("data.csv")
    df["grid_square"] = df.apply(lambda row: get_grid_square(row["Lat"], row["Long"]), axis=1)

    # Filter repeaters based on grid square match
    matches = df[df["grid_square"].isin(route_grids)]

    # Create a folium map centered on the first city
    m = folium.Map(location=[route[0][1], route[0][0]], zoom_start=6)

    # Add route as a polyline
    folium.PolyLine([(lat, lon) for lon, lat in route], color="blue", weight=5).add_to(m)

    # Plot only the filtered repeaters
    for _, row in matches.iterrows():
        folium.Marker(
            location=[row["Lat"], row["Long"]],
            popup=f"Repeater: {row['Call']}",
            icon=folium.Icon(color="red")
        ).add_to(m)

    # Save map as an HTML file
    html_file = "filtered_route_map.html"
    m.save(html_file)
    print(f"Filtered map saved as {html_file}")

    # Save filtered repeaters list as CSV
    filtered_csv = "filtered_repeaters_list.csv"
    matches.to_csv(filtered_csv, index=False)
    print(f"Filtered repeaters list saved as {filtered_csv}")

else:
    print("Error retrieving route from OSRM.")
