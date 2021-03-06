import gensim.summarization


def news_title_filter(title):
    return True


def news_summary_filter(summary):
    return True


class Processor:

    def __init__(self, news):
        self.list_news = news

    def summarize(self):
        for news in self.list_news:
            news['summary_gensim'] = gensim.summarization.summarize(news['article'], word_count=100)

    @property
    def news_list(self):
        return self.list_news
