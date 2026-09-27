"""
Data Loading Module for Netflix Data Analysis
Uses pathlib for robust, platform-independent path handling.
"""

from pathlib import Path
import pandas as pd

def get_project_root() -> Path:
    """Returns the root directory of the project."""
    # Assuming this file is located at <PROJECT_ROOT>/src/data_loading.py
    return Path(__file__).resolve().parent.parent

def load_raw_data(filename: str = "netflix_titles.csv") -> pd.DataFrame:
    """
    Locates and loads raw Netflix CSV data from data/raw/ directory.
    
    Parameters:
        filename (str): Name of the CSV file.
        
    Returns:
        pd.DataFrame: Raw dataset.
    """
    project_root = get_project_root()
    raw_data_path = project_root / "data" / "raw" / filename
    
    if not raw_data_path.exists():
        # Fallback search inside data/raw
        raw_dir = project_root / "data" / "raw"
        csv_files = list(raw_dir.glob("*.csv"))
        if csv_files:
            raw_data_path = csv_files[0]
        else:
            raise FileNotFoundError(f"No CSV file found in {raw_dir}. Please place your Netflix CSV dataset there.")

    print(f"Loading raw data from: {raw_data_path}")
    df = pd.read_csv(raw_data_path)
    print(f"Successfully loaded dataset with {df.shape[0]} rows and {df.shape[1]} columns.")
    return df

if __name__ == "__main__":
    df_raw = load_raw_data()
    print(df_raw.head())
