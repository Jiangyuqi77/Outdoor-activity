import requests
import urllib.parse
import csv

# Function to fetch check-in data for a specific location type
def fetch_check_in_data(keyword, access_token, center_coordinates, radius, proxy):
    url = "https://graph.facebook.com/v13.0/search"
    params = {
        "q": urllib.parse.quote(keyword),  # URL-encode the keyword
        "type": "place",
        "center": center_coordinates,
        "distance": radius,
        "fields": "name,checkins,location",
        "access_token": access_token
    }

    response = requests.get(url, params=params, proxies=proxy)
    
    # Print raw response for debugging
    print(f"Raw response for keyword '{keyword}': {response.text}")
    
    return response.json()

# Define the parameters
access_token = "EAAAAUaZAM0y4KdO7Un22x8SOQBy5oKtGjWMH0KSoM0y4KdAcJC5svbjqTLwtUphaoteN5mYwomyP4eSObzuTzUsQ8ZCviyRfWKwdUxmz33v2YyyiaiumcLpVGU9ZAGHk7ttyZBOZCvNsk82ariQ0lJsvbjqTLwtUp8SSoiDa7q0B35dC7pJIhV1ytXIyAIp6HbLwZDZD"  # Replace with your actual app access token
# Coordinates for the centers of the districts in Hong Kong
districts = {
    "Wan Chai": "22.2770,114.1717",
    "Sham Shui Po": "22.3292,114.1591",
    "Kwun Tong": "22.3131,114.2259",
    "Sai Wan": "22.2871,114.1280"
}
search_radius = 1500  # Distance in meters

# List of keywords to search for
keywords = ["park", "garden", "sitting-out area", "plaza", "street", "playground", "promenade", "waterfront harbor garden", "rest garden", "street park", "road garden"]

# Define your proxy
proxy = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890"
}

# CSV file to store results
csv_filename = "facebook_checkins.csv"

# Open CSV file for writing
with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ["district", "keyword", "name", "checkins", "latitude", "longitude"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()  # Write header row

    # Fetch data for each keyword and district, and write results to CSV
    for district, coordinates in districts.items():
        for keyword in keywords:
            print(f"Fetching data for: {keyword} in {district}")
            data = fetch_check_in_data(keyword, access_token, coordinates, search_radius, proxy)
            if 'data' in data:
                for place in data['data']:
                    row = {
                        "district": district,
                        "keyword": keyword,
                        "name": place.get('name', 'Unknown'),
                        "checkins": place.get('checkins', 0),
                        "latitude": place['location'].get('latitude', 'Unknown'),
                        "longitude": place['location'].get('longitude', 'Unknown')
                    }
                    writer.writerow(row)
            else:
                print(f"No data found for '{keyword}' in {district} or an error occurred.")
            print("\n")  # Add space between keyword results

print(f"Data successfully written to {csv_filename}")
