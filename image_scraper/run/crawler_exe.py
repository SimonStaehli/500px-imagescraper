from image_scraper.imagescraper500 import ImageCrawler500
from selenium import webdriver
import json

if __name__ == '__main__':
    # Load configuration file
    with open('config.json', 'rb') as json_file:
        data = json.load(json_file)['crawler']
    
    
    print(10*'*', 'Start Process', 10*'*')
    crawler = ImageCrawler500(webdriver=webdriver.Chrome(data['webdriver_path']),
                              amount_per_class=data['amount_per_class'],
                              popularity_ranking=data['popularity_ranking']
                              )
    crawler.crawl()
    print(10*'*', 'End Process', 10*'*')

