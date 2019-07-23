from dynamic_bike import extract_df, merge_df, data_manip, save_excel

import pandas as pd
from pandas import ExcelWriter
import glob
import os
import sys
import PySimpleGUI as sg      


def user_input(): # GUI testing
    event, values = sg.Window('Data Chooser').Layout([[sg.Text('Folder with raw bike files')],
                                                [sg.In(), sg.FolderBrowse()],
                                                [sg.CloseButton('Open'), sg.CloseButton('Cancel')]]).Read()
    raw_folder = values[0]
    print(raw_folder)

    layout = [[sg.Text('Would you like to clean your data?')],      
                    [sg.Radio('Yes!', "RADIO1", default=True),
                    sg.Radio('No!', "RADIO1")],
                    [sg.Submit()]]      
    window = sg.Window('Bike Data Tool', layout)    
    event, values = window.Read()   
    window.Close()
    manip = values[0]    
    if manip == True:
    ### Info Gather GUI ###
        layout = [      
            [sg.Text('Replace all HR with "0" if they are <:', size=(27, 1)), sg.InputText()],      
            [sg.Text('Replace all HR with "0" if they are >:', size=(27, 1)), sg.InputText()],      
            [sg.Text('All rows will be deleted if the Cadence there is less than:', size=(27, 2)), sg.InputText()],      
            [sg.Submit(), sg.Cancel()]]      
        window = sg.Window('Data Cleaning', layout)  
        event, values = window.Read()   
        window.Close()

        low_HR = int(values[0])
        high_HR = int(values[1])
        low_Cadence = int(values[2])
    ### Confirmation GUI still needed ###
        reorg_excels_and_manip(low_HR, high_HR, low_Cadence, manip, raw_folder)


    if manip == False:
        reorg_excels_no_manip(manip, raw_folder)

def reorg_excels_and_manip(low_HR, high_HR, low_Cadence, manip, raw_folder):
    path = raw_folder  # where the raw csv files are located
    all_files = glob.glob(os.path.join(path, "*.csv"))  # make a list of paths
    for files in all_files:
        csv_file = os.path.splitext(os.path.basename(files))[
            0]  # get file name without extension
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
    #### Finished Window with Options ###
    layout = [[sg.Text('Finished! What would you like to do next?')],
                [sg.Combo(['Quit', 'Combine Files','Start Over'])],       
                [sg.Submit(), sg.Cancel()]
             ]      
    window = sg.Window('File Restructuring Finished!', layout)    

    event, values = window.Read()    
    window.Close()
    combine = values[0]

    if combine == 'Quit':
        quit
    elif combine == 'Combine Files':
        combine_excels(manip)
    elif combine == 'Start Over':
        user_input()
    combine_excels(manip)

 
def reorg_excels_no_manip(manip, raw_folder):
    path = raw_folder  # where the raw csv files are located
    all_files = glob.glob(os.path.join(path, "*.csv"))  # make a list of paths

    for files in all_files:
        csv_file = os.path.splitext(os.path.basename(files))[0]  # get file name without extension
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
    
    #### Finished Window with Options ###
    layout = [[sg.Text('Finished! What would you like to do next?')],
                [sg.Combo(['Quit', 'Combine Files','Start Over'])],       
                [sg.Submit(), sg.Cancel()]
             ]      
    window = sg.Window('File Restructuring Finished!', layout)    

    event, values = window.Read()    
    window.Close()
    combine = values[0]

    if combine == 'Quit':
        quit
    elif combine == 'Combine Files':
        combine_excels(manip)
    elif combine == 'Start Over':
        user_input()

def combine_excels(manip):
    path1 = 'output/'
    path2 = 'output/raw_reorg/'
    all_data = pd.DataFrame()
    #--- Convert Dataframe to Excel ---#
    if manip == True:
        for f in glob.glob(os.path.join(path1, '*.xlsx')):
            df = pd.read_excel(f)
            all_data = all_data.append(df, ignore_index=True)
        writer = pd.ExcelWriter('combined_data_manip.xlsx')
        # save without name of columns and the row-numbers
        all_data.to_excel(writer, sheet_name='Sheet1', index=False)
        writer.save()
        ### Finished Notification GUI ###
        layout = [[sg.Text('Finished! Your new file saved as combined_data_manip.xlsx')],
                    [sg.Radio('Quit', "RADIO1", default=False, size=(10,1)), sg.Radio('Start Over', "RADIO1")],
                    [sg.Submit(), sg.Cancel()]]      
        window = sg.Window('Finished!', layout)
        event, values = window.Read()    
        window.Close()
        
        again = values[0]
        if again == False:
            user_input()
        else:
            quit
    if manip == False:
        for f in glob.glob(os.path.join(path2, '*.xlsx')):
            df = pd.read_excel(f)
            all_data = all_data.append(df, ignore_index=True)
        writer = pd.ExcelWriter('combined_data_raw.xlsx')
        # save without name of columns and the row-numbers
        all_data.to_excel(writer, sheet_name='Sheet1', index=False)
        ### Finished Notification GUI ###
        layout = [[sg.Text('Finished! Your new file saved as combined_data_raw.xlsx')],
                    [sg.Radio('Quit', "RADIO1", default=False, size=(10,1)), sg.Radio('Start Over', "RADIO1")],
                    [sg.Submit(), sg.Cancel()]]      
        window = sg.Window('Finished!', layout)
        event, values = window.Read()    
        window.Close()
        
        again = values[0]
        if again == False:
            user_input()
        else:
            quit

user_input()
