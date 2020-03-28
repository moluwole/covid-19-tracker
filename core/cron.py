import os

from subprocess import call
from controllers import crontab


@crontab.job(minute=30)
def crawl_ncdc() -> None:
    """
    Crawl the NCDC website every 30 minutes with Scrapy
    """
    call(['scrapy', 'runspider', 'covidScrapper/spiders/crawler.py'])
