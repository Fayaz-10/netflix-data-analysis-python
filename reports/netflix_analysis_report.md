# Netflix Data Analysis Report

## Executive Summary
This report provides a quantitative exploratory data analysis (EDA) of Netflix's streaming catalog based on 7,787 titles. The primary objective is to evaluate catalog composition, geographic country associations, temporal addition trends, maturity ratings, and runtime metrics using objective dataset calculations.

---

## 1. Key Data Quality & Processing Metrics

| Metric | Empirical Value |
|---|---|
| **Raw Dataset Records** | 7,787 rows, 12 columns |
| **Cleaned Dataset Records** | 7,787 rows |
| **Duplicate Rows Removed** | 0 |
| **Total Nulls Before Cleaning** | 3,631 |
| **Total Nulls After Cleaning** | 50 (10 missing dates across 5 date-derived columns) |
| **Actual Null Reduction** | **98.62%** |

---

## 2. Main Exploratory Findings

### A. Content Type Breakdown
- **Movies**: 5,377 titles (**69.05%** of catalog)
- **TV Shows**: 2,410 titles (**30.95%** of catalog)
- **Ratio**: Approximately 2.23 Movies for every 1 TV Show.

### B. Addition Velocity Over Time
- **Peak Addition Year**: **2019** with **2,153** titles added.
- **Growth (2015–2019)**: Increased by **2,346.59%** (from 88 titles added in 2015 to 2,153 titles added in 2019).

### C. Geographic Content Representation
- **United States**: **3,296** titles are associated with the United States in the country field (**42.33%** of catalog).
- **India**: **993** titles are associated with India in the country field.
- **United Kingdom**: **723** titles are associated with the United Kingdom in the country field.

### D. Rating & Audience Demographics
- **TV-MA** (Mature Audiences): **2,870** titles (**36.86%**).
- **TV-14** (Parents Strongly Cautioned): **1,931** titles (**24.80%**).
- Combined mature/young-adult content accounts for over 61% of the total catalog.

### E. Runtime & Season Counts
- **Average Movie Duration**: **99.31 minutes** (Median: 98.0 minutes).
- **TV Show Season Counts**: **66.72%** of TV Shows in the dataset have one season (**1,608** TV shows), meaning single-season titles represent a substantial portion of the TV Show catalog.

---

## 3. Visualizations Generated

1. `visualizations/content_type_distribution.png`: Catalog split between Movies and TV Shows.
2. `visualizations/content_added_by_year.png`: Historical annual content addition trend.
3. `visualizations/top_countries.png`: Top 10 countries associated with titles.
4. `visualizations/top_genres.png`: Top 10 genres represented across the catalog.
5. `visualizations/ratings_distribution.png`: Maturity rating breakdown.
6. `visualizations/movie_duration_distribution.png`: Histogram & KDE of movie feature runtimes.
7. `visualizations/movies_vs_tv_shows_over_time.png`: Comparative trajectory of Movies vs. TV Shows over time.
8. `visualizations/top_countries_by_type.png`: Content type breakdown for top 5 associated countries.
9. `visualizations/tv_show_seasons_distribution.png`: TV Show season count distribution.

---

## 4. Summary Observations

1. **TV Show Season Representation**: 66.72% of TV Shows in the dataset have one season, meaning single-season titles represent a substantial portion of the TV Show catalog.
2. **Geographic Distribution**: 3,296 titles are associated with the United States in the country field, representing the highest frequency among recorded countries.
3. **Genre Tags**: 2,437 titles are associated with the International Movies genre, representing the most common genre tag in the dataset.
4. **Rating Representation**: TV-MA and TV-14 ratings are associated with the largest number of titles in the dataset.
