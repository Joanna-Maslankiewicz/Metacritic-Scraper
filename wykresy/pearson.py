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

# Grupowanie danych po miesiącu i typie, obliczanie średniej
data.set_index('Review Date', inplace=True)
monthly_scores = data.groupby([pd.Grouper(freq='M'), 'Type'])['Score Adjusted'].mean().unstack()

# Upewnienie się, że istnieją obie kolumny
if 'Critic' not in monthly_scores.columns or 'User' not in monthly_scores.columns:
    raise ValueError("Brak wystarczających danych dla obu grup (krytyków i użytkowników)")

# Obliczenie korelacji Pearsona między ocenami krytyków a ocenami użytkowników
correlation = monthly_scores['Critic'].corr(monthly_scores['User'])
print("Współczynnik korelacji Pearsona:", correlation)

# Rysowanie wykresu rozproszenia z linią trendu
plt.figure(figsize=(10, 6))
plt.scatter(monthly_scores['Critic'], monthly_scores['User'], alpha=0.5, label='Dane')
z = np.polyfit(monthly_scores.dropna()['Critic'], monthly_scores.dropna()['User'], 1)
p = np.poly1d(z)
plt.plot(monthly_scores['Critic'], p(monthly_scores['Critic']), "r--", label='Linia trendu')

# Formatowanie wykresu
plt.title('Miesięczna korelacja między ocenami krytyków a ocenami użytkowników')
plt.xlabel('Średnia ocen krytyków')
plt.ylabel('Średnia ocen użytkowników')
plt.legend()
plt.grid(True)
plt.show()