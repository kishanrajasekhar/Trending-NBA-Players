# Trending-NBA-Players
Try to find trending free agent nba players for my fantasy league

I want to be competetive in my fantasy league. However, I don't want to check player stats everyday.
I want a computer to do that for me. This is a script to find trending free agents.

## Current Goals:
 1. I want to find the top players for a day (basketball-reference.com already provides that).
 2. I want to find the top players in a specific time range (e.g. Top players this week). This way, I may find players I never
    heard of who are doing well in fantasy. To accomplish this I can either:
    1. Query basketball-reference.com for each date and aggregate the data, or 
    2. Store the data in my own database after retrieving them from the web. I'd rather do this because this makes the project more fun, and having my own database allows me to do more custom queries and data anayltics (maybe in the future). 
 3. I also need to make sure the players returned in the search query are free agents in my league (that may be challenging).

Who knows, this project might evolve into something greater.

Trello board (my budget jira): https://trello.com/b/VHNj95qc/nba-data. I'll try to keep this organized.

## Setup for web scraper:
1. Clone this repo
2. Setup a python virtual environment for python3 in the git project
    1. Windows: `python -m venv .\my-venv` (Doesn't have to be called my-venv, could be called whatever you want). Make sure the python command is setup for python 3. If you have both python2 and python3 on your computer, you may have to do `py -3 -m venv .\my-venv`
    2. Mac: `python3.6 -m venv nba-env`
3. Add `my-venv` to `.gitignore` so that you don't accidently commit it. Your virtual environment does not need to be pushed.
4. Activate the virual environment
    1. Windows: `.\my-venv\Scripts\activate.bat`
    2. Mac: `source nba-env/bin/activate`
5. Run the script: `python nba_web_scraper.py`. You may have to pip install `bs4`. The virtual environment keeps the pip installs from conflicting with other projects.
6. To exit the virtual environment, type the command `deactivate`

## Setup to populate database
1. Download mongodb
    1. Windows 10 setup
        1. Go to environment variables. Under System Variables look for the variable called "Path". Open it up and the location of the mongodb directory you just loaded. There is a "bin" directory. Make sure the path you put points to that directory (e.g "C:\Program Files\MongoDB\Server\4.2\bin")
2. Open a cmd and run `mongod` to get mongodb running.
3. In the python virtual environment run the script `python nba_database_populator.py`. Check your database afterwards to see if the `team` collection in your database has been populated. The `player` collection might be populated as well.
    1. Tools to look at your database
        1. MongoDB Compass: Click the option "Fill in connection fields individually. Enter `localhost` for hostname and `27017` for the port (the defaults).
        2. Robo 3T

### How to populate the database with game stats of a specific date
  - e.g.) March 11th 2020: `python nba_database_populator.py --month 3 --day 11 --year 2020`
  
### How to quickly populate the database with game stats of the 2019 to 2020 season
  - e.g.) `python season_database_population_scripts/2019_2020_season.py`... Or at least this is how I want this to work. This didn't work for me from the command line. I had to run the `2019_2020_season.py` script from PyCharm.
  
## Query Player Stats
e.g.)How to get the cumulative fantasy points of each player from Jan 1st 2020 to March 11th 2020 (All 2020 games until Covid-19 cancellation). 
```python nba_query_stats.py --year_start 2020 --month_start 1 --day_start 1 --year_end 2020 --month_end 3 --day_end 11```

Sample output:
```
Player: Nikola Jokić, Fantasy Points: 1784.5
Player: LeBron James, Fantasy Points: 1719.75
Player: James Harden, Fantasy Points: 1682.0
Player: Trae Young, Fantasy Points: 1642.75
Player: Giannis Antetokounmpo, Fantasy Points: 1611.5
Player: Hassan Whiteside, Fantasy Points: 1558.0
Player: Nikola Vučević, Fantasy Points: 1557.25
...
```

## Etc.
  - how to not have git ask for password all the time if you used https instead of ssh: `git config credential.helper store`
