"""
This modules implements the scraper_wsj which is used to scrap news from Reuters
"""
import bs4
import datetime as dt
import logging
from crawlers.clean import clean_text

logger = logging.getLogger("NewsScraper.crawlers.wsj")


def scraper_wsj(driver, date):

    list_news = list()
    url = 'http://www.wsj.com/public/page/archive-' + dt.datetime.strftime(date, '%Y-%m-%d') + '.html'
    try:
        driver.get(url)
        soup = bs4.BeautifulSoup(driver.page_source, 'lxml')
        for tag in soup.find('ul', {'class': 'newsItem'}).find_all('li'):
            title = clean_text(tag.find('a').get_text())
            this_news = dict()
            this_news['title'] = title
            this_news['url'] = tag.find('a').get('href')
            this_news['summary'] = clean_text(tag.find('p').get_text())
            try:
                driver.get(this_news['url'])
                art_soup = bs4.BeautifulSoup(driver.page_source, 'lxml')
                this_news['news_date'] = str(date)
                article = art_soup.find_all('p', {'class': None})
                texts = [a.get_text() for a in article if 'http' not in a.get_text()]
                text = ''.join(texts)
                this_news['article'] = clean_text(text)
            except:
                logger.exception("Error in scraping {}".format(this_news['url']))
            list_news.append(this_news)
    except:
        logger.exception("Error in scraping {}".format(url))
    return list_news
