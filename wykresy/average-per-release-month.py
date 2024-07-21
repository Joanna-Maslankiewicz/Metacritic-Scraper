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

# Agregacja średnich ocen dla każdego typu recenzji oraz ogólnie
monthly_scores = filtered_data.groupby(['Month', 'Type'])['Score Adjusted'].mean().unstack()
monthly_scores['Average'] = filtered_data.groupby('Month')['Score Adjusted'].mean()

# Rysowanie wykresu
fig, ax = plt.subplots(figsize=(14, 8))
monthly_scores[['Critic', 'User', 'Average']].plot(kind='bar', color=['red', 'blue', 'green'], alpha=0.7, ax=ax)
month_indices = np.arange(len(monthly_scores))  # Generuje indeksy od 0 do 11 dla 12 miesięcy

# Rysowanie linii trendu z użyciem całego zakresu osi x
for color, column in zip(['red', 'blue', 'green'], ['Critic', 'User', 'Average']):
    z = np.polyfit(month_indices, monthly_scores[column], 1)
    p = np.poly1d(z)
    plt.plot(month_indices, p(month_indices), color=color, linestyle='--', label=f'Trend {column}')
    
# Miesiące po polsku
polish_months = ['Styczeń', 'Luty', 'Marzec', 'Kwiecień', 'Maj', 'Czerwiec', 'Lipiec', 'Sierpień', 'Wrzesień', 'Październik', 'Listopad', 'Grudzień']
    
# Ustawienie większych czcionek
plt.rc('font', size=14)
plt.rc('axes', titlesize=16)
plt.rc('axes', labelsize=14)
plt.rc('xtick', labelsize=12)
plt.rc('ytick', labelsize=12)
plt.rc('legend', fontsize=12)
plt.rc('figure', titlesize=18)

# Formatowanie wykresu
plt.xlabel('Miesiąc premiery', fontsize=16)
plt.ylabel('Średnia ocena', fontsize=16)
plt.xticks(ticks=np.arange(len(monthly_scores)), labels=[polish_months[i-1] for i in monthly_scores.index], rotation=45, fontsize=14)
plt.yticks(fontsize=14)
plt.legend(['Trend Recenzent', 'Trend Użytkownik', 'Trend Średnia', 'Recenzent', 'Użytkownik', 'Średnia'], fontsize=14, bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.tight_layout()
plt.show()