import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
shapefile_path = 'Shapefiles/Africa_Boundaries.shp'
african_map = gpd.read_file(shapefile_path)


########## INITIAL CODE ##########

# loading the data to be working with
df = pd.read_excel('Child-Health-Coverage-Database-May-2022.xlsx', 'ITN')
# selecting the categories to work with
categories = ['National', 'Male', 'Female', 'Rural', 'Urban', 'Poorest', 'Second', 'Middle', 'Fourth', 'Richest']
# grouping data by countries and years
df_countries = df.groupby(['ISO', 'Countries and areas', 'Year'])[categories].mean().reset_index()
df_countries.fillna(0, inplace=True)
# importing shapefile for African continent
african_continent = gpd.read_file('Shapefiles/Africa_Boundaries.shp')

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


    ######### NEW CODE ##########
df = pd.read_excel("/Users/hamenyimanagervas/PycharmProjects/ITN-Sheet-Test/Spatial Plotting Exercise/Child-Health-Coverage-Database-May-2022.xlsx", sheet_name=9)
# Extract the African countries, Create a GeoDataFrame with the country geometries and Group data by year
african_countries = df[df['UNICEF Reporting Region'].str.contains('Africa')]
african_countries_gdf = african_map[['ISO', 'geometry']].merge(african_countries, on='ISO')
grouped_by_year = african_countries_gdf.groupby('Year')

# Define the number of rows and columns for subplots
num_rows = 4
num_cols = 6
# Loop through each category
for category in categories:
    num_years = len(grouped_by_year)
    num_subplots = num_rows * num_cols
    num_figures = (num_years // num_subplots) + (1 if num_years % num_subplots > 0 else 0)

    for figure_index in range(num_figures):
        start_idx = figure_index * num_subplots
        end_idx = min((figure_index + 1) * num_subplots, num_years)

        fig, axs = plt.subplots(num_rows, num_cols, figsize=(15, 10))
        fig.suptitle(f'{category}', fontsize=16)

        # Create a common legend for each row
        cax = fig.add_axes([0.92, 0.2, 0.02, 0.6])

        for i, (year, data) in enumerate(grouped_by_year):
            if start_idx <= i < end_idx and not data[category].isnull().all():
                row = (i - start_idx) // num_cols
                col = (i - start_idx) % num_cols
                ax = axs[row, col]
                vmin, vmax = 0, 100
                data.plot(column=category, cmap='viridis', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True, cax=cax, vmin=vmin, vmax=vmax)
                ax.set_title(f'{year}')
                ax.set_aspect('equal')
                ax.set_xticks([])
                ax.set_yticks([])

        plt.tight_layout(rect=[0, 0, 0.9, 1])
        plt.savefig(f'{category}.png', dpi=300, bbox_inches='tight')