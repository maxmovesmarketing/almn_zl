
import requests
import csv
import json

URL = "https://www.almn.nl/voorraad-api/vehiclelist/10/vehicles.json?limit=100&webspaceKey=&lease_type=business&sort=created_at_desc&page=1"

def scrape_website():
    """
    Scrapes the ALMN website for car listings using its internal API.
    """
    try:
        response = requests.get(URL)
        response.raise_for_status()  # Raise an exception for bad status codes

        data = response.json()
        cars = data.get("items", [])

        # Convert to JSON and save to a file
        with open("cars.json", "w") as f:
            json.dump(cars, f, indent=4)

        print(f"Successfully scraped {len(cars)} cars and saved to cars.json")

        # Write to CSV
        with open('cars.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'title', 'description', 'link', 'image_link', 'price', 'brand', 'availability', 'condition'])

            for car in cars:
                car_id = car.get('id')
                title = f"{car.get('brand', '')} {car.get('model', '')} {car.get('type', '')}"
                description = '' # No description available
                link = f"https://www.almn.nl{car.get('url')}"
                image_link = car['images'][0]['path'] if car.get('images') else ''
                price_float = car.get('price', 0)
                price = f"€ {price_float:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

                brand = car.get('brand')
                availability = 'in stock'
                condition = 'used' # All are occasions

                writer.writerow([car_id, title, description, link, image_link, price, brand, availability, condition])
        print(f"Successfully wrote {len(cars)} cars to cars.csv")

    except requests.exceptions.RequestException as e:
        print(f"Error during requests to {URL}: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    scrape_website()
