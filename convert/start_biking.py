from dynamic_bike import extract_df, merge_df, data_manip, save_excel

import pandas as pd
from pandas import ExcelWriter
import glob
import os
import sys
import PySimpleGUI as sg      

def start():
    event, values = sg.Window('Choice').Layout([[sg.Text('What would you like to do?')],
                                                [sg.Radio('Reorganize Raw Files', 'RADIO1', default=True),
                                                sg.Radio('Combine New Files', 'RADIO1')],
                                                [sg.CloseButton('Submit')]]).Read()
    window = sg.Window('Bike Data Tool')
    window.Close()
    if values[0] == True:
        ## Define input and output folders
        event, values = sg.Window('Bike Data Tool').Layout([[sg.Text('Input folder')],
                                                            [sg.In(), sg.FolderBrowse()], #0
                                                            [sg.Text('Output folder')],
                                                            [sg.In(), sg.FolderBrowse()], #1
                                                            [sg.Text('Would you like to clean your data?')],      
                                                            [sg.Radio('Yes', "RADIO1", default=True), #2
                                                            sg.Radio('No', "RADIO1")],#3
                                                            [sg.Text('Would you like to count the number of lines with Power < 0?')],
                                                            [sg.Radio('Yes', "RADIO2", default=True), #4
                                                            sg.Radio('No', "RADIO2")],#5
                                                            [sg.CloseButton('Submit'), sg.CloseButton('Cancel')]]).Read()
        window = sg.Window('Bike Data Tool')    
        window.Close()
        if event == 'Submit':
            # raw_folder = values[0]
            raw_folder = 'C:\\Users\\albei\\OneDrive\\Desktop\\analyze\\input'
            # output_folder=values[1]
            output_folder = 'C:\\Users\\albei\\OneDrive\\Desktop\\analyze\\output'
            manip = values[2]
            timeQ = values[4]
            user_input(raw_folder,output_folder,manip, timeQ)
        else:
            quit
    elif values[1] == True:
        ## Define input and output folders
        event, values = sg.Window('Bike Data Combining Tool').Layout([[sg.Text('Which folder are the files in?')],
                                                            [sg.In(), sg.FolderBrowse()], #0
                                                            [sg.Text('Has the data been cleaned?')],      
                                                            [sg.Radio('Yes', "RADIO1", default=True), #1
                                                            sg.Radio('No', "RADIO1")],#2
                                                            [sg.CloseButton('Submit'), sg.CloseButton('Cancel')]]).Read()
        window = sg.Window('Bike Data Combining Tool')    
        window.Close()

        output_folder = values[0]
        manip = values[1]
        if event == 'Submit':
            combine_excels(manip, output_folder)
        if event == 'Cancel':
            raise SystemError(0)

def progressGUI(raw_folder):
    count = len([name for name in os.listdir(raw_folder) if os.path.isfile(os.path.join(raw_folder, name))])
    layout = [[sg.Text('Press start to begin')],
            [sg.ProgressBar(count, orientation='h', size=(20, 20), key='progbar')],
            [sg.Output(size=(60,20))],
            [sg.Button('Start'),
            sg.Button('Quit')],
            ]
    window = sg.Window('Begin Restructuring and Cleaning', layout)
    return window
def user_input(raw_folder, output_folder, manip, timeQ):     
    if manip == True:
    ### Info Gather GUI ###
        layout = [      
            [sg.Text('Replace all HR with "NaN" if they are <:', size=(30, 1)), sg.InputText()],      
            [sg.Text('Replace all HR with "NaN" if they are >:', size=(30, 1)), sg.InputText()],      
            [sg.Text('All rows will be deleted if the Cadence there is less than:', size=(30, 2)), sg.InputText()],      
            [sg.Submit(), sg.Cancel()]]      
        window = sg.Window('Data Cleaning', layout)  
        event, values = window.Read()   
        window.Close()
        if event == 'Submit':
            low_HR = int(values[0])
            high_HR = int(values[1])
            low_Cadence = int(values[2])
        ### Confirmation GUI still needed ###
            reorg_excels_and_manip(low_HR, high_HR, low_Cadence, manip, raw_folder, output_folder, timeQ)
        else:
            raise SystemError(0)
    if manip == False:
        reorg_excels_no_manip(manip, raw_folder, output_folder, timeQ)

def reorg_excels_and_manip(low_HR, high_HR, low_Cadence, manip, raw_folder, output_folder, timeQ):
    neg_pow_df = pd.DataFrame()
    path = raw_folder  # where the raw csv files are located
    all_files = glob.glob(os.path.join(path, "*.csv"))  # make a list of paths
    
    # Progress bar window #
    i = 1
    window = progressGUI(raw_folder)
    #--   --#
    while True:
        event,values = window.Read()
        if event == 'Start' or None:
            for files in all_files:
                i = i+1
                try:
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
                    manip_dic = data_manip(subject_data, csv_file, low_HR, high_HR, low_Cadence, manip, output_folder)

                    subject_data = manip_dic['subject_data']

                    perc_nan = manip_dic['perc_nan']
                    if perc_nan > 0:
                        print(perc_nan,"% of HR values have been replaced with 'NaN' in ", csv_file)
                    save_excel(subject_data, csv_file, manip, output_folder)
                    if timeQ == True:
                        data = powerQ(subject_data)
                        neg_pow_df = neg_pow_df.append(data)

                    # Updates the progress bar #
                    event, values = window.Read(timeout=0)
                    if event == 'Cancel' or event is None:
                        break
                    window.Element('progbar').UpdateBar(i)
                    #--    --#
                    print(csv_file + ".csv reorganized!")
                except Exception as e:
                    csv_file = os.path.splitext(os.path.basename(files))[0]
                    print('___________________________________')
                    print('ERROR:', e)
                    print('There is a problem with ', csv_file, '.csv')
                    print('___________________________________')
                    print(' ')
                    window.Element('progbar').UpdateBar(i)
        
            finished(manip, output_folder, neg_pow_df, timeQ)
        elif event == 'Quit':
            raise SystemError(0)

def reorg_excels_no_manip(manip, raw_folder, output_folder, timeQ):
    neg_pow_df = pd.DataFrame()
    path = raw_folder  # where the raw csv files are located
    all_files = glob.glob(os.path.join(path, "*.csv"))  # make a list of paths
    
    # Progress bar window #
    i = 1
    window = progressGUI(raw_folder)
    #--   --#
    while True:
        event,values = window.Read()
        if event == 'Start' or None:
            for files in all_files:
                i = i+1
                try:
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
                    
                    # Update the progress bar #
                    event, values = window.Read(timeout=0)
                    if event == 'Cancel' or event is None:
                        break
                    window.Element('progbar').UpdateBar(i)
                    #--   --#
                    print(csv_file + ".csv reorganized!")
                except Exception as e:
                    csv_file = os.path.splitext(os.path.basename(files))[0]
                    print('___________________________________')
                    print('ERROR:', e)
                    print('There is a problem with ', csv_file, '.csv')
                    print('___________________________________')
                    print(' ')
                    window.Element('progbar').UpdateBar(i)

            finished(manip, output_folder, neg_pow_df, timeQ)
        elif event == 'Quit':
            raise SystemError(0)

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
        raise SystemError(0)
    elif values[1] == True:
        combine_excels(manip, output_folder)
    elif values[2] == True:
        start()

def combine_excels(manip, output_folder):
    path = output_folder
    all_data = pd.DataFrame()
    #--- Convert Dataframe to Excel ---#   
    while True:
        if manip == True:
            for f in glob.glob(os.path.join(path, '*_new.xlsx')):
                try:
                    df = pd.read_excel(f)
                    all_data = all_data.append(df, ignore_index=True)
                except:
                    print('There is a problem with ',f)
            all_manip = output_folder + '/' + '[combined_data_manip].xlsx'
            writer = pd.ExcelWriter(all_manip)
            # save without name of columns and the row-numbers
            all_data.to_excel(writer, sheet_name='Sheet1', index=False)
            writer.save()
            ### Finished Notification GUI ###
            layout = [[sg.Text('Finished! Your new file is saved as [combined_data_manip].xlsx')],
                        [sg.Radio('Quit', "RADIO1", default=True, size=(10,1)), sg.Radio('Start Over', "RADIO1")],
                        [sg.Submit()]]      
            window = sg.Window('Finished!', layout)
            event, values = window.Read()    
            window.Close()
            
            again = values[0]
            if again == False:
                start()
            else:
                raise SystemError(0)
        if manip == False:
            for f in glob.glob(os.path.join(path, '*_new_raw.xlsx')):
                try:
                    df = pd.read_excel(f)
                    all_data = all_data.append(df, ignore_index=True)
                except:
                    print('There is a problem with ',f)
            all_manip = output_folder + '/' + '[combined_data_raw].xlsx'
            writer = pd.ExcelWriter(all_manip)
            # save without name of columns and the row-numbers
            all_data.to_excel(writer, sheet_name='Sheet1', index=False)
            writer.save()
            ### Finished Notification GUI ###
            layout = [[sg.Text('Finished! Your new file is saved as [combined_data_raw].xlsx')],
                        [sg.Radio('Quit', "RADIO1", default=True, size=(10,1)), sg.Radio('Start Over', "RADIO1")],
                        [sg.Submit()]]      
            window = sg.Window('Finished!', layout)
            event, values = window.Read()
            window.Close()
            
            again = values[0]
            if again == False:
                start()
            else:
                raise SystemError(0)

start()