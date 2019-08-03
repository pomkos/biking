from dynamic_bike import extract_df, merge_df, data_manip, save_excel

import pandas as pd
from pandas import ExcelWriter
import glob
import os
import sys
import PySimpleGUI as sg      

def start():
    ## Define input and output folders
    event, values = sg.Window('Data Chooser').Layout([[sg.Text('Input folder')],
                                                [sg.In(), sg.FolderBrowse()],
                                                [sg.Text('Output folder')],
                                                [sg.In(), sg.FolderBrowse()],
                                                [sg.CloseButton('Open'), sg.CloseButton('Cancel')]]).Read()
    raw_folder = values[0]
    output_folder=values[1]

    if event == 'Open':
        ## Choose Options
        layout = [[sg.Text('Would you like to clean your data?')],      
                    [sg.Radio('Yes', "RADIO1", default=True),
                    sg.Radio('No', "RADIO1")],
                    [sg.Text('Would you like to count the number of lines with Power < 0?')],
                    [sg.Radio('Yes', "RADIO2", default=True),
                    sg.Radio('No', "RADIO2")],
                    [sg.Submit()]]      
        window = sg.Window('Bike Data Tool', layout)    
        event, values = window.Read()   
        window.Close()
        manip = values[0]
        timeQ = values[2]
        user_input(raw_folder,output_folder,manip, timeQ)
    else:
        quit

def user_input(raw_folder, output_folder, manip, timeQ):     
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
        reorg_excels_and_manip(low_HR, high_HR, low_Cadence, manip, raw_folder, output_folder, timeQ)

    if manip == False:
        reorg_excels_no_manip(manip, raw_folder, output_folder, timeQ)

def reorg_excels_and_manip(low_HR, high_HR, low_Cadence, manip, raw_folder, output_folder, timeQ):
    neg_pow_df = pd.DataFrame()
    path = raw_folder  # where the raw csv files are located
    all_files = glob.glob(os.path.join(path, "*.csv"))  # make a list of paths
    for files in all_files:
        csv_file = os.path.splitext(os.path.basename(files))[
            0]  # get file name without extension
        ext_dic = extract_df(csv_file, raw_folder)
        #-- Extract the dictionary into its variables --#
        HR = ext_dic['HR']
        Cadence = ext_dic['Cadence']
        Power = ext_dic['Power']
        Torque = ext_dic['Torque']
        #--   --#
        subject_data = merge_df(HR, Cadence, Power, Torque, csv_file)
        subject_data = data_manip(subject_data, csv_file, low_HR, high_HR, low_Cadence, manip, output_folder)
        save_excel(subject_data, csv_file, manip, output_folder)
        if timeQ == True:
            data = powerQ(subject_data)
            neg_pow_df = neg_pow_df.append(data)
        # sg.OneLineProgressMeter('One Line Meter Example', files+1, 'key') add progress bar here
        
            # layout = [[sg.Text('Persistent window')],      
            #         [sg.Input(do_not_clear=True)],      
            #         [sg.Button('Read'), sg.Exit()]]      

            # window = sg.Window('Window that stays open', layout)      

            # while True:      
            #     event, values = window.Read()      
            #     if event is None or event == 'Exit':      
            #         break      
            #     print(event, values)    

            # window.Close()
            
        # add window with printout feedback here
        print(csv_file + ".csv reorganized!")
    finished(manip, output_folder, neg_pow_df, timeQ)
 
def reorg_excels_no_manip(manip, raw_folder, output_folder, timeQ):
    neg_pow_df = pd.DataFrame()
    path = raw_folder  # where the raw csv files are located
    all_files = glob.glob(os.path.join(path, "*.csv"))  # make a list of paths

    for files in all_files:
        csv_file = os.path.splitext(os.path.basename(files))[0]  # get file name without extension
        ext_dic = extract_df(csv_file,raw_folder)
        #-- Extract the dictionary into its variables --#
        HR = ext_dic['HR']
        Cadence = ext_dic['Cadence']
        Power = ext_dic['Power']
        Torque = ext_dic['Torque']
        #--   --#
        subject_data = merge_df(HR, Cadence, Power, Torque, csv_file)
        save_excel(subject_data, csv_file, manip, output_folder)
        if timeQ == True:
            data = powerQ(subject_data)
            neg_pow_df = neg_pow_df.append(data)
        print(csv_file + ".csv reorganized!")
    finished(manip, output_folder, neg_pow_df, timeQ)

def powerQ(subject_data):
    time = subject_data[subject_data.Power < 0].shape[0] # time on bike where Power is less than 0
    data = [(subject_data['ID'][1],time)]
    return data

def powerQ_save(neg_pow_df, output_folder, manip):
    if manip == True:
        neg_pow_loc = output_folder + '/' + '[neg_power_manip].xlsx'
    if manip == False:
        neg_pow_loc = output_folder + '/' + '[neg_power_raw].xlsx'
    writer = pd.ExcelWriter(neg_pow_loc)
    neg_pow_df.columns = ['ID', 'Seconds of NegPow']
    neg_pow_df.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.save()
    
def finished(manip, output_folder, neg_pow_df, timeQ):
    if timeQ == True:
        powerQ_save(neg_pow_df, output_folder, manip)
    #### Finished Window with Options ###
    layout = [[sg.Text('Finished! What would you like to do next?')],
                [sg.Radio('Quit', "RADIO1", default=True),
                sg.Radio('Combine Files', "RADIO1"),
                sg.Radio ('Start Over', "RADIO1")],
                [sg.Submit()]]      
    window = sg.Window('File Restructuring Finished!', layout)    

    event, values = window.Read()    
    window.Close()

    if values[0] == True:
        quit
    elif values[1] == True:
        combine_excels(manip, output_folder)
    elif values[2] == True:
        start()

def combine_excels(manip, output_folder):
    path = output_folder
    all_data = pd.DataFrame()
    #--- Convert Dataframe to Excel ---#
    if manip == True:
        for f in glob.glob(os.path.join(path, '*_new.xlsx')):
            df = pd.read_excel(f)
            all_data = all_data.append(df, ignore_index=True)
        all_manip = output_folder + '/' + '[combined_data_manip].xlsx'
        writer = pd.ExcelWriter(all_manip)
        # save without name of columns and the row-numbers
        all_data.to_excel(writer, sheet_name='Sheet1', index=False)
        writer.save()
        ### Finished Notification GUI ###
        layout = [[sg.Text('Finished! Your new file saved as [combined_data_manip].xlsx')],
                    [sg.Radio('Quit', "RADIO1", default=False, size=(10,1)), sg.Radio('Start Over', "RADIO1")],
                    [sg.Submit()]]      
        window = sg.Window('Finished!', layout)
        event, values = window.Read()    
        window.Close()
        
        again = values[0]
        if again == False:
            start()
        else:
            quit
    if manip == False:
        for f in glob.glob(os.path.join(path, '*_new_raw.xlsx')):
            df = pd.read_excel(f)
            all_data = all_data.append(df, ignore_index=True)
        all_manip = output_folder + '/' + '[combined_data_raw].xlsx'
        writer = pd.ExcelWriter(all_manip)
        # save without name of columns and the row-numbers
        all_data.to_excel(writer, sheet_name='Sheet1', index=False)
        writer.save()
        ### Finished Notification GUI ###
        layout = [[sg.Text('Finished! Your new file saved as [combined_data_raw].xlsx')],
                    [sg.Radio('Quit', "RADIO1", default=False, size=(10,1)), sg.Radio('Start Over', "RADIO1")],
                    [sg.Submit()]]      
        window = sg.Window('Finished!', layout)
        event, values = window.Read()
        window.Close()
        
        again = values[0]
        if again == False:
            start()
        else:
            quit

start()
