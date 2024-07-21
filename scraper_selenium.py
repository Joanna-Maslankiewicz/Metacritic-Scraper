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
    games_list = ['Starfield', 'Dark Souls II', 'The Elder Scrolls V: Skyrim', 'Cyberpunk 2077', 'Fallout 4', 'Genshin Impact', 'Mass Effect 3', 'Dragons Dogma 2', 'Dragon Age II', 'Honkai: Star Rail', 'Mass Effect: Andromeda', 'New World', 'Warhammer: Chaosbane']
    base_url = 'https://www.metacritic.com/game/'
    options = Options()
    options.binary_location = 'chrome-win64\chrome.exe'
    options.add_argument("--headless")  # Uruchomienie przeglądarki w trybie bezgłowym
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(10)

    results = []
        
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
