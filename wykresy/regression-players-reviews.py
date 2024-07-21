import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

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

# Funkcja do przeprowadzenia analizy regresji
def regression_analysis(game_title, player_file):
    
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

    # Dopasowanie modelu regresji liniowej
    X = combined_data[['Score']].values
    y = combined_data['Players'].values
    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)

    r2 = r2_score(y, y_pred)

    return game_title, model.coef_[0], model.intercept_, r2

# Analiza regresji dla wszystkich gier
results = []
for player_file in player_files:
    game_title = ' '.join(player_file.split('-')[1:]).replace('.csv', '').replace('-', ' ').title()
    game_title, coef, intercept, r2 = regression_analysis(game_title, player_file)
    if coef is not None:
        results.append((game_title, coef, intercept, r2))

# Tworzenie wykresu
wyniki_df = pd.DataFrame(results, columns=['Gra', 'Współczynnik', 'Przecięcie', 'R2'])
wyniki_df.sort_values(by='R2', inplace=True)

plt.figure(figsize=(16, 9))
bars = plt.barh(wyniki_df['Gra'], wyniki_df['R2'], color=plt.cm.viridis(wyniki_df['R2'] / max(wyniki_df['R2'])))

# Dodawanie wartości współczynnika na wykresie
for bar, coef, intercept, r2 in zip(bars, wyniki_df['Współczynnik'], wyniki_df['Przecięcie'], wyniki_df['R2']):
    plt.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height() / 2,
             f'wsp={coef:.2f}, przec={intercept:.2f}, R2={r2:.2f}', 
             va='center', ha='left', color='black', fontsize=15)

plt.xlabel('R^2', fontsize=20)
plt.ylabel('Gra', fontsize=20)
plt.grid(True)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.tight_layout()
plt.show()