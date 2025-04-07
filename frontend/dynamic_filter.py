import pandas as pd

def extract_storey_mid(s):
    try:
        parts = s.split(" to ")
        return (int(parts[0]) + int(parts[1])) // 2
    except:
        return None

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

        elif filter_key in ['education_score', 'shopping_score', 'food_score', 'recreation_score', 'healthcare_score']:
            df = df[df[filter_key] >= val]

    # Final deduplication
    df = df.sort_values(by='prediction_reverted')
    df = df.drop_duplicates(subset=['lat', 'lon', 'flat_type', 'floor_area_sqm'])

    return df.reset_index(drop=True)
