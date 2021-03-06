import pandas as pd
import numpy as np
from pandas import ExcelWriter
#--- Manipulate an Excel File ---#

def extract_df(csv_file, raw_folder):
    csv_file2 = raw_folder + '/' + csv_file + '.csv'
    # import csv page. Sheetname refers to sheet in file
    sheet = pd.read_csv(csv_file2, delimiter=',')
    sheet.columns = ['Date', 'Time', 'Millitm', 'Marker', 'Tag', 'Status', 'Value'] # remove ; from ;Date
    tag = sheet.set_index(['Tag'])  # set Tag column as the default index    
    # NOTE: use isin to iterate: tag.loc['item one','item two']
    HR = tag.loc['{[CompactLogix]Heart_Rate}'].reset_index(drop=True) # select all rows that have this tag
    HR.rename(columns={'Value': 'HR'}, inplace=True)
    Cadence = tag.loc['{[CompactLogix]Rider_Cadence}'].reset_index(drop=True)
    Cadence.rename(columns={'Value': 'Cadence'}, inplace=True)
    Power = tag.loc['{[CompactLogix]Actual_Power}'].reset_index(drop=True)
    # rename Value column to Power
    Power.rename(columns={'Value': 'Power'}, inplace=True)
    Torque = tag.loc['{[CompactLogix]Actual_Torque}'].reset_index(drop=True)
    Torque.rename(columns={'Value': 'Torque'}, inplace=True)
    ext_dic = {
        'HR': HR,
        'Cadence': Cadence,
        'Power': Power,
        'Torque': Torque
    }
    return ext_dic

def merge_df(HR, Cadence, Power, Torque, csv_file):
    #--- Merge Dataframes ---#
    subject_data = pd.merge(HR,
                            Cadence[['Time', 'Cadence']],
                            on='Time')
    subject_data = pd.merge(subject_data,  # left dataframe to merge to
                            # Right dataframe: select two columns
                            Power[['Time', 'Power']],
                            on='Time')  # merge based on matching "Time" column
    subject_data = pd.merge(subject_data,
                            Torque[['Time', 'Torque']],
                            on='Time')

    # subject_data.insert(0,'Name',csv_file)
    del subject_data['Torque']
    return subject_data


def data_manip(subject_data, csv_file, low_HR, high_HR, low_Cadence, manip, output_folder):
    df = subject_data
    if low_Cadence != 00:
        df = df.drop(df[(df.Cadence <= low_Cadence)].index).reset_index(drop=True)

    ## Replace with NaN ##
    if low_HR !=00:
        df['HR'][df['HR'] <= low_HR] = np.nan
    if high_HR !=00:
        df['HR'][df['HR'] >= high_HR] = np.nan    
    ## ---------------- ##

    nans_made = df['HR'].isna().sum()
    total_rows = df.shape[0]
    perc_nan = round((nans_made/total_rows) * 100, 2)
    subject_data = df

    manip_dic = {
        'subject_data' : df,
        'perc_nan' : perc_nan
        }
    return manip_dic

def save_excel(subject_data, csv_file, manip, output_folder):
    subject_data['ID'] = csv_file
    if manip == True:
        del subject_data['Time']
        del subject_data['Millitm']
        del subject_data['Status']
        del subject_data['Marker']
        csv_file = output_folder + '\\' + csv_file + '_new.xlsx'
        #--- Convert Dataframe to Excel ---#
        writer = ExcelWriter(csv_file)
        # , header=False) #save without name of columns and the row-numbers
        subject_data.to_excel(writer, sheet_name='Sheet1', index=False)
        writer.save()
    if manip == False:
        # does not delete time or millitm columns.
        # NOT GOOD FOR MATLAB
        del subject_data['Status']
        del subject_data['Marker']
        csv_file = output_folder + '\\' + csv_file + '_new_raw.xlsx'
        #--- Convert Dataframe to Excel ---#
        writer = ExcelWriter(csv_file)
        # , header=False) #save without name of columns and the row-numbers
        subject_data.to_excel(writer, sheet_name='Sheet1', index=False)
        writer.save()    
    