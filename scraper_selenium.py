from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

def scrape_metacritic_with_selenium():
    games_list = ['Starfield', 'Dark Souls II', 'The Elder Scrolls V: Skyrim', 'Cyberpunk 2077', 'Fallout 4', 'World of Warcraft', 'Genshin Impact', 'Mass Effect 3', 'Dragons Dogma 2', 'Dragon Age II', 'Honkai: Star Rail', 'Mass Effect: Andromeda', 'New World', 'Warhammer: Chaosbane']
    base_url = 'https://www.metacritic.com/game/'
    options = Options()
    options.binary_location = 'chrome-win64\chrome.exe'
    options.add_argument("--headless")  # Uruchomienie przeglądarki w trybie bezgłowym
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(10)

    results = []

    # def scroll_page(driver):
    #     try:
    #         last_height = driver.execute_script("return document.body.scrollHeight")
    #         while True:
    #             driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #             time.sleep(7)  # Zwiększono czas oczekiwania
    #             new_height = driver.execute_script("return document.body.scrollHeight")
    #             if new_height == last_height:
    #                 break
    #             last_height = new_height
    #             print("Scrolled to the bottom.")
    #     except Exception as e:
    #         print(f"Error while scrolling: {e}")
        
    # for game in games_list:
    #     # Zbieranie recenzji krytyków
    #     critic_url = f"{base_url}{game.lower().replace(' ', '-').replace(':', '')}/critic-reviews?platform=pc"
    #     driver.get(critic_url)
    #     scroll_page(driver)
    #     # time.sleep(5)  # Odczekanie, aby strona mogła załadować zawartość

    #     # # Przewijanie strony, żeby załadować więcej recenzji
    #     # last_height = driver.execute_script("return document.body.scrollHeight")
    #     # while True:
    #     #     # Przewiń na dół
    #     #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
    #     #     # Czekaj na załadowanie strony
    #     #     time.sleep(2)
            
    #     #     # Oblicz nową wysokość po przewijaniu i porównaj z poprzednią wysokością
    #     #     new_height = driver.execute_script("return document.body.scrollHeight")
    #     #     if new_height == last_height:
    #     #         break
    #     #     last_height = new_height

    #     reviews = driver.find_elements(By.CSS_SELECTOR, 'div.c-siteReview_main')
    #     for review in reviews:
    #         score = review.find_element(By.CSS_SELECTOR, 'div.c-siteReviewScore span').text
    #         date = review.find_element(By.CSS_SELECTOR, 'div.c-siteReviewHeader_reviewDate').text
    #         results.append({'Game': game, 'Type': 'Critic', 'Score': score, 'Review Date': date})

    #     # Zbieranie recenzji graczy
    #     gamer_url = f"{base_url}{game.lower().replace(' ', '-').replace(':', '')}/user-reviews?platform=pc"
    #     driver.get(gamer_url)
    #     time.sleep(5)
        
    #     gamer_reviews = driver.find_elements(By.CSS_SELECTOR, 'div.c-siteReview_main')
    #     for review in gamer_reviews:
    #         score = review.find_element(By.CSS_SELECTOR, 'div.c-siteReviewScore span').text
    #         date = review.find_element(By.CSS_SELECTOR, 'div.c-siteReviewHeader_reviewDate').text
    #         results.append({'Game': game, 'Type': 'User', 'Score': score, 'Review Date': date})
        
    for game in games_list:
        for review_type in ['critic-reviews', 'user-reviews']:
            url = f"{base_url}{game.lower().replace(' ', '-').replace(':', '')}/{review_type}?platform=pc"
            driver.get(url)
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.c-siteReview_main')))

            # Przewijanie do momentu załadowania wszystkich recenzji
            last_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            reviews = driver.find_elements(By.CSS_SELECTOR, 'div.c-siteReview_main')
            for review in reviews:
                try:
                    score = review.find_element(By.CSS_SELECTOR, 'div.c-siteReviewScore span').text
                    date = review.find_element(By.CSS_SELECTOR, 'div.c-siteReviewHeader_reviewDate').text
                    results.append({'Game': game, 'Type': 'Critic' if review_type == 'critic-reviews' else 'User', 'Score': score, 'Review Date': date})
                except Exception as e:
                    print(f"Error parsing review for {game}: {e}")
                    
    driver.quit()

    if results:
        df = pd.DataFrame(results)
        df.to_csv('metacritic_reviews_selenium.csv', index=False)
        print("Data saved to CSV.")
    else:
        print("No data to save.")

scrape_metacritic_with_selenium()
