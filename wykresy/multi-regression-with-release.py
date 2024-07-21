import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
import matplotlib.pyplot as plt

reviews = pd.read_csv('metacritic_reviews_selenium.csv')
release_dates = pd.read_csv('game_release.csv')

reviews['Score'] = pd.to_numeric(reviews['Score'], errors='coerce')
reviews['Score Adjusted'] = reviews.apply(lambda x: x['Score'] / 10 if x['Type'] == 'Critic' else x['Score'], axis=1)

# Konwersja daty na format datetime
release_dates['Release'] = pd.to_datetime(release_dates['Release'])
release_dates['Year'] = release_dates['Release'].dt.year

# Łączenie danych
merged_data = pd.merge(reviews, release_dates[['Game', 'Year']], on='Game')

# Przygotowanie danych do regresji
merged_data = merged_data.dropna(subset=['Score Adjusted', 'Year'])
X = merged_data[['Year']]
X = sm.add_constant(X)  # Dodanie stałej do modelu
y = merged_data['Score Adjusted']

# Regresja wielokrotna
model = sm.OLS(y, X).fit()
print(model.summary())

# Wykres regresji
plt.figure(figsize=(12, 6))
plt.scatter(merged_data['Year'], merged_data['Score Adjusted'], alpha=0.5, label='Dane')
plt.plot(merged_data['Year'], model.predict(X), color='red', label='Linia regresji')
plt.title('Regresja wieloraka: Oceny a rok wydania')
plt.xlabel('Rok wydania')
plt.ylabel('Skorygowana ocena')
plt.legend()
plt.show()