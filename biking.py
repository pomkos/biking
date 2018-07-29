import pandas as pd
from pandas import ExcelWriter

#--- Manipulate an Excel File ---#
def extract_df(csv_file):
    csv_file2 = 'files\\' + csv_file + '.csv'
    sheet = pd.read_csv(csv_file2, delimiter=',') #import excel page. Sheetname refers to sheet in file
    tag = sheet.set_index(['Tag']) #set Tag column as the default index

    # NOTE: use isin to iterate: tag.loc['item one','item two']
    Power = tag.loc['{[CompactLogix]Actual_Power}'].set_index(';Date') #select all rows that have this tag
    Power.rename(columns={'Value':'Power'}, inplace=True) #rename Value column to Power
    Torque = tag.loc['{[CompactLogix]Actual_Torque}'].set_index(';Date')
    Torque.rename(columns={'Value':'Torque'}, inplace=True)
    HR = tag.loc['{[CompactLogix]Heart_Rate}'].set_index(';Date')
    HR.rename(columns={'Value':'HR'}, inplace=True)
    Minute = tag.loc['{[CompactLogix]Minute_Counter}'].set_index(';Date')
    Minute.rename(columns={'Value':'Minute'}, inplace=True)
    Second = tag.loc['{[CompactLogix]Second_Counter}'].set_index(';Date')
    Second.rename(columns={'Value':'Second'}, inplace=True)
    Cadence = tag.loc['{[CompactLogix]Rider_Cadence}'].set_index(';Date')
    Cadence.rename(columns={'Value':'Cadence'}, inplace=True)

    merge_df(Power, Torque, HR, Minute, Second, Cadence, csv_file)

def merge_df(Power, Torque, HR, Minute, Second, Cadence, csv_file):
    #--- Merge Dataframes ---#
    #dfs=[Power,Torque,HR,Minute,Second,Cadence]
    subject_data = pd.merge(Power,
                    Torque[['Time','Torque']],
                    on='Time')
    subject_data = pd.merge(subject_data, #left dataframe to merge to
                    HR[['Time','HR']], #Right dataframe: select two columns 
                    on='Time') #merge based on matching "Time" column
    subject_data = pd.merge(subject_data,
                    Minute[['Time','Minute']],
                    on='Time')
    subject_data = pd.merge(subject_data,
                    Second[['Time','Second']],
                    on='Time')
    subject_data = pd.merge(subject_data,
                    Cadence[['Time','Cadence']],
                    on='Time')

    subject_data.insert(0,'Name',csv_file)

    data_manip(subject_data, csv_file)

def data_manip(subject_data, csv_file):
    df = subject_data
    df = df.drop(df[(df.Power <= 0) & (df.Cadence < 75)].index)
    df = df.drop(df[(df.Marker == 'E') | (df.Marker == 'B')].index)
    df = df.drop(df[(df.Minute == 0) & (df.Cadence <= 75)].index)
    df = df.drop(df[(df.Minute == 5) & (df.Cadence <= 75)].index)
    subject_data = df
    save_excel(subject_data, csv_file)

def save_excel(subject_data, csv_file):
    csv_file = 'new_files\\' + csv_file + '_new.xlsx'
    #--- Convert Dataframe to Excel ---#
    writer = ExcelWriter(csv_file)
    subject_data.to_excel(writer,sheet_name='Sheet1')
    writer.save()