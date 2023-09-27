import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
shapefile_path = 'Africa_Boundaries.shp'
gdf = gpd.read_file(shapefile_path)

df = pd.read_excel("/Users/hamenyimanagervas/PycharmProjects/ITN-Sheet-Test/Spatial Plotting Exercise1/Child-Health-Coverage-Database-May-2022.xlsx", sheet_name=9)
categories = ['National', 'Male', 'Female', 'Rural', 'Urban', 'Poorest', 'Second', 'Middle', 'Fourth', 'Richest']

df['Region'] = df['UNICEF Reporting Region'].apply(lambda x: x.split(' ')[-1])
df_africa = df[df['Region'] == 'Africa']
df_africa['Countries and areas'] = df_africa['Countries and areas'].astype(str)

merged_gdf = gdf.copy()
# Looping each category
for category in categories:
    category_data = df_africa[['Countries and areas', 'Year', category]]
    category_gdf = gpd.GeoDataFrame(category_data, geometry=None)
    merged_gdf = pd.concat([merged_gdf, category_gdf], axis=1)

for category in categories:
    #Choropleth map
    fig, ax = plt.subplots(1, 1, figsize=(12, 12))
    merged_gdf.plot(column=category, cmap='viridis', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)
    vmin = merged_gdf[category].min()

    ax.set_title(category)
    plt.savefig(f'{category}', dpi=300, bbox_inches='tight')
    plt.close()

