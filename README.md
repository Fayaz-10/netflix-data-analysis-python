# Netflix Data Analysis using Python

An end-to-end data analysis portfolio project inspecting Netflix's streaming catalog. This project demonstrates raw data loading, quality auditing, data cleaning, feature engineering, exploratory data analysis (EDA), statistical modeling, and data visualization using Python, Pandas, Matplotlib, and Seaborn.

---

## 1. Project Overview
Understanding catalog composition—movie-to-TV ratio, geographic country associations, maturity ratings, genre representation, and release addition velocity—is critical for analyzing streaming catalog trends.

This repository implements a modular Python pipeline and an interactive Jupyter Notebook to analyze **7,787 catalog records** cleanly and reproducibly.

---

## 2. Project Objectives
- **Data Quality Audit**: Identify and resolve missing values, improper data types, whitespace inconsistencies, and duplicate records.
- **Catalog Structure Analysis**: Quantify the proportion of Movies vs. TV Shows and track annual addition trends.
- **Geographic & Genre Representation**: Analyze country associations and genre frequencies across catalog titles.
- **Duration & Rating Distribution**: Evaluate feature film runtimes, TV show season counts, and rating categories.
- **Data-Driven Summaries**: Formulate objective summary insights based strictly on empirical dataset metrics.

---

## 3. Dataset Characteristics
- **Source**: Authentic Netflix Movies and TV Shows Catalog Dataset.
- **Rows**: 7,787
- **Columns**: 12 (`show_id`, `type`, `title`, `director`, `cast`, `country`, `date_added`, `release_year`, `rating`, `duration`, `listed_in`, `description`)
- **Raw Null Count**: 3,631 total missing values across `director`, `cast`, `country`, `date_added`, and `rating`.

---

## 4. Technologies & Libraries
- **Language**: Python 3.13
- **Data Manipulation**: Pandas, NumPy
- **Data Visualization**: Matplotlib, Seaborn
- **Environment**: Jupyter Notebook, Pathlib

---

## 5. Project Structure
```
Netflix-Data-Analysis/
│
├── data/
│   ├── raw/
│   │   └── netflix_titles.csv
│   └── cleaned/
│       └── netflix_cleaned.csv
│
├── notebooks/
│   └── Netflix_Data_Analysis.ipynb
│
├── src/
│   ├── data_loading.py
│   ├── data_cleaning.py
│   └── analysis.py
│
├── visualizations/
│   ├── content_type_distribution.png
│   ├── content_added_by_year.png
│   ├── top_countries.png
│   ├── top_genres.png
│   ├── ratings_distribution.png
│   ├── movie_duration_distribution.png
│   ├── movies_vs_tv_shows_over_time.png
│   ├── top_countries_by_type.png
│   └── tv_show_seasons_distribution.png
│
├── reports/
│   └── netflix_analysis_report.md
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

## 6. Data Cleaning & Feature Engineering

### Quality Improvements:
- **Duplicate Removal**: 0 duplicate rows detected.
- **Null Value Treatment**:
  - Imputed missing `director`, `cast`, and `country` with `'Unknown'`.
  - Resolved misplaced duration values in `rating` column.
  - Imputed missing `rating` with mode (`'TV-MA'`).
- **Null Value Reduction**: Decreased total missing fields from **3,631** to **50** (a **98.62%** null reduction across primary catalog fields).

### Engineered Features:
- `date_added_clean`: Standardized datetime format.
- `added_year`, `added_month`, `added_quarter`: Temporal addition attributes.
- `duration_value` & `duration_unit`: Parsed numeric duration (minutes vs seasons).
- `content_age`: Derived catalog age (`2026 - release_year`).
- `release_decade`: Categorized decade groupings.

---

## 7. Key Findings & Empirical Results

| Metric | Calculated Result |
|---|---|
| **Total Catalog Titles** | 7,787 |
| **Movies Count & Percentage** | 5,377 titles (**69.05%**) |
| **TV Shows Count & Percentage** | 2,410 titles (**30.95%**) |
| **Peak Addition Year** | **2019** (**2,153** additions) |
| **Addition Growth (2015–2019)** | **2,346.59%** increase |
| **Top Country Association** | **3,296** titles are associated with the United States in the country field (**42.33%**) |
| **Top Rating Category** | **TV-MA** (**2,870** titles, **36.86%**) |
| **Top Genre Representation** | **2,437** titles are associated with the International Movies genre |
| **Average Movie Duration** | **99.31 minutes** (Median: 98.0 min) |
| **Single-Season TV Shows** | **1,608** TV Shows in the dataset have one season (**66.72%** of all TV shows) |

---

## 8. Catalog Summary Observations

1. **TV Show Season Distribution**: **66.72%** of TV Shows in the dataset have one season, meaning single-season titles represent a substantial portion of the TV Show catalog.
2. **Geographic Representation**: **3,296** titles are associated with the United States in the country field, **993** titles are associated with India, and **723** titles are associated with the United Kingdom.
3. **Genre Diversity**: **2,437** titles are associated with the International Movies genre, representing the most common genre tag in the dataset.
4. **Maturity Distribution**: Titles rated **TV-MA** (**2,870** titles) and **TV-14** (**1,931** titles) form the majority of rated content in the catalog.

---

## 9. How to Run the Project

### Step 1: Clone or Navigate to Project
```bash
cd Netflix-Data-Analysis
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Execute Data Pipeline
```bash
python src/data_cleaning.py
python src/analysis.py
```

### Step 4: Run Jupyter Notebook
```bash
jupyter notebook notebooks/Netflix_Data_Analysis.ipynb
```

---

## 10. Resume-Ready Project Description

> Developed an end-to-end Netflix catalog analysis using Python, Pandas, NumPy, Matplotlib, and Seaborn. Performed data cleaning, missing-value analysis, feature engineering, exploratory data analysis, and visualization on 7,787 titles. Analyzed catalog composition across content type, genres, countries, ratings, movie duration, and content addition trends, generating 9 data-driven visualizations.
