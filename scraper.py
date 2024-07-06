import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_metacritic():
    # Lista wybranych gier
    games_list = ['Starfield', 'Dark Souls II', 'The Elder Scrolls V: Skyrim', 'Cyberpunk 2077', 'Fallout 4', 'World of Warcraft', 'Genshin Impact', 'Mass Effect 3', 'Dragons Dogma 2', 'Dragon Age II', 'Honkai: Star Rail', 'Mass Effect: Andromeda', 'New World', 'Warhammer: Chaosbane']
    base_url = 'https://www.metacritic.com/game/'
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br"
    }
    
    # Lista do przechowywania danych
    results = []
    
    # for game in games_list:
        
    #     # Budowanie URL dla każdej gry
    #     game_url = base_url + game.lower().replace(' ', '-').replace(':', '')
    #     response = requests.Session().get(game_url, headers=headers)
    #     soup = BeautifulSoup(response.content, 'html.parser')
        
        # # Znalezienie daty wydania gry
        # print(f"Fetching URL: {game_url}")
        # response = requests.get(game_url, headers=headers)
        # print(f"Status code: {response.status_code}")
        # if response.status_code == 200:
        #     soup = BeautifulSoup(response.content, 'html.parser')
        #     release_date = soup.find(text="Released On: ").find_next('span').text.strip() if soup.find(text="Released On: ") else 'Release date not found or incorrectly formatted'
        #     print(f"Release Date: {release_date}")
        # else:
        #     print(f"Failed to retrieve data for URL: {game_url}")
            
        # # Krótki czas oczekiwania, aby nie obciążać serwera
        # time.sleep(5)
        
    for game in games_list:
        # Zbieranie recenzji krytyków
        critic_url = base_url + game.lower().replace(' ', '-').replace(':', '') + '/critic-reviews/?platform=pc'
        print(f"Fetching critic reviews from: {critic_url}")
        critic_response = requests.get(critic_url, headers=headers)
        if critic_response.status_code == 200:
            critic_soup = BeautifulSoup(critic_response.content, 'html.parser')
            critic_reviews = critic_soup.find_all(attrs={"class": "c-siteReviewHeader"})
            if not critic_reviews:
                print("No reviews found.")
                print(critic_soup.prettify())
            for review in critic_reviews:
                try:
                    critic_score = review.find(class_='c-siteReviewScore').find_next('span').text.strip()
                    review_date = review.find(class_='c-siteReviewHeader_reviewDate').text.strip()
                    results.append({'Game': game, 'Type': 'Critic', 'Score': critic_score, 'Review Date': review_date})
                except AttributeError:
                    print("Critic review parsing error.")
        else:
            print(f"Failed to fetch critic reviews for {game}")
            
        # Zbieranie recenzji graczy
        gamer_url = base_url + game.lower().replace(' ', '-').replace(':', '') + '/user-reviews/?platform=pc'
        print(f"Fetching user reviews from: {gamer_url}")
        gamer_response = requests.get(gamer_url, headers=headers)
        if gamer_response.status_code == 200:
            gamer_soup = BeautifulSoup(gamer_response.content, 'html.parser')
            gamer_reviews = gamer_soup.find_all(attrs={"class": "c-siteReviewHeader"})
            if not gamer_reviews:
                    print("No reviews found.")
            for review in gamer_reviews:
                try:
                    gamer_score = review.find(class_='c-siteReviewScore').text.strip()
                    review_date = review.find(class_='c-siteReviewHeader_reviewDate').text.strip()
                    results.append({'Game': game, 'Type': 'Gamer', 'Score': gamer_score, 'Review Date': review_date})
                except AttributeError:
                    print("User review parsing error.")
        else:
            print(f"Failed to fetch user reviews for {game}")
            
        # Krótki czas oczekiwania, aby nie obciążać serwera
        time.sleep(5)
        
    # Zapisywanie danych do pliku CSV
    if results:
        df = pd.DataFrame(results)
        df.to_csv('metacritic_reviews.csv', index=False)
        print("Data saved to CSV.")
    else:
        print("No data to save.")

scrape_metacritic()