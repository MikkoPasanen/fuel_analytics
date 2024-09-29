from fuel_data_object import fuel_data
import pandas as pd
import matplotlib.pyplot as plt

class ShowDiagrams:
    def __init__(self, fuel_data):
        # Store fuel darta and create a DataFrame from it
        self.fuel_data = fuel_data 
        self.df = pd.DataFrame(list(self.fuel_data["average_prices"].items()), columns=["Fuel type", "Average price"])

    def plot_bar_chart(self):
        # Create a bar chart for average prices
        plt.bar(self.df["Fuel type"], self.df["Average price"], color="skyblue")
        plt.xlabel("Fuel type")
        plt.ylabel("Average price (€/l)")
        plt.title("Average fuel prices in Finland")

        # Set custom labels for the x-axis and rotate them for better readability
        new_labels = ['95', '98', '98+', '85', 'Diesel', 'Diesel+', 'HVO', 'Biogas']
        plt.xticks(ticks=range(len(self.df["Fuel type"])), labels=new_labels, rotation=45)
        plt.tight_layout()

    def plot_pie_chart(self):
        # Extract the number of stations for each gas station chain
        number_of_stations = self.fuel_data["stations"]
        labels = list(number_of_stations.keys())
        sizes = list(number_of_stations.values())
        colors = plt.cm.Paired.colors
        
        # Create a new figure for the pie chart with specific size
        plt.figure(figsize=(12, 10))
        plt.subplots_adjust(right=0.6)

        # Create the pie chart with custom labels
        wedges, _ = plt.pie(sizes, colors=colors, startangle=140)
        custom_labels = [f"{label}: {count}" for label, count in zip(labels, sizes)]

        # Add legends with custom labels
        plt.legend(wedges, custom_labels, title="Gas station chains and the amounts", loc="center left", bbox_to_anchor=(0.95, 0.5), ncol=2)
        plt.title("Different gas station chains in Finland")
        plt.axis('equal')
        plt.tight_layout()

    def plot_horiz_bar_chart(self):
        # Extract min and max prices for each fuel type
        min_max_prices = self.fuel_data["min_max_prices"]

        # Create lists for fuel types, min prices, and max prices
        fuel_types = list(min_max_prices.keys())
        min_prices = [data["min"]["price"] for data in min_max_prices.values()]
        max_prices = [data["max"]["price"] for data in min_max_prices.values()]

        # Create a horizontal bar chart for min and max prices
        plt.figure(figsize=(10, 6))
        bar_width = 0.35
        index = range(len(fuel_types))

        # Plot the horizontal bar chart with min and max prices
        plt.barh(index, min_prices, bar_width, color="skyblue", label="Min prices")
        plt.barh(index, max_prices, bar_width, color="orange", label="Max prices", left=min_prices)

        # Add labels and legends to the chart
        plt.yticks(index, fuel_types)
        plt.xlabel("Price (€/l)")
        plt.title("Min and max prices for different fuel types")
        plt.legend()

        # Add text labels for min and max prices with locations
        for i, fuel in enumerate(fuel_types):
            plt.text(min_prices[i] / 2, i, f"{min_prices[i]:.2f} ({min_max_prices[fuel]['min']['location']})", ha='center', va='center', color='black')
            plt.text(min_prices[i] + max_prices[i] / 2, i, f"{max_prices[i]:.2f} ({min_max_prices[fuel]['max']['location']})", ha='center', va='center', color='black')

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