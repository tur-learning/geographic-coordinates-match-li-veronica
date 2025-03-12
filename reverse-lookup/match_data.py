# Import necessary functions from utils.py
from utils import extract_files, load_data, find_best_matches, save_to_json, save_to_geojson, find_closest_matches
from shapely.geometry import shape, Point

###############################
# 1) Define the input files
###############################
# HINT: The data is stored inside a ZIP archive.
# You need to extract two GeoJSON files:
# - `nolli_points_open.geojson`: Contains historical Nolli map features.
# - `osm_node_way_relation.geojson`: Contains OpenStreetMap (OSM) features.

zip_file = "../gottamatch-emall/geojson_data.zip"
geojson_files = ["nolli_points_open.geojson", "osm_node_way_relation.geojson"]

###############################
# 2) Extract GeoJSON files
###############################
# HINT: Use the function `extract_files()` to extract the required files.
# This function returns a list of extracted file paths.

nolli_file, osm_file = extract_files(zip_file, geojson_files)

###############################
# 3) Load the GeoJSON data
###############################
# HINT: Use the function `load_data()` to read the JSON content of each extracted file.
# You should end up with two dictionaries:
# - `nolli_data`: Contains the historical map data.
# - `osm_data`: Contains modern OpenStreetMap features.

nolli_data = load_data(nolli_file)
osm_data = load_data(osm_file)


###############################
# 4) Extract relevant info from Nolli data
###############################
# HINT: Each feature in `nolli_data["features"]` represents a historical landmark or road.
# You need to:
# 1️⃣ Extract the unique "Nolli Number" for each feature (use it as the dictionary key).
# 2️⃣ Extract the possible names for each feature from:
#    - "Nolli Name"
#    - "Unravelled Name"
#    - "Modern Name"
# 3️⃣ Store the feature's coordinates (geometry).
#
# Expected structure:
# {
#   "1319": {
#       "nolli_names": [
#           "Mole Adriana, or Castel S. Angelo",
#           "Mole Adriana, or Castel Sant'Angelo",
#           "Castel Sant'Angelo"
#       ],
#       "nolli_coords": {
#           "type": "Point",
#           "coordinates": [12.46670095, 41.90329709]
#       }
#   }
# }

nolli_features = nolli_data["features"]

unmatched_nolli = [
    feature for feature in nolli_features 
    if "Match_Score" not in feature["properties"]
]

print(f"Found {len(unmatched_nolli)} unmatched Nolli features.")

nolli_features = nolli_data["features"]

unmatched_nolli = [
    feature for feature in nolli_features 
    if "Match_Score" not in feature["properties"]
]

print(f"Found {len(unmatched_nolli)} unmatched Nolli features.")


###############################
# 5) Fuzzy match with OSM data
###############################
# HINT: The `osm_data["features"]` list contains modern landmarks and roads.
# Each feature has a "name" field in its properties.
#
# For each Nolli entry:
# ✅ Compare its names with the "name" field of OSM features.
# ✅ Use fuzzy matching to find the closest match.
# ✅ Store the best match in the `nolli_relevant_data` dictionary.
#
# Use the function `find_best_matches()`:
# - Pass the list of names from Nolli.
# - Search in the OSM dataset using `key_field="name"`.
# - Set `threshold=85` (minimum similarity score).
# - Use `scorer="partial_ratio"` for better matching.

print(f"Searching best match for Nolli names:")

counter = 0  
osm_features = osm_data["features"]
osm_centroids = []
matched_features = [] 
for feature in osm_features:
    geom = shape(feature["geometry"]) 
    if geom.is_empty or not geom.is_valid:
        continue  
    if geom.geom_type in ["Point", "Polygon", "MultiPolygon"]:  
        centroid = geom.centroid  
    else:
        centroid = geom.representative_point()
    osm_centroids.append(([centroid.x, centroid.y], feature))

for nolli in unmatched_nolli:
    nolli_point = shape(nolli["geometry"])  
    if not isinstance(nolli_point, Point):
        nolli_point = nolli_point.centroid  
    
    best_match = find_closest_matches([nolli_point], [feature for _, feature in osm_centroids], use_geodesic=False)


    if best_match and len(best_match) > 1:
        nolli["properties"]["Geo_Match"] = best_match[1]["properties"]
        nolli["properties"]["Geo_Distance"] = best_match[0]
        matched_features.append(nolli) 
        matched_features.append(best_match[1]) 
    else:
        print(f"No match found for Nolli feature: {nolli['properties'].get('Nolli Number', 'Unknown')}")
        matched_features.append(nolli) 

    matched_features.append(nolli) 
    matched_features.append(best_match[1]) 

print("Geospatial matching complete.")

###############################
# 6) Save results as JSON and GeoJSON
###############################
# HINT: Once all matches are found, save the results in two formats:
# ✅ `matched_nolli_features.json` → Standard JSON format for analysis.
# ✅ `matched_nolli_features.geojson` → A structured GeoJSON file for visualization.
#
# Use:
# - `save_to_json(nolli_relevant_data, "matched_nolli_features.json")`
# - `save_to_geojson(nolli_relevant_data, "matched_nolli_features.geojson")`

save_to_json(unmatched_nolli, "nolli_geographic_match.json")

geojson_output = {
    "type": "FeatureCollection",
    "features": matched_features 
}

save_to_geojson(geojson_output, "nolli_geographic_match.geojson")

print("Files saved: nolli_geographic_match.json & nolli_geographic_match.geojson")

###############################
# 7) Visualization
###############################
# 🎯 **Final Task**: Upload `matched_nolli_features.geojson` to:
# 🔗 **[geojson.io](https://geojson.io/)**
#
# 📌 Observe if the matched features align correctly.
# 📝 Take a screenshot and submit it as proof of completion!
