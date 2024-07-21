import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

reviews = pd.read_csv('metacritic_reviews_selenium.csv')
releases = pd.read_csv('game_release.csv')

# Przetwarzanie daty recenzji
reviews['Review Date'] = pd.to_datetime(reviews['Review Date'], format='%b %d, %Y', errors='coerce')

# Przetwarzanie daty wydania gry
releases['Release'] = pd.to_datetime(releases['Release'], format='%b %d, %Y', errors='coerce')

# Konwersja wartości 'Score' na numeryczne, 'tbd' zostanie zamienione na NaN
reviews['Score'] = pd.to_numeric(reviews['Score'], errors='coerce')

# Dołączanie roku wydania gry do recenzji
reviews = reviews.merge(releases, on='Game', how='left')

# Obliczenie lat od wydania gry do daty recenzji
reviews['Years Since Release'] = reviews['Review Date'].dt.year - reviews['Release'].dt.year

# Usuwanie rekordów z brakującymi danymi
reviews.dropna(subset=['Score', 'Years Since Release'], inplace=True)

# Skorygowanie ocen krytyków
reviews['Score Adjusted'] = reviews.apply(lambda x: x['Score'] / 10 if x['Type'] == 'Critic' else x['Score'], axis=1)

# Przygotowanie danych do analizy regresji
X = reviews[['Years Since Release']]  # Niezależna zmienna
y = reviews['Score Adjusted']  # Zależna zmienna

# Podział danych na zestaw treningowy i testowy
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model regresji liniowej
model = LinearRegression()
model.fit(X_train, y_train)

# Predykcje
predictions = model.predict(X_test)

# Wizualizacja wyników
plt.figure(figsize=(10, 6))
plt.scatter(X_test, y_test, color='blue', label='Rzeczywiste wartości')
plt.plot(X_test, predictions, color='red', label='Predykcje modelu')
plt.title('Regresja liniowa - wpływ lat od wydania na oceny')
plt.xlabel('Lata od premiery gry')
plt.ylabel('Ocena')
plt.legend()
plt.show()

# Wyświetlenie współczynnika determinacji R^2
print(f"Współczynnik determinacji R^2: {model.score(X_test, y_test):.2f}")