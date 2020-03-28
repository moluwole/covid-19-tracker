import scrapy
import json

from scrapy.crawler import CrawlerProcess

from datetime import datetime


class ScrapeNigeriaData(scrapy.Spider):
    name = "scraper"

    def start_requests(self):
        url = 'https://covid19.ncdc.gov.ng/'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        overall_data = {}
        all_data = response.xpath('//table[@id="custom1"]//tr')
        for row in all_data:
            text = row.css("td::text").getall()
            count = row.css("b::text").getall()

            overall_data[text[0]] = count[0]

        state_data = response.xpath('//table[@id="custom3"]//tr')

        result = []
        for row in state_data:
            row_data = row.css('td::text').getall()

            count = row.css('b::text').getall()

            if len(row_data) > 0:
                for i in range(0, len(row_data)):
                    data = {"state": row_data[i], "count": count[i]}
                    result.append(data)

        all_result = {
            "states": result,
            "overall": overall_data,
            "date": datetime.now().strftime('%c')
        }
        with open('result.json', 'w', encoding='utf-8') as file:
            json.dump(all_result, file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(ScrapeNigeriaData)
    process.start()
