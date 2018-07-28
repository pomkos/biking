import glob
import os

path = r'''C:\Users\albei\Nextcloud\Programming\biking\files'''
all_files = glob.glob(os.path.join(path, "*.csv")) #make a list of paths

for files in all_files:
    csv_file = os.path.splitext(os.path.basename(files))[0] #get file name without extension
    extract_df(csv_file)

    