from dynamic_bike import extract_df

import pandas as pd
from pandas import ExcelWriter
import glob
import os

def reorg_excels():
    path = 'input' #where the csv files are located
    all_files = glob.glob(os.path.join(path, "*.csv")) #make a list of paths

    for files in all_files:
        csv_file = os.path.splitext(os.path.basename(files))[0] #get file name without extension
        extract_df(csv_file)
        print(csv_file + ".csv reorganized!")

def combine_excels():
    dataframes = []
    path2 = 'output'
    new_files = glob.glob(os.path.join(path2, "*.xlsx"))
    for f in new_files:
        data = pd.read_excel(f, 'Sheet1').iloc[:-2]
        data.index = [os.path.basename(f)] * len(data)
        dataframes.append(data)

    df = pd.concat(dataframes)
    #save df as excel:
    csv_file = 'dynamic_sheets.xlsx'
    #--- Convert Dataframe to Excel ---#
    writer = ExcelWriter(csv_file)
    df.to_excel(writer,sheet_name='Sheet1')
    writer.save()
    print(csv_file + " saved!")

reorg_excels()
combine_excels()