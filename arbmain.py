
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

nrl = str('https://www.odds.com.au/sport/rugby-league/nrl/matches/')
afl = str('https://www.odds.com.au/sport/australian-rules/afl/matches/')


def twowayarb(sport):
    driver = webdriver.Chrome('./chromedriver') 
    driver.get(f"{sport}")
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    games = soup.find_all('p', class_="meeting__name meeting__name--head-to-head")
    odds = soup.find_all('span',class_="outcome__odds")
    full_odds_list = []
    for odd in odds:
        full_odds_list.append(str(odd).split('>')[1].split('<')[0])
    for i in range(len(full_odds_list)):
        if full_odds_list[i] == ' - ':
            full_odds_list[i]= float(0)
        full_odds_list[i] = float(full_odds_list[i])
    counter = 0
    for game in games:
        counter += 2
        match = str(game).split('>')[1].split('<')[0]
        print(f"Match: {match}")
        print(f"{match.split(' Vs ')[0]} odds: {full_odds_list[counter-2]}")
        print(f"{match.split(' Vs ')[1]} odds: {full_odds_list[counter-1]}")
        if full_odds_list[counter-1]!=0 and full_odds_list[counter-2]!=0:
            margin = (1/(full_odds_list[counter-2])+1/(full_odds_list[counter-1]))*100
            print(f"Margin: {round(margin,2)}")
            if margin<100:
                print("^^ARBITRAGE OPPORTUNITY!!!^^")
                print(f"Stake: ${round(margin,2)}")
                print(f"Winnings: ${round(100-margin,2)}")
                print(f"% return: {round(((100-margin)/margin)*100,2)}%")
                print(f"{match.split(' Vs ')[0]} stake: ${round(1/(full_odds_list[counter-2])*100,2)}")
                print(f"{match.split(' Vs ')[1]} stake: ${round(1/(full_odds_list[counter-1])*100,2)}\n")
            else:
                print("No Arb:(\n")
        else:
            print("Odds not updated\n")
    
twowayarb(nrl)
twowayarb(afl)

"""games = soup.find_all('div',class_ = "head-to-head-wrapper")
for game in games:
    match = game.find('p', class_="meeting__name meeting__name--head-to-head").text
    print(match)
"""

"""
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}
html_text=requests.get('https://www.odds.com.au/sport/rugby-league/nrl/matches/', headers=headers).text
soup = BeautifulSoup(html_text, 'lxml')
game = soup.find('div',class_ = "head-to-head-wrapper")
team_name = game.find('div', class_="meeting__details")
print(team_name)
"""
