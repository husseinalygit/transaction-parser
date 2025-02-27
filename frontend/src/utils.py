import pandas as pd
import os

def dict_to_string(d):
    """Converts a dictionary to a string of key : value pairs, each on a new line."""
    return "\n".join([f"{k} : {v}" for k, v in d.items()])

def append_to_csv(data, filepath , filename="ner_results.csv"):
    """Append a dictionary to a CSV file. If file does not exist, create it."""
    df = pd.DataFrame([data])
    if os.path.exists(f"{filepath}/{filename}"):
        df.to_csv(f"{filepath}/{filename}", mode='a', header=False, index=False, date_format='%m/%d/%Y')
    else:
        df.to_csv(f"{filepath}/{filename}", index=False, date_format='%m/%d/%Y')

def load_csv(filepath , filename="ner_results.csv"):
    """Load the CSV file into a DataFrame, if it exists."""
    if os.path.exists(f"{filepath}/{filename}"):
        return pd.read_csv(f"{filepath}/{filename}", date_format='%m/%d/%Y' )
    return pd.DataFrame() 