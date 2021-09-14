from image_scraper.imagescraper500 import ImageStream500
from selenium import webdriver
import datetime as dt
import json

if __name__ == '__main__':
    # load config
    with open('config.json', 'rb') as json_file:
        data = json.load(json_file)['no_scheduler']
    
    # Map times to running times
    running_times = list(data['running_times'].values())
   
    while True:
        if dt.datetime.now().strftime('%H:%M') in running_times:
            print(10 * '*', f'Start Process at {dt.datetime.now().strftime("%H:%M:%S")}', 10 * '*')
            streaming = ImageStream500(
                webdriver=webdriver.Chrome(data['webdriver_path']),
                popularity=data['popularity'],
                iter_sampling_rate=data['iter_sampling_rate'],
                batchsize=data['batchsize'],
                stream_time=data['stream_time']
            )
            streaming.stream()
            
            print(10 * '*', f'End Process at {dt.datetime.now().strftime("%H:%M:%S")}', 10 * '*')
