import argparse
import os
import tarfile
import glob
import subprocess


def untar(folder):
    '''The command tar -xvf *.tar does not work because the wildcard (*.tar) is 
    expanded by the shell before it is passed as an argument to the tar command. 
    This means that tar receives a list of individual .tar files as arguments, 
    and it doesn't know how to handle multiple files at once in this manner.'''
    
    # List all tars in the directory
    tar_files = glob.glob(f'{folder}/*.tar')

    # Loop through each tar file and extract it
    for tar_file in tar_files:
        # Create a tarfile object and extract the contents
        with tarfile.open(tar_file, 'r') as tar:
            tar.extractall(path=folder)

        print(f"Extracted: {tar_file}")

        
def remove_tars(folder):
    tar_files = glob.glob(f'{folder}/*.tar')
    for file_path in tar_files:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"File {file_path} has been deleted.")
            except OSError as e:
                print(f"Error deleting {file_path}: {e}")
        else:
            print(f"File {file_path} does not exist.")
       
    
def unzip(folder):
    gz_files = glob.glob(f'{folder}/*.gz')    
    # Run gunzip for each GZ file
    for gz_file in gz_files:                
        try:
            """gunzip by default removes the source GZ file after successful extraction. 
            To prevent this behavior, you can use the -k (or --keep)"""
            subprocess.run(["gunzip", gz_file], check=True)
            print(f"File {gz_file} has been successfully uncompressed.")
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
                 
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Untar files from folder')    
    parser.add_argument('--folder', metavar='folder', type=str, required=False,
                        help='Folder with tarballs', default='.')    
    parser.add_argument('--rm_tar', metavar='rm_tar', type=str, required=False,
                        help='Folder with tarballs', default=True)    
    args = parser.parse_args()

    if args.folder is None:
        print('Wrong usage')
        print(parser.print_help())
        quit()

    folder = os.path.expanduser(args.folder + '/')
    untar(folder)
    if args.rm_tar:
        remove_tars(folder)
    unzip(folder)
    