import requests
from bs4 import BeautifulSoup
import csv

def read_areas_name(soup):
    areas_name = []
    side_bar = soup.find("ul", class_ = "sidebar-menu")
    for li in side_bar.find_all("li"):
        for a in li.find_all("a"):
            areas_name.append(a.get("href")[1:]) # remove sharp
    return areas_name

def read_trend_words(soup, area_name):
    ranking = soup.find("div", id = area_name).div.find("div", class_=  "box-body").ul.find_all("li")
    words = []
    for i in ranking:
        for s in i.find_all("p", class_ = "trend"):
            words.append(s.a.string)
    return words

if __name__ == "__main__":
    resp = requests.get("http://twittrend.jp/")
    soup = BeautifulSoup(resp.text, "html.parser")

    areas_name = read_areas_name(soup)

    words = {}
    for name in areas_name:
        words[name] = read_trend_words(soup, name)

        file_name = name + ".csv"
        with open(file_name, "w", encoding='utf_8_sig') as f:
            wr = csv.writer(f, dialect="excel")
            wr.writerow(words[name])
