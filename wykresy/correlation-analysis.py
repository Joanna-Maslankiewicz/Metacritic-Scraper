import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def perform_combined_correlation_analysis():
    df = pd.read_csv('metacritic_reviews_selenium.csv')
    df['Review Date'] = pd.to_datetime(df['Review Date'], errors='coerce')
    df['Score'] = pd.to_numeric(df['Score'], errors='coerce')
    
    # Normalizacja ocen krytyków do skali 0-10
    df.loc[df['Type'] == 'Critic', 'Score'] /= 10

    # Usunięcie błędnych danych
    df.dropna(subset=['Score', 'Review Date'], inplace=True)

    # Grupowanie danych po miesiącach i typach recenzji
    df.set_index('Review Date', inplace=True)
    df_grouped = df.groupby([pd.Grouper(freq='M'), 'Type'])['Score'].mean().unstack()

    # Usunięcie miesięcy, gdzie brakuje ocen którejkolwiek z grup
    df_grouped.dropna(subset=['Critic', 'User'], inplace=True)

    # Korelacja między ocenami krytyków i użytkowników dla wszystkich gier
    correlation = df_grouped['Critic'].corr(df_grouped['User'])

    # Wykres rozproszenia z linią trendu i większymi czcionkami
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=df_grouped['Critic'], y=df_grouped['User'])
    sns.regplot(x=df_grouped['Critic'], y=df_grouped['User'], scatter=False, color='red')
    plt.xlabel('Oceny krytyków', fontsize=14)
    plt.ylabel('Oceny użytkowników', fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    print(f'Korelacja między ocenami użytkowników i krytyków dla wszystkich gier: {correlation:.2f}')

perform_combined_correlation_analysis()
