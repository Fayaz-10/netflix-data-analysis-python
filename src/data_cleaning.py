"""
Data Cleaning and Feature Engineering Module for Netflix Data Analysis
"""

from pathlib import Path
import pandas as pd
import numpy as np

def get_project_root() -> Path:
    return Path(__file__).resolve().parent.parent

def clean_netflix_data(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """
    Cleans raw Netflix dataframe and performs feature engineering.
    
    Returns:
        tuple[pd.DataFrame, dict]: (Cleaned DataFrame, Quality metrics dictionary)
    """
    df_clean = df.copy()
    
    # 1. Quality metrics BEFORE cleaning
    nulls_before = df_clean.isnull().sum().sum()
    null_summary_before = df_clean.isnull().sum().to_dict()
    duplicates_before = df_clean.duplicated().sum()
    total_rows_before = len(df_clean)
    
    # 2. String Whitespace Strip
    string_cols = df_clean.select_dtypes(include=['object']).columns
    for col in string_cols:
        df_clean[col] = df_clean[col].astype(str).str.strip()
        # Replace string 'nan' with actual NaN
        df_clean[col] = df_clean[col].replace({'nan': np.nan, '': np.nan, 'None': np.nan})
    
    # 3. Handle Duplicate Rows
    if duplicates_before > 0:
        df_clean = df_clean.drop_duplicates()
    duplicates_removed = duplicates_before
    
    # 4. Handle Rating Anomalies (e.g., duration values misplaced in rating column)
    # Some rows in raw dataset have duration misplaced in rating column (e.g. '74 min', '84 min', '66 min')
    rating_misplaced = df_clean['rating'].astype(str).str.contains('min', na=False)
    for idx in df_clean[rating_misplaced].index:
        df_clean.loc[idx, 'duration'] = df_clean.loc[idx, 'rating']
        df_clean.loc[idx, 'rating'] = np.nan

    # Fill Missing Categorical Values
    df_clean['director'] = df_clean['director'].fillna('Unknown')
    df_clean['cast'] = df_clean['cast'].fillna('Unknown')
    df_clean['country'] = df_clean['country'].fillna('Unknown')
    
    # Fill Missing Rating with Mode
    mode_rating = df_clean['rating'].mode()[0] if not df_clean['rating'].mode().empty else 'TV-MA'
    df_clean['rating'] = df_clean['rating'].fillna(mode_rating)
    
    # 5. Date Parsing and Date Feature Engineering
    df_clean['date_added_clean'] = pd.to_datetime(df_clean['date_added'], errors='coerce')
    
    # For missing date_added, drop or keep with NaN in date features
    df_clean['added_year'] = df_clean['date_added_clean'].dt.year
    df_clean['added_month'] = df_clean['date_added_clean'].dt.month_name()
    df_clean['added_month_num'] = df_clean['date_added_clean'].dt.month
    df_clean['added_quarter'] = df_clean['date_added_clean'].dt.to_period('Q').astype(str)
    
    # 6. Duration Feature Engineering
    # Extract numeric duration and unit ('min' vs 'Season'/'Seasons')
    df_clean['duration_value'] = df_clean['duration'].astype(str).str.extract(r'(\d+)')[0].astype(float)
    df_clean['duration_unit'] = df_clean['duration'].astype(str).str.extract(r'([a-zA-Z]+)')[0]
    
    # 7. Content Age & Release Decade
    current_year = 2026
    df_clean['content_age'] = current_year - df_clean['release_year']
    df_clean['release_decade'] = (df_clean['release_year'] // 10) * 10
    
    # Quality metrics AFTER cleaning
    nulls_after = df_clean.isnull().sum().sum()
    null_summary_after = df_clean.isnull().sum().to_dict()
    total_rows_after = len(df_clean)
    
    null_reduction_pct = ((nulls_before - nulls_after) / nulls_before * 100) if nulls_before > 0 else 0.0
    
    metrics = {
        'total_rows_before': total_rows_before,
        'total_rows_after': total_rows_after,
        'duplicates_before': duplicates_before,
        'duplicates_removed': duplicates_removed,
        'nulls_before': nulls_before,
        'nulls_after': nulls_after,
        'null_reduction_pct': round(null_reduction_pct, 2),
        'null_summary_before': null_summary_before,
        'null_summary_after': null_summary_after
    }
    
    return df_clean, metrics

def save_cleaned_data(df_clean: pd.DataFrame, filename: str = "netflix_cleaned.csv") -> Path:
    project_root = get_project_root()
    cleaned_dir = project_root / "data" / "cleaned"
    cleaned_dir.mkdir(parents=True, exist_ok=True)
    out_path = cleaned_dir / filename
    df_clean.to_csv(out_path, index=False)
    print(f"Saved cleaned dataset ({len(df_clean)} rows) to: {out_path}")
    return out_path

if __name__ == "__main__":
    from data_loading import load_raw_data
    df_raw = load_raw_data()
    df_clean, metrics = clean_netflix_data(df_raw)
    save_cleaned_data(df_clean)
    print("Cleaning Metrics:", metrics)
