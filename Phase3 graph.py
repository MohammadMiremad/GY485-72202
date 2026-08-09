# import geopandas as gpd
# import matplotlib.pyplot as plt
# import numpy as np
# import pandas as pd
# from shapely.geometry import Point
# import seaborn as sns

# # 1. Load Excel file using full correct path
# excel_path = r"C:\Users\ABC\Desktop\thesis 2\LULC tif\galougah_ready_for_regression.xlsx"
# df = pd.read_excel(excel_path)
# df["log_price"] = np.log(df["Residential_IRR-real deal"].replace(0, np.nan))

# # 2. Load the Urban Expansion Frontier Shapefile created in Phase 3
# frontier_shp_path = (
#     r"C:\Users\ABC\Desktop\thesis 2\LULC tif\urban_expansion_frontier.shp"
# )
# frontier_gdf = gpd.read_file(frontier_shp_path)

# # 3. Create GeoDataFrame for blocks and project both to UTM Zone 39N (EPSG:32639)
# geometry = [Point(xy) for xy in zip(df["longitude"], df["latitude"])]
# blocks_gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326").to_crs(
#     "EPSG:32639"
# )
# frontier_gdf = frontier_gdf.to_crs("EPSG:32639")

# # 4. Calculate exact minimum distance from each block to the Urban Expansion Frontier (in kilometers)
# blocks_gdf["distance_to_frontier"] = blocks_gdf.geometry.apply(
#     lambda geom: frontier_gdf.geometry.unary_union.distance(geom) / 1000.0
# )

# # 5. Plotting regression plots using seaborn
# sns.set_theme(style="whitegrid")
# fig, axes = plt.subplots(1, 2, figsize=(14, 6), dpi=300)

# # Plot 1: Distance to Frontier vs Log Residential Price
# sns.regplot(
#     data=blocks_gdf,
#     x="distance_to_frontier",
#     y="log_price",
#     ax=axes[0],
#     scatter_kws={"alpha": 0.7, "color": "#1f77b4"},
#     line_kws={"color": "#d62728", "linewidth": 2},
# )
# axes[0].set_title(
#     "Distance to Urban Expansion Frontier vs. Log Price",
#     fontsize=12,
#     fontweight="bold",
#     pad=15,
# )
# axes[0].set_xlabel(
#     "Distance to Urban Expansion Frontier (km)", fontsize=10, fontweight="bold"
# )
# axes[0].set_ylabel(
#     "Log Residential Real Deal Price", fontsize=10, fontweight="bold"
# )

# # Plot 2: Distance to Frontier vs GI Buffer (500m)
# sns.regplot(
#     data=blocks_gdf,
#     x="distance_to_frontier",
#     y="gi_buffer_500",
#     ax=axes[1],
#     scatter_kws={"alpha": 0.7, "color": "#2ca02c"},
#     line_kws={"color": "#d62728", "linewidth": 2},
# )
# axes[1].set_title(
#     "Distance to Urban Expansion Frontier vs. GI Buffer (500m)",
#     fontsize=12,
#     fontweight="bold",
#     pad=15,
# )
# axes[1].set_xlabel(
#     "Distance to Urban Expansion Frontier (km)", fontsize=10, fontweight="bold"
# )
# axes[1].set_ylabel(
#     "Green Infrastructure Proportion (500m Buffer)",
#     fontsize=10,
#     fontweight="bold",
# )

# # 6. Save output plot
# plt.tight_layout()
# output_filename = (
#     r"C:\Users\ABC\Desktop\thesis 2\LULC tif\frontier_distance_regression_plot.png"
# )
# plt.savefig(output_filename, dpi=300)
# print(f"Plot successfully saved to: {output_filename}")
import os
import geopandas as gpd
import pandas as pd

# 1. Set working directory
working_directory = r"C:\Users\ABC\Desktop\thesis 2\LULC tif"
os.chdir(working_directory)

shapefile_name = "urban_expansion_frontier.shp"
excel_name = "urban_expansion_metrics.xlsx"

print(f"Loading {shapefile_name}...")
gdf_frontier = gpd.read_file(shapefile_name)

# 2. Calculate metrics and CREATE the Excel file
print("Calculating metrics and creating Excel file...")
frontier_length_m = gdf_frontier.geometry.length.sum()
frontier_length_km = frontier_length_m / 1e3

metrics_data = {
    "Metric": ["Urban Frontier Length (m)", "Urban Frontier Length (km)"],
    "Value": [frontier_length_m, frontier_length_km],
}

df_metrics = pd.DataFrame(metrics_data)
df_metrics.to_excel(
    excel_name, index=False
)  # This line creates and saves the Excel file
print(f"Excel file successfully created: {os.path.abspath(excel_name)}")

# 3. Transpose the metrics DataFrame so it becomes a single-row table with column names as metrics
df_transposed = df_metrics.set_index("Metric").T.reset_index(drop=True)

# Clean up column names to be shapefile-friendly
df_transposed.columns = [
    str(c)
    .strip()
    .replace(" ", "_")
    .replace("(", "")
    .replace(")", "")
    .replace("/", "_")
    for c in df_transposed.columns
]

# 4. Join/assign the metrics columns to every feature in the GeoDataFrame
for col in df_transposed.columns:
  gdf_frontier[col] = df_transposed[col].iloc[0]

# 5. Save the updated GeoDataFrame to a new shapefile
output_shapefile = "urban_expansion_frontier_with_metrics.shp"
gdf_frontier.to_file(output_shapefile)

print(
    "Successfully created Excel and merged metrics into the shapefile!"
    f"\nSaved at: {os.path.abspath(output_shapefile)}"
)