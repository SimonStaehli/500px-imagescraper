from imagescraper500 import ImageStream500

if __name__ == '__main__':
    streaming = ImageStream500(popularity='upcoming',
                               iter_sampling_rate=10,
                               iteration_batch=2,
                               stream_time=1)
    streaming.stream()