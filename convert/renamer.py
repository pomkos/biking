# DESCRIPTION
# This script was made to rename bunch of bike files, each of them named "Data_Log.csv", and copy them to a new folder.

# GOAL
# Get files ready for start_biking script (to reorganize) and eventual MatLab analysis (for entropy analysis)


import glob # for getting list of files
from shutil import copyfile # for copying files to new location
import pandas as pd
import numpy as np

files = glob.glob("temp/*/*.csv")
files = pd.Series(files)

def file_renamer(files_list, new_location):
    '''
    Renames .csv files based on its parent folder
    
    [input]
    files_list: current location of files, must be no more than 2 dir deep. List of string. 'path/to_the/file.csv'
    new_location: new location to copy files to. String. 'new/path/'
    
    [output]
    Copy of file in the new_location. File will be named 'to_the.csv'
    '''
    
    files = files_list.copy()
    files2 = files_list.copy()
    files2 = files2.str.lower()
    
    position = 0
    for i in files2.str.split('/'):
        if type(i) != float:
            i[1] = i[1].replace(" ","")
            i[1] = i[1].replace("-","_")
            i[1] = i[1]+".csv"
            old = files[position]
            new = new_location + i[1]
            copyfile(old,new)
            position += 1
            print(f'{files[position]} done!')

file_renamer(files, 'temp/1new/')
