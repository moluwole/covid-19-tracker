FROM python:3.8.1-slim-buster

EXPOSE 5000

WORKDIR /usr/src/www

RUN apt-get update \
    && apt-get install -y build-essential \
    && apt-get clean

RUN pip install --upgrade pip

RUN pip install supervisor \
    && pip install gunicorn

COPY requirements.txt /usr/src/www/requirements.txt

RUN pip install -r requirements.txt

COPY . /usr/src/www

COPY .env.example .env

RUN scrapy runspider covidScrapper/spiders/crawler.py

COPY ./services/supervisord.conf /etc/supervisor/supervisord.conf
COPY services/covidtracker.conf /etc/supervisor/conf.d/covidtracker.conf
COPY ./services/startup.sh /etc/startup.sh

RUN chmod u+x app.py

RUN chmod +x /etc/startup.sh

ENTRYPOINT ["/etc/startup.sh"]