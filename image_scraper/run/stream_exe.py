from image_scraper.imagescraper500 import ImageStream500
from selenium import webdriver
import json

if __name__ == '__main__':
    # load configuration file
    with open('config.json', 'rb') as json_file:
        data = json.load(json_file)['scheduler']
    
    print(10*'*', 'Start Process', 10*'*')
    streaming = ImageStream500(
        webdriver=webdriver.Chrome(data['webdriver_path']),
        popularity=data['popularity'],
        iter_sampling_rate=data['iter_sampling_rate'],
        batchsize=data['batchsize'],
        stream_time=data['stream_time']
    )
    streaming.stream()
    
    print(10*'*', 'End Process', 10*'*')
