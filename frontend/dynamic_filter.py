import pandas as pd

def extract_storey_mid(s):
    try:
        parts = s.split(" To ")
        return (int(parts[0]) + int(parts[1])) // 2
    except:
        return None

amenity_column_map = {
    'schools': 'education_score',
    'shopping': 'shopping_score',
    'food': 'food_score',
    'recreation': 'recreation_score',
    'healthcare': 'healthcare_score'
}

def dynamic_filter(df, budget_range, flat_types, filter_order, filter_values):
    # Required filters — Budget and Flat Type
    df = df[(df['prediction_reverted'] >= budget_range[0]) & (df['prediction_reverted'] <= budget_range[1])]
    df = df[df['flat_type'].isin(flat_types)]

    # Convert storey_range (string) → midpoint
    df['storey_mid'] = df['storey_range'].apply(extract_storey_mid)

    # Progressive filtering
    for filter_key in filter_order:
        if filter_key not in filter_values:
            continue

        val = filter_values[filter_key]

        if filter_key == 'town':
            df = df[df['town'].isin(val)]

        elif filter_key == 'storey_range':
            df = df[(df['storey_mid'] >= val[0]) & (df['storey_mid'] <= val[1])]

        elif filter_key == 'remaining_lease':
            df = df[(df['remaining_lease_reverted'] >= val[0]) & (df['remaining_lease_reverted'] <= val[1])]

        elif filter_key == 'nearest_mrt_distance':
            df = df[df['nearest_mrt_distance'] <= val]

        elif filter_key == 'nearest_bus_distance':
            df = df[df['nearest_bus_distance'] <= val]

        elif filter_key in amenity_column_map:
            actual_col = amenity_column_map[filter_key]
            df = df[df[actual_col] >= val]

    # Final deduplication
    df = df.sort_values(by='prediction_reverted')


    return df.reset_index(drop=True)
