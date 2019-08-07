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

    i = 1
    window = progressGUI(raw_folder)
    while True:
        for x in file_list:
            i = i+1
            try:
                file = pd.read_excel(x)
                file_id = file.loc[0,'ID']
                hr_mean = round(np.mean(file['HR']),2)
                cad_mean = round(np.mean(file['Cadence']),2)
                pow_mean = round(np.mean(file['Power']),2)
                print(file_id)
                df.append({'ID':file_id, 'avg_HR':hr_mean, 'avg_Cad':cad_mean, 'avg_Pow':pow_mean})

                # Updates the progress bar #
                event, values = window.Read(timeout=0)
                if event == 'Cancel' or event is None:
                    break
                window.Element('progbar').UpdateBar(i)
                #--    --#
            except Exception as e:
                print(file_id, ': ',e)
        df = pd.DataFrame(df)
        avgs_save(df, output_folder, window)

def avgs_save(df, output_folder, window):
    print('Saving [averages].xlsx file')
    event, values = window.Read(timeout=0)
    save_file = output_folder + '\\' + '[averages].xlsx'
    writer = pd.ExcelWriter(save_file)
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.save()
    print('[averages].xlsx saved')

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