from apscheduler.schedulers.blocking import BlockingScheduler
from subprocess import call

import logging

scheduler = BlockingScheduler()


@scheduler.scheduled_job('interval', minutes=30)
def crawl_ncdc():
    """
    Crawl the NCDC website every 30 minutes with Scrapy
    """
    try:
        call(['python', 'covidScrapper/spiders/crawler.py'])
    except Exception as e:
        logging.error(str(e))
        print(str(e))


scheduler.start()
