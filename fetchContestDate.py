import pandas as pd

url = 'http://onlinemathcontest.com/contests'

def fetch():
    tables = pd.read_html(url)
    upcomingContests = tables[0]
    return upcomingContests