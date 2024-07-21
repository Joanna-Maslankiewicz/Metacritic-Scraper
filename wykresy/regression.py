import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

data = pd.read_csv('metacritic_reviews_selenium.csv')
data['Score'] = pd.to_numeric(data['Score'], errors='coerce')

# Usuwanie wierszy z brakującymi lub błędnymi danymi
data.dropna(subset=['Score'], inplace=True)

# Przygotowanie danych
data['Score Adjusted'] = data.apply(lambda x: x['Score'] / 10 if x['Type'] == 'Critic' else x['Score'], axis=1)

# Agregacja danych dla sparowania ocen krytyków i użytkowników
data_critic = data[data['Type'] == 'Critic'].groupby(['Game', 'Review Date']).agg({'Score Adjusted': 'mean'}).reset_index()
data_user = data[data['Type'] == 'User'].groupby(['Game', 'Review Date']).agg({'Score Adjusted': 'mean'}).reset_index()

# Dołączanie danych krytyków i użytkowników
merged_data = pd.merge(data_critic, data_user, on=['Game', 'Review Date'], suffixes=('_critic', '_user'))

# Podział na zestawy danych
X = merged_data['Score Adjusted_critic'].values.reshape(-1, 1)
y = merged_data['Score Adjusted_user'].values

# Podział na zestawy treningowe i testowe
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model regresji liniowej
model = LinearRegression()
model.fit(X_train, y_train)

# Predykcje i ocena
predictions = model.predict(X_test)
r2_score = model.score(X_test, y_test)

# Wykres
plt.scatter(X_test, y_test, color='blue', label='Actual scores')
plt.plot(X_test, predictions, color='red', label='Predicted regression line')
plt.title('Analiza regresji liniowej')
plt.xlabel('Oceny krytyków')
plt.ylabel('Oceny użytkowników')
plt.legend()
plt.grid(True)
plt.show()

print(f"R-squared: {r2_score}")
