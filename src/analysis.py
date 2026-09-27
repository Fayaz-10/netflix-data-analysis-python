"""
Exploratory Data Analysis and Visualization Module for Netflix Data Analysis
"""

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set global plot style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10

def get_project_root() -> Path:
    return Path(__file__).resolve().parent.parent

def run_analysis_and_visualizations(df: pd.DataFrame) -> tuple[dict, list[str]]:
    """
    Performs full exploratory data analysis and exports visualizations to visualizations/ folder.
    
    Returns:
        tuple[dict, list[str]]: (Dictionary of calculated insights, List of generated plot paths)
    """
    project_root = get_project_root()
    viz_dir = project_root / "visualizations"
    viz_dir.mkdir(parents=True, exist_ok=True)
    
    insights = {}
    generated_plots = []
    
    # Palette definition
    primary_color = '#E50914'  # Netflix Red
    secondary_color = '#221F1F'  # Dark Charcoal
    
    # ----------------------------------------------------
    # A, B, C: Content Type Breakdown
    # ----------------------------------------------------
    type_counts = df['type'].value_counts()
    total_titles = len(df)
    movie_count = int(type_counts.get('Movie', 0))
    tv_count = int(type_counts.get('TV Show', 0))
    movie_pct = round((movie_count / total_titles) * 100, 2)
    tv_pct = round((tv_count / total_titles) * 100, 2)
    
    insights['total_titles'] = total_titles
    insights['movie_count'] = movie_count
    insights['tv_count'] = tv_count
    insights['movie_pct'] = movie_pct
    insights['tv_pct'] = tv_pct
    
    # Chart 1: Movies vs TV Shows
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = sns.barplot(
        x=type_counts.index, 
        y=type_counts.values, 
        hue=type_counts.index,
        palette=[primary_color, secondary_color], 
        legend=False,
        ax=ax
    )
    ax.set_title('Netflix Catalog Distribution: Movies vs TV Shows', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Content Type', fontsize=12)
    ax.set_ylabel('Number of Titles', fontsize=12)
    for p in ax.patches:
        height = int(p.get_height())
        pct = round((height / total_titles) * 100, 1)
        ax.annotate(f'{height:,}\n({pct}%)', (p.get_x() + p.get_width() / 2., height / 2),
                    ha='center', va='center', fontsize=11, color='white', fontweight='bold')
    plt.tight_layout()
    chart1_path = viz_dir / "content_type_distribution.png"
    plt.savefig(chart1_path, dpi=300)
    plt.close()
    generated_plots.append("content_type_distribution.png")

    # ----------------------------------------------------
    # D, E: Content Added by Year
    # ----------------------------------------------------
    yearly_added = df.groupby(['added_year', 'type']).size().unstack(fill_value=0)
    yearly_total = df['added_year'].value_counts().sort_index()
    
    peak_year = int(yearly_total.idxmax()) if not yearly_total.empty else 0
    peak_count = int(yearly_total.max()) if not yearly_total.empty else 0
    
    insights['peak_addition_year'] = peak_year
    insights['peak_addition_count'] = peak_count
    
    count_2015 = int(yearly_total.get(2015, 0))
    count_2019 = int(yearly_total.get(2019, 0))
    growth_2015_2019_pct = round(((count_2019 - count_2015) / count_2015) * 100, 2) if count_2015 > 0 else 0
    insights['growth_2015_2019_pct'] = growth_2015_2019_pct
    
    # Chart 2: Content Added by Year (Total)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(yearly_total.index.astype(int), yearly_total.values, marker='o', color=primary_color, linewidth=2.5)
    ax.set_title('Total Netflix Content Added per Year', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Year Added', fontsize=12)
    ax.set_ylabel('Number of Titles Added', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    chart2_path = viz_dir / "content_added_by_year.png"
    plt.savefig(chart2_path, dpi=300)
    plt.close()
    generated_plots.append("content_added_by_year.png")

    # Chart 8: Movies vs TV Shows Over Time
    fig, ax = plt.subplots(figsize=(10, 5))
    if 'Movie' in yearly_added.columns:
        ax.plot(yearly_added.index.astype(int), yearly_added['Movie'], marker='o', label='Movies', color=primary_color, linewidth=2)
    if 'TV Show' in yearly_added.columns:
        ax.plot(yearly_added.index.astype(int), yearly_added['TV Show'], marker='s', label='TV Shows', color=secondary_color, linewidth=2)
    ax.set_title('Movies vs TV Shows Added Over Time', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Year Added', fontsize=12)
    ax.set_ylabel('Titles Added', fontsize=12)
    ax.legend(title='Content Type')
    ax.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    chart8_path = viz_dir / "movies_vs_tv_shows_over_time.png"
    plt.savefig(chart8_path, dpi=300)
    plt.close()
    generated_plots.append("movies_vs_tv_shows_over_time.png")

    # ----------------------------------------------------
    # F, M: Top Contributing Countries
    # ----------------------------------------------------
    country_series = df['country'].str.split(', ').explode()
    country_series = country_series[country_series != 'Unknown']
    top_countries = country_series.value_counts().head(10)
    
    top_country_name = top_countries.index[0] if not top_countries.empty else "N/A"
    top_country_count = int(top_countries.iloc[0]) if not top_countries.empty else 0
    top_country_pct = round((top_country_count / total_titles) * 100, 2)
    
    insights['top_country'] = top_country_name
    insights['top_country_count'] = top_country_count
    insights['top_country_pct'] = top_country_pct

    # Chart 3: Top 10 Countries
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        x=top_countries.values, 
        y=top_countries.index, 
        hue=top_countries.index,
        palette='Reds_r', 
        legend=False,
        ax=ax
    )
    ax.set_title('Top 10 Content Producing Countries in Catalog', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Number of Titles (Includes Joint Productions)', fontsize=12)
    ax.set_ylabel('Country', fontsize=12)
    for p in ax.patches:
        width = int(p.get_width())
        ax.annotate(f'{width:,}', (width + 10, p.get_y() + p.get_height() / 2.),
                    va='center', fontsize=10)
    plt.tight_layout()
    chart3_path = viz_dir / "top_countries.png"
    plt.savefig(chart3_path, dpi=300)
    plt.close()
    generated_plots.append("top_countries.png")

    # ----------------------------------------------------
    # G, K, L: Top Genres
    # ----------------------------------------------------
    genre_series = df['listed_in'].str.split(', ').explode()
    top_genres = genre_series.value_counts().head(10)
    
    movie_genres = df[df['type'] == 'Movie']['listed_in'].str.split(', ').explode().value_counts().head(5)
    tv_genres = df[df['type'] == 'TV Show']['listed_in'].str.split(', ').explode().value_counts().head(5)
    
    insights['top_genre_overall'] = top_genres.index[0]
    insights['top_genre_overall_count'] = int(top_genres.iloc[0])
    insights['top_movie_genre'] = movie_genres.index[0]
    insights['top_tv_genre'] = tv_genres.index[0]

    # Chart 4: Top 10 Genres
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        x=top_genres.values, 
        y=top_genres.index, 
        hue=top_genres.index,
        palette='dark:#E50914_r', 
        legend=False,
        ax=ax
    )
    ax.set_title('Top 10 Genres in Netflix Catalog', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Number of Titles', fontsize=12)
    ax.set_ylabel('Genre', fontsize=12)
    for p in ax.patches:
        width = int(p.get_width())
        ax.annotate(f'{width:,}', (width + 15, p.get_y() + p.get_height() / 2.),
                    va='center', fontsize=10)
    plt.tight_layout()
    chart4_path = viz_dir / "top_genres.png"
    plt.savefig(chart4_path, dpi=300)
    plt.close()
    generated_plots.append("top_genres.png")

    # ----------------------------------------------------
    # H, N: Ratings Analysis
    # ----------------------------------------------------
    rating_counts = df['rating'].value_counts()
    top_rating_name = rating_counts.index[0]
    top_rating_count = int(rating_counts.iloc[0])
    top_rating_pct = round((top_rating_count / total_titles) * 100, 2)
    
    insights['top_rating'] = top_rating_name
    insights['top_rating_count'] = top_rating_count
    insights['top_rating_pct'] = top_rating_pct

    # Chart 5: Ratings Distribution
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(
        x=rating_counts.index, 
        y=rating_counts.values, 
        hue=rating_counts.index,
        palette='flare', 
        legend=False,
        ax=ax
    )
    ax.set_title('Distribution of Content Ratings', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Rating Category', fontsize=12)
    ax.set_ylabel('Number of Titles', fontsize=12)
    plt.xticks(rotation=45)
    for p in ax.patches:
        height = int(p.get_height())
        if height > 0:
            ax.annotate(f'{height}', (p.get_x() + p.get_width() / 2., height + 15),
                        ha='center', fontsize=9)
    plt.tight_layout()
    chart5_path = viz_dir / "ratings_distribution.png"
    plt.savefig(chart5_path, dpi=300)
    plt.close()
    generated_plots.append("ratings_distribution.png")

    # ----------------------------------------------------
    # I: Movie Duration Analysis
    # ----------------------------------------------------
    movie_df = df[(df['type'] == 'Movie') & (df['duration_unit'] == 'min')].copy()
    avg_movie_duration = round(movie_df['duration_value'].mean(), 2) if not movie_df.empty else 0
    median_movie_duration = round(movie_df['duration_value'].median(), 2) if not movie_df.empty else 0
    
    insights['avg_movie_duration'] = float(avg_movie_duration)
    insights['median_movie_duration'] = float(median_movie_duration)

    # Chart 6: Movie Duration Distribution
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(movie_df['duration_value'], bins=30, kde=True, color=primary_color, ax=ax)
    ax.axvline(avg_movie_duration, color='black', linestyle='--', linewidth=2, label=f'Mean: {avg_movie_duration} min')
    ax.set_title('Movie Duration Distribution (Minutes)', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Duration (Minutes)', fontsize=12)
    ax.set_ylabel('Count of Movies', fontsize=12)
    ax.legend()
    plt.tight_layout()
    chart6_path = viz_dir / "movie_duration_distribution.png"
    plt.savefig(chart6_path, dpi=300)
    plt.close()
    generated_plots.append("movie_duration_distribution.png")

    # ----------------------------------------------------
    # J: TV Show Season Counts
    # ----------------------------------------------------
    tv_df = df[df['type'] == 'TV Show'].copy()
    season_counts = tv_df['duration_value'].value_counts().sort_index()
    single_season_count = int(season_counts.get(1.0, 0))
    single_season_pct = round((single_season_count / tv_count) * 100, 2) if tv_count > 0 else 0
    
    insights['tv_single_season_count'] = single_season_count
    insights['tv_single_season_pct'] = single_season_pct

    # Chart 10: TV Show Season Distribution
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(
        x=season_counts.index.astype(int), 
        y=season_counts.values, 
        hue=season_counts.index.astype(int),
        palette='crest', 
        legend=False,
        ax=ax
    )
    ax.set_title('TV Show Duration by Number of Seasons', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Number of Seasons', fontsize=12)
    ax.set_ylabel('Number of TV Shows', fontsize=12)
    for p in ax.patches:
        height = int(p.get_height())
        if height > 0:
            ax.annotate(f'{height}', (p.get_x() + p.get_width() / 2., height + 10),
                        ha='center', fontsize=9)
    plt.tight_layout()
    chart10_path = viz_dir / "tv_show_seasons_distribution.png"
    plt.savefig(chart10_path, dpi=300)
    plt.close()
    generated_plots.append("tv_show_seasons_distribution.png")

    # ----------------------------------------------------
    # Chart 9: Top Countries by Content Type
    # ----------------------------------------------------
    top_5_countries = top_countries.head(5).index.tolist()
    country_type_df = df[df['country'].isin(top_5_countries)].groupby(['country', 'type']).size().unstack(fill_value=0)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    country_type_df.plot(kind='bar', color=[primary_color, secondary_color], ax=ax, width=0.7)
    ax.set_title('Content Type Breakdown for Top 5 Production Countries', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Country', fontsize=12)
    ax.set_ylabel('Number of Titles', fontsize=12)
    plt.xticks(rotation=0)
    plt.legend(title='Content Type')
    plt.tight_layout()
    chart9_path = viz_dir / "top_countries_by_type.png"
    plt.savefig(chart9_path, dpi=300)
    plt.close()
    generated_plots.append("top_countries_by_type.png")

    print(f"Generated {len(generated_plots)} visualization files in {viz_dir}")
    return insights, generated_plots

if __name__ == "__main__":
    from data_loading import load_raw_data
    from data_cleaning import clean_netflix_data
    df_raw = load_raw_data()
    df_clean, _ = clean_netflix_data(df_raw)
    insights, plots = run_analysis_and_visualizations(df_clean)
    print("Calculated Insights:", insights)
