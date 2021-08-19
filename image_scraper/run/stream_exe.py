from imagescraper500 import ImageStream500

if __name__ == '__main__':
    # This script can be added to the computers task schedulers
    # Additionally this script can be individualized with parameters
    print(10*'*', 'Start Process', 10*'*')
    streaming = ImageStream500(popularity='upcoming',
                               iter_sampling_rate=10,
                               iteration_batch=2,
                               stream_time=1)
    streaming.stream()
    print(10*'*', 'End Process', 10*'*')
