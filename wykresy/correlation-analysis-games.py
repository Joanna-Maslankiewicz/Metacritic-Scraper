import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def perform_correlation_analysis():
    df = pd.read_csv('metacritic_reviews_selenium.csv')
    df['Review Date'] = pd.to_datetime(df['Review Date'], errors='coerce')
    df['Score'] = pd.to_numeric(df['Score'], errors='coerce')
    
    # Normalizacja ocen krytyków do skali 0-10, jeśli jest taka potrzeba
    df.loc[df['Type'] == 'Critic', 'Score'] /= 10

    # Usunięcie błędnych danych
    df.dropna(subset=['Score', 'Review Date'], inplace=True)

    # Grupowanie danych po grach i miesiącach
    df.set_index('Review Date', inplace=True)
    df_grouped = df.groupby([pd.Grouper(freq='M'), 'Game', 'Type']).mean().unstack()
    
    # Zapisanie do nowego DataFrame tylko tych gier, które mają oceny zarówno od krytyków, jak i graczy
    df_grouped = df_grouped.dropna(subset=[('Score', 'Critic'), ('Score', 'User')])

    # Lista do przechowywania wyników korelacji
    correlation_results = []

    for game in df_grouped.index.get_level_values(1).unique():
        game_data = df_grouped.xs(game, level='Game')
        correlation = game_data[('Score', 'Critic')].corr(game_data[('Score', 'User')])
        correlation_results.append({'Game': game, 'Correlation': correlation})
        
        # Wykres rozproszenia
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=game_data[('Score', 'Critic')], y=game_data[('Score', 'User')])
        plt.title(f'Korelacja między ocenami użytkowników i krytyków dla gry {game}: {correlation:.2f}')
        plt.xlabel('Oceny krytyków')
        plt.ylabel('Oceny użytkowników')
        plt.grid(True)
        plt.show()

    correlation_df = pd.DataFrame(correlation_results)
    print(correlation_df)

perform_correlation_analysis()