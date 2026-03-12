import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

URLS = [
    "https://en.wikipedia.org/wiki/Black_hole",
    "https://en.wikipedia.org/wiki/Mars",
    "https://en.wikipedia.org/wiki/Exoplanet",
    "https://en.wikipedia.org/wiki/Milky_Way",
    "https://en.wikipedia.org/wiki/Space_exploration",
    "https://en.wikipedia.org/wiki/International_Space_Station",
    "https://en.wikipedia.org/wiki/Dark_matter"
]


def collect_articles():

    articles = []

    for url in URLS:

        try:

            print("Scraping:", url)

            response = requests.get(url, timeout=10)

            soup = BeautifulSoup(response.text, "html.parser")

            title = soup.find("h1").text

            paragraphs = soup.find_all("p")

            content = " ".join([p.text for p in paragraphs[:20]])

            articles.append({
                "title": title,
                "content": content,
                "source": url,
                "date": datetime.now()
            })

        except Exception as e:

            print("Failed:", url, e)

    df = pd.DataFrame(articles)

    df.to_csv("data/new_articles.csv", index=False)

    print("New knowledge collected")