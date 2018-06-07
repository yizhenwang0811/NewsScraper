"""
This modules implements the scraper_nytimes which is used to scrap news from The New York Times
"""
import requests
import bs4
from crawlers.clean import clean_text
import datetime as dt
import logging

logger = logging.getLogger("NewsScraper.crawlers.nytimes")


def scraper_nytimes():
    list_news = list()
    url = 'https://www.nytimes.com/section/world'
    try:
        response = requests.get(url)
        soup = bs4.BeautifulSoup(response.content, 'lxml')
        for tag in soup.find_all('div', {'class': 'story-meta'}):
            title = tag.find('h2').get_text().lower()
            title = clean_text(title)
            this_news = dict()
            this_news['title'] = title
            this_news['url'] = tag.parent.parent.find('a').get('href')
            this_news['summary'] = clean_text(tag.find('p', {'class': 'summary'}).get_text())
            try:
                art_response = requests.get(this_news['url'])
                art_soup = bs4.BeautifulSoup(art_response.content, 'lxml')
                art_date = art_soup.find('time').get('datetime')
                this_news['news_date'] = art_date
                # article = art_soup.find('div', {'class': 'StoryBodyCompanionColumn'})
                texts = [a.get_text() for a in art_soup.find_all('p')]
                text = ''.join(texts)
                this_news['article'] = clean_text(text)
            except:
                logger.exception("Error in scraping {}".format(this_news['url']))
            list_news.append(this_news)
    except:
        logger.exception("Error in scraping {}".format(url))
    return list_news


def scraper_nytimes_daily(date):
    list_news = list()
    url = 'https://www.nytimes.com/issue/todayspaper/' + dt.datetime.strftime(date, '%Y/%m/%d') + '/todays-new-york-times'
    try:
        response = requests.get(url)
        soup = bs4.BeautifulSoup(response.content, 'lxml')
        STOPWORD = ["Corrections:", "Bulletin", "Review:"]
        for tag in soup.find_all('h2', {'class': 'headline'}):
            if not any(word in tag.get_text() for word in STOPWORD):
                this_news = dict()
                tag_title = tag.find('a')
                this_news['title'] = clean_text(tag_title.get_text())
                this_news['url'] = tag_title.get('href')
                if tag.parent.find('p', {'class': 'summary'}):
                    this_news['summary'] = clean_text(tag.parent.find('p', {'class': 'summary'}).get_text())
                try:
                    art_response = requests.get(this_news['url'])
                    art_soup = bs4.BeautifulSoup(art_response.content, 'lxml')
                    art_date = art_soup.find('time').get('datetime')
                    this_news['news_date'] = art_date
                    texts = [a.get_text() for a in art_soup.find_all('p')]
                    text = ''.join(texts)
                    this_news['article'] = clean_text(text)
                except:
                    logger.exception("Error in scraping {}".format(this_news['url']))
                list_news.append(this_news)
    except:
        logger.exception("Error in scraping {}".format(url))
    return list_news