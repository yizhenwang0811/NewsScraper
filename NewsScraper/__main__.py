import datetime as dt
import optparse
import logging
import os, os.path


from NLP import Processor
from output import save_json
from crawlers import Scraper


def main():
    today = dt.date.today().strftime("%Y%m%d")

    # command line option parser

    usage = "usage: %prog [options]"
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-e", "--end_date", type=str, dest="end_date", default=today,
                      help="the end DATE of news scraping in format of 'YYYYmmdd'", metavar="DATE")
    parser.add_option("-d", "--num_days", type=int, dest="num_days", default=1,
                      help="NUMBER of days for news scraping", metavar="NUMBER")
    parser.add_option("-n", "--news_path", type=str, dest="news_path", default="news",
                      help="save news scraped to FOLDER", metavar="FOLDER")
    parser.add_option("-l", "--log_path", type=str, dest="log_path", default="log",
                      help="save log file to FOLDER", metavar="FOLDER")
    parser.add_option("-p", "--phantomjs_path", type=str, dest="phantomjs_path",
                      default="/Users/xinyiwu/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs",
                      help="change executable path of PhantomJS to PATH", metavar="PATH")
    parser.add_option("-u", "--username_wsj", type=str, dest="username_wsj", default='redoakrichard@gmail.com',
                      help="change USERNAME of Wall Street Journal", metavar="USERNAME")
    parser.add_option("-w", "--password_wsj", type=str, dest="password_wsj", default='ready2ca',
                      help="change PASSWORD of Wall Street Journal", metavar="PASSWORD")
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose", default=True,
                      help="don't print status messages to stdout")

    (options, args) = parser.parse_args()

    end_date = dt.datetime.strptime(options.end_date, '%Y%m%d')
    news_path = options.news_path

    if not os.path.exists(news_path + '/'):
        os.makedirs(news_path + '/')

    if not os.path.exists(options.log_path + '/'):
        os.makedirs(options.log_path + '/')

    # Set logging

    logger = logging.getLogger("NewsScraper")
    logger.setLevel(logging.INFO)
    # create the logging file handler
    fh = logging.FileHandler(options.log_path + '/' + today + '.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    # add handler to logger object
    logger.addHandler(fh)

    logger.info('Started')

    # Start scraping

    scrapers = Scraper(options.phantomjs_path, options.username_wsj, options.password_wsj)
    date_list = [end_date - dt.timedelta(days=x) for x in range(0, options.num_days)]

    # wsj
    # save each day's news in a single file
    for date in date_list:
        scrapers.scraper_wsj(date)
        nlp_proc = Processor(scrapers.news_list)
        nlp_proc.summarize()
        save_json(nlp_proc.news_list, news_path + '/wsj_' + dt.datetime.strftime(date, '%Y-%m-%d'))

    # reuters
    scrapers.scraper_reuters()
    nlp_proc = Processor(scrapers.news_list)
    nlp_proc.summarize()
    save_json(nlp_proc.news_list, news_path + '/reuters')

    # nytimes
    scrapers.scraper_nytimes()
    nlp_proc = Processor(scrapers.news_list)
    nlp_proc.summarize()
    save_json(nlp_proc.news_list, news_path + '/nytimes')

    scrapers.quit()

    logger.info('Finished')


if __name__ == "__main__":
    main()