import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import calendar

# Załadowanie danych
reviews = pd.read_csv('metacritic_reviews_selenium.csv')
release_dates = pd.read_csv('game_release.csv')

# Konwersja dat na format daty i ekstrakcja miesiąca premiery
release_dates['Release'] = pd.to_datetime(release_dates['Release'], format='%b %d, %Y', errors='coerce')
release_dates['Month'] = release_dates['Release'].dt.month

# Łączenie danych
merged_data = pd.merge(reviews, release_dates, on='Game')

# Konwersja kolumny 'Score' na numeryczną, zastąpienie nieprzetwarzalnych wartości NaN
merged_data['Score'] = pd.to_numeric(merged_data['Score'], errors='coerce')
merged_data.dropna(subset=['Score'], inplace=True)  # Usunięcie wpisów z NaN w 'Score'

# Skalowanie ocen recenzentów
merged_data['Score Adjusted'] = merged_data.apply(lambda x: x['Score'] / 10 if x['Type'] == 'Critic' else x['Score'], axis=1)

# Filtracja danych, aby uwzględnić tylko miesiące z premiarami gier
valid_months = release_dates['Month'].unique()
filtered_data = merged_data[merged_data['Month'].isin(valid_months)]

# Agregacja średnich ocen dla każdego miesiąca
monthly_scores = filtered_data.groupby('Month')['Score Adjusted'].mean().sort_index()

# Wyświetlenie wyników
print("Średnie oceny po miesiącach:")
print(monthly_scores)

# Rysowanie wykresu
plt.figure(figsize=(10, 6))
monthly_scores.plot(kind='bar', color='skyblue')
plt.title('Średnia ocena gier w zależności od miesiąca premiery')
plt.xlabel('Miesiąc premiery')
plt.ylabel('Średnia ocena')
plt.xticks(ticks=np.arange(len(monthly_scores)), labels=[calendar.month_abbr[i] for i in monthly_scores.index], rotation=45)  # Ustawienie właściwych etykiet
plt.grid(True)
plt.tight_layout()
plt.show()