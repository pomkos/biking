import pandas as pd
import numpy as np
import glob
import os

from pandas import ExcelWriter
import PySimpleGUI as sg      


# Logic: create a dictionary of averages from file, then append that dictionary to df2. Do this for all files
# Columns are made from the keys, data from the values of the dictionary

def df_avg(raw_folder, output_folder):
    file_list = glob.glob(os.path.join(raw_folder, "*_new.xlsx"))  # make a list of paths
    df = []
    cols = ['ID', 'avg_HR', 'std_HR', 'avg_Cad', 'std_Cad', 'avg_Pow', 'std_Pow', 'HR_NaN', 'Cad_NaN', 'Pow_NaN', 'Length']
    i = 1
    window = progressGUI(raw_folder)
    while True:
        for x in file_list:
            i = i+1
            try:
                file = pd.read_excel(x)
                file_id = file.loc[0,'ID']

                means = round(np.mean(file),2) # Mean for each column
                stds = round(np.std(file),2)   # Standard deviation for each column
                file_length = file.shape[0]
                is_nan = file.isna().sum() # Number of NaN values for each column

                print(file_id, ' analyzed')
                df.append({'ID':file_id, 
                            'avg_HR':means['HR'],
                            'std_HR':stds['HR'],
                            'avg_Cad':means['Cadence'],
                            'std_Cad':stds['Cadence'], 
                            'avg_Pow':means['Power'],
                            'std_Pow':stds['Power'], 
                            'Length':file_length,
                            'HR_NaN':is_nan['HR'] 
                            #'Cad_NaN':is_nan['Cadence'],
                            #'Pow_NaN':is_nan['Power']
                            })

                #-- Updates the progress bar --#
                event, values = window.Read(timeout=0)
                if event == 'Cancel' or event is None:
                    break
                window.Element('progbar').UpdateBar(i)
                #------------------------------#
            except Exception as e:
                print(file_id, ': ',e)
        
        df = pd.DataFrame(df,columns=cols)

        #-- Add Mean and Std to end of each columns --#
        df.loc['Mean'] = round(np.mean(df),2)
        df.loc['Std'] = round(np.std(df),2)
        df.loc['Mean','ID'] = 'Mean'
        df.loc['Std','ID'] = 'Std'
        #---------------------------------------------#
        avgs_save(df, output_folder, window)
        window.Close()
    print('Finished!')

def avgs_save(df, output_folder, window):
    print('Saving [basic_stats].xlsx file')
    event, values = window.Read(timeout=0)
    save_file = output_folder + '\\' + '[basic_stats].xlsx'
    writer = pd.ExcelWriter(save_file)
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.save()
    print('[basic_stats].xlsx saved')
    finished()

def finished():
    layout = [[sg.Popup('Finished! The file has been saved [basic_stats].xlsx')],
                [sg.Button('OK')]]      
    window = sg.Window('Statistical Analysis Finished!', layout)    
    event, values = window.Read()   

    if event == 'OK':
        raise SystemError(0)
    window.Close()

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