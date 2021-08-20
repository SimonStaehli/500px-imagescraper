from image_scraper.imagescraper500 import ImageCrawler500
from selenium import webdriver

if __name__ == '__main__':
    print(10*'*', 'Start Process', 10*'*')
    crawler = ImageCrawler500(webdriver=webdriver.Chrome('../src/chromedriver.exe'),
                              amount_per_class=100,
                              popularity_ranking='popular'
                              )
    crawler.crawl()
    print(10*'*', 'End Process', 10*'*')

