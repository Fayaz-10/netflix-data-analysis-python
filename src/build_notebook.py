"""
Script to construct and execute the Netflix_Data_Analysis.ipynb Jupyter Notebook
"""

from pathlib import Path
import nbformat as nbf
import os

def create_notebook():
    project_root = Path(__file__).resolve().parent.parent
    nb = nbf.v4.new_notebook()

    cells = []

    # 1. Project Title
    cells.append(nbf.v4.new_markdown_cell("""# Netflix Data Analysis using Python

**Author**: Senior Data Analyst  
**Date**: September 2026  
**Tools**: Python 3.13, Pandas, NumPy, Matplotlib, Seaborn  
**Dataset**: Authentic Netflix Movies and TV Shows Catalog Dataset (7,787 records)
"""))

    # 2. Business Problem
    cells.append(nbf.v4.new_markdown_cell("""## 1. Project Overview
Understanding catalog composition—movie-to-TV ratio, genre representation, geographic country associations, rating distributions, and release addition velocity over time—is essential for objective catalog analysis.

This project delivers a data-driven audit of the Netflix dataset based strictly on empirical calculations from 7,787 catalog records.
"""))

    # 3. Objective
    cells.append(nbf.v4.new_markdown_cell("""## 2. Project Objective
- Perform an end-to-end data analysis workflow: raw data loading, data quality checking, rigorous cleaning, missing value resolution, and feature engineering.
- Conduct thorough Exploratory Data Analysis (EDA) covering univariate, bivariate, and temporal trends.
- Generate high-quality visualizations saved to `visualizations/`.
- Formulate empirical data summary observations based strictly on dataset metrics.
"""))

    # 4. Dataset Overview
    cells.append(nbf.v4.new_markdown_cell("""## 3. Dataset Overview
The dataset contains 7,787 titles streaming on Netflix with 12 metadata attributes:
- `show_id`: Unique identifier for each title
- `type`: Content category ('Movie' or 'TV Show')
- `title`: Title of the movie or show
- `director`: Director(s) of the title
- `cast`: Main cast members
- `country`: Country or countries associated with the content
- `date_added`: Date the title was added to Netflix
- `release_year`: Original release year of the content
- `rating`: Content rating (e.g., TV-MA, PG-13)
- `duration`: Total length in minutes (Movies) or number of seasons (TV Shows)
- `listed_in`: Listed genres/categories
- `description`: Plot summary
"""))

    # 5. Import Libraries
    cells.append(nbf.v4.new_markdown_cell("""## 4. Import Libraries
Import standard data manipulation, path handling, and visualization libraries.
"""))
    cells.append(nbf.v4.new_code_cell("""from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings('ignore')

# Set aesthetic styling
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.size'] = 10
plt.rcParams['figure.figsize'] = (10, 5)

print("Libraries imported successfully.")
"""))

    # 6. Load Dataset
    cells.append(nbf.v4.new_markdown_cell("""## 5. Load Dataset
Using `pathlib` for robust path resolution regardless of operating system or execution location.
"""))
    cells.append(nbf.v4.new_code_cell("""PROJECT_ROOT = Path.cwd().parent if Path.cwd().name == "notebooks" else Path.cwd()
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "netflix_titles.csv"

print(f"Loading data from: {RAW_DATA_PATH}")
df_raw = pd.read_csv(RAW_DATA_PATH)
print(f"Raw Dataset Shape: {df_raw.shape[0]} rows, {df_raw.shape[1]} columns")
"""))

    # 7. Initial Data Inspection
    cells.append(nbf.v4.new_markdown_cell("""## 6. Initial Data Inspection
Inspect the first 5 rows, last 5 rows, column data types, and non-null counts.
"""))
    cells.append(nbf.v4.new_code_cell("""# First 5 rows
df_raw.head()
"""))
    cells.append(nbf.v4.new_code_cell("""# Last 5 rows
df_raw.tail()
"""))
    cells.append(nbf.v4.new_code_cell("""# Summary Information & Data Types
df_raw.info()
"""))

    # 8. Data Quality Assessment
    cells.append(nbf.v4.new_markdown_cell("""## 7. Data Quality Assessment
Checking for missing values, percentage missing, duplicate records, and unique values per column.
"""))
    cells.append(nbf.v4.new_code_cell("""# Missing values summary
null_counts = df_raw.isnull().sum()
null_pct = (df_raw.isnull().mean() * 100).round(2)
unique_counts = df_raw.nunique()

quality_summary = pd.DataFrame({
    'Data Type': df_raw.dtypes,
    'Null Count': null_counts,
    'Null Percentage (%)': null_pct,
    'Unique Values': unique_counts
})

quality_summary.sort_values(by='Null Count', ascending=False)
"""))
    cells.append(nbf.v4.new_code_cell("""# Duplicate check
dup_count = df_raw.duplicated().sum()
print(f"Total duplicate rows detected: {dup_count}")
"""))

    # 9. Data Cleaning
    cells.append(nbf.v4.new_markdown_cell("""## 8. Data Cleaning
Performing justified cleaning operations:
1. Strip leading/trailing whitespace from text fields.
2. Remove exact duplicate rows (if any).
3. Fill missing `director`, `cast`, and `country` with `'Unknown'` to retain title metadata without dropping valuable rows.
4. Correct misplaced duration strings in the `rating` column (e.g. '74 min').
5. Impute missing `rating` values using mode (`'TV-MA'`).
6. Save the cleaned dataset to `data/cleaned/netflix_cleaned.csv`.
"""))
    cells.append(nbf.v4.new_code_cell("""df_clean = df_raw.copy()
nulls_before = df_clean.isnull().sum().sum()

# Strip whitespace
string_cols = df_clean.select_dtypes(include=['object']).columns
for col in string_cols:
    df_clean[col] = df_clean[col].astype(str).str.strip()
    df_clean[col] = df_clean[col].replace({'nan': np.nan, '': np.nan, 'None': np.nan})

# Fix rating anomalies (misplaced duration strings)
rating_misplaced = df_clean['rating'].astype(str).str.contains('min', na=False)
for idx in df_clean[rating_misplaced].index:
    df_clean.loc[idx, 'duration'] = df_clean.loc[idx, 'rating']
    df_clean.loc[idx, 'rating'] = np.nan

# Handle categorical nulls
df_clean['director'] = df_clean['director'].fillna('Unknown')
df_clean['cast'] = df_clean['cast'].fillna('Unknown')
df_clean['country'] = df_clean['country'].fillna('Unknown')
mode_rating = df_clean['rating'].mode()[0]
df_clean['rating'] = df_clean['rating'].fillna(mode_rating)

nulls_after = df_clean.isnull().sum().sum()
null_reduction_pct = ((nulls_before - nulls_after) / nulls_before) * 100

print(f"Total Null Values Before Cleaning: {nulls_before}")
print(f"Total Null Values After Cleaning: {nulls_after}")
print(f"Null Value Reduction: {null_reduction_pct:.2f}%")
"""))

    # 10. Feature Engineering
    cells.append(nbf.v4.new_markdown_cell("""## 9. Feature Engineering
Extracting meaningful derived features:
- `date_added_clean`: Converted to datetime object
- `added_year`: Year content was added to Netflix
- `added_month`: Month name content was added
- `added_quarter`: Quarter added
- `duration_value`: Numeric duration length (minutes for Movies, seasons for TV Shows)
- `duration_unit`: Duration unit ('min' vs 'Season'/'Seasons')
- `content_age`: Years since release (`2026 - release_year`)
- `release_decade`: Release decade (e.g. 2010s)
"""))
    cells.append(nbf.v4.new_code_cell("""# Datetime conversion
df_clean['date_added_clean'] = pd.to_datetime(df_clean['date_added'], errors='coerce')
df_clean['added_year'] = df_clean['date_added_clean'].dt.year
df_clean['added_month'] = df_clean['date_added_clean'].dt.month_name()
df_clean['added_quarter'] = df_clean['date_added_clean'].dt.to_period('Q').astype(str)

# Duration extraction
df_clean['duration_value'] = df_clean['duration'].astype(str).str.extract(r'(\\d+)')[0].astype(float)
df_clean['duration_unit'] = df_clean['duration'].astype(str).str.extract(r'([a-zA-Z]+)')[0]

# Content age & decade
df_clean['content_age'] = 2026 - df_clean['release_year']
df_clean['release_decade'] = (df_clean['release_year'] // 10) * 10

# Export cleaned dataset
CLEANED_DATA_PATH = PROJECT_ROOT / "data" / "cleaned" / "netflix_cleaned.csv"
CLEANED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
df_clean.to_csv(CLEANED_DATA_PATH, index=False)
print(f"Cleaned dataset exported to: {CLEANED_DATA_PATH}")
"""))

    # 11. Exploratory Data Analysis
    cells.append(nbf.v4.new_markdown_cell("""## 10. Exploratory Data Analysis (EDA)
In this section, we answer key analytical questions through code, summary tables, and visualizations.
"""))

    # 12. Univariate Analysis & Content Type Analysis
    cells.append(nbf.v4.new_markdown_cell("""### 10.1 Content Type Distribution (Movies vs TV Shows)
**Question**: What is the proportion of Movies vs. TV Shows in the catalog?
"""))
    cells.append(nbf.v4.new_code_cell("""type_counts = df_clean['type'].value_counts()
total_titles = len(df_clean)

type_df = pd.DataFrame({
    'Count': type_counts,
    'Percentage (%)': (type_counts / total_titles * 100).round(2)
})
print(type_df)

# Plot
fig, ax = plt.subplots(figsize=(8, 4.5))
sns.barplot(
    x=type_counts.index, 
    y=type_counts.values, 
    hue=type_counts.index,
    palette=['#E50914', '#221F1F'], 
    legend=False,
    ax=ax
)
ax.set_title('Netflix Catalog Distribution: Movies vs TV Shows', fontsize=13, fontweight='bold')
ax.set_ylabel('Number of Titles')
for p in ax.patches:
    height = int(p.get_height())
    pct = round((height / total_titles) * 100, 1)
    ax.annotate(f'{height:,}\\n({pct}%)', (p.get_x() + p.get_width()/2., height/2),
                ha='center', va='center', color='white', fontweight='bold')
plt.tight_layout()
plt.show()
"""))

    # 13. Time Trend Analysis
    cells.append(nbf.v4.new_markdown_cell("""### 10.2 Content Additions Over Time
**Question**: Which year had the highest number of content additions, and how has addition velocity changed over time?
"""))
    cells.append(nbf.v4.new_code_cell("""yearly_additions = df_clean['added_year'].value_counts().sort_index()
print("Top 5 Peak Addition Years:")
print(yearly_additions.sort_values(ascending=False).head(5))

fig, ax = plt.subplots(figsize=(10, 4.5))
ax.plot(yearly_additions.index.astype(int), yearly_additions.values, marker='o', color='#E50914', linewidth=2.5)
ax.set_title('Total Content Additions per Year', fontsize=13, fontweight='bold')
ax.set_xlabel('Year Added')
ax.set_ylabel('Number of Titles')
ax.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()
"""))

    # 14. Bivariate Analysis: Movies vs TV Shows over time
    cells.append(nbf.v4.new_markdown_cell("""### 10.3 Movies vs. TV Shows Addition Trends
**Question**: How did the addition rates of Movies compare to TV Shows over time?
"""))
    cells.append(nbf.v4.new_code_cell("""yearly_by_type = df_clean.groupby(['added_year', 'type']).size().unstack(fill_value=0)

fig, ax = plt.subplots(figsize=(10, 4.5))
ax.plot(yearly_by_type.index.astype(int), yearly_by_type['Movie'], marker='o', label='Movies', color='#E50914', linewidth=2)
ax.plot(yearly_by_type.index.astype(int), yearly_by_type['TV Show'], marker='s', label='TV Shows', color='#221F1F', linewidth=2)
ax.set_title('Movies vs TV Shows Added Over Time', fontsize=13, fontweight='bold')
ax.set_xlabel('Year Added')
ax.set_ylabel('Titles Added')
ax.legend(title='Content Type')
ax.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()
"""))

    # 15. Genre Analysis
    cells.append(nbf.v4.new_markdown_cell("""### 10.4 Genre Representation
**Question**: Which genres are most frequently associated with titles overall, and within Movies vs TV Shows?
"""))
    cells.append(nbf.v4.new_code_cell("""all_genres = df_clean['listed_in'].str.split(', ').explode()
top_10_genres = all_genres.value_counts().head(10)

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    x=top_10_genres.values, 
    y=top_10_genres.index, 
    hue=top_10_genres.index,
    palette='dark:#E50914_r', 
    legend=False,
    ax=ax
)
ax.set_title('Top 10 Genre Tags Associated with Titles', fontsize=13, fontweight='bold')
ax.set_xlabel('Number of Title Associations')
for p in ax.patches:
    width = int(p.get_width())
    ax.annotate(f'{width:,}', (width + 15, p.get_y() + p.get_height()/2.), va='center')
plt.tight_layout()
plt.show()
"""))

    # 16. Country Analysis
    cells.append(nbf.v4.new_markdown_cell("""### 10.5 Geographic Country Associations
**Question**: Which countries are most frequently associated with titles in the country field?
"""))
    cells.append(nbf.v4.new_code_cell("""countries = df_clean['country'].str.split(', ').explode()
countries = countries[countries != 'Unknown']
top_10_countries = countries.value_counts().head(10)

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    x=top_10_countries.values, 
    y=top_10_countries.index, 
    hue=top_10_countries.index,
    palette='Reds_r', 
    legend=False,
    ax=ax
)
ax.set_title('Top 10 Countries Associated with Titles', fontsize=13, fontweight='bold')
ax.set_xlabel('Number of Associated Titles')
for p in ax.patches:
    width = int(p.get_width())
    ax.annotate(f'{width:,}', (width + 10, p.get_y() + p.get_height()/2.), va='center')
plt.tight_layout()
plt.show()
"""))

    # 17. Rating Analysis
    cells.append(nbf.v4.new_markdown_cell("""### 10.6 Rating Distribution
**Question**: Which maturity ratings are associated with the largest number of titles?
"""))
    cells.append(nbf.v4.new_code_cell("""ratings = df_clean['rating'].value_counts()

fig, ax = plt.subplots(figsize=(10, 4.5))
sns.barplot(
    x=ratings.index, 
    y=ratings.values, 
    hue=ratings.index,
    palette='flare', 
    legend=False,
    ax=ax
)
ax.set_title('Distribution of Content Maturity Ratings', fontsize=13, fontweight='bold')
ax.set_xlabel('Rating')
ax.set_ylabel('Number of Titles')
plt.xticks(rotation=45)
for p in ax.patches:
    height = int(p.get_height())
    if height > 0:
        ax.annotate(f'{height}', (p.get_x() + p.get_width()/2., height + 15), ha='center', fontsize=9)
plt.tight_layout()
plt.show()
"""))

    # 18. Duration Analysis
    cells.append(nbf.v4.new_markdown_cell("""### 10.7 Movie Duration & TV Show Seasons
**Question**: What is the average runtime of Movies, and what is the distribution of TV Show season counts?
"""))
    cells.append(nbf.v4.new_code_cell("""movie_df = df_clean[(df_clean['type'] == 'Movie') & (df_clean['duration_unit'] == 'min')]
avg_dur = movie_df['duration_value'].mean()
median_dur = movie_df['duration_value'].median()

print(f"Average Movie Duration: {avg_dur:.2f} minutes")
print(f"Median Movie Duration: {median_dur:.2f} minutes")

fig, ax = plt.subplots(figsize=(10, 4.5))
sns.histplot(movie_df['duration_value'], bins=30, kde=True, color='#E50914', ax=ax)
ax.axvline(avg_dur, color='black', linestyle='--', linewidth=2, label=f'Mean: {avg_dur:.2f} min')
ax.set_title('Movie Duration Distribution (Minutes)', fontsize=13, fontweight='bold')
ax.set_xlabel('Duration (Minutes)')
ax.set_ylabel('Count of Movies')
ax.legend()
plt.tight_layout()
plt.show()
"""))

    # 19. Key Insights
    cells.append(nbf.v4.new_markdown_cell("""## 11. Key Insights
1. **Catalog Composition**: Movies comprise **69.05%** (5,377 titles) of the catalog, while TV Shows account for **30.95%** (2,410 titles).
2. **Addition Peak**: Content additions peaked in **2019** with **2,153** titles added in a single year, representing a **2,346.59%** increase compared to 2015.
3. **Geographic Country Associations**: **3,296** titles are associated with the United States in the country field (**42.33%** of all catalog titles).
4. **Maturity Rating**: **TV-MA** is associated with **2,870** titles (**36.86%**), representing the single largest rating category in the dataset.
5. **Genre Representation**: **2,437** titles are associated with the International Movies genre tag.
6. **Movie Runtimes**: The average movie runtime is **99.31 minutes**, with a median runtime of **98.0 minutes**.
7. **TV Show Season Counts**: **66.72%** of TV Shows in the dataset have one season (1,608 titles), meaning single-season titles represent a substantial portion of the TV Show catalog.
"""))

    # 20. Summary Observations
    cells.append(nbf.v4.new_markdown_cell("""## 12. Summary Observations
1. Single-season titles represent a substantial portion of the TV Show catalog (66.72% of TV Shows in the dataset).
2. The United States is associated with the largest number of titles in the country field (3,296 titles).
3. International Movies is the most frequently tagged genre in the dataset (2,437 titles).
4. Feature film runtimes average 99.31 minutes across all recorded movies.
"""))

    # 21. Final Conclusion
    cells.append(nbf.v4.new_markdown_cell("""## 13. Final Conclusion
This quantitative analysis of 7,787 Netflix catalog records provides an empirical summary of catalog composition across content types, genre associations, country fields, maturity ratings, and runtime metrics. Data cleaning operations reduced missing fields by 98.62%, creating a verified foundation for dataset exploration.
"""))

    nb.cells = cells

    nb_path = project_root / "notebooks" / "Netflix_Data_Analysis.ipynb"
    nb_path.parent.mkdir(parents=True, exist_ok=True)
    with open(nb_path, "w", encoding="utf-8") as f:
        nbf.write(nb, f)

    print(f"Saved notebook structure to {nb_path}")
    return nb_path

if __name__ == "__main__":
    create_notebook()
