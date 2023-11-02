import argparse
import requests
import datetime


months = {1: '01_Jan',
          2: '02_Feb',
          3: '03_Mar',
          4: '04_Apr',
          5: '05_May',
          6: '06_Jun',
          7: '07_Jul',
          8: '08_Aug',
          9: '09_Sep',
          10: '10_Oct',
          11: '11_Nov',
          12: '12_Dec'}


def make_url(date, masked):
    if masked:
        masked = 'masked'
    else:
        masked= 'unmasked' 
    year = date.year
    month = date.month
    day = date.day    
    month_str = months[month]
    file_name = f'SNODAS_{year}{month:02}{day:02}.tar'
    url = f'https://noaadata.apps.nsidc.org/NOAA/G02158/{masked}/{year}/{month_str}/{file_name}'
    return url


def make_urls(start, stop, masked):
    urls = []
    start = datetime.datetime.strptime(start, '%Y-%m-%d').date()
    stop = datetime.datetime.strptime(stop, '%Y-%m-%d').date()
    step = datetime.timedelta(days=1)
    iterator = start  
    while iterator + step <= stop:        
        url = make_url(iterator, masked)
        urls.append(url)
        iterator += step
    return urls  


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get URLs from the ArthurHou server')        
    parser.add_argument('--start', metavar='start', required=True, type=str, 
                        help='start date (yyyy-mm-dd)')
    parser.add_argument('--stop', metavar='stop', required=True, type=str, 
                        help='stop date (yyyy-mm-dd)')
    parser.add_argument('--masked', metavar='masked', required=False, type=bool, 
                        help='True/False')
    parser.add_argument('--out', metavar='out', required=False, type=str, 
                        help='the csv filename to store the links in')
    parser.set_defaults(out='urls.csv')    
    parser.set_defaults(masked=True)
    args = parser.parse_args()   
    
    urls = make_urls(args.start, args.stop, args.masked)
    with open(args.out, 'a') as files_log:        
        files_log.writelines("\n".join(urls))
        files_log.write('\n')