from fuel_data_object import fuel_data
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

class ShowDiagrams:
    def __init__(self, fuel_data):
        # Store fuel darta and create a DataFrame from it
        self.fuel_data = fuel_data 
        self.df = pd.DataFrame(list(self.fuel_data["average_prices"].items()), columns=["Fuel type", "Average price"])


    def plot_summary_pie_chart(self):
        # Extract the total number of stations and stations without fuel data
        total_stations = self.fuel_data["summary"]["total_stations"]
        stations_without_fuel_data = self.fuel_data["summary"]["stations_without_fuel_data"]
        stations_with_fuel_data = total_stations - stations_without_fuel_data

        # Data for the pie chart
        labels = ["Asemia joilla on hintatiedot", "Asemia ilman hintatietoja"]
        sizes = [stations_with_fuel_data, stations_without_fuel_data]
        colors = ['skyblue', 'orange']

        # Create a pie chart for the summary data
        plt.figure(figsize=(6, 6))
        plt.pie(sizes, labels=labels, colors=colors, autopct=lambda pct: f'{int(pct/100 * total_stations)}', 
        pctdistance=0.80, startangle=90, wedgeprops=dict(width=0.4))
        plt.title(f'Bensa-asemia yhteensä Suomessa: {total_stations}')
        plt.tight_layout()


    def plot_bar_chart(self):
        # Create a bar chart for average prices
        bars = plt.bar(self.df["Fuel type"], self.df["Average price"], color="skyblue")
        plt.xlabel("Polttoainetyypit")
        plt.ylabel("Keskiverto hinta (€/l)")
        plt.title("Keskiverto hinta eri polttoainetyypeille Suomessa")

        # Set custom labels for the x-axis and rotate them for better readability
        new_labels = ['95', '98', '98+', '85', 'Diesel', 'Diesel+', 'HVO', 'Biokaasu']
        plt.xticks(ticks=range(len(self.df["Fuel type"])), labels=new_labels, rotation=45)

        # Add the exact price values on top of the bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, height - 0.15, f'{height:.3f}', ha='center', va='bottom', color='black')

        plt.tight_layout()


    def plot_pie_chart(self):
        # Extract the number of stations for each gas station chain
        number_of_stations = self.fuel_data["stations"]
        labels = list(number_of_stations.keys())
        sizes = list(number_of_stations.values())

        # Ensure sizes are numeric (convert them to int, filter out non-numeric)
        sizes = []
        for size in number_of_stations.values():
            try:
                sizes.append(int(size))
            except ValueError:
                print(f"Non-numeric value found: {size}")

        # Combine into a list of tuples and sort by station count in descending order
        station_data = sorted(zip(sizes, labels), reverse=True)

        # Keep top 10 and group the rest into "Others"
        top_10 = station_data[:10]
        others = station_data[10:]

        # Separate sizes and labels for the top 10, ensure there are top 10 items
        if top_10:
            top_sizes, top_labels = zip(*top_10)
        else:
            top_sizes, top_labels = [], []

        # Sum the sizes of the "Muut" group (ensure sizes are integers)
        other_size = sum(size for size, _ in others) if others else 0  # Safely handle as int
        top_sizes = list(top_sizes) + [other_size]
        top_labels = list(top_labels) + ["Muut"]

        # Create a new figure for the pie chart with specific size
        plt.figure(figsize=(12, 10))
        plt.subplots_adjust(right=0.6)

        # Create the pie chart with top 10 + "Muut"
        wedges, _ = plt.pie(top_sizes, colors=plt.cm.Paired.colors, startangle=140)
        custom_labels = [f"{label}: {count}" for label, count in zip(top_labels, top_sizes)]

        # Add legends with custom labels
        plt.legend(wedges, custom_labels, title="Bensa-asemaketjut ja niiden määrät", loc="center left", bbox_to_anchor=(0.95, 0.5), ncol=2)
        plt.title("Eri bensa-asemaketjujen määrät Suomessa (top 10)")
        plt.axis('equal')
        plt.tight_layout()


    def plot_station_prices(self):
        # Filter out stations with no price data
        average_fuel_prices_by_station = self.fuel_data["average_fuel_prices_by_station"]
        filtered_station_data = {station: prices for station, prices in average_fuel_prices_by_station.items() if prices}

        # Select fuel types for comparison and define new labels
        fuel_types = ["95", "98", "dsl", "bgas"]
        new_labels = ["95", "98", "Diesel", "Biokaasu"]

        # Filter station data to include only relevant fuel types
        stations = list(filtered_station_data.keys())
        prices = np.array([[filtered_station_data[station].get(fuel, np.nan) for fuel in fuel_types] for station in stations])

        # Create a heatmap
        plt.figure(figsize=(10, 8))
        sns.heatmap(prices, annot=np.round(prices, 3), fmt=".3f", cmap="coolwarm", xticklabels=new_labels, yticklabels=stations, cbar_kws={'label': 'Hinta (€)'})

        plt.title("Keskimääräiset polttoainehinnat eri bensa-asemilla Suomessa")
        plt.xlabel("Polttoainetyypit")
        plt.ylabel("Bensa-asemat")
        plt.tight_layout()

    def plot_average_region_fuels_prices(self):
        # Extract average fuel prices by region, define relevant fuel types and new labels
        region_prices = self.fuel_data["average_fuel_prices_by_region"]
        regions = list(region_prices.keys())
        relevant_fuel_types = ["95", "98", "dsl"]
        new_labels = ["95", "98", "Diesel"]

        # Create a array of prices for the relevant fuel types 
        prices = np.array([[region_prices[region].get(fuel, 0) for fuel in relevant_fuel_types] for region in regions])

        # Create a bar chart for average prices by region
        bar_width = 0.15
        x = np.arange(len(regions))
        plt.figure(figsize=(14, 8))

        # Plot the bars for each fuel type 
        for i, fuel in enumerate(relevant_fuel_types):
            bar = plt.bar(x + i * bar_width, prices[:, i], bar_width, label=fuel)

            # Add the price values on top of the bars
            for rectangle in bar:
                height = rectangle.get_height()
                plt.text(rectangle.get_x() + rectangle.get_width() / 2, height, 
                f'{height:.3f}', ha='center', va='bottom', color='black', fontsize=6)

        # Set the labels and title
        plt.xlabel("Maakunnat")
        plt.ylabel("Keskiverto hinta (€/l)")
        plt.title("Keskiverto hinta yleisimmille polttoainetyypeille maakunnittain Suomessa")
        plt.xticks(x + bar_width * (len(relevant_fuel_types) - 1) / 2, labels=regions, rotation=55)
        plt.legend(title="Polttoainetyypit", labels=new_labels, loc="upper right", bbox_to_anchor=(1.2, 1))
        plt.tight_layout()


    def plot_horiz_bar_chart(self):
        # Extract min and max prices for each fuel type
        min_max_prices = self.fuel_data["min_max_prices"]

        # Create lists for fuel types, min prices, and max prices
        fuel_types = list(min_max_prices.keys())
        min_prices = [data["min"]["price"] for data in min_max_prices.values()]
        max_prices = [data["max"]["price"] for data in min_max_prices.values()]
        min_labels = [f'{min_max_prices[fuel]["min"]["price"]} ({min_max_prices[fuel]["min"]["location"]})' for fuel in fuel_types]
        max_labels = [f'{min_max_prices[fuel]["max"]["price"]} ({min_max_prices[fuel]["max"]["location"]})' for fuel in fuel_types]

        bar_width = 0.4
        y_positions = np.arange(len(fuel_types))
        fig, ax = plt.subplots(figsize=(10, 6))

        # Plot min and max prices
        min_bars = ax.barh(y_positions - bar_width / 2, min_prices, bar_width, label='Matalin hinta', color='skyblue')
        max_bars = ax.barh(y_positions + bar_width / 2, max_prices, bar_width, label='Korkein hinta', color='orange')

        # Add labels to the bars
        for i, bar in enumerate(min_bars):
            ax.text(bar.get_width() - 0.5, bar.get_y() + bar.get_height() / 2, min_labels[i], va='center', ha='left', color='black')

        for i, bar in enumerate(max_bars):
            ax.text(bar.get_width() - 0.5, bar.get_y() + bar.get_height() / 2, max_labels[i], va='center', ha='left', color='black')

        # Set y-ticks and labels
        ax.set_yticks(y_positions)
        ax.set_yticklabels(fuel_types)

        # Set axis labels and title
        ax.set_xlabel('Hinta (€/l)')
        ax.set_title('Matalimmat ja korkeimmat hinnat eri polttoainetyypeille Suomessa')

        # Set x-axis limits manually to fit the data
        plt.xlim(0, max(max_prices) + 0.5)

        # Add legend
        ax.legend()
        plt.tight_layout()


    def plot_manned_vs_unmannded_stations(self):
        # Extract fuel prices for manned and unmanned stations
        station_prices = self.fuel_data["fuel_prices_by_station"]
        fuel_types = list(station_prices["unmanned"].keys())
        unmanned_prices = station_prices["unmanned"]
        manned_prices = station_prices["manned"]

        # Define custom labels for the fuel types
        custom_labels = ["95", "98", "98+", "85", "Diesel", "Diesel+", "HVO", "Biokaasu"]

        # Get the prices for each fuel type, fill missing values with 0
        unmanned_prices = [unmanned_prices.get(fuel, 0) for fuel in fuel_types]
        manned_prices = [manned_prices.get(fuel, 0) for fuel in fuel_types]

        # Create a bar chart for manned and unmanned stations 
        x = np.arange(len(fuel_types))
        width = 0.35
        fig, ax = plt.subplots(figsize=(10, 6))
        rect1 = ax.bar(x - width / 2, unmanned_prices, width, label='Kylmäasema', color='skyblue')
        rect2 = ax.bar(x + width / 2, manned_prices, width, label='Miehitetty', color='orange')

        # Add the exact price values on top of the bars
        for rect in rect1: 
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2, height, f'{height:.3f}', ha='center', va='bottom', color='black')

        for rect in rect2: 
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2, height + 0.01, f'{height:.3f}', ha='center', va='bottom', color='black')            

        # Set the labels and title
        ax.set_xlabel('Polttoainetyypit')
        ax.set_ylabel('Keskiverto hinta (€/l)')
        ax.set_title('Keskiverto hinta kylmä- ja miehitetyillä asemilla Suomessa')
        ax.set_xticks(x)
        ax.set_xticklabels(custom_labels)
        ax.legend()
        plt.tight_layout()

        

# Create an instance of ShowDiagrams with the entire fuel_data object
visualizer = ShowDiagrams(fuel_data)

# Plot the pie chart for the summary data and show it
visualizer.plot_summary_pie_chart()
plt.show()

# Plot the bar chart for average prices and show it
visualizer.plot_bar_chart()
plt.show()

# Plot the bar chart for average prices by region and show it
visualizer.plot_average_region_fuels_prices()
plt.show()

# Plot the pie chart for the number of gas stations and show it
visualizer.plot_pie_chart()
plt.show()

# Plot the heatmap for station prices and show it
visualizer.plot_station_prices()
plt.show()

# Plot the bar chart for manned vs. unmanned stations and show it
visualizer.plot_manned_vs_unmannded_stations()
plt.show()

# Plot the horizontal bar chart for min and max prices and show it
visualizer.plot_horiz_bar_chart()
plt.show()