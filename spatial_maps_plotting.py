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
    years = [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017,
             2018, 2019, 2020, 2021]

    # determine the number of rows and columns for the subplots
    num_rows = 4
    num_cols = int(np.ceil(len(years) / num_rows))

    # create a grid of subplots
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 12))

    # flatten the axes array if necessary (in case num_rows * num_cols is greater than len(years))
    axes = axes.flatten()

    # iterate through the years and create subplots
    for i, year in enumerate(years):
        ax = axes[i]  # select the current subplot
        merged_data.plot(column=variable_of_interest, cmap='viridis' if year == 2000 else 'viridis', linewidth=0.8, ax=ax,
                         edgecolor='0.8', legend=True)

        # customize the plot
        ax.set_title(f'{variable_of_interest} in {year}')
        ax.axis('off')

    # remove any empty subplots (if num_rows * num_cols > len(years))
    for i in range(len(years), num_rows * num_cols):
        fig.delaxes(axes[i])

    # adjust spacing between subplots
    fig.tight_layout()

    # show the plot
    plt.show()

# call the function for 'National'
generate_plots('Male')