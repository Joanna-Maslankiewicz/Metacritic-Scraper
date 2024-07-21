import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv('metacritic_reviews_selenium.csv')

# Konwersja kolumny 'Score' na numeryczną, ignorując błędy dla 'tbd'
data['Score'] = pd.to_numeric(data['Score'], errors='coerce')

# Usuwanie wierszy z NaN w kolumnie 'Score' wynikających z 'tbd'
data.dropna(subset=['Score'], inplace=True)

# Konwersja daty recenzji na typ daty
data['Review Date'] = pd.to_datetime(data['Review Date'], format="%b %d, %Y", errors='coerce')

# Dzielenie ocen krytyków przez 10, aby dostosować skalę
data['Score Adjusted'] = data.apply(lambda x: x['Score'] / 10 if x['Type'] == 'Critic' else x['Score'], axis=1)

# Grupowanie danych po grze, miesiącu, i typie, obliczanie średniej
data.set_index('Review Date', inplace=True)
grouped = data.groupby(['Game', pd.Grouper(freq='ME'), 'Type'])['Score Adjusted'].mean().unstack()

# Przygotowanie wykresów dla każdej gry
for game, monthly_scores in grouped.groupby(level=0):
    if monthly_scores.empty:
        continue

    if 'Critic' not in monthly_scores.columns or 'User' not in monthly_scores.columns:
        continue

    # Sprawdzenie, czy istnieje wystarczająca liczba danych do analizy
    monthly_scores = monthly_scores.dropna(subset=['Critic', 'User'])
    valid_critic_scores = monthly_scores['Critic']
    valid_user_scores = monthly_scores['User']

    if len(valid_critic_scores) < 2 or len(valid_user_scores) < 2:
        print(f"Niewystarczająca liczba danych dla gry {game} do obliczenia korelacji.")
        continue

    # Obliczenie korelacji Pearsona między ocenami krytyków a ocenami użytkowników
    correlation = valid_critic_scores.corr(valid_user_scores)
    print(f"Współczynnik korelacji Pearsona dla gry {game}: {correlation}")

    # Rysowanie wykresu rozproszenia z linią trendu
    plt.figure(figsize=(10, 6))
    plt.scatter(valid_critic_scores, valid_user_scores, alpha=0.5, label='Dane')

    # Obliczenie linii trendu
    z = np.polyfit(valid_critic_scores, valid_user_scores, 1)
    p = np.poly1d(z)

    # Generowanie x wartości dla linii trendu
    x_vals = np.linspace(valid_critic_scores.min(), valid_critic_scores.max(), 100)
    plt.plot(x_vals, p(x_vals), "r--", label='Linia trendu')

    # Formatowanie wykresu
    plt.title(f'Korelacja między ocenami krytyków a użytkowników dla gry {game}')
    plt.xlabel('Średnia ocen krytyków')
    plt.ylabel('Średnia ocen użytkowników')
    plt.legend()
    plt.grid(True)
    plt.show()
