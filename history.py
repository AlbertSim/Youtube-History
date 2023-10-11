from bs4 import BeautifulSoup
import sqlite3
from tqdm import tqdm
import dateutil.parser
import pandas as pd
from datetime import datetime

# Creating DB
conn = sqlite3.connect("myhistory.db")
c = conn.cursor()

# Creating SQL table
def make_table():
    c.execute("CREATE TABLE IF NOT EXISTS history(id INTEGER PRIMARY KEY, unix REAL, title TEXT, channel TEXT, day TEXT, hour INTEGER)")


# Main function that looks through history.html
def search_data():
    # Fetch the youtube history page
    with open('history.html', encoding='utf8') as f:
        html_doc = f.read()

        soup = BeautifulSoup(html_doc, 'lxml')
        
        # Splits each cell and makes variables
        for item in tqdm(soup.find_all('div', attrs={'class': 'content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1'})):
            try:
                # Extracting the title and channel from each block
                title_channel_string = item.find_all('a')
                title = title_channel_string[0].text
                channel = title_channel_string[1].text
                item_list = list(item.stripped_strings)

                # Extracting the day and hour from each block
                date = item_list[3]
                d = dateutil.parser.parse(date).timestamp()
                video_date = datetime.fromtimestamp(d)
                day = video_date.strftime('%A')
                hour = int(video_date.strftime('%H'))

                # Inserting data into SQLite DB
                c.execute("INSERT INTO history (unix, title, channel, day, hour) VALUES (?, ?, ?, ?, ?)", (d, title, channel, day, hour))

            except IndexError:
                pass

make_table()
search_data()

conn.commit()
conn.close()