import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import numpy as np

# Ładowanie danych o recenzjach
reviews = pd.read_csv('metacritic_reviews_selenium.csv', parse_dates=['Review Date'])
reviews['Score'] = pd.to_numeric(reviews['Score'], errors='coerce')  # Konwersja na liczby, ignorowanie błędów
reviews.dropna(subset=['Score'], inplace=True)  # Usunięcie wierszy z 'tbd' lub innymi nie-liczbowymi wartościami

# Pliki z danymi graczy
player_files = [
    'players-cyberpunk-2077.csv', 
    'players-dark-souls-II.csv', 
    'players-dragons-dogma-2.csv',
    'players-fallout-4.csv',
    'players-mass-effect-3.csv',
    'players-mass-effect-andromeda.csv',
    'players-new-world.csv',
    'players-the-elder-scrolls-V-skyrim.csv',
    'players-starfield.csv',
    'players-warhammer-chaosbane.csv'
]

# Funkcja do analizy korelacji i dodania wartości p
def analyze_correlation(game_title, player_file):

    players = pd.read_csv(player_file, sep=';', parse_dates=['DateTime'], dayfirst=True)
    players['DateTime'] = pd.to_datetime(players['DateTime'], format='%d.%m.%Y %H:%M')
    
    # Filtrowanie recenzji dla danej gry
    game_reviews = reviews[reviews['Game'].str.lower().str.replace(':', '') == game_title.lower().replace(':', '')]
    if game_reviews.empty:
        return game_title, None, None

    # Konwersja ocen na liczby
    game_reviews['Score'] = pd.to_numeric(game_reviews['Score'], errors='coerce')
    game_reviews.dropna(subset=['Score'], inplace=True)

    # Grupowanie miesięczne i obliczanie średnich
    monthly_reviews = game_reviews.set_index('Review Date').resample('M').mean(numeric_only=True)
    monthly_players = players.set_index('DateTime').resample('M').mean()

    # Łączenie danych
    combined_data = pd.merge(monthly_players, monthly_reviews, left_index=True, right_index=True)
    
    if combined_data.empty:
        return game_title, None, None
    
    # Usunięcie NaNs i infs
    combined_data = combined_data.replace([float('inf'), float('-inf')], float('nan')).dropna()

    if combined_data.empty:
        return game_title, None, None

    # Obliczanie korelacji
    correlation, p_value = pearsonr(combined_data['Players'], combined_data['Score'])
    return game_title, correlation, p_value

# Analiza korelacji dla wszystkich gier
results = []
for player_file in player_files:
    game_title = ' '.join(player_file.split('-')[1:]).replace('.csv', '').replace('-', ' ').title()
    game_title, correlation, p_value = analyze_correlation(game_title, player_file)
    if correlation is not None:
        results.append((game_title, correlation, p_value))

# Tworzenie wykresu
results_df = pd.DataFrame(results, columns=['Game', 'Correlation', 'P-Value'])
results_df.sort_values(by='Correlation', inplace=True)

# Definiowanie kolorów w zależności od mocy korelacji
colors = plt.cm.viridis(results_df['Correlation'] / max(results_df['Correlation']))

plt.figure(figsize=(16, 9))
bars = plt.barh(results_df['Game'], results_df['Correlation'], color=colors)

# Dodawanie wartości p na wykresie
for bar, p_value in zip(bars, results_df['P-Value']):
    plt.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height() / 2,
             f'p={p_value:.2f}', 
             va='center', ha='left', color='black', fontsize=14)

plt.xlabel('Współczynnik korelacji', fontsize=18)
plt.ylabel('Gra', fontsize=18)
plt.title('Korelacja między ocenami recenzji a liczbą graczy dla różnych gier', fontsize=20)
plt.axvline(0, color='black', linewidth=0.8, linestyle='--')
plt.grid(True)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.tight_layout()
plt.show()
