import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter

def quarter_ticks(x, pos):
    month = mdates.num2date(x).month
    year = mdates.num2date(x).year
    quarter = (month - 1) // 3 + 1
    return f'Q{quarter} {year}'

# Załadowanie danych
df = pd.read_csv('metacritic_reviews_selenium.csv')

# Konwersja daty recenzji na format daty
df['Review Date'] = pd.to_datetime(df['Review Date'], errors='coerce')
df = df.dropna(subset=['Review Date'])

# Konwersja kolumny Score na typ numeryczny
df['Score'] = pd.to_numeric(df['Score'], errors='coerce')
df = df.dropna(subset=['Score'])

# Normalizacja ocen krytyków
df.loc[df['Type'] == 'Critic', 'Score'] = df.loc[df['Type'] == 'Critic', 'Score'] / 10

# Grupowanie danych po grach, rodzaju recenzji i miesiącach
for game in df['Game'].unique():
    fig, ax = plt.subplots(figsize=(10, 5))
    game_data = df[df['Game'] == game]

    # Dla każdego typu recenzji
    for review_type in game_data['Type'].unique():
        type_data = game_data[game_data['Type'] == review_type]
        quarterly_avg = type_data.resample('Q', on='Review Date').mean(numeric_only=True)['Score']

        ax.plot(quarterly_avg.index, quarterly_avg.values, marker='o', linestyle='-', label=f'{review_type} Reviews')
    
    ax.set_title(f'Średnia ocena kwartalna - {game}')
    ax.set_xlabel('Kwartał')
    ax.set_ylabel('Średnia ocena')
    ax.legend()

    # Ustawienie większej ilości linii siatki
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 4, 7, 10)))
    ax.xaxis.set_major_formatter(FuncFormatter(quarter_ticks))

    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()