import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import ols

# Załadowanie danych
reviews = pd.read_csv('metacritic_reviews_selenium.csv')
release_dates = pd.read_csv('game_release.csv')

# Konwersja dat na format daty i ekstrakcja miesiąca premiery
release_dates['Release'] = pd.to_datetime(release_dates['Release'], format='%b %d, %Y')
release_dates['Month'] = release_dates['Release'].dt.month

# Łączenie danych
merged_data = pd.merge(reviews, release_dates, on='Game')

# Konwersja kolumny 'Score' na numeryczną, zastąpienie nieprzetwarzalnych wartości NaN, a następnie uzupełnienie ich medianą
merged_data['Score'] = pd.to_numeric(merged_data['Score'], errors='coerce')
merged_data['Score'].fillna(merged_data['Score'].median(), inplace=True)

# Skorygowanie ocen krytyków
merged_data['Score_Adjusted'] = merged_data.apply(lambda x: x['Score'] / 10 if x['Type'] == 'Critic' else x['Score'], axis=1)

# Przygotowanie danych do testów
critic_scores = merged_data[merged_data['Type'] == 'Critic']
user_scores = merged_data[merged_data['Type'] == 'User']

# Test ANOVA
model_critic = ols('Score_Adjusted ~ C(Month)', data=critic_scores).fit()
anova_table_critic = sm.stats.anova_lm(model_critic, typ=2)

model_user = ols('Score_Adjusted ~ C(Month)', data=user_scores).fit()
anova_table_user = sm.stats.anova_lm(model_user, typ=2)

print("ANOVA dla ocen recenzentów:")
print(anova_table_critic)
print("\nANOVA dla ocen użytkowników:")
print(anova_table_user)

# Test Kruskala-Wallisa
kw_critic = stats.kruskal(*[group["Score_Adjusted"].values for name, group in critic_scores.groupby("Month")])
kw_user = stats.kruskal(*[group["Score_Adjusted"].values for name, group in user_scores.groupby("Month")])

print("\nKruskal-Wallis dla ocen recenzentów:", kw_critic)
print("Kruskal-Wallis dla ocen użytkowników:", kw_user)