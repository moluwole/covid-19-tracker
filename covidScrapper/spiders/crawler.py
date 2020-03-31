import json
import logging
import os
from datetime import datetime

import boto3
import scrapy
import redis
from scrapy.crawler import CrawlerProcess

REDIS_URL = os.getenv("REDIS_URL", 'redis://127.0.0.1:6379')
Store = redis.Redis.from_url(REDIS_URL)


class ScrapeNigeriaData(scrapy.Spider):
    name = "scraper"

    def __init__(self):
        super(ScrapeNigeriaData, self).__init__()
        self.all_result = None

    def start_requests(self):
        url = "https://covid19.ncdc.gov.ng/"
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
            row_data = row.css("td::text").getall()

            count = row.css("b::text").getall()

            if len(row_data) > 0:
                for i in range(0, len(row_data)):
                    data = {"state": row_data[i], "count": count[i]}
                    result.append(data)

        current_time = datetime.now()
        self.all_result = {
            "states": result,
            "overall": overall_data,
            "date": current_time.strftime("%c"),
        }
        self.save_result_to_cache()
        self.upload_result_to_s3()
        return self.all_result

    def save_result_to_cache(self, key=None):
        key = key or datetime.now().strftime('%d/%m/%Y')
        one_day = 60 * 60 * 24
        json_result = json.dumps(self.all_result, ensure_ascii=False)
        Store.set(name='latest', value=json_result)
        Store.set(name=key, value=json_result, ex=one_day)

    def upload_result_to_s3(self, bucket_name="covid-19-nigeria-tracker",
                            file_name="result.json"):
        if os.getenv("FLASK_ENV") == "production":
            try:
                s3_resource = boto3.resource(
                    "s3",
                    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", ""),
                    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                )

                s3_resource.Bucket(bucket_name).put_object(
                    Key=file_name,
                    Body=bytes(json.dumps(
                        self.all_result, indent=4, ensure_ascii=False),
                        encoding='utf8'),
                    ACL="public-read",
                )
            except Exception as e:
                print(str(e))
                logging.error(str(e))
        else:
            self.save_result_to_file()

    def save_result_to_file(self, file_name="result.json"):
        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(self.all_result, file, ensure_ascii=False, indent=4)


def main():
    process = CrawlerProcess(
        {
            "USER_AGENT": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)"}
    )

    process.crawl(ScrapeNigeriaData)
    process.start()


if __name__ == "__main__":
    main()
