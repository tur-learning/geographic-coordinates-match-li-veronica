# 🏛️ Nolli Map - Fuzzy Matching Assignment

## 📌 Assignment Overview
Welcome to this assignment! You will write a Python script to **match historical points** from the **Nolli Map** dataset with modern OpenStreetMap (OSM) data using **fuzzy string matching**.

You will work with:
- **GeoJSON files** (JSON format used for geographical data)
- **Python dictionaries & lists**
- **For loops, functions, and conditionals**
- **Fuzzy string matching** with the help of pre-written utility functions (see `utils.py` module)

**Goal**: Extract relevant Nolli point names, fuzzy-match them to OSM features, and produce two outputs:
1. A JSON file (`matched_nolli_features.json`) containing the raw match results.
2. A GeoJSON file (`matched_nolli_features.geojson`) for map visualization.

## 🎯 Your Tasks
### **1️⃣ Extract Required GeoJSON Files**
- Extract the files `nolli_points_open.geojson` and `osm_node_way_relation.geojson` from `geojson_data.zip`.
- **Hint:** Use `extract_files()` from `utils.py`.

### **2️⃣ Load GeoJSON Data**
- Load both extracted files into Python dictionaries.
- **Hint:** Use `load_data()` from `utils.py`.

### **3️⃣ Prepare Nolli Data**
- Loop through `nolli_data["features"]` and extract:
  - `"Nolli Number"` → **Use it as the dictionary key**.
  - `"Nolli Name"`, `"Unravelled Name"`, `"Modern Name"` → **Store these as a list of possible names**.
  - `"geometry"` → **Store the coordinates**.
- **Example structure:**
  ```python
  nolli_relevant_data = {
      "1": {
          "nolli_names": ["Chiesa di Santo Stefano Rotondo", "Basilica di S. Stefano Rotondo al Celio"],
          "nolli_coords": { "type": "Point", "coordinates": [12.49686742, 41.88497152] }
      }
  }
  ```

  ### **4️⃣ Perform Fuzzy Matching**
- Loop through each Nolli point and find the best match in the OSM dataset.
- **Hint:** Use `find_best_matches()` from `utils.py`, with:
  - **Search names:** `nolli_names`
  - **Key field:** `"name"`
  - **Threshold:** `85`
  - **Scorer:** `"partial_ratio"`

### **5️⃣ Save & Visualize Results**
- Save the results in:
  - **JSON format:** `"matched_nolli_features.json"` using `save_to_json()`
  - **GeoJSON format:** `"matched_nolli_features.geojson"` using `save_to_geojson()`
- **Upload your final `"matched_nolli_features.geojson"` file to [geojson.io](https://geojson.io/)** and **take a screenshot** of the visualization.

---

## 📜 Expected Output
After completing the assignment, your **final JSON output** (`matched_nolli_features.json`) should look similar to:
```json
{
  "1": {
    "nolli_names": ["Chiesa di Santo Stefano Rotondo"],
    "nolli_coords": { "type": "Point", "coordinates": [12.49686742, 41.88497152] },
    "match": {
      "Matched_Name": "Basilica di S. Stefano Rotondo",
      "Match_Score": 95,
      "osm_coords": [12.4969, 41.8850]
    }
  }
}
```
Your **GeoJSON output** (`matched_nolli_features.geojson`) should contain geographical points for visualization.

---

## 🛠️ Hints & Help
- The **`utils.py`** file contains all the helper functions you need!
- Follow the **commented hints in `main.py`** to structure your code.
- **Debugging tip:** Print out intermediate results to check your progress.
- If you're stuck, **try working step by step!** Extract → Load → Prepare Data → Match → Save → Visualize.

---

## ✅ Submission Instructions
1. **Upload your final `matched_nolli_features.geojson` to [geojson.io](https://geojson.io/)**
2. **Take a screenshot of the visualization**
3. **Submit your completed `main.py`, `matched_nolli_features.json`, and screenshot**

---

🚀 **Good luck! Have fun coding!** 🎉

