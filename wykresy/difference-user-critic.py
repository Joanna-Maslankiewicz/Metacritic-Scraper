import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter

def visualize_reviews():
    # Załadowanie danych
    df = pd.read_csv('metacritic_reviews_selenium.csv')
    df['Review Date'] = pd.to_datetime(df['Review Date'], errors='coerce')
    df.dropna(subset=['Review Date'], inplace=True)

    df['Score'] = pd.to_numeric(df['Score'], errors='coerce')
    df.loc[df['Type'] == 'Critic', 'Score'] /= 10
    df.dropna(subset=['Score'], inplace=True)

    df.set_index('Review Date', inplace=True)

    for game in df['Game'].unique():
        game_data = df[df['Game'] == game]
        critic_scores = game_data[game_data['Type'] == 'Critic'].resample('Q').mean(numeric_only=True)['Score']
        user_scores = game_data[game_data['Type'] == 'User'].resample('Q').mean(numeric_only=True)['Score']
            
        # Ujednolicenie indeksów dla obu serii
        all_quarters = critic_scores.index.union(user_scores.index)
        critic_scores = critic_scores.reindex(all_quarters).interpolate()
        user_scores = user_scores.reindex(all_quarters).interpolate()

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(critic_scores.index, critic_scores, label='Critic Scores', marker='o')
        ax.plot(user_scores.index, user_scores, label='User Scores', marker='o')

        ax.fill_between(all_quarters, critic_scores, user_scores, where=(critic_scores >= user_scores), facecolor='lightgreen', interpolate=True, alpha=0.3, label='Critics > Users')
        ax.fill_between(all_quarters, critic_scores, user_scores, where=(critic_scores <= user_scores), facecolor='lightcoral', interpolate=True, alpha=0.3, label='Users > Critics')

        ax.set_title(f'Porównanie ocen dla gry {game}')
        ax.set_xlabel('Kwartał')
        ax.set_ylabel('Średnia ocena')
        ax.legend()

        ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 4, 7, 10)))
        ax.xaxis.set_major_formatter(FuncFormatter(lambda x, pos: f'Q{((mdates.num2date(x).month-1)//3)+1} {mdates.num2date(x).year}'))

        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.show()

visualize_reviews()