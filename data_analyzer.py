import pandas as pd
import json
from datetime import datetime
import pprint

def analyze_data():
    live_file = 'latest_station_status.json'
    static_file = 'station_info.json'

    # Load JSON
    with open(live_file) as f:
        live_json = json.load(f)
    with open(static_file) as f:
        static_json = json.load(f)

    # Extract 'stations' lists
    live_stations = live_json['data'].get('stations', live_json['data'])
    static_stations = static_json['data'].get('stations', static_json['data'])

    # Convert to DataFrames
    df_live = pd.DataFrame(live_stations)
    df_static = pd.DataFrame(static_stations)

    # Ensure 'station_id' exists
    if 'station_id' not in df_live.columns or 'station_id' not in df_static.columns:
        return {'error': 'station_id missing in one of the datasets'}

    # Merge live + static data
    df_merged = pd.merge(df_live, df_static, on='station_id', how='left')

    # Extract bike / e-bike counts
    def extract_bikes(vehicle_list, vehicle_type_id):
        if not isinstance(vehicle_list, list):
            return 0
        for v in vehicle_list:
            if v.get('vehicle_type_id') == str(vehicle_type_id):
                return v.get('count', 0)
        return 0

    df_merged['num_bikes'] = df_merged['vehicle_types_available'].apply(lambda x: extract_bikes(x, 1))
    df_merged['num_ebikes'] = df_merged['vehicle_types_available'].apply(lambda x: extract_bikes(x, 2))

    # Define the station filters: list of (AND_keywords, OR_keywords) tuples
    station_filters = [
        (['Clark', 'Wrightwood'], []),           # Clark AND Wrightwood
        (['Clark', 'Drummond'], []),             # Clark AND Drummond
        (['Southport', 'Clybourn'], [])          # Southport AND Clybourn
    ]

    # Build filtered station output
    filtered_stations = []
    for and_keywords, or_keywords in station_filters:
        for _, row in df_merged.iterrows():
            name = str(row.get('name', '')).lower()
            # AND condition
            if all(kw.lower() in name for kw in and_keywords):
                filtered_stations.append({
                    'name': row.get('name'),
                    'num_bikes': int(row.get('num_bikes', 0)),
                    'num_ebikes': int(row.get('num_ebikes', 0)),
                    'num_docks_available': int(row.get('num_docks_available', 0)),
                    'is_renting': bool(row.get('is_renting', 0))
                })
            # OR condition
            elif or_keywords and any(kw.lower() in name for kw in or_keywords):
                filtered_stations.append({
                    'name': row.get('name'),
                    'num_bikes': int(row.get('num_bikes', 0)),
                    'num_ebikes': int(row.get('num_ebikes', 0)),
                    'num_docks_available': int(row.get('num_docks_available', 0)),
                    'is_renting': bool(row.get('is_renting', 0))
                })

    return {
        'filtered_stations': filtered_stations,
        'last_updated_ts': int(datetime.now().timestamp())
    }

if __name__ == '__main__':
    pprint.pprint(analyze_data())

