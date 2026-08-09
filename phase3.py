# import os
# import geopandas as gpd
# import numpy as np
# import rasterio
# from rasterio.features import shapes
# from shapely.geometry import MultiPolygon, shape
# from shapely.ops import unary_union

# # 1. Set working directory
# working_directory = r"C:\Users\ABC\Desktop\thesis 2\LULC tif"
# os.chdir(working_directory)

# # 2. Define the target LULC raster file (e.g., 2030 prediction or baseline raster)
# raster_file = "LULC_2030_StateOfTheArt_Predicted.tif"

# # 3. Define the built-up class value in your raster classification scheme
# # (Note: Depending on your dataset, built-up class might be 1, 2, or 6. Adjust if needed.)
# built_up_class_value = 1

# print(f"Opening raster file: {raster_file}")
# with rasterio.open(raster_file) as src:
#   image = src.read(1)
#   transform = src.transform
#   crs = src.crs

#   # Extract shapes (vectorize raster pixels) for the built-up class
#   mask = image == built_up_class_value
#   shape_generator = shapes(image, mask=mask, transform=transform)

#   # Convert extracted shapes into Shapely geometries
#   geoms = [shape(geom) for geom, val in shape_generator if val == 1]

# if len(geoms) == 0:
#   print(
#       "Warning: No patches found for the specified built-up class value. Please"
#       " verify 'built_up_class_value'."
#   )
# else:
#   print(
#       f"Extracted {len(geoms)} built-up patches. Performing spatial union..."
#   )

#   # 4. Aggregate patches via spatial union (Equation 3: unary union of built-up patches)
#   multi_poly = MultiPolygon(geoms)
#   aggregated_builtin = unary_union(multi_poly)

#   # 5. Extract the outer geometric boundary (Urban Expansion Frontier: Ω_frontier)
#   frontier_boundary = aggregated_builtin.boundary

#   # 6. Create GeoDataFrames and project to UTM Zone 39N (EPSG:32639)
#   gdf_frontier = gpd.GeoDataFrame(geometry=[frontier_boundary], crs=crs).to_crs(
#       "EPSG:32639"
#   )
#   gdf_polygon = gpd.GeoDataFrame(
#       geometry=[aggregated_builtin], crs=crs
#   ).to_crs("EPSG:32639")

#   # 7. Export results to Shapefiles
#   output_frontier = "urban_expansion_frontier.shp"
#   output_polygon = "urban_expansion_polygon.shp"

#   gdf_frontier.to_file(output_frontier)
#   gdf_polygon.to_file(output_polygon)

#   print(
#       f"Phase 3 completed successfully!\n- Frontier boundary saved at:"
#       f" {os.path.abspath(output_frontier)}\n- Aggregated polygon saved at:"
#       f" {os.path.abspath(output_polygon)}"
#   )
import os
import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from rasterio.features import shapes
from shapely.geometry import MultiPolygon, shape
from shapely.ops import unary_union

# 1. Set working directory
working_directory = r"C:\Users\ABC\Desktop\thesis 2\LULC tif"
os.chdir(working_directory)

# 2. Define the target LULC raster file (e.g., 2030 prediction or baseline raster)
raster_file = "LULC_2030_StateOfTheArt_Predicted.tif"

# 3. Define the built-up class value in your raster classification scheme
built_up_class_value = 1

print(f"Opening raster file: {raster_file}")
with rasterio.open(raster_file) as src:
    image = src.read(1)
    transform = src.transform
    crs = src.crs

    # Extract shapes (vectorize raster pixels) for the built-up class
    mask = image == built_up_class_value
    shape_generator = shapes(image, mask=mask, transform=transform)

    # Convert extracted shapes into Shapely geometries
    geoms = [shape(geom) for geom, val in shape_generator if val == 1]

if len(geoms) == 0:
    print(
        "Warning: No patches found for the specified built-up class value. Please verify 'built_up_class_value'."
    )
else:
    print(f"Extracted {len(geoms)} built-up patches. Performing spatial union...")

    # 4. Aggregate patches via spatial union (Equation 3: unary union of built-up patches)
    multi_poly = MultiPolygon(geoms)
    aggregated_builtin = unary_union(multi_poly)

    # 5. Extract the outer geometric boundary (Urban Expansion Frontier: Ω_frontier)
    frontier_boundary = aggregated_builtin.boundary

    # 6. Create GeoDataFrames and project to UTM Zone 39N (EPSG:32639)
    gdf_frontier = gpd.GeoDataFrame(geometry=[frontier_boundary], crs=crs).to_crs(
        "EPSG:32639"
    )
    gdf_polygon = gpd.GeoDataFrame(
        geometry=[aggregated_builtin], crs=crs
    ).to_crs("EPSG:32639")

    # 7. Export results to Shapefiles
    output_frontier = "urban_expansion_frontier.shp"
    output_polygon = "urban_expansion_polygon.shp"

    gdf_frontier.to_file(output_frontier)
    gdf_polygon.to_file(output_polygon)

    print(
        f"Phase 3 completed successfully!\n- Frontier boundary saved at: {os.path.abspath(output_frontier)}\n- Aggregated polygon saved at: {os.path.abspath(output_polygon)}"
    )

# 8. Calculate spatial metrics for Excel export
polygon_area_m2 = aggregated_builtin.area
polygon_area_km2 = polygon_area_m2 / 1e6
frontier_length_m = frontier_boundary.length
frontier_length_km = frontier_length_m / 1e3

# 9. Compile metrics into a DataFrame
metrics_data = {
    "Metric": [
        "Raster File",
        "Built-up Class Value",
        "Total Built-up Patches Count",
        "Urban Expansion Area (m2)",
        "Urban Expansion Area (km2)",
        "Urban Frontier Length (m)",
        "Urban Frontier Length (km)",
    ],
    "Value": [
        raster_file,
        built_up_class_value,
        len(geoms),
        polygon_area_m2,
        polygon_area_km2,
        frontier_length_m,
        frontier_length_km,
    ],
}

df_metrics = pd.DataFrame(metrics_data)

# 10. Export metrics to an Excel file
output_excel = "urban_expansion_metrics.xlsx"
df_metrics.to_excel(output_excel, index=False)

print(f"Excel metrics file successfully saved at: {os.path.abspath(output_excel)}")