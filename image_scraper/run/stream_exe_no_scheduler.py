from image_scraper.imagescraper500 import ImageStream500
from selenium import webdriver
import datetime as dt


if __name__ == '__main__':
    running_times = ['10:01', '15:14', '20:53'] # <- put your preferred running time in here
    duration_in_minutes = 15
    while True:
        if dt.datetime.now().strftime('%H:%M') in running_times:
            print(10 * '*', f'Start Process at {dt.datetime.now().strftime("%H:%M:%S")}', 10 * '*')
            streaming = ImageStream500(webdriver=webdriver.Chrome('../src/chromedriver.exe'),
                                       popularity='upcoming',
                                       iter_sampling_rate=10,
                                       batchsize=20,
                                       stream_time=duration_in_minutes)
            streaming.stream()
            print(10 * '*', f'End Process at {dt.datetime.now().strftime("%H:%M:%S")}', 10 * '*')
