from apscheduler.schedulers.blocking import BlockingScheduler
from subprocess import call

scheduler = BlockingScheduler()


@scheduler.scheduled_job('interval', minutes=30)
def crawl_ncdc():
    """
    Crawl the NCDC website every 30 minutes with Scrapy
    """
    call(['python', 'covidScrapper/spiders/crawler.py'])


scheduler.start()
