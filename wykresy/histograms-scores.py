import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

reviews = pd.read_csv('metacritic_reviews_selenium.csv')

# Skorygowanie ocenn recenzentów
reviews['Score'] = pd.to_numeric(reviews['Score'], errors='coerce')
reviews['Score Adjusted'] = reviews.apply(lambda x: x['Score'] / 10 if x['Type'] == 'Critic' else x['Score'], axis=1)

# Histogram ocen recenzentów
plt.figure(figsize=(12, 6))
sns.histplot(reviews[reviews['Type'] == 'Critic']['Score Adjusted'], bins=20, color='red', kde=True)
plt.xlabel('Ocena')
plt.ylabel('Liczba recenzji')
plt.show()

# Histogram ocen graczy
plt.figure(figsize=(12, 6))
sns.histplot(reviews[reviews['Type'] == 'User']['Score Adjusted'], bins=20, color='blue', kde=True)
plt.xlabel('Ocena')
plt.ylabel('Liczba recenzji')
plt.show()