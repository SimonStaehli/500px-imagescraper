from image_scraper.imagescraper500 import ImageStream500
from selenium import webdriver

if __name__ == '__main__':
    # This script can be added to the computers task schedulers
    # Additionally this script can be individualized with parameters
    print(10*'*', 'Start Process', 10*'*')
    streaming = ImageStream500(webdriver=webdriver.Chrome('../src/chromedriver.exe'),
                               popularity='fresh',
                               iter_sampling_rate=5,
                               batchsize=10,
                               stream_time=5)
    streaming.stream()
    print(10*'*', 'End Process', 10*'*')
