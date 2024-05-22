import xml.etree.ElementTree as ET
import sys

sys.stdout.reconfigure(encoding='utf-8')

def flatten_keys(dataset):
    flattened_dataset = {}
    for key, value in dataset.items():
        if isinstance(value, dict):
            flattened_subkeys = flatten_keys(value)
            for subkey, subvalue in flattened_subkeys.items():
                flattened_dataset[f"{key}_{subkey}"] = subvalue
        else:
            flattened_dataset[key] = value
    return flattened_dataset


def get_column_name(key):
    parts = key.split('_')[-4:]
    return '_'.join(parts)


def create_table_and_insert_data(cursor, datasets, table_name):
    if not datasets:
        print("No datasets provided.")
        return
    
    # DICT WITH HIGHEST NUMBER OF KEYS
    max_keys_dataset = max(datasets, key=lambda x: len(x.keys()))
    
    # GET COLUMN NAMES FROM THE DICT THAT HAS HIGHEST KEYS
    flattened_keys = flatten_keys(max_keys_dataset)

    column_names = [get_column_name(key) for key in flattened_keys.keys()]
    
    column_types = {}
    for column in column_names:
        if column.endswith('Id'):
            column_types[column] = 'INT'
        elif column.endswith('Date'):
            column_types[column] = 'TIMESTAMP'
        else:
            column_types[column] = 'VARCHAR'
    
    # CREATE TABLE
    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join([f'"{name}" {type}' for name, type in column_types.items()])})"
    cursor.execute(create_table_query)
    
    # INSERT DATA
    for dataset in datasets:

        flattened_dataset = flatten_keys(dataset)
        
        insert_query = f"INSERT INTO {table_name} ({', '.join([f'"{column}"' for column in column_names])}) VALUES ({', '.join(['%s' for _ in column_names])})"
        
        values = [flattened_dataset.get(key) for key in flattened_keys.keys()]

        cursor.execute(insert_query, tuple(values))