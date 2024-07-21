import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# Load data
reviews = pd.read_csv('metacritic_reviews_selenium.csv')
release_dates = pd.read_csv('game_release.csv')

# Convert 'Score' column to numeric, replace unprocessable values with NaN, then fill NaN with the median
reviews['Score'] = pd.to_numeric(reviews['Score'], errors='coerce')
reviews['Score'].fillna(reviews['Score'].median(), inplace=True)

# Adjust critic scores
reviews['Score Adjusted'] = reviews.apply(lambda x: x['Score'] / 10 if x['Type'] == 'Critic' else x['Score'], axis=1)

# Merge review data with game release dates
reviews = pd.merge(reviews, release_dates, on='Game')

# Add a column for the review year
reviews['Review Year'] = pd.to_datetime(reviews['Review Date'], errors='coerce').dt.year

# Debugging - Check the initial data
print("Initial Data:")
print(reviews.head())

# Group data and calculate mean scores
grouped_data = reviews.groupby(['Game', 'Type', 'Review Year'])['Score Adjusted'].mean().unstack()

# Debugging - Check the structure of grouped data
print("Grouped Data:")
print(grouped_data.head())

# Reset index and rename columns properly
grouped_data = grouped_data.reset_index()
grouped_data.columns.name = None

# Debugging - Check the structure of data after resetting index
print("\nData after reset_index():")
print(grouped_data.head())

# Melt the data with the years as value variables
melted_data = grouped_data.melt(id_vars=['Game', 'Type'], var_name='Review Year', value_name='Score Adjusted')

# Convert 'Review Year' to numeric
melted_data['Review Year'] = pd.to_numeric(melted_data['Review Year'], errors='coerce')

# Debugging - Check the structure of melted data
print("\nMelted Data:")
print(melted_data.head())

# Pivot data
pivot_data = melted_data.pivot_table(index=['Game', 'Review Year'], columns='Type', values='Score Adjusted').dropna()

# Debugging - Check the structure of pivoted data
print("\nPivoted Data:")
print(pivot_data.head())

# Calculate the difference between mean scores of critics and users
pivot_data['Difference'] = pivot_data['Critic'] - pivot_data['User']

# Plot trends for each game
for game in pivot_data.index.get_level_values(0).unique():
    game_data = pivot_data.loc[game]
    plt.figure(figsize=(10, 5))
    plt.plot(game_data.index, game_data['Difference'], marker='o')
    plt.title(f'Trend różnic średnich ocen recenzentów i graczy dla gry {game}')
    plt.xlabel('Rok recenzji')
    plt.ylabel('Średnia różnica ocen')
    plt.grid(True)
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))  # Ensure x-axis shows integer year values
    plt.show()
