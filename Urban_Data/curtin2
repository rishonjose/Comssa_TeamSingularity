import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon

# Step 1: Load Data
# -----------------
# Load all datasets
nodes = pd.read_csv('node.csv')
links = pd.read_csv('link.csv')
zones = pd.read_csv('zone.csv')
demand = pd.read_csv('demand.csv')
pois = pd.read_csv('poi.csv')

# Step 2: Ensure Zone Geometry
# ----------------------------
# Create polygons from bounding box columns if 'geometry' or 'centroid' isn't usable
if 'centroid' in zones.columns:
    zones['geometry'] = gpd.GeoSeries.from_wkt(zones['centroid'])
else:
    zones['geometry'] = zones.apply(
        lambda row: Polygon([
            (row['x_min'], row['y_min']),
            (row['x_min'], row['y_max']),
            (row['x_max'], row['y_max']),
            (row['x_max'], row['y_min']),
            (row['x_min'], row['y_min'])
        ]),
        axis=1
    )
zones_gdf = gpd.GeoDataFrame(zones, geometry=zones['geometry'])

# Step 3: Calculate Node Degree and Identify Critical Nodes
# ---------------------------------------------------------
# Node degree based on connected links
node_degree = links.groupby('from_node_id').size().reset_index(name='degree')

# Identify critical nodes (degree > 3 for this example)
critical_nodes = node_degree[node_degree['degree'] > 3]
critical_nodes = pd.merge(
    critical_nodes,
    nodes,
    left_on='from_node_id',
    right_on='node_id',
    how='left'
)

# Step 4: Convert Critical Nodes to GeoDataFrame
# ----------------------------------------------
gdf_critical_nodes = gpd.GeoDataFrame(
    critical_nodes,
    geometry=gpd.points_from_xy(critical_nodes['x_coord'], critical_nodes['y_coord'])
)

# Step 5: Set Active Geometry and Create Buffers
# -----------------------------------------------
# Set buffer as active geometry for critical nodes
gdf_critical_nodes['buffer'] = gdf_critical_nodes.geometry.buffer(100)  # 100 meters radius
gdf_critical_nodes = gdf_critical_nodes.set_geometry('buffer')

# Ensure zone geometry is active
zones_gdf = zones_gdf.set_geometry('geometry')

# Step 6: Verify and Align CRS
# ----------------------------
# Ensure both GeoDataFrames have matching CRS
if gdf_critical_nodes.crs != zones_gdf.crs:
    gdf_critical_nodes = gdf_critical_nodes.to_crs(zones_gdf.crs)

# Step 7: Intersect Buffers with Zones and POIs
# ---------------------------------------------
# Perform overlay with zones and retain all geometries
zone_intersection = gpd.overlay(
    gdf_critical_nodes[['node_id', 'buffer']],
    zones_gdf,
    how='intersection',
    keep_geom_type=False  # Retain all geometry types
)

# Filter to include only polygons/multipolygons for area calculation
zone_intersection = zone_intersection[zone_intersection.geometry.type.isin(['Polygon', 'MultiPolygon'])]

# Calculate area of valid intersections
zone_intersection['zone_area'] = zone_intersection['geometry'].area

# Intersect with POIs to check proximity
pois_gdf = gpd.GeoDataFrame(
    pois,
    geometry=gpd.points_from_xy(pois['x_coord'], pois['y_coord'])
)
if gdf_critical_nodes.crs != pois_gdf.crs:
    pois_gdf = pois_gdf.to_crs(gdf_critical_nodes.crs)
poi_intersection = gpd.overlay(gdf_critical_nodes[['node_id', 'buffer']], pois_gdf, how='intersection', keep_geom_type=False)
poi_intersection['poi_count'] = poi_intersection.groupby('node_id')['poi_id'].transform('count')

# Step 8: Aggregate Area and POI Details
# ---------------------------------------
# Sum the available area for each critical node
area_details = zone_intersection.groupby('node_id')['zone_area'].sum().reset_index()

# Count POIs for each critical node
poi_details = poi_intersection.groupby('node_id').size().reset_index(name='poi_count')

# Merge area and POI details back with critical nodes
critical_nodes_with_stats = pd.merge(
    gdf_critical_nodes,
    area_details,
    on='node_id',
    how='left'
).merge(
    poi_details,
    on='node_id',
    how='left'
)

# Fill missing values with 0 (if no intersections occurred)
critical_nodes_with_stats['zone_area'] = critical_nodes_with_stats['zone_area'].fillna(0)
critical_nodes_with_stats['poi_count'] = critical_nodes_with_stats['poi_count'].fillna(0)

# Step 9: Print Results
# ---------------------
print("Critical Nodes with Zone Area and POI Count:")
print(critical_nodes_with_stats[['node_id', 'degree', 'zone_area', 'poi_count']])
