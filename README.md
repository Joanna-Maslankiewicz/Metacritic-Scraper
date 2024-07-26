# Analiza Różnic w Recenzjach Gier Między Profesjonalistami a Graczami

Projekt koncentruje się na badaniu różnic między recenzjami gier wideo wystawianymi przez profesjonalnych recenzentów a recenzjami użytkowników. Analiza obejmuje również dodatkowe czynniki, takie jak data wydania gier, kampanie marketingowe, oraz zainteresowanie grami, mierzone poprzez dane z Google Trends. Celem projektu jest lepsze zrozumienie, jak różnice w ocenach wpływają na percepcję gier i decyzje zakupowe graczy.

Projekt składa się z kilku głównych katalogów i plików, które są kluczowe dla analizy danych oraz wizualizacji wyników. Oto szczegółowy opis poszczególnych elementów struktury projektu:

## Główne katalogi i pliki:

### katalog *wykresy*:

Jest to katalog zawierający skrypty Pythona oraz wygenerowane wykresy z analiz. Znajdują się tutaj zarówno pliki obrazów (.png), jak i skrypty (.py) służące do przetwarzania danych i tworzenia wizualizacji. Przykłady plików to:
- *ANOVA.py*: skrypt do analizy wariancji.
- *Boxplot ocen recenzentów i graczy.png*: wykres pudełkowy pokazujący rozkład ocen.
- *correlation-analysis.py*: skrypt do analizy korelacji.

### Pliki CSV:

W głównym katalogu projektu znajdują się pliki CSV z danymi, które zostały wykorzystane do analizy. Każdy plik odpowiada innemu zbiorowi danych, np.:
- *game_release.csv*: zawiera informacje o datach wydania gier.
- *metacritic_reviews_selenium.csv*: dane z recenzji zebrane przy pomocy Selenium.
- *players-[nazwa gry].csv*: dane dotyczące liczby graczy dla poszczególnych gier.

### Skrypty do scrapowania:

- *scraper_selenium.py*: główny skrypt odpowiedzialny za scrapowanie danych z Metacritic przy użyciu Selenium.


Każdy plik pełni specyficzną rolę w procesie analizy i pozwala na reprodukcję wyników lub dalsze eksploracje danych.
