import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString, Point
import matplotlib.pyplot as plt

# Step 1: Load the Data with Error Handling
# -----------------------------------------
try:
    links = pd.read_csv('Urban_Data/csv/link.csv', delimiter=',', encoding='utf-8', error_bad_lines=False)
    nodes = pd.read_csv('Urban_Data/csv/node.csv', delimiter=',', encoding='utf-8', error_bad_lines=False)
    demand = pd.read_csv('Urban_Data/csv/demand.csv', delimiter=',', encoding='utf-8', error_bad_lines=False)
except Exception as e:
    print(f"Error reading CSV files: {e}")
    exit()

# Step 2: Check Data Consistency
# ------------------------------
# Ensure necessary columns exist in the data
required_columns_links = ['link_id', 'from_node_id', 'to_node_id', 'lanes', 'free_speed', 'geometry']
required_columns_nodes = ['node_id', 'x_coord', 'y_coord']
required_columns_demand = ['o_zone_id', 'd_zone_id', 'volume']

for col in required_columns_links:
    if col not in links.columns:
        print(f"Missing column '{col}' in link.csv")
        exit()

for col in required_columns_nodes:
    if col not in nodes.columns:
        print(f"Missing column '{col}' in node.csv")
        exit()

for col in required_columns_demand:
    if col not in demand.columns:
        print(f"Missing column '{col}' in demand.csv")
        exit()

# Step 3: Calculate Road Capacity
# -------------------------------
# Estimate road capacity (simple formula: lanes * free_speed * constant)
links['capacity'] = links['lanes'] * links['free_speed'] * 10  # Constant = 10 for simplicity

# Step 4: Aggregate Traffic Demand on Links
# -----------------------------------------
# Group demand by origin-destination and sum up traffic volumes
demand_summary = demand.groupby(['o_zone_id', 'd_zone_id'])['volume'].sum().reset_index()

# Merge demand with link data (assign traffic demand to links)
traffic_on_links = pd.merge(
    demand_summary, 
    links, 
    left_on='o_zone_id', 
    right_on='from_node_id', 
    how='left'
)

# Handle potential NaN values after merging
traffic_on_links['volume'] = traffic_on_links['volume'].fillna(0)
traffic_on_links['capacity'] = traffic_on_links['capacity'].fillna(1)  # Avoid division by zero

# Step 5: Compute Link Utilization
# --------------------------------
# Calculate utilization: traffic demand / capacity
traffic_on_links['utilization'] = traffic_on_links['volume'] / traffic_on_links['capacity']

# Identify overloaded links (utilization > 1)
overloaded_links = traffic_on_links[traffic_on_links['utilization'] > 1]

# Step 6: Identify Critical Nodes
# --------------------------------
# Find nodes with high degrees of overloaded links
critical_nodes = overloaded_links.groupby('from_node_id').size().reset_index(name='overloaded_count')
critical_nodes = critical_nodes[critical_nodes['overloaded_count'] > 1]  # Filter nodes connected to >1 overloaded link

# Step 7: Visualization
# ----------------------
# Convert links and nodes to GeoDataFrames for visualization
try:
    gdf_links = gpd.GeoDataFrame(
        links, 
        geometry=gpd.GeoSeries.from_wkt(links['geometry'])
    )

    gdf_nodes = gpd.GeoDataFrame(
        nodes,
        geometry=gpd.points_from_xy(nodes['x_coord'], nodes['y_coord'])
    )

    gdf_overloaded_links = gdf_links[gdf_links['link_id'].isin(overloaded_links['link_id'])]
    gdf_critical_nodes = gdf_nodes[gdf_nodes['node_id'].isin(critical_nodes['from_node_id'])]
except Exception as e:
    print(f"Error creating GeoDataFrames: {e}")
    exit()

# Plot the network
plt.figure(figsize=(12, 8))
base = gdf_links.plot(color='lightgrey', linewidth=0.5, label='All Links')
gdf_overloaded_links.plot(ax=base, color='red', linewidth=2, label='Overloaded Links')
gdf_critical_nodes.plot(ax=base, color='blue', markersize=50, label='Critical Nodes')
plt.title('Choke Points in Road Network')
plt.legend()
plt.show()

# Step 8: Print Results
# ---------------------
print("Overloaded Links (Utilization > 1):")
print(overloaded_links[['link_id', 'from_node_id', 'to_node_id', 'utilization']])

print("\nCritical Nodes (Connected to Multiple Overloaded Links):")
print(critical_nodes)
