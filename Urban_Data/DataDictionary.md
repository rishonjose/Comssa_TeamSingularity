# Data Dictionary

Note `link.csv`, `node.csv` and `poi.csv` are based on the [GMNS Format](https://osm2gmns.readthedocs.io/en/latest/mrm.html#macroscopic-network). WKT refers to [Well-Known Text](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry).

## demand.csv
| Field     | Description                  | Type   | Example           |
|-----------|------------------------------|--------|-------------------|
| o_zone_id | Origin zone ID               | int    | 0                 |
| d_zone_id | Destination zone ID          | int    | 1                 |
| dist_km   | Distance in kilometers       | float  | 8.54295575697721  |
| volume    | Demand of 1-hour peak window | float  | 38.47759214095043 |

## link.csv

Note: all links are forward in direction and for "auto" mode, meaning for cars.

| Field          | Description                       | Type   | Example                                                                 |
|----------------|-----------------------------------|--------|-------------------------------------------------------------------------|
| name           | Name of the road that link is in  | string | ""                                                                      |
| link_id        | Link ID                           | int    | 0                                                                       |
| osm_way_id     | OpenStreetMap way ID              | int    | 24548917                                                                |
| from_node_id   | ID of the starting node           | int    | 0                                                                       |
| to_node_id     | ID of the ending node             | int    | 1                                                                       |
| length         | Length of the link (meters)       | float  | 395.25                                                                  |
| lanes          | Number of lanes                   | int    | 2                                                                       |
| free_speed     | Free speed on the link (km/hour)  | float  | 60                                                                      |
| link_type_name | Type name of the link             | string | secondary                                                               |
| link_type      | Type of the link                  | int    | 4                                                                       |
| geometry       | Geometry of the link (WKT Format) | string | "LINESTRING (103.6301643 31.0059626, 103.6278327 31.0045744, 103.6267671 31.0039241)" |
| from_biway     | If created from bidirectional way | bool   | 0                                                                       |
| is_link        | If connecting two roads           | bool   | 0                                                                       |

## node.csv
| Field    | Description   | Type   | Example          |
|----------|---------------|--------|------------------|
| node_id  | Node ID       | int    | 0                |
| x_coord  | X coordinate  | float  | 103.6301643      |
| y_coord  | Y coordinate  | float  | 31.0059626       |
| zone_id  | Zone ID       | int    | 51               |
| geometry | Geometry of the node (WKT Format) | string | "POINT (103.6301643 31.0059626)" |

## poi.csv
| Field     | Description              | Type   | Example          |
|-----------|--------------------------|--------|------------------|
| poi_id    | Point of interest ID     | int    | 0                |
| x_coord   | X coordinate             | float  | 104.0245006      |
| y_coord   | Y coordinate             | float  | 30.5716335       |
| building  | Building tag in OSM data | string | yes              |
| amenity   | Amenity tag in OSM data  | string | parking          |
| centroid  | Centroid of POI (WKT Format) | string | "POINT (104.0245006 30.5716335)" |
| area      | Area of POI              | float  | 3179.2           |
| trip_rate | Factors on trip_rate for POI | string | "{'building': 'yes', 'unit_of_measure': '1,000 Sq. Ft. GFA', 'trip_purpose': 1, 'production_rate1': 1.15, 'attraction_rate1': 1.15, 'production_notes': 1, 'attraction_notes': 1}" |
| geometry  | Geometry of POI (WKT Format) | string | "POLYGON ((104.0240097 30.5719187, 104.0242073 30.5718596, 104.0250911 30.571595, 104.0249915 30.5713482, 104.02391 30.5716719, 104.0240097 30.5719187))" |
| zone_id   | Zone ID                  | int    | 151              |

## zone.csv
| Field         | Description            | Type   | Example          |
|---------------|------------------------|--------|------------------|
| zone_id       | Zone ID                | int    | 0                |
| name          | Name of the zone       | string | A0               |
| x_coord       | X coordinate           | float  | 103.3849053      |
| y_coord       | Y coordinate           | float  | 31.19243844      |
| centroid      | Centroid of the zone (WKT Format) | string | "POINT (103.38490531250001 31.1924384375)" |
| x_max         | Maximum X coordinate   | float  | 103.4298116      |
| x_min         | Minimum X coordinate   | float  | 103.339999       |
| y_max         | Maximum Y coordinate   | float  | 31.227001        |
| y_min         | Minimum Y coordinate   | float  | 31.15787588      |
| node_id_list  | List of node IDs in the zone | string | "[40248, 40249, 40250, 40251, 40252, 40253, 40254, 40255]" |
| poi_id_list   | List of POI IDs in the zone | string | "[]"             |
| production    | Production value (gravity model) | float | 400              |
| attraction    | Attraction value (gravity model) | float | 400              |
| geometry      | Geometry of the zone (WKT Format) | string | "POLYGON ((103.339999 31.157875875000002, 103.429811625 31.157875875000002, 103.429811625 31.227001, 103.339999 31.227001, 103.339999 31.157875875000002))" |
