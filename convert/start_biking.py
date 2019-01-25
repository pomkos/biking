from dynamic_bike import extract_df, merge_df, data_manip, save_excel

import pandas as pd
from pandas import ExcelWriter
import glob
import os

def user_input(): #prompt data_manip() integers
    manip = input("Would you like to clean the HR/cadence data? (Press 1 for yes, 2 for no): ")
    manip = int(manip)
    if manip == 1:
        print('-------------------------------------------------------------')
        low_HR = input("All HR should be replaced with '0' if they are less than: ") #
        low_HR = int(low_HR)
        high_HR = input("All HR should be replaced with '0' if they are greater than: ")
        high_HR = int(high_HR)
        low_Cadence = input("All rows will be deleted if the Cadence there is less than: ")
        low_Cadence = int(low_Cadence)
        print('-------------------------------------------------------------')
        print("I will replace HR <", low_HR,"bpm or >", high_HR, "bpm with a '0'")
        print("I will delete rows who's cadence is <", low_Cadence)
        print('-------------------------------------------------------------')      
        confirm = input("Press 1 to confirm or 2 to start over: ")
        confirm = int(confirm)
        if confirm == 1:
            reorg_excels_and_manip(low_HR, high_HR, low_Cadence, manip)
        if confirm == 2:
            user_input()
     
    if manip == 2:
        confirm = input("Press 1 to confirm or 2 to start over: ")
        confirm = int(confirm)
        if confirm == 1:
            reorg_excels_no_manip(manip)
        if confirm == 2:
            user_input()
        
def reorg_excels_and_manip(low_HR, high_HR, low_Cadence, manip):
    path = 'input' #where the raw csv files are located
    all_files = glob.glob(os.path.join(path, "*.csv")) #make a list of paths
    for files in all_files:
        csv_file = os.path.splitext(os.path.basename(files))[0] #get file name without extension
        ext_dic = extract_df(csv_file)
        #-- Extract the dictionary into its variables --#
        HR = ext_dic['HR']
        Cadence = ext_dic['Cadence']
        Power = ext_dic['Power']
        Torque = ext_dic['Torque']
        #--   --#
        subject_data = merge_df(HR, Cadence, Power, Torque, csv_file)
        data_manip(subject_data, csv_file, low_HR, high_HR, low_Cadence, manip)
        print(csv_file + ".csv reorganized!")
    combine_excels(manip)

def reorg_excels_no_manip(manip):
    path = 'input' #where the raw csv files are located
    all_files = glob.glob(os.path.join(path, "*.csv")) #make a list of paths
    for files in all_files:
        csv_file = os.path.splitext(os.path.basename(files))[0] #get file name without extension
        ext_dic = extract_df(csv_file)
        #-- Extract the dictionary into its variables --#
        HR = ext_dic['HR']
        Cadence = ext_dic['Cadence']
        Power = ext_dic['Power']
        Torque = ext_dic['Torque']
        #--   --#
        subject_data = merge_df(HR, Cadence, Power, Torque, csv_file)
        save_excel(subject_data, csv_file, manip)
        print(csv_file + ".csv reorganized!")
    combine_excels(manip)

def combine_excels(manip):
    all_data = pd.DataFrame()
    for f in glob.glob('output/*.xlsx'):
        df = pd.read_excel(f)
        all_data = all_data.append(df, ignore_index=True)
    #--- Convert Dataframe to Excel ---#
    if manip == 1:
        writer = pd.ExcelWriter('combined_data_manip.xlsx')
        all_data.to_excel(writer,sheet_name='Sheet1', index=False) #save without name of columns and the row-numbers
        writer.save()
        again = input("Finished! Press 1 to quit or 2 to start again: ") #only quit when prompted
        again = int(again)
        if again == 2:
            user_input()
        else:
            quit
    if manip == 2:
        writer = pd.ExcelWriter('combined_data_raw.xlsx')
        all_data.to_excel(writer,sheet_name='Sheet1', index=False) #save without name of columns and the row-numbers
        writer.save()
        print("combined_data_raw.xlsx saved!")
        again = input("Finished! Press 1 to quit or 2 to start again: ") #only quit when prompted
        again = int(again)
        if again == 2:
            user_input()
        else:
            quit
user_input()