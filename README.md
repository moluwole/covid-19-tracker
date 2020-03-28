# Covid-19 Tracker

Uses
- Scrapy
- Flask
- Bulma CSS

How it Works
- Run `docker-compose up --build -d` and the system should be up at `127.0.0.1:5001`

The System uses Scrapy to scrape [covid19.ncdc.gov.ng](https://covid19.ncdc.gov.ng).
The Spider resides in `covidScrapper/spiders/crawler.py`. 

To update the JSON result manually run
```bash
docker-compose exec app scrapy runspider covidScrapper/spiders/crawler.py
```

#### Online Deployment
Currently runs on Heroku here: [covid-19-tracker](https://covid-tracker-nigeria.herokuapp.com)

Result is updated every 30 minutes on Schedule

Contributors:
- Oluwole Majiyagbe (@moluwole)