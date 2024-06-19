import os
import pandas as pd
from datetime import datetime

now = datetime.now()
# Format the datetime as a string
current_time = now.strftime('%m/%d/%Y %H:%M')



def find_latest_report(directory, prefix):
    """
    Function to find the latest date report with the specified prefix in the given directory.
    Args:
    - prefix (str): Prefix of the report filename.
    - directory (str): Directory path to search for reports.
    Returns:
    - str: Filename of the latest date report with the specified prefix, or None if not found.
    """
    latest_report = None
    latest_creation_time = None

    # Iterate through files in the directory
    for filename in os.listdir(directory):
        # Check if the file starts with the specified prefix
        if filename.startswith(prefix):
            file_path = os.path.join(directory, filename)
            # Get the creation time of the file
            creation_time = os.path.getctime(file_path)
            # Update latest_report if the file creation time is later than the current latest_creation_time
            if latest_creation_time is None or creation_time > latest_creation_time:
                latest_creation_time = creation_time
                latest_report = filename

    return latest_report


def get_latest_inventory_df(directory, prefix):
    inv_item_filename = find_latest_report(directory, prefix)
    inv_item_path = directory + inv_item_filename
    inv_item_df = pd.read_csv(inv_item_path, dtype={"Internal ID":str})
    inv_item_df = inv_item_df[['Internal ID', 'Name', 'Location On Hand']]
    return inv_item_df

def merge_df(inventory, sku_list):
    merged_df = pd.merge(left=sku_list, right=inventory, left_on='SKU', right_on='Name', how="left").reset_index()
    merged_df = merged_df[merged_df['SKU'].isin(sku_list['SKU'])].drop(columns=['index', 'Name'])
    merged_df = merged_df[['Internal ID', 'SKU', 'Physical Count', 'Location On Hand']]
    merged_df['To Adjust'] = merged_df['Physical Count'] - merged_df['Location On Hand']
    merged_df['On Hand Timestamp'] = current_time
    return merged_df