# importing the required modules
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# loading the data to be working with
df = pd.read_excel('Child-Health-Coverage-Database-May-2022.xlsx', 'ITN')

# selecting the categories to work with
categories = ['National', 'Male', 'Female', 'Rural', 'Urban', 'Poorest', 'Second', 'Middle', 'Fourth', 'Richest']

# grouping data by countries and years
df_countries = df.groupby(['ISO', 'Countries and areas', 'Year'])[categories].mean().reset_index()
df_countries.fillna(0, inplace=True)

# importing shapefile for African continent
african_continent = gpd.read_file('Africa_Boundaries.shp')

# merging the data
merged_data = african_continent.merge(df_countries, on='ISO', how='outer')

# create a function to generate plots for a given variable_of_interest
def generate_plots(variable_of_interest):
    years = list(range(2000, 2022))  # generate the list of years from 2000 to 2021

    # determine the number of rows and columns for the subplots
    num_rows = 4
    num_cols = int(np.ceil(len(years) / num_rows))

    # create a grid of subplots
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 12))

    # flatten the axes array if necessary
    axes = axes.flatten()

    # iterate through the years and create subplots
    for i, year in enumerate(years):
        ax = axes[i]  # select the current subplot
        merged_data.plot(column=variable_of_interest, cmap='viridis', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)

        # customize the plot
        ax.set_title(f'{variable_of_interest} in {year}')
        ax.axis('off')

    # remove any empty subplots
    for i in range(len(years), num_rows * num_cols):
        fig.delaxes(axes[i])

    # adjust spacing between subplots
    fig.tight_layout()

    # save the plot as an image
    filename = f'{variable_of_interest}_plot.png'
    plt.savefig(filename, dpi=300)  # adjust dpi as needed for high-quality images

    # show the plot
    plt.show()

# loop through the list of variables and generate plots
for category in categories:
    generate_plots(category)