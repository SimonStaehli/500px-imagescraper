from bs4 import BeautifulSoup
import shutil, requests
import time, sys, os
import re
import random
from constructor import HTTPHeaderConstructor


class OnePieceMangaScraper(HTTPHeaderConstructor):
    """
    This class implements a webscraper to collect One-Piece Manga and saves it locally.

    """

    def __init__(self):
        """

        This class scrapes One-Piece Manga Chapters from the webpage: "https://onepiece-manga-online.net/"

        arguments:
        -------------------
        ?headers:
            Headers used for the requests. User Agend included only, so that there is not just
            a headless browser making a call to the webpages. If there is a problem with the given header.
            This can be adapted. Set within class method

        ?proxy:
            Proxy is set within a class method. Fakes different proxies.

        base_url:
            URL to make calls to. This class only works with this URL!

        response_code:
            Response Code to check if a call to the website is even possible.
            This attribute will be created automatically at the initialization of the class.
            If the response code is not equal to <200> the programm will stop abrupt.

        chapter_dict:
            This attribute will be created automatically at initializaiton fo the class.
            It's a dictionary of URL containing the URL's the chapters of the Manga.

        """
        super().__init__()
        self.base_url = 'https://onepiece-manga-online.net/'

        self.response_code = requests.get(self.base_url)
        if self.response_code.status_code != 200:
            raise Exception('Something went wrong with the webpage connection. HTTP-Code ' + str(self.response_code))
        print('HTTP-Response Code : ' + str(self.response_code))
        self.chapter_dict = self._create_chapter_dict()

    def _create_chapter_dict(self):
        """(None) ---> (dict)

        Scrapes all the chapters from https://onepiece-manga-online.net/ and creates a dictinoary with
        all chapters and the depending hyperlinks to their chapter.

        returns:
        ---------------
        chapter_urls:
            Dictionary with all chapters on the webpage and the depending urls.

        """
        latest_chapter = self.get_latest_chapter()
        chapter_urls = {}

        response = requests.get(self.base_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        soup_ = soup.find_all('li', attrs={'class': 'widget ceo_latest_comics_widget'})

        for i in soup_[0].find_all('a'):
            url = i['href']
            url = url.split('/')[-2]
            chapter = (re.findall(pattern=r'\d+', string=url)[0])
            if int(chapter) > latest_chapter:
                continue
            else:
                chapter_urls[int(chapter)] = i['href']

        return chapter_urls

    def scrape_chapter(self, chapter_no):
        """(int) ---> (None)

        Scrapes a chapter by given chapter-ID and saves it locally in OnePiece/Chapter_{chapter_no}/Page_...

        The scraper gets the date from source: https://onepiece-manga-online.net/.
        This functino makes use of further functions within the class (_extract_images, _save_images)

        params:
        ---------------
        chapter_no:
            Number of chapter which should be scraped

        returns:
        ---------------
        None
            Saves image in a local folder.

        """
        chapter_url = self.chapter_dict[chapter_no]
        header = self.get_user_agent()
        proxy = self.get_proxy()
        try:
            response = requests.get(chapter_url, stream=True, headers=header,
                                    proxies=proxy)
            soup = BeautifulSoup(response.text, 'html.parser')
            soup_ = soup.find_all('meta', attrs=dict(property="og:image"))

            page_content_ = []
            for i in soup_:
                page_content_.append(i['content'])
        except:
            print(f'Exception occured at scraping Chapter {chapter_no}')

        page_content_ = dict(enumerate(page_content_[1:]))
        self._extract_images(page_content=page_content_, chapter_no=chapter_no)
        sys.stdout.write(f'\n - Chapter {chapter_no} saved. -')

    def scrape_all_chapters(self):
        """(None) ---> (None)

        Scrapes all chapters from the webpage: https://onepiece-manga-online.net/ and saves it
        to a local folder.

        returns:
        ---------------
        None
            Saves image in a local folder.

        """
        latest_chapter = self.get_latest_chapter()
        i = 1
        while i < latest_chapter:
            sys.stdout.flush()
            sys.stdout.write(f'\r ---- Currently Scraping Chapter {i} of {latest_chapter} ----')
            self.scrape_chapter(chapter_no=i)
            time.sleep(random.randint(0, 10))
            i += 1

    def get_latest_chapter(self):
        """() ---> (int)

        Gets the number of the latest chapter
        """
        response = requests.get('http://onepiece-tube.com/kapitel-mangaliste#oben')
        soup = BeautifulSoup(response.text, 'html.parser')
        table_div = soup.find_all('div', attrs={'class': 'sagatable'})
        all_rows = table_div[0].find_all('tr')
        latest_chapter = all_rows[1].find('td').text

        return int(latest_chapter)

    def _extract_images(self, page_content, chapter_no):
        """(dict, int) ---> None

        Gets the content of the image source URL's and delivers the image content to the next funciton
        which saves the page image in a local folder

        params:
        ---------------
        page_content:
            The URL's to the depending chapter pages images.

        chapter_no:
            The number of the chapter which should be scraped.
        """
        for page, url in page_content.items():
            response = requests.get(url=url, stream=True, headers=self.get_user_agent(),
                                    proxies=self.get_proxy())
            OnePieceMangaScraper._save_image(image_ressources=response, chapter_no=chapter_no,
                                             page_number=page)

    @staticmethod
    def _save_image(image_ressources, chapter_no, page_number):
        """(str, int, int) ---> (None)

        Saves a given image ressources in a local folder. Therefore a new folder OnePiece will be
        created and the chapters with their respective content saved in it.

        params:
        ---------------
        image_ressources:
            Ressources of the image, which will be decoded in the next step

        chapter_no:
            Number of the chapter which should be scraped.

        page_number:
            Number of the depending page.
        """
        try:
            if 'OnePiece' not in os.listdir():
                os.mkdir('OnePiece')
            os.mkdir('OnePiece/' + 'Chapter_' + str(chapter_no))
        except:
            pass

        if image_ressources.status_code == 200:
            with open('OnePiece/Chapter_' + str(chapter_no) + '/Page_' + str(page_number + 1) + '.png', 'wb') as f:
                image_ressources.raw.decode_content = True
                shutil.copyfileobj(image_ressources.raw, f)
                f.close()

if __name__ == '__main__':
    user_input = input('Which chapter should be scraped?\n Give a number of a chapter or just all: ')
    scraper = OnePieceMangaScraper()
    if user_input == 'all':
        scraper.scrape_all_chapters()
    else:
        user_input = int(user_input)
        scraper.scrape_chapter(chapter_no=user_input)
