import csv
import json
from regions_data import regions

# Constants for fuel types
FUEL_TYPES = ['95', '98', '98+', '85', 'dsl', 'dsl+', 'hvo', 'bgas']

class FuelDataProcessor:
    def __init__(self):
        self.total_stations = 0
        self.stations_without_fuel_data = 0
        self.fuel_data = {fuel: [] for fuel in FUEL_TYPES}
        self.brand_counts = {}
        self.station_types = {}
        self.fuel_prices_by_station = {}
        self.fuel_prices_by_region = {region: [] for region in regions}

    def read_and_process_csv(self, file_path):
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header
            for row in csv_reader:
                if row and row[0].strip():
                    self.total_stations += 1
                    self.process_row(row)

        self.generate_report()

    def process_row(self, row):
        try:
            address_data = json.loads(row[0])
            brand = row[2]
            station_type = row[3]
            fuels_data = json.loads(row[4])

            # Update brand and station type counts
            self.update_count(self.brand_counts, brand)
            self.update_count(self.station_types, station_type)

            # Record fuel prices by station
            self.fuel_prices_by_station.setdefault(brand, []).append(fuels_data)

            # Check and record fuel data
            if not fuels_data:
                self.stations_without_fuel_data += 1
            else:
                self.process_fuel_data(fuels_data, address_data['city'])

            # Record fuel prices by region
            self.process_region_data(fuels_data, address_data['city'])

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

    def process_fuel_data(self, fuels_data, city):
        """Process fuel prices and append to the respective fuel type."""
        for fuel in fuels_data:
            if fuel['tag'] in self.fuel_data:
                self.fuel_data[fuel['tag']].append((fuel['price'], city))

    def process_region_data(self, fuels_data, city):
        """Assign fuel data to the correct region based on the city."""
        for region, cities in regions.items():
            if city in cities:
                self.fuel_prices_by_region[region].append(fuels_data)
                break

    def update_count(self, counter_dict, key):
        """Increment the count of a given key in a dictionary."""
        counter_dict[key] = counter_dict.get(key, 0) + 1

    def calculate_average(self, fuel_data):
        """Calculate average price for a given fuel data list."""
        return round(sum(price for price, _ in fuel_data) / len(fuel_data), 3) if fuel_data else 0

    def calculate_min_max(self, fuel_data):
        """Calculate min and max price for a given fuel data list."""
        if fuel_data:
            min_price = min(fuel_data, key=lambda x: x[0])
            max_price = max(fuel_data, key=lambda x: x[0])
            return min_price, max_price
        return None, None

    def generate_report(self):
        """Generate and save a summary report to a text file."""
        with open('report.txt', 'w', encoding='utf-8') as file:
            file.write(self.generate_summary())
            file.write(self.generate_average_prices())
            file.write(self.generate_min_max_prices())
            file.write(self.generate_station_details())
            file.write(self.generate_average_prices_by_station())
            file.write(self.generate_average_prices_by_region())

    def generate_summary(self):
        """Generate a general summary section."""
        return (
            f"\n****** SUMMARY ******\n"
            f"Total stations: {self.total_stations}\n"
            f"Stations without fuel data: {self.stations_without_fuel_data}\n"
        )

    def generate_average_prices(self):
        """Generate average price section for each fuel type."""
        output = '\n****** AVERAGE PRICES ******\n'
        for fuel_type in FUEL_TYPES:
            average_price = self.calculate_average(self.fuel_data[fuel_type])
            output += f"{fuel_type}: {average_price}\n"
        return output

    def generate_min_max_prices(self):
        """Generate min/max prices section for each fuel type."""
        output = '\n****** MIN / MAX ******\n'
        for fuel_type in FUEL_TYPES:
            min_price, max_price = self.calculate_min_max(self.fuel_data[fuel_type])
            if min_price and max_price:
                output += (
                    f"{fuel_type}: {min_price[0]} ({min_price[1]}) - {max_price[0]} ({max_price[1]})\n"
                )
        return output

    def generate_station_details(self):
        """Generate details of station brands and types."""
        output = '\n****** STATIONS ******\n'
        for brand, count in self.brand_counts.items():
            output += f"{brand}: {count}\n"

        output += '\n****** STATION TYPES ******\n'
        for station_type, count in self.station_types.items():
            output += f"{station_type}: {count}\n"
        return output

    def generate_average_prices_by_station(self):
        """Generate average fuel prices grouped by station brand."""
        output = '\n****** AVERAGE FUEL PRICES BY STATION ******\n'
        for brand, fuel_prices in self.fuel_prices_by_station.items():
            output += f"{brand}:\n"
            for fuel_type in FUEL_TYPES:
                prices = [fuel['price'] for station in fuel_prices for fuel in station if fuel['tag'] == fuel_type]
                if prices:
                    average_price = round(sum(prices) / len(prices), 3)
                    comparison = "above average" if average_price > self.calculate_average(self.fuel_data[fuel_type]) else "below average"
                    output += f"\t{fuel_type}: {average_price} ({comparison})\n"
        return output

    def generate_average_prices_by_region(self):
        """Generate average fuel prices grouped by region."""
        output = '\n****** AVERAGE FUEL PRICES BY REGION ******\n'
        for region, fuel_prices in self.fuel_prices_by_region.items():
            output += f"{region}:\n"
            for fuel_type in FUEL_TYPES:
                prices = [fuel['price'] for station in fuel_prices for fuel in station if fuel['tag'] == fuel_type]
                if prices:
                    average_price = round(sum(prices) / len(prices), 3)
                    comparison = "above average" if average_price > self.calculate_average(self.fuel_data[fuel_type]) else "below average"
                    output += f"\t{fuel_type}: {average_price} ({comparison})\n"
        return output


if __name__ == "__main__":
    file_path = './stations.csv'
    processor = FuelDataProcessor()
    processor.read_and_process_csv(file_path)
