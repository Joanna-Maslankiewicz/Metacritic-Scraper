import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr
import numpy as np

# Funkcja do ładowania danych o liczbie graczy dla danej gry
def load_player_data(game_file):
    return pd.read_csv(game_file, delimiter=';', parse_dates=['DateTime'], dayfirst=True)

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

# Funkcja do analizy korelacji
def analyze_correlation(game_title, player_file):
    # Wczytanie danych graczy
    players = pd.read_csv(player_file, sep=';', parse_dates=['DateTime'], dayfirst=True)
    players['DateTime'] = pd.to_datetime(players['DateTime'], format='%d.%m.%Y %H:%M')
    
    # Filtrowanie recenzji dla danej gry
    game_reviews = reviews[reviews['Game'].str.lower().str.replace(':', '') == game_title.lower().replace(':', '')]
    
    if game_reviews.empty:
        print(f"Brak recenzji dla gry: {game_title}")
        return

    # Sprawdzenie, czy kolumna 'Score' zawiera tylko liczby
    game_reviews['Score'] = pd.to_numeric(game_reviews['Score'], errors='coerce')
    game_reviews.dropna(subset=['Score'], inplace=True)

    # Grupowanie danych miesięcznie i obliczenie średniej ocen
    monthly_reviews = game_reviews.set_index('Review Date').resample('M').mean(numeric_only=True)
    monthly_players = players.set_index('DateTime').resample('M').mean()

    # Usuwanie wierszy z brakującymi wartościami
    combined_data = pd.merge(monthly_players, monthly_reviews, left_index=True, right_index=True, how='inner')
    combined_data = combined_data.dropna(subset=['Players', 'Score'])

    # Obliczenie korelacji
    if combined_data.empty:
        print(f"Brak wystarczających danych do analizy korelacji dla gry: {game_title}")
        return
    
    correlation, p_value = pearsonr(combined_data['Players'], combined_data['Score'])
    print(f"Gra: {game_title}, Korelacja: {correlation:.2f}, P-wartość: {p_value:.2f}")

    # Wykres korelacji
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='Score', y='Players', data=combined_data)
    plt.title(f'Korelacja między ocenami recenzji a liczbą graczy dla gry {game_title}')
    plt.xlabel('Średnia ocena recenzji')
    plt.ylabel('Średnia liczba graczy')
    plt.grid(True)
    plt.show()

# Iteracja przez wszystkie pliki graczy
for player_file in player_files:
    game_title = ' '.join(player_file.split('-')[1:]).replace('.csv', '').replace('-', ' ').title()
    analyze_correlation(game_title, player_file)
