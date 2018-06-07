from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import datetime as dt
from crawlers.nytimes import scraper_nytimes
from crawlers.reuters import scraper_reuters
from crawlers.wallstreetjournal import scraper_wsj
import logging

logger = logging.getLogger("NewsScraper.crawlers")


class Scraper:
    """Base class for scrapers.
    """

    def __init__(self, phantomjs_path, username, password):
        logger.info("Initialize crawler")
        # declare variables
        # list of news
        # store each news as a dict(title, url, news_date, article, summary, time, location, people, event)
        self.list_news = list()

        # WSJ driver setting
        try:
            self.driver = webdriver.PhantomJS(executable_path=phantomjs_path)
            login_url = 'https://accounts.wsj.com/login?target=https%3A%2F%2Fwww.wsj.com'
            self.driver.get(login_url)
            username_field = self.driver.find_element_by_id("username")
            password_field = self.driver.find_element_by_id("password")
            login_button = self.driver.find_element_by_class_name("basic-login-submit")
            username_field.clear()
            password_field.clear()
            username_field.send_keys(username)
            password_field.send_keys(password)
            login_button.send_keys(Keys.ENTER)
            self.driver.wait = WebDriverWait(self.driver, 30)  # waits up to 10 seconds before throwing a TimeoutException
            self.driver.wait.until(lambda driver: driver.current_url == 'https://www.wsj.com/')
        except:
            logger.exception("Error in initializing WSJ crawler")

    def scraper_reuters(self):
        logger.info("Start scraping Reuters")
        self.list_news = scraper_reuters()
        logger.info('{} news scraped from Reuters'.format(len(self.list_news)))

    def scraper_nytimes(self):
        logger.info("Start scraping NYTimes")
        self.list_news = scraper_nytimes()
        logger.info('{} news scraped from NYTimes'.format(len(self.list_news)))

    def scraper_wsj(self, date):
        logger.info("Start scraping Wall Street Journal for " + dt.datetime.strftime(date, '%Y-%m-%d'))
        self.list_news = scraper_wsj(self.driver, date)
        logger.info('{} news scraped from Wall Street Journal for '.format(len(self.list_news)) + dt.datetime.strftime(date, '%Y-%m-%d'))

    def quit(self):
        self.driver.quit()

    @property
    def news_list(self):
        return self.list_news
