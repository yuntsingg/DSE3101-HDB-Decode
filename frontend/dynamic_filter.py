import pandas as pd

def dynamic_filter(df, budget_range, flat_types, filter_order, filter_values):
    # Step 1: Required filters — Budget and Flat Type
    df = df[(df['resale_price'] >= budget_range[0]) & (df['resale_price'] <= budget_range[1])]
    df = df[df['flat_type'].isin(flat_types)]

    # Step 2: Apply filters progressively
    for filter_key in filter_order:
        if filter_key not in filter_values:
            continue

        val = filter_values[filter_key]

        if filter_key == 'town':
            df = df[df['town'].isin(val)]

        elif filter_key == 'storey_range':
            df = df[(df['storey_range'] >= val[0]) & (df['storey_range'] <= val[1])]

        elif filter_key == 'floor_area_sqm':
            df = df[(df['floor_area_sqm'] >= val[0]) & (df['floor_area_sqm'] <= val[1])]

        elif filter_key == 'remaining_lease':
            df = df[(df['remaining_lease'] >= val[0]) & (df['remaining_lease'] <= val[1])]

        elif filter_key == 'nearest_mrt_distance':
            df = df[df['nearest_mrt_distance'] <= val]

        elif filter_key == 'nearest_bus_distance':
            df = df[df['nearest_bus_distance'] <= val]

        elif filter_key in ['education_score', 'shopping_score', 'food_score', 'recreation_score', 'healthcare_score']:
            df = df[df[filter_key] >= val]


    return df.reset_index(drop=True)
