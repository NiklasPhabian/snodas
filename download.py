#!/usr/bin/python3

import argparse
import os
import requests
import time
from eta import ETA


class Granule:
    
    def __init__(self, url, folder):        
        self.url = url
        self.file_name = None
        self.make_file_name()
        self.session = requests.Session()
        self.file_path = folder + '/' + self.file_name
    
    def make_file_name(self):
        self.file_name = self.url.split('/')[-1]
    
    def already_downloaded(self):
        if os.path.isfile(self.file_path):
            print('file already downloaded. Skipping')
            return True
        else:
            return False
    
    def download(self):
        downloaded = self.already_downloaded()        
        while not downloaded:                
            try:
                ret = self.session.get(self.url)                   
            except Exception as e:
                print(e)
                print('download failed, trying again')
                time.sleep(5)     
                continue            
            if ret.status_code == 200:
                downloaded = True
                with open(self.file_path, 'wb') as out_file:
                    out_file.write(ret.content)
            elif ret.status_code == 401:
                print('Got 401. Wrong user/pwd?')
                break
            else:
                print(ret.status_code)
                

def download(folder, file_name):
    urls = open(file_name).readlines()
    eta = ETA(n_tot=len(urls))
    for url in urls[::-1]:
        url = url.strip()
        granule = Granule(url=url, folder=folder)
        eta.display(step='Downloading {name}'.format(name=granule.file_name))
        granule.download()
        del urls[-1]
        open(file_name, 'w').writelines(urls)

        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Downloads files from file list')
    parser.add_argument('--file_list', metavar='csv', required=True, type=str, 
                        help='CSV to read urls from')
    parser.add_argument('--folder', metavar='folder', type=str, required=False,
                        help='Destination folder', default='.')    
    args = parser.parse_args()

    if args.file_list is None or args.folder is None:
        print('Wrong usage')
        print(parser.print_help())
        quit()

    folder = os.path.expanduser(args.folder + '/')
    download(folder, args.file_list)
