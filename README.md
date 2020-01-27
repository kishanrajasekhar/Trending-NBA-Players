# Trending-NBA-Players
Try to find trending free agent nba players for my fantasy league

I want to be competetive in my fantasy league. However, I don't want to check player stats everyday.
I want a computer to do that for me. This is a script to find trending free agents.

Current Goals:
 1. I want to find the top players for a day (basketball-reference.com already provides that).
 2. I want to find the top players in a specific time range (e.g. Top players this week). This way, I may find players I never
    heard of who are doing well in fantasy. To accomplish this I can either:
    1. Query basketball-reference.com for each date and aggregate the data, or 
    2. Store the data in my own database after retrieving them from the web. I'd rather do this because this makes the project more fun, and having my own database allows me to do more custom queries and data anayltics (maybe in the future). 
 3. I also need to make sure the players returned in the search query are free agents in my league (that may be challenging).

Who knows, this project might evolve into something greater.

Trello board (my budget jira): https://trello.com/b/VHNj95qc/nba-data. I'll try to keep this organized.

Setup:
1. Clone this repo
2. Setup a python virtual environment for python3 in the git project
  1. Windows: `python -m venv .\my-venv` (Doesn't have to be called my-venv, could be called whatever you want). Make sure the python command is setup for python 3. If you have both python2 and python3 on your computer, you may have to do `py -3 -m venv .\my-venv`
3. Add `my-venv` to `.gitignore` so that you don't accidently commit it. Your virtual environment does not need to be pushed.
4. Activate the virual environment: `.\my-venv\Scripts\activate.bat`.
5. Run the script: `python nba_web_scraper.py`. You may have to pip install `bs4`. The virtual environment keeps the pip installs from conflicting with other projects.

Etc.
  - how to not have git ask for password all the time if you used https instead of ssh: `git config credential.helper store`
