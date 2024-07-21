import pandas as pd
from pytrends.request import TrendReq
import matplotlib.pyplot as plt
import time

# Lista gier
games = ["Dark Souls II", "Dragons Dogma 2", "Mass Effect: Andromeda"]

# Wczytanie danych o datach wydania z pliku CSV
release_dates = pd.read_csv('game_release.csv', parse_dates=['Release'], dayfirst=True)

# Funkcja do pobrania i wizualizacji danych Google Trends
def analyze_hype(game_name, release_date):
    pytrends = TrendReq(hl='en-US', tz=360)
    
    # Ustawienie parametrów wyszukiwania
    kw_list = [game_name]
    pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='', gprop='')
    
    # Pobranie danych z Google Trends z obsługą błędów
    retries = 5
    for i in range(retries):
        try:
            data = pytrends.interest_over_time()
            break
        except Exception as e:
            print(f"Błąd: {e}. Próbuję ponownie...")
            time.sleep(120)  # Opóźnienie 120 sekund
    else:
        print(f"Nie udało się pobrać danych dla gry: {game_name}")
        return
    
    # Sprawdzenie, czy dane zawierają kolumnę 'isPartial'
    if 'isPartial' in data.columns:
        data = data.drop(columns=['isPartial'])
    
    # Tworzenie wykresu
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data[game_name], label=game_name)
    
    # Oznaczenie punktu wydania gry
    plt.axvline(release_date, color='red', linestyle='--', label='Data wydania')
    
    # Dodanie etykiet i tytułu
    plt.xlabel('Data')
    plt.ylabel('Zainteresowanie w wyszukiwaniach')
    plt.title(f'Zainteresowanie w Google Trends dla {game_name}')
    plt.legend()
    plt.grid(True)
    plt.show()

# Analiza hype dla każdej gry z listy
for game in games:
    if game in release_dates['Game'].values:
        release_date = release_dates.loc[release_dates['Game'] == game, 'Release'].values[0]
        analyze_hype(game, release_date)
        time.sleep(10)  # Opóźnienie 10 sekund między zapytaniami
    else:
        print(f"Gra {game} nie została znaleziona w pliku release_dates")
