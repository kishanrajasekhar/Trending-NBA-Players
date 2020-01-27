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

three_point = "3P"
points = "PTS"
total_rebounds = "TRB"
assists = "AST"
blocks = "BLK"
steals = "STL"
turn_overs = "TOV"

DOUBLE_DOUBLE = 6
TRIPLE_DOUBLE = 12
QUADRUPLE_DOUBLE = 400

fantasy_scores = {three_point: 1, points: 1, total_rebounds: 1.25,
                  assists: 1.5, blocks: 3, steals: 3, turn_overs: -1}
score_indices = {}
for i in range(len(headers)):
    if headers[i] in fantasy_scores.keys():
        score_indices[headers[i]] = i - 1  # -1 since rank not included in player list

rows = table[1:]
player_stats = [[td.getText() for td in rows[i].findAll('td')] for i in range(len(rows))]

player_ftpts = []
for player in player_stats:
    if player == []:
        continue
    name = player[0]

    ftpts = 0
    num_10s = 0  # keep track of double-doubles and triple-doubles
    
    pts = int(player[score_indices[points]])
    ftpts += pts * fantasy_scores[points]
    num_10s = num_10s+1 if pts >= 10 else num_10s
    
    rbs = int(player[score_indices[total_rebounds]])
    ftpts += rbs * fantasy_scores[total_rebounds]
    num_10s = num_10s+1 if rbs >= 10 else num_10s
    
    ast = int(player[score_indices[assists]])
    ftpts += ast * fantasy_scores[assists]
    num_10s = num_10s+1 if ast >= 10 else num_10s
    
    threes = int(player[score_indices[three_point]])
    ftpts += threes * fantasy_scores[three_point]
    # threes not counted for double double
    
    blk = int(player[score_indices[blocks]])
    ftpts += blk * fantasy_scores[blocks]
    num_10s = num_10s+1 if blk >= 10 else num_10s
    
    stl = int(player[score_indices[steals]])
    ftpts += stl * fantasy_scores[steals]
    num_10s = num_10s+1 if stl >= 10 else num_10s
    
    tov = int(player[score_indices[turn_overs]])
    ftpts += tov * fantasy_scores[turn_overs]
    # don't count turn overs for double double

    # double-double
    if num_10s >= 2:
        ftpts += DOUBLE_DOUBLE
    # triple-double
    if num_10s >= 3:
        ftpts += TRIPLE_DOUBLE
    # quadruple-double
    if num_10s >= 4:
        ftpts += QUADRUPLE_DOUBLE
    
##    print("{}:ftpts-{}, pts-{}, rb-{}, ast-{}, 3p-{}, blk-{}, stl-{}, tov-{}".format(
##        name, ftpts, pts, rbs, ast, threes, blk, stl, tov))

    # sort players based on ftpts
    player_ftpts.append((name, ftpts))

player_ftpts.sort(key=lambda tup: tup[1], reverse=True)

for player in player_ftpts:
    print('{}: ftps - {}'.format(player[0], player[1]))

##stats = pd.DataFrame(player_stats, columns=headers[1:])
##stats.head(10)
