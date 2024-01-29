import pandas as pd
import matplotlib.pyplot as plt

def linePlot():
    """
        Generate a line plot to visualize birth and death rates over time.

        This function assumes the existence of the following variables:
        - indicators: List of indicators to be plotted.
        - pivot_table: Pandas DataFrame containing data for the specified indicators.
        - country: Name of the country for which the data is plotted.

        The function uses Matplotlib to create a line plot with years on the x-axis
        and rates on the y-axis for each specified indicator.

        Parameters:
        None

        Returns:
        None
    """
    plt.figure(figsize = (10 , 6))

    for indicator in indicators:
        plt.plot(pivot_table.index , pivot_table[indicator] , label = indicator)

    plt.title(f'{country} - Birth and Death Rates Over Time')
    plt.xlabel('Year')
    plt.ylabel('Rate')
    plt.legend()
    plt.grid(True)
    plt.show()


def scatterplot():
    """
        Generate a scatter plot to visualize the relationship between two indicators.

        This function assumes the existence of the following variables:
        - indicators: List of indicators to be plotted.
        - pivot_table: Pandas DataFrame containing data for the specified indicators.

        The function uses Seaborn and Matplotlib to create a scatter plot with one
        indicator on the x-axis, another on the y-axis, and colors representing different
        countries over time.

        Parameters:
        None

        Returns:
        None
    """
    # Set up the figure
    fig , ax = plt.subplots(figsize = (12, 8))

    # Scatter plot using Matplotlib
    for country , color in zip(pivot_table.index , plt.cm.viridis.colors):
        subset = pivot_table[pivot_table.index == country]
        ax.scatter(subset[indicators[0]] , subset[indicators[1]] , label = country , color = color)

    # Set title and labels
    ax.set_title(f'Scatter Plot: {indicators[0]} vs. {indicators[1]} by Country')
    ax.set_xlabel(indicators[0])
    ax.set_ylabel(indicators[1])

    # Add legend
    ax.legend(title = 'Country' , bbox_to_anchor = (1 , 1))

    # Show the plot
    plt.show()


def barplot():
    """
        Generate a stacked bar plot to visualize CO2 emissions from different fuel types.

        This function assumes the existence of the following variables:
        - pivot_table: Pandas DataFrame containing data for CO2 emissions from different fuel types.
        - year: The specific year for which the data is plotted.

        The function uses Matplotlib to create a stacked bar plot, where each country is represented
        with bars stacked for different fuel types.

        Parameters:
        None

        Returns:
        None
    """
    plt.figure(figsize = (12 , 8))
    pivot_table.plot(kind = 'bar' , stacked = True , colormap = 'viridis')
    plt.title(f'CO2 Emissions from Different Fuel Types in {year}')
    plt.xlabel('Country')
    plt.ylabel('CO2 Emissions (kt)')
    plt.legend(title = 'Fuel Type' , bbox_to_anchor = (1 , 1))
    plt.show()


# Read the CSV file into a pandas DataFrame
d = pd.read_csv('./WDIData_T.csv')

# Display the first few rows of the DataFrame
print(d.head())

# Calculate the mean value for a specific indicator
mean_birth_rate = d[d['IndicatorName'] == 'Birth rate, crude (per 1,000 people)']['Value'].mean()
print(f"Mean Birth Rate: {mean_birth_rate}")

# Select data for specific indicators and country
indicators = ['Birth rate, crude (per 1,000 people)' , 'Death rate, crude (per 1,000 people)']
country = 'Arab World'
f = d[(d['CountryName'] == country) & (d['IndicatorName'].isin(indicators))]

# Pivot the data for better plotting
pivot_table = f.pivot_table('Value' , 'Year' , 'IndicatorName' , 'mean')

linePlot()

# Select data for birth rate and life expectancy
indicators = ['Birth rate, crude (per 1,000 people)' , 'Life expectancy at birth, total (years)']
f = d[(d['IndicatorName'].isin(indicators))]

# Pivot the data for plotting
pivot_table = f.pivot_table('Value' , 'CountryName' , 'IndicatorName' , 'mean')

scatterplot()

# Select data for CO2 emissions from different fuel types in a specific year
year = 1960
f_data = d[(d['IndicatorCode'].str.startswith('EN.ATM') & (d['Year'] == year))]

# Pivot the data for plotting
pivot_table = f_data.pivot_table('Value' , 'CountryName' , 'IndicatorName' , 'sum')
pivot_table = pivot_table.head(10)
barplot()
