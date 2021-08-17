from imagescraper500 import ImageStream500
import datetime as dt


if __name__ == '__main__':
    running_times = ['10:01', '15:14', '20:53'] # <- put your preferred running time in here
    duration_in_minutes = 15
    while True:
        if dt.datetime.now().strftime('%H:%M') in running_times:
            print(10 * '*', f'Start Process at {dt.datetime.now().strftime("%H:%M:%S")}', 10 * '*')
            streaming = ImageStream500(popularity='upcoming',
                                       iter_sampling_rate=10,
                                       iteration_batch=2,
                                       stream_time=duration_in_minutes)
            streaming.stream()
            print(10 * '*', f'End Process at {dt.datetime.now().strftime("%H:%M:%S")}', 10 * '*')
