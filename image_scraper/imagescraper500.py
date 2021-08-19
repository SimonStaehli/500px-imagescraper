from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import requests
import os
import time
import random
import datetime as dt
from tqdm import tqdm


class SiteContent500(object):

    def __init__(self):
        """
        This class is for the storage of particular site content like image classes and popularity rankings.

        """
        super(SiteContent500, self).__init__()
        self.popularity_rankings = ['popular', 'upcomming', 'fresh']
        self.__all_image_classes()

    def __all_image_classes(self):
        """
        """
        image_classes_string = "abstract-aerial-animals-black+and+white-celebrities-city+%26+architecture-commercial-concert-family-fashion-film-fine+art-food-journalism-landscapes-macro-nature-night-people-performing+arts-sport-still+life-street-transportation-travel-underwater-urban+exploration-wedding"
        image_classes = image_classes_string.split('-')
        image_classes = [img.replace('+', ' ') for img in image_classes]
        image_classes = [img.replace('%26', 'and') for img in image_classes]
        image_classes_dict = dict(zip(image_classes, image_classes_string.split('-')))

        self.image_classes_dict = image_classes_dict
        random.shuffle(image_classes)
        self.image_classes = image_classes


class ImageSaver(SiteContent500):
    """
    This class is for the image donwload and storage in a given folder structure.
    """

    def __init__(self, image_folder_path='./images'):
        """
        This class calls the functions construct_image_folder_path() which constructs a directory which fits
        to the image classes on the website. After the class methods can be used to download an image by a hyperlink to
        image source.

        Parameters
        --------------------------------------
        image_folder_path : string
            Relative Path where the images should be saved and the folder structure should be created.

        """
        super(ImageSaver, self).__init__()
        self.image_folder_path = image_folder_path
        self._construct_folder_structure()

    def _download_images(self, image_urls):
        """
        Takes a list of image source urls and downloads it to a given folder by image class and image_folder_path.

        Parameters
        --------------------------------------
        image_urls : dict
            A dictionary which consists of classification of the image as key and the value is the image source.
        """
        print('| Starting download of all images ...')
        for picture_class, all_urls in tqdm(iterable=image_urls.items()):
            # Extract id of the image from retrieve url
            for url in all_urls:
                # Save images
                try:
                    with open(f'{self.image_folder_path}/{picture_class}/{url.split("/")[4]}.jpg',
                              'wb') as image_file:
                        image_file.write(requests.get(url).content)
                except:
                    print(f'-- Could not Save image with class {picture_class} ({url})')


    def _construct_folder_structure(self):
        """
        Constructs a folder structure with the given image_folder_path attribute.
        """
        try:
            os.mkdir(self.image_folder_path)
        except:
            pass
        for img_class in self.image_classes:
            try:
                os.mkdir(self.image_folder_path + '/' + img_class)
            except:
                pass

    def count_collected_images(self, print_count=True):
        """Counts how many images were collected in the path until now."""
        counter = 0
        for directories in os.listdir(self.image_folder_path):
            for elements in os.listdir(self.image_folder_path + '/' + directories):
                if '.jpg' in elements:
                    counter += 1
        if print_count:
            print(f'Counted {counter} Collected Images.')

        return counter


class ImageStream500(ImageSaver):

    def __init__(self, webdriver,
                 popularity='upcoming', iter_sampling_rate=10,
                 batchsize=10, stream_time=60, image_folder_path='./images'):
        """
        To use this class a compatible webdriver of selenium needs to be installed and initiated. 
        See here for more inforamtion: https://www.selenium.dev/downloads/
        
        When the class is initiated, it will create a folder strucutre automatically within the directory where 
        the script is located.
        
        Example:
        --------------------------------------
        stream = ImageStream500(webdriver=webdriver.Chrome('../src/chromedriver.exe'),
                                popularity='upcoming', iter_sampling_rate=10,
                                iteration_batch=10, stream_time=60, image_folder_path='./images')
        
        Parameters
        --------------------------------------
        webdriver: selenium webdriver
            Created webdriver with selenium to make use of different webdrivers possible.         
            Further information and Downloads here: https://www.selenium.dev/downloads/
            
        popularity : string
            popularity which should be streamed. The higher the popularity the less image can be scraped
            but the more information to the classes will be probably available.
            possible parameters: (popular, upcoming, fresh)

        iter_sampling_rate: int
            Defines how much images should be extracted in one iteration.

        batchsize: int
            Defines after how many extracted images they shall be saved.

        stream_time: int
            Defines streamtime in minutes how long the streaming should take place.
            
        image_folder_path: string
            Path where to images shall be  stored after the download.

        """
        super(ImageStream500, self).__init__(image_folder_path=image_folder_path)
        self.driver = webdriver
        self.popularity = popularity
        self.iter_sampling_rate = iter_sampling_rate
        self.batchsize = batchsize
        self.stream_time = stream_time

    def stream(self):
        """
        if this method is called the latest images of the popularity given as parameter will be streamed
        until process is interrupted or the stream_time exceeded.

        """
        image_urls = {}
        href_history = []
        iteration = 0
        end_time = dt.datetime.now() + dt.timedelta(minutes=self.stream_time)

        while dt.datetime.now() < end_time:
            iteration += 1

            try:
                self.driver.get('https://500px.com/' + self.popularity)
                # Wait on elements to appear
                element_present = EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="content"]/div/div[1]/div[3]/div/div[1]/div/div/div[1]/a/img'))
                WebDriverWait(self.driver, 5).until(element_present)
            except:
                print('-- Skip Iteration due to failure to get webpage in certain amount of time.')
                continue

            # Community window
            try:
                self.driver.find_element_by_xpath('//*[@id="modal_content"]/div/div/div/div/div[1]/div[1]').click()
            except:
                pass

            # get all href
            href_urls = []
            for i in range(1, self.iter_sampling_rate + 1):
                href = self.driver.find_element_by_xpath(
                    f'//*[@id="content"]/div/div[1]/div[3]/div/div[1]/div/div/div[{i}]/a').get_attribute('href')
                if href in href_history:
                    # Check if href already exists in history
                    break
                else:
                    href_urls.append(href)
            if len(href_urls) == 0:
                # if there is no new element in the list then skip loop
                time.sleep(random.randint(10, 20))
                continue

            # go to href and extract image urls and image class + save it as dict
            for href in href_urls:
                try:
                    self.driver.get(href)
                    element_present = EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="copyrightTooltipContainer"]/div/img'))
                    WebDriverWait(self.driver, 5).until(element_present)
                except:
                    print('-- Could not reach element in time. Skip element.')

                try:
                    image_source = self.driver.find_element_by_xpath(
                        '//*[@id="copyrightTooltipContainer"]/div/img').get_attribute('src')
                except:
                    pass
                # sometimes images have diff div no. loop over a possible numbers
                for i in range(4, 9):
                    try:
                        image_class = self.driver.find_element_by_xpath(
                            f'//*[@id="root"]/div[4]/div/div/div/div/div[3]/div[{i}]/p[2]/a/span').text
                        if image_class.casefold() in self.image_classes:
                            break
                    except:
                        image_class = None

                if image_class:
                    image_class = image_class.casefold()
                    try:
                        image_urls[image_class].append(image_source)
                    except:
                        # In case there is no
                        image_urls[image_class] = []
                        image_urls[image_class].append(image_source)

                time.sleep(random.randint(0, 2))

            count_collected_images = sum((len(v) for v in image_urls.values()))
            print(f'| Extracted {count_collected_images} images in total.')

            # Set history of scraped images to avoid duplicates
            for href in href_urls:
                href_history.append(href)

            # If amount of collected images is bigger than batchsize than save images and empty url dict
            if count_collected_images >= self.batchsize:
                self._download_images(image_urls=image_urls)
                image_urls = {}
                print('| Saved Image Batch to folder.')

            time.sleep(random.randint(1, 10))

        # Comes after while loop
        self.driver.close()
        if image_urls != {}:
            self._download_images(image_urls=image_urls)
            print('| Saved Last Image Batch to folder.')
        print(f'| Stream Time of {self.stream_time} min over.')

        return self


class ImageCrawler500(ImageSaver):
    """
    This class extracts images from 500px.
    """

    def __init__(self, webdriver,
                 amount_per_class=10, popularity_ranking='popular', image_folder_path='./images'):
        """
        With this class images of the website 500px can be downloaded in mass. You can download images with selenium and
        a downloaded webdriver. This class will download image from a certain popularity_ranking which is defined as class
        attribute and the given ammount of images by each class.
        
        When the class is initiated it will create a folder strucutre automatically within the directory where 
        the script is located.

        Example:
        --------------------------------------
        crawler = ImageCrawler500(webdriver=webdriver.Chrome('../src/chromedriver.exe'),
                                 amount_per_class=10, popularity_ranking='popular', 
                                 image_folder_path='./images')
        
        Parameters
        --------------------------------------
        webdriver : selenium webdriver
            Created webdriver with selenium to make use of different webdrivers possible.         
            Further information and Downloads here: https://www.selenium.dev/downloads/

        amount_per_class: int
            How many images per class should be scraped

        popularity_ranking: string
            Can be one of: "popular", "upcoming", "fresh"
            
        image_folder_path: string
            Path where webdriver is stored

        """
        super(ImageCrawler500, self).__init__(image_folder_path=image_folder_path)
        self.driver = webdriver
        self.base_url = 'https://500px.com/'
        self.amount_per_class = amount_per_class
        self.popularity_ranking = popularity_ranking

        # Set within class method
        self.image_urls = None

    def crawl(self):
        """
        If this method is called the process with the image crawling from the website is started.
        """

        image_urls = self._crawl_mixed()

        self.driver.close()
        self._download_images(image_urls=image_urls)

        return self

    def _crawl_mixed(self):
        """
        This method crawls a given amount of images by each image class.

        Returns:
        --------------------------------------
        image_urls: dict
            dictionary of image classes as keys and the depending image urls.
        """
        # Scraping part
        image_urls = {}
        for image_class_number, img_class in enumerate(self.image_classes):
            print(f"| Extracting: {self.amount_per_class} Images of {img_class} ({image_class_number+1}/{len(self.image_classes)})")
            image_sources = []
            url = self.base_url + '/' + self.popularity_ranking + '/' + self.image_classes_dict[img_class]
            self.driver.get(url)
            element_present = EC.presence_of_element_located(
                (By.XPATH, '//*[@id="content"]/div/div[1]/div[3]/div/div[1]/div/div/div[1]/a/img'))
            WebDriverWait(self.driver, 5).until(element_present)

            element_number = 1
            while element_number < self.amount_per_class + 1:
                try:
                    try:
                        web_element = self.driver.find_element_by_xpath(
                            '//*[@id="content"]/div/div[1]/div[3]/div/div[1]/div/div/div[{}]/a/img'.format(
                                element_number))
                        image_sources.append(web_element.get_attribute('src'))

                    except:
                        print('-- Could not extract image url.')

                    element = self.driver.find_element_by_xpath(
                        '//*[@id="content"]/div/div[1]/div[3]/div/div[1]/div/div/div[{}]/a'.format(element_number))
                    ActionChains(self.driver).move_to_element(element).perform()
                    element_number += 1
                    # time.sleep(random.randint(0, 2))

                except:
                    print('-- Could not Jump to next image.')

            image_urls[img_class] = image_sources

        return image_urls
