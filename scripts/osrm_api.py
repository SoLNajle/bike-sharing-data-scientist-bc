

import requests

# Define the coordinates for the start and end points
start = "41.3911035,2.1801763"  # Longitude, Latitude (Barcelona)
end = "41.3821314,2.1606534"    # Longitude, Latitude (Barcelona)

# OSRM API endpoint
url = f"http://router.project-osrm.org/route/v1/cycling/{start};{end}"
# Optional parameters
params = {
    'overview': 'full',
    'geometries': 'geojson',
}

# Make the request
response = requests.get(url, params=params)
data = response.json()

# Print the route information
print(data)