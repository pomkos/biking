import pandas as pd
import numpy as np
import glob
import os
import nolds #sampen calc

from pandas import ExcelWriter
import PySimpleGUI as sg      


# Logic: create a dictionary of averages from file, then append that dictionary to df2. Do this for all files
# Columns are made from the keys, data from the values of the dictionary

def df_avg(output_folder, manip, ent_yes):
    if manip == True:
        file_list = glob.glob(os.path.join(output_folder, "*_new.xlsx"))  # make a list of paths
    elif manip == False:
        file_list = glob.glob(os.path.join(output_folder, "*_new_raw.xlsx"))
    df = []
    cols = ['ID', 'avg_HR', 'std_HR', 'SamEn_HR','avg_Cad', 'std_Cad', 'SamEn_Cad','avg_Pow', 'std_Pow', 'SamEn_Pow','neg_Pow', 'HR_NaN', 'Length']
    i = 1
    window = progressGUI(output_folder)
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
                
                seconds = neg_Pow_count(file)

                sampEn_HR = round(nolds.sampen(file['HR']),2)
                sampEn_Cad = round(nolds.sampen(file['Cadence']),2)
                sampEn_Pow = round(nolds.sampen(file['Power']),2)

                df.append({'ID':file_id, 
                            'avg_HR':means['HR'],
                            'std_HR':stds['HR'],
                            'Sam_HR':sampEn_HR,
                            'avg_Cad':means['Cadence'],
                            'std_Cad':stds['Cadence'],
                            'Sam_Cad':sampEn_Cad, 
                            'avg_Pow':means['Power'],
                            'std_Pow':stds['Power'],
                            'Sam_Pow':sampEn_Pow,
                            'neg_Pow':seconds, 
                            'Length':file_length,
                            'HR_NaN':is_nan['HR'] 
                            #'Cad_NaN':is_nan['Cadence'],
                            #'Pow_NaN':is_nan['Power']
                            })

                #-- Updates the progress bar --#
                event, values = window.Read(timeout=0)
                print(file_id, ' analyzed')
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
        avgs_save(df, output_folder, window,manip, ent_yes)
        window.Close()
    print('Finished!')

def entropy_matlab(res, cad, output_folder):
    import matlab.engine as mat

    res = res # resistance setting used
    cad = cad # cadence setting used
    root = os.path.dirname(os.path.realpath(__file__)) # directory of matlab files

    eng = mat.start_matlab() # starts the matlab engine
    answer = eng.apsamen_cleaned(res, cad, root, output_folder, nargout=0) # calls the apsamen_cleaned.m file's function
    print(answer) # prints everything out, because of nargout=0 argument

def neg_Pow_count(file):
    time = file[file.Power < 0].shape[0] # time on bike where Power is less than 0
    return time

def avgs_save(df, output_folder, window,manip, ent_yes):
    if manip == True:
        print('Saving [basic_stats].xlsx file')
        event, values = window.Read(timeout=0)
        save_file = output_folder + '\\' + '[basic_stats].xlsx'
        writer = pd.ExcelWriter(save_file)
        df.to_excel(writer, sheet_name='Sheet1', index=False)
        writer.save()
        print('[basic_stats].xlsx saved')
    elif manip == False:
        print('Saving [basic_stats_raw].xlsx file')
        event, values = window.Read(timeout=0)
        save_file = output_folder + '\\' + '[basic_stats_raw].xlsx'
        writer = pd.ExcelWriter(save_file)
        df.to_excel(writer, sheet_name='Sheet1', index=False)
        writer.save()
        print('[basic_stats_raw].xlsx saved')

    if ent_yes == True:
        layout = [[sg.Text('What was the resistance setting?')],
            [sg.Input()], # 0
            [sg.Text('What was the cadence setting?')],
            [sg.Input()], # 1
            [sg.Output(size=(60,20))],
            [sg.Button('Submit')]
            ]    
        window = sg.Window('Entropy Analysis Options!', layout)    
        event, values = window.Read()  

        res = values[0]
        cad = values[1]

        entropy_matlab(res,cad,output_folder)

    elif ent_yes == False:
        finished(manip)

def finished(manip):
    if manip == True:
        layout = [[sg.Popup('Finished! The file has been saved as [basic_stats].xlsx')],
                    [sg.Button('OK')]]      
        window = sg.Window('Statistical Analysis Finished!', layout)    
        event, values = window.Read()   
    elif manip == False:
        layout = [[sg.Popup('Finished! The file has been saved as [basic_stats_raw].xlsx')],
        [sg.Button('OK')]]      
        window = sg.Window('Statistical Analysis Finished!', layout)    
        event, values = window.Read()  
    if event == 'OK':
        return
    window.Close()

def progressGUI(output_folder):
    count = len([name for name in os.listdir(output_folder) if os.path.isfile(os.path.join(output_folder, name))])
    layout = [[sg.Text('Press start to begin')],
            [sg.ProgressBar(count, orientation='h', size=(20, 20), key='progbar')],
            [sg.Output(size=(60,20))],
            [sg.Button('Start'),
            sg.Button('Quit')],
            ]
    window = sg.Window('Begin Restructuring and Cleaning', layout)
    return window