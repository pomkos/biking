from dynamic_bike import extract_df

import pandas as pd
from pandas import ExcelWriter
import glob
import os

def user_input(): #prompt data_manip() integers
    low_HR = input("All HR should be replaced with '0' if they are less than: ") #
    low_HR = int(low_HR)
    high_HR = input("All HR should be replaced with '0' if they are greater than: ")
    high_HR = int(high_HR)
    low_Cadence = input("All rows will be deleted if the Cadence there is less than: ")
    low_Cadence = int(low_Cadence)
    print("I will replace HR <", low_HR,"bpm or >", high_HR, "bpm with a '0'")
    print("I will delete rows who's cadence is <", low_Cadence)
    reorg_excels(low_HR, high_HR, low_Cadence)

def reorg_excels(low_HR, high_HR, low_Cadence):
    path = 'input' #where the csv files are located
    all_files = glob.glob(os.path.join(path, "*.csv")) #make a list of paths

    for files in all_files:
        csv_file = os.path.splitext(os.path.basename(files))[0] #get file name without extension
        extract_df(csv_file, low_HR, high_HR, low_Cadence)
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
    df.to_excel(writer,sheet_name='Sheet1') #save without name of columns and the row-numbers
    writer.save()
    print(csv_file + " saved!")
    input("Finished! Press enter to quit.") #only quit when prompted
user_input()
#reorg_excels()
combine_excels()