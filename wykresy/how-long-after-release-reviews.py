import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

reviews = pd.read_csv('metacritic_reviews_selenium.csv')
release_dates = pd.read_csv('game_release.csv')

# Przetwarzanie daty
reviews['Review Date'] = pd.to_datetime(reviews['Review Date'], errors='coerce')
release_dates['Release'] = pd.to_datetime(release_dates['Release'], errors='coerce')

# Scalenie danych
merged_data = pd.merge(reviews, release_dates, on='Game')

# Obliczenie różnicy czasu między datą recenzji a datą wydania w miesiącach
merged_data['Months Since Release'] = ((merged_data['Review Date'] - merged_data['Release']) / pd.Timedelta(days=30)).astype(int)

merged_data['Typ recenzenta'] = merged_data['Type'].replace({'Critic': 'Recenzent', 'User': 'Użytkownik'})

# Usuwanie NaN i wartości ujemnych
merged_data = merged_data.dropna(subset=['Months Since Release'])
merged_data = merged_data[merged_data['Months Since Release'] >= 0]

# Wykres
plt.figure(figsize=(14, 7))
sns.boxplot(x='Typ recenzenta', y='Months Since Release', data=merged_data, palette=['red', 'blue'])
plt.xlabel('Typ recenzenta', fontsize=14)
plt.ylabel('Miesiące od wydania', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.grid(True)
plt.tight_layout()
plt.show()
