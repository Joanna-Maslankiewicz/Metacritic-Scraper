import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Wczytanie danych
data = pd.read_csv('metacritic_reviews_selenium.csv')

# Konwersja danych
data['Review Date'] = pd.to_datetime(data['Review Date'], errors='coerce', format='%b %d, %Y')
data['Score'] = pd.to_numeric(data['Score'], errors='coerce')

# Skorygowanie ocen krytyków
data['Score Adjusted'] = data.apply(lambda x: x['Score'] / 10 if x['Type'] == 'Critic' else x['Score'], axis=1)

# Usunięcie rekordów z brakującymi danymi
data = data.dropna(subset=['Score Adjusted', 'Review Date'])

# Podział danych na gry
grouped = data.groupby('Game')

# Słownik do przechowywania modeli regresji dla każdej gry
regression_models = {}

for game, group in grouped:
    # Przygotowanie danych do modelowania
    X = group[['Score Adjusted']]  # Przewidywana zmienna niezależna
    y = group['Score']  # Zmienna zależna
    
    # Podział danych na zestaw treningowy i testowy
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Tworzenie modelu regresji liniowej
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Zapisanie modelu do słownika
    regression_models[game] = model
    
    # Wizualizacja
    plt.figure(figsize=(10, 5))
    plt.scatter(X_train, y_train, color='blue', label='Dane treningowe')
    plt.scatter(X_test, y_test, color='green', label='Dane testowe')
    plt.plot(X_train, model.predict(X_train), color='red', label='Linia regresji')
    plt.title(f'Analiza regresji dla gry {game}')
    plt.xlabel('Ocena krytyków')
    plt.ylabel('Ocena użytkowników')
    plt.legend()
    plt.show()