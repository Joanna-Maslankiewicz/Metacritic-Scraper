import pandas as pd
import matplotlib.pyplot as plt

# Wczytanie danych
reviews = pd.read_csv('metacritic_reviews_selenium.csv')
reviews['Review Date'] = pd.to_datetime(reviews['Review Date'])

# Skorygowanie ocen recenzentów
reviews['Score'] = pd.to_numeric(reviews['Score'], errors='coerce')
reviews['Score Adjusted'] = reviews.apply(lambda x: x['Score'] / 10 if x['Type'] == 'Critic' else x['Score'], axis=1)

# Obliczenie średnich miesięcznych ocen
monthly_avg = reviews.groupby([reviews['Review Date'].dt.to_period('M'), 'Type'])['Score Adjusted'].mean().unstack()

# Obliczenie różnic średnich ocen
monthly_avg['Difference'] = monthly_avg['Critic'] - monthly_avg['User']

# Wykres trendu różnic średnich ocen
plt.figure(figsize=(12, 6))
monthly_avg['Difference'].plot()
plt.xlabel('Data')
plt.ylabel('Średnia różnica ocen')
plt.show()