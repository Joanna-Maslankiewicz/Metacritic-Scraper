import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Wczytanie danych
reviews = pd.read_csv('metacritic_reviews_selenium.csv')

# Skorygowanie ocen recenzentów
reviews['Score'] = pd.to_numeric(reviews['Score'], errors='coerce')
reviews['Score Adjusted'] = reviews.apply(lambda x: x['Score'] / 10 if x['Type'] == 'Critic' else x['Score'], axis=1)

reviews['Typ recenzenta'] = reviews['Type'].replace({'Critic': 'Profesjonalista', 'User': 'Użytkownik'})

# Boxplot ocen
plt.figure(figsize=(12, 6))
sns.boxplot(x='Typ recenzenta', y='Score Adjusted', data=reviews, palette=['red', 'blue'])
plt.xlabel('Typ recenzenta', fontsize=14)
plt.ylabel('Ocena', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.grid(True)
plt.tight_layout()
plt.show()