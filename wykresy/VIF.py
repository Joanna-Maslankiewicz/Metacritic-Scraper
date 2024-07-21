import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split

reviews = pd.read_csv('metacritic_reviews_selenium.csv')
release_dates = pd.read_csv('game_release.csv')

# Przetworzenie daty i scalenie danych
release_dates['Release'] = pd.to_datetime(release_dates['Release'])
release_dates['Release Year'] = release_dates['Release'].dt.year
reviews['Review Date'] = pd.to_datetime(reviews['Review Date'])
merged_data = pd.merge(reviews, release_dates, on='Game')

# Przekształcenie ocen krytyków
merged_data['Score'] = pd.to_numeric(merged_data['Score'], errors='coerce')
merged_data['Score'] = merged_data.apply(lambda x: x['Score'] / 10 if x['Type'] == 'Critic' else x['Score'], axis=1)

# Obliczenie lat od wydania
merged_data['Years Since Release'] = (merged_data['Review Date'] - merged_data['Release']).dt.days / 365.25

# Usuń NaN
merged_data = merged_data.dropna(subset=['Score', 'Years Since Release'])

# Przygotowanie zmiennych niezależnych
X = merged_data[['Years Since Release', 'Release Year']]
X = sm.add_constant(X)

# Obliczenie VIF
vif_data = pd.DataFrame()
vif_data['feature'] = X.columns
vif_data['VIF'] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]

print("Współczynnik VIF:")
print(vif_data)

# Regresja wielomianowa i model drzewa decyzyjnego
X = merged_data[['Years Since Release', 'Release Year']]
y = merged_data['Score']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Regresja wielomianowa
poly = PolynomialFeatures(degree=2)
X_poly_train = poly.fit_transform(X_train)
X_poly_test = poly.transform(X_test)

poly_reg = LinearRegression()
poly_reg.fit(X_poly_train, y_train)
y_poly_pred = poly_reg.predict(X_poly_test)

# Drzewo decyzyjne
tree_reg = DecisionTreeRegressor(random_state=42)
tree_reg.fit(X_train, y_train)
y_tree_pred = tree_reg.predict(X_test)

# Wykresy

# Wykres regresji wielomianowej
plt.figure(figsize=(10, 6))
plt.scatter(X_test['Years Since Release'], y_test, color='blue', label='Dane testowe')
plt.scatter(X_test['Years Since Release'], y_poly_pred, color='red', label='Regresja wielomianowa')
plt.xlabel('Lata od wydania', fontsize=14)
plt.ylabel('Oceny', fontsize=14)
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=12)
plt.grid(True)
plt.tight_layout()
plt.show()

# Wykres drzewa decyzyjnego
plt.figure(figsize=(10, 6))
plt.scatter(X_test['Years Since Release'], y_test, color='blue', label='Dane testowe')
plt.scatter(X_test['Years Since Release'], y_tree_pred, color='green', label='Drzewo decyzyjne')
plt.xlabel('Lata od wydania', fontsize=14)
plt.ylabel('Oceny', fontsize=14)
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=12)
plt.grid(True)
plt.tight_layout()
plt.show()