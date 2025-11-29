import random
import string
import pandas as pd
import json
from datetime import datetime
import os

def generate_stock_id():
    """Generates a random stock ID."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def save_dataset(data_list, output_dir="datasets"):
    """Saves a list of dictionaries or Pydantic models to JSON and CSV."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Convert Pydantic models to dicts if necessary
    serializable_data = []
    for item in data_list:
        if hasattr(item, 'model_dump'):
            serializable_data.append(item.model_dump(mode='json'))
        elif hasattr(item, 'dict'):
            serializable_data.append(item.dict())
        else:
            serializable_data.append(item)

    # Save JSON
    json_path = os.path.join(output_dir, f"dataset_{timestamp}.json")
    with open(json_path, 'w') as f:
        json.dump(serializable_data, f, indent=4, default=str)
    
    # Save CSV
    if serializable_data:
        df = pd.DataFrame(serializable_data)
        csv_path = os.path.join(output_dir, f"dataset_{timestamp}.csv")
        df.to_csv(csv_path, index=False)
        return json_path, csv_path
    
    return json_path, None
