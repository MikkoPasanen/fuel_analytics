from fuel_data_object import fuel_data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class ShowDiagrams:
    def __init__(self, fuel_data):
        # Store fuel darta and create a DataFrame from it
        self.fuel_data = fuel_data 
        self.df = pd.DataFrame(list(self.fuel_data["average_prices"].items()), columns=["Fuel type", "Average price"])


    def plot_bar_chart(self):
        # Create a bar chart for average prices
        plt.bar(self.df["Fuel type"], self.df["Average price"], color="skyblue")
        plt.xlabel("Polttoainetyypit")
        plt.ylabel("Keskiverto hinta (€/l)")
        plt.title("Keskiverto hinta eri polttoainetyypeille Suomessa")

        # Set custom labels for the x-axis and rotate them for better readability
        new_labels = ['95', '98', '98+', '85', 'Diesel', 'Diesel+', 'HVO', 'Biokaasu']
        plt.xticks(ticks=range(len(self.df["Fuel type"])), labels=new_labels, rotation=45)
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

        # Separate sizes and labels for the top 10
        if top_10:  # Ensure there are top 10 items
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

        # Plot min prices
        min_bars = ax.barh(y_positions - bar_width / 2, min_prices, bar_width, label='Matalin hinta', color='skyblue')

        # Plot max prices
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



# Create an instance of ShowDiagrams with the entire fuel_data object
visualizer = ShowDiagrams(fuel_data)

# Plot the bar chart for average prices and show it
visualizer.plot_bar_chart()
plt.show()

# Plot the pie chart for the number of gas stations and show it
visualizer.plot_pie_chart()
plt.show()

# Plot the horizontal bar chart for min and max prices and show it
visualizer.plot_horiz_bar_chart()
plt.show()