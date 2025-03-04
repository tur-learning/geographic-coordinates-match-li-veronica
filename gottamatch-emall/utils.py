import json
import math
import zipfile
import os
from thefuzz import fuzz, process


def extract_files(zip_filename, filenames, extract_path="."):
    """
    Extracts specific GeoJSON files from a ZIP archive.

    Parameters:
    zip_filename (str): The path to the ZIP archive.
    filenames (list): List of filenames to extract from the archive.
    extract_path (str): Directory where extracted files will be saved (default is current directory).

    Returns:
    list: Paths of the extracted files.
    """
    extracted_files = []

    if not os.path.exists(zip_filename):
        raise FileNotFoundError(f"ZIP file {zip_filename} not found.")

    with zipfile.ZipFile(zip_filename, "r") as zip_ref:
        for file in filenames:
            if file in zip_ref.namelist():
                zip_ref.extract(file, extract_path)
                extracted_files.append(os.path.join(extract_path, file))
            else:
                print(f"Warning: {file} not found in {zip_filename}.")

    return extracted_files


def load_data(filename):
    """
    Loads data from a JSON file.

    Parameters:
    filename (str): The path to the JSON file.

    Returns:
    dict: Parsed JSON data.
    """
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data


def extract_coords(data):
    """
    Extracts the first coordinate pair from a nested list of coordinates.

    This function is useful for extracting a representative point from 
    complex geometries (e.g., polygons or multipolygons).

    Parameters:
    data (list): A nested list of coordinates.

    Returns:
    list: A list containing latitude and longitude.
    """
    if not isinstance(data, list):
        return None

    nested_data = data[0]
    depth = 0
    while isinstance(nested_data, list):
        depth += 1
        nested_data = nested_data[0]

    for _ in range(depth):
        data = data[0]

    return data


def print_dict(data):
    """
    Prints a dictionary in a well-formatted JSON style.

    Parameters:
    data (dict): The dictionary to print.

    Returns:
    None
    """
    print(json.dumps(data, indent=2, ensure_ascii=False))


def find_best_matches(search_names, features, key_field="name", threshold=80, scorer="ratio"):
    """
    Performs a fuzzy search to find the best match between a set of search names and a given feature set.

    Parameters:
    search_names (list): A list of names to search for.
    features (list): A list of GeoJSON features to match against.
    key_field (str): The key field in the features' properties to compare (default: "name").
    threshold (int): The minimum similarity score required for a match (default: 80).
    scorer (str): The fuzzy matching function name as a string ("ratio", "partial_ratio", "token_sort_ratio", "token_set_ratio").

    Returns:
    tuple: (best match feature dict, number of matches found)
    """
    if "n/a" in search_names:
        search_names.remove("n/a")

    # Dynamically resolve the scorer from the `fuzz` module
    scorer_func = getattr(fuzz, scorer, fuzz.ratio)

    matches = []
    for feature in features:
        properties = feature.get("properties", {})
        if key_field in properties:
            feature_name = properties[key_field]
            best_match, score = process.extractOne(feature_name, search_names, scorer=scorer_func)
            if score >= threshold:
                matches.append((feature_name, best_match, score, {"osm_coords": feature["geometry"]["coordinates"]}))

    if matches:
        unique_match = max(matches, key=lambda x: x[2])  # Choose match with highest score
        coords_to_convert = unique_match[-1]["osm_coords"]
        unique_match[-1]["osm_coords"] = extract_coords(coords_to_convert)
        return unique_match, 1

    return None, 0


def save_to_json(data, output_file):
    """
    Saves data to a JSON file.

    Parameters:
    data (dict or list): The data to be saved.
    output_file (str): The path of the output JSON file.

    Returns:
    None
    """
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Results saved to {output_file}")


def save_to_geojson(data, output_file):
    """
    Saves matched results to a GeoJSON file with two distinct points per feature:
    - The Nolli coordinate as one point
    - The matched OSM coordinate as another point (if available)

    Parameters:
    data (dict): Dictionary containing matched Nolli data with coordinates.
    output_file (str): The path of the output GeoJSON file.

    Returns:
    None
    """
    features = []
    
    for nolli_id, values in data.items():
        # Check if nolli_coords exists and has valid coordinates
        if "nolli_coords" in values and values["nolli_coords"] and "coordinates" in values["nolli_coords"]:
            nolli_point = {
                "type": "Feature",
                "properties": {
                    "Nolli_ID": nolli_id,
                    "Nolli_Name": values["nolli_names"][0],  # First name for reference
                    "Marker_Type": "Nolli",  # Marker identifier for styling
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": values["nolli_coords"]["coordinates"]
                }
            }
            features.append(nolli_point)
        else:
            print(f"⚠️ Warning: No valid coordinates for Nolli ID {nolli_id}. Skipping.")

        # If there is a match, add the corresponding OSM point
        if "match" in values and values["match"] is not None:
            match_data = values["match"]
            if "osm_coords" in match_data[-1] and match_data[-1]["osm_coords"]:
                osm_point = {
                    "type": "Feature",
                    "properties": {
                        "Nolli_ID": nolli_id,
                        "Nolli_Name": values["nolli_names"][0],
                        "Matched_Name": match_data[0],  # Matched OSM name
                        "Match_Score": match_data[2],  # Similarity score
                        "Marker_Type": "OSM",  # Marker identifier for styling
                    },
                    "geometry": {
                        "type": "Point",
                        "coordinates": match_data[-1]["osm_coords"]
                    }
                }
                features.append(osm_point)
            else:
                print(f"⚠️ Warning: No valid OSM coordinates for Nolli ID {nolli_id}. Skipping.")

    geojson_output = {
        "type": "FeatureCollection",
        "features": features
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(geojson_output, f, indent=2, ensure_ascii=False)
    
    print(f"✅ GeoJSON results saved to {output_file}")


def link2map(data):
    """
    Generates a Google Maps link for a given coordinate pair.

    Parameters:
    data (dict): A dictionary containing coordinates in the format:
                 {"type": "Point", "coordinates": [longitude, latitude]}.

    Returns:
    None (prints the Google Maps URL).
    """
    coords = data["coordinates"]
    print(f"https://www.google.com/maps/@{coords[1]},{coords[0]},21z")


def calculate_distance(point1, point2):
    """
    Calculates the Euclidean distance between two points in a 2D space.

    Parameters:
    point1 (list): [longitude, latitude] of the first point.
    point2 (list): [longitude, latitude] of the second point.

    Returns:
    float: The Euclidean distance between the two points.
    """
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)


def get_nearest(iterable, objects):
    """
    Finds the nearest object in a list based on the minimum distance.

    Parameters:
    iterable (list): A list of distances.
    objects (list): A list of objects corresponding to the distances.

    Returns:
    object: The object with the minimum distance.
    """
    index = min(enumerate(iterable), key=lambda x: x[1])[0]
    return objects[index]
