# 🏛️ Assignment 2: Reverse Geospatial Matching  

## 📌 Overview  
In **Assignment 1**, we matched **Nolli Map** locations to **OpenStreetMap (OSM)** using **fuzzy string matching**.  
However, some Nolli locations remained **unmatched**.  

### 🔍 Goal  
Use **geographic distance** instead of **text similarity** to match previously **unmatched** Nolli features.  

---

## 📝 Steps to Complete the Assignment  

### 1️⃣ Load Previous GeoJSON Results  
- **Input File:** `matched_nolli_features.geojson`  
- Load it using `load_data()`.  

### 2️⃣ Filter Non-Matched Nolli Entries  
- Extract **matched** and **non-matched** Nolli entries.  
- **Matched entries** have `"Match_Score"` in their properties.  
- **Keep only** non-matched Nolli entries.  

### 3️⃣ Load OSM Features from ZIP File  
- Extract **`osm_node_way_relation.geojson`** from `geojson_data.zip`.  
- Load it using `load_data()`.  

### 4️⃣ Find the Closest OSM Match  
- Extract **centroids** from OSM features using **Shapely**.  
- Measure the **distance** from each non-matched Nolli location to the nearest OSM centroid.  
- Use:  
```python
find_closest_matches(... , use_geodesic=False)
```  

### 5️⃣ Save the Results  
- **Output File:** `nolli_geographic_match.json` and `.geojson`
- Save using `save_to_json()` and `convert_to_geojson()`.  

---

## 📜 Expected Output (`output.json`)  
Each **previously unmatched** Nolli location will now have:  
✅ **Its original coordinates**  
✅ **The closest OSM feature & its coordinates**  
✅ **The calculated distance (meters)**  

```json
{
            "type": "Feature",
            "properties": {
                "Nolli_ID": "10",
                "Nolli_Name": "Obelisco gi\u00e0 del Circo Massimo",
                "Marker_Type": "Nolli"
            },
            "geometry": {
                "type": "Point",
                "coordinates": [
                    12.50478077,
                    41.88693845
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "@id": "way/191153016",
                "footway": "sidewalk",
                "highway": "footway",
                "lit": "yes",
                "surface": "paving_stones"
            },
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [
                        12.5048197,
                        41.8869246
                    ],
                    [
                        12.5047727,
                        41.8869179
                    ],
                    [
                        12.5047307,
                        41.886906
                    ],
                    [
                        12.5047004,
                        41.8868909
                    ],
                    [
                        12.5046867,
                        41.8868831
                    ]
                ]
            },
            "id": "way/191153016"
        }
```

---

## 📊 Final Task: Analyze Your Results  
- Compare **name matching (Assignment 1) vs. distance matching (Assignment 2).**  
- **Which method was more accurate?**
- Copy/paste your GeoJSON file in https://geojson.io/ and check it.

---

## ✅ Submission Instructions  
1️⃣ Run your script & generate `nolli_geographic_match.json` and `nolli_geographic_match.geojson`.  
2️⃣ Review results & submit `nolli_geographic_match.json` + your completed `main.py`.  

🚀 **Happy coding!** 🌍✨  

---

### 🎯 Learning Outcomes  
✔ Work with **geospatial data in Python**  
✔ Extract **centroids** from polygons using **Shapely**  
✔ Compute **nearest geographic feature**  
✔ Compare **text vs. spatial matching**  
