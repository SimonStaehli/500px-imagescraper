from imagescraper500 import ImageStream500, ImageCrawler500
from selenium import webdriver

if __name__ == '__main__':
    # The time frames of each script can cause duplicates which were not regarded in print statement
    # at the end of each class method.
    streamer = ImageStream500(webdriver=webdriver.Chrome('./src/chromedriver.exe'),
                              popularity='upcoming',
                              iter_sampling_rate=15,
                              batchsize=3,
                              stream_time=.5
                              )
    image_before = streamer.count_collected_images()
    streamer.stream()
    image_after = streamer.count_collected_images()
    print(f'Streamed {image_after-image_before} new Images')
    print(50*'*')

    crawler = ImageCrawler500(amount_per_class=1)
    image_before = crawler.count_collected_images()
    crawler.crawl()
    image_after = crawler.count_collected_images()
    print(f'Crawled {image_after-image_before} new Images')
    print(50*'*')

    crawler = ImageCrawler500(amount_per_class=10,
                              popularity_ranking='popular'
                              )
    image_before = crawler.count_collected_images()
    crawler.crawl()
    image_after = crawler.count_collected_images()
    print(f'Crawled {image_after-image_before} new Images')
