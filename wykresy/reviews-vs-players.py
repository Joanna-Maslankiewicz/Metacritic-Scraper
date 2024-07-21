import pandas as pd
import matplotlib.pyplot as plt

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

# Funkcja do tworzenia wykresów dla każdej gry
def plot_reviews_vs_players(game_title, player_file):
    # Wczytanie danych graczy
    players = pd.read_csv(player_file, sep=';', parse_dates=['DateTime'], dayfirst=True)
    players['DateTime'] = pd.to_datetime(players['DateTime'], format='%d.%m.%Y %H:%M')
    
    # Filtrowanie recenzji dla danej gry
    game_reviews = reviews[reviews['Game'].str.lower().str.replace(':', '') == game_title.lower().replace(':', '')]
    print(f"Gra: {game_title}, Liczba recenzji: {len(game_reviews)}")  # Diagnostyka
    
    if game_reviews.empty:
        print(f"Brak recenzji dla gry: {game_title}")
        return

    # Sprawdzenie, czy kolumna 'Score' zawiera tylko liczby
    game_reviews['Score'] = pd.to_numeric(game_reviews['Score'], errors='coerce')
    game_reviews.dropna(subset=['Score'], inplace=True)

    # Grupowanie danych miesięcznie i obliczanie średniej ocen
    monthly_reviews = game_reviews.set_index('Review Date').resample('M').mean(numeric_only=True)
    monthly_players = players.set_index('DateTime').resample('M').mean()

    # Klasyfikowanie miesięcy jako pozytywne lub negatywne
    monthly_reviews['Review Type'] = monthly_reviews['Score'].apply(lambda x: 'Pozytywna recenzja' if x > 6 else 'Negatywna recenzja')

    # Tworzenie wykresu
    plt.figure(figsize=(14, 6))
    plt.plot(monthly_players.index, monthly_players['Players'], marker='o', label='Liczba graczy')

    # Dodanie recenzji jako pionowe linie
    for idx, row in monthly_reviews.iterrows():
        if row['Review Type'] == 'Pozytywna recenzja':
            plt.axvline(idx, color='green', linestyle='--', alpha=0.7, label='Pozytywna recenzja')
        else:
            plt.axvline(idx, color='red', linestyle='--', alpha=0.7, label='Negatywna recenzja')

    plt.xlabel('Data')
    plt.ylabel('Liczba graczy')
    plt.title(f'Liczba graczy dla gry {game_title} w odniesieniu do typu recenzji')
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())
    plt.grid(True)
    plt.show()

# Iteracja przez wszystkie pliki graczy
for player_file in player_files:
    game_title = ' '.join(player_file.split('-')[1:]).replace('.csv', '').replace('-', ' ').title()
    plot_reviews_vs_players(game_title, player_file)
