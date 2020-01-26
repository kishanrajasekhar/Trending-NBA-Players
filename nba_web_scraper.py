# web scraper for nba stats
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

# This url shows to top 100 players of yesterday's basketball games
# To show a specific date, append these query parameter to the url
# (e.g January 24, 2020: ?month=01&day=24&year=2020&type=all)
BB_REFERENCE_URL ="https://www.basketball-reference.com/friv/dailyleaders.fcgi"

html = urlopen(BB_REFERENCE_URL)
soup = BeautifulSoup(html, features="html.parser")

table = soup.findAll('tr')

# column headers
headers = [th.getText() for th in table[0].findAll('th')]

print(headers)

rows = table[1:]
player_stats = [[td.getText() for td in rows[i].findAll('td')] for i in range(len(rows))]

for i in range(len(player_stats)):
    print(player_stats[i])

##stats = pd.DataFrame(player_stats, columns=headers[1:])
##stats.head(10)
