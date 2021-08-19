from imagescraper500 import ImageCrawler500

if __name__ == '__main__':
    print(10*'*', 'Start Process', 10*'*')
    crawler = ImageCrawler500(amount_per_class=100,
                              popularity_ranking='popular'
                              )
    crawler.crawl()
    print(10*'*', 'End Process', 10*'*')

