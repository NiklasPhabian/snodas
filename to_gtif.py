import argparse
import os
import glob
import subprocess
from eta import ETA

"""
https://nsidc.org/data/user-resources/help-center/how-do-i-convert-snodas-binary-files-geotiff-or-netcdf
"""

def make_hdr(filename):
    f_type = filename.split('/')[-1].split('_')[0]
    if f_type == 'us':
        '''masked file'''
        content = 'ENVI\nsamples = 6935\nlines = 3351\nbands = 1\nheader offset = 0\nfile type = ENVI Standard\ndata type = 2\ninterleave = bsq\nbyte order = 1'
    if f_type == 'zz':
        content = 'ENVI\nsamples = 8192\nlines = 4096\nbands = 1\nheader offset = 0\nfile type = ENVI Standard\ndata type = 2\ninterleave = bsq\nbyte order = 1'

    file_path = filename.split('.dat')[0] + '.hdr'
    
    with open(file_path, 'w') as file:
        # Write the string to the file
        file.write(content)


def write_headers(folder):
    files = glob.glob(f'{folder}/*.dat')
    for file in files:
        make_hdr(file)
        
        
def make_tif(dat_file):    
    tif_file = dat_file.replace('.dat', '.tif')
    cmd = f"gdal_translate -of GTiff -a_srs '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs' -a_nodata -9999 -a_ullr -124.73333333333333 52.87500000000000 -66.94166666666667 24.95000000000000 {dat_file} {tif_file}"
    result = subprocess.run(cmd, shell=True, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)    

    
def make_tifs(folder):
    files = glob.glob(f'{folder}/*.dat')
    eta = ETA(n_tot=len(files))
    for file in files:        
        make_tif(file)
        eta.display(step='Converted {name}'.format(name=file))
        

def remove_dats(folder):    
    files = glob.glob(f'{folder}/*.dat')
    for file_path in files:
        os.remove(file_path)                


def remove_txts(folder):    
    files = glob.glob(f'{folder}/*.txt')
    for file_path in files:        
        os.remove(file_path)     


def remove_hdrs(folder):    
    files = glob.glob(f'{folder}/*.hdr')
    for file_path in files:        
        os.remove(file_path)
            

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert dat files to geotiffs')        
    parser.add_argument('--folder', metavar='folder', type=str, required=False,
                        help='Folder with dat files', default='.')            
    args = parser.parse_args()                                        
    folder = os.path.expanduser(args.folder + '/')    
    write_headers(folder)
    make_tifs(folder)
    remove_dats(folder)
    remove_txts(folder)
    remove_hdrs(folder)
    
