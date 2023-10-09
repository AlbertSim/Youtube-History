import requests
from bs4 import BeautifulSoup
import sqlite3
from tqdm import tqdm
import nltk
import dateutil.parser

# Creating DB
conn = sqlite3.connect("myhistroy.db")
c = conn.cursor()

# Creating SQL table
def make_table():
    c.execute("CREATE TABLE IF NOT EXISTS history(id INTEGER PRIMARY KEY, unix REAL, title TEXT, channel TEXT)")

# Main function that looks through history.html
def search_data():
    # NLTK's list of stopwords
    stop_words = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]
    # Fetch the youtube history page
    with open('history.html', encoding='utf8') as f:
        html_doc = f.read()

        soup = BeautifulSoup(html_doc, 'lxml')

        for tag in soup.find_all('a'):
            print(f'{tag.name}: {tag.text}')

        with open('history.html', encoding='utf8') as f:
                html_doc = f.read()

                soup = BeautifulSoup(html_doc, 'lxml')
                
                # Splits each cell and makes variables
                for item in tqdm(soup.find_all('div', attrs={'class': 'content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1'})):
                        try:
                            title_channel_string = item.find_all('a')
                            title = title_channel_string[0].text
                            channel = title_channel_string[1].text
                            item_list = list(item.stripped_strings)
                            date = item_list[3]
                            d = dateutil.parser.parse(date).timestamp()

                            # Inserting data into DB
                            c.execute("INSERT INTO history (unix, title, channel) VALUES (?, ?, ?)", (d, title, channel))
                        except IndexError:
                            pass

make_table()
search_data()

conn.commit()
conn.close()