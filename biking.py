import pandas as pd
from pandas import ExcelWriter

# name = 'Alaina' #Name of subject
# AV = '11' #Acceleration/Velocity settings
# csv_file = "Alaina11.xlsx" #name of csv file from the bike
# output = "Alaina11_new.xlsx"#name for new, reorganized file

#--- Manipulate an Excel File ---#
def extract_df(name, AV, csv_file, output):
    sheet = pd.read_excel(csv_file, sheet_name=0,) #sheetname refers to sheet in file
    tag = sheet.set_index(['Tag']) #set Tag column as the default index

    # NOTE: use isin to iterate: tag.loc['item one','item two']
    Power = tag.loc['{[CompactLogix]Actual_Power}'].set_index(';Date') #select all rows that have this tag
    Power.rename(columns={'Value':'Power'}, inplace=True) #rename Value column to Power
    Torque = tag.loc['{[CompactLogix]Actual_Torque}'].set_index(';Date')
    Torque.rename(columns={'Value':'Torque'}, inplace=True)
    HR = tag.loc['{[CompactLogix]Heart_Rate}'].set_index(';Date')
    HR.rename(columns={'Value':'Heart Rate'}, inplace=True)
    Minute = tag.loc['{[CompactLogix]Minute_Counter}'].set_index(';Date')
    Minute.rename(columns={'Value':'Minute'}, inplace=True)
    Second = tag.loc['{[CompactLogix]Second_Counter}'].set_index(';Date')
    Second.rename(columns={'Value':'Second'}, inplace=True)
    Cadence = tag.loc['{[CompactLogix]Rider_Cadence}'].set_index(';Date')
    Cadence.rename(columns={'Value':'Cadence'}, inplace=True)

    merge_df(name, AV, Power, Torque, HR, Minute, Second, Cadence, output)

def merge_df(name, AV, Power, Torque, HR, Minute, Second, Cadence, output):
    #--- Merge Dataframes ---#
    #dfs=[Power,Torque,HR,Minute,Second,Cadence]
    name_data = pd.merge(Power,
                    Torque[['Time','Torque']],
                    on='Time')
    name_data = pd.merge(name_data, #left dataframe to merge to
                    HR[['Time','Heart Rate']], #Right dataframe: select two columns 
                    on='Time') #merge based on matching "Time" column
    name_data = pd.merge(name_data,
                    Minute[['Time','Minute']],
                    on='Time')
    name_data = pd.merge(name_data,
                    Second[['Time','Second']],
                    on='Time')
    name_data = pd.merge(name_data,
                    Cadence[['Time','Cadence']],
                    on='Time')

    name_data.insert(0,'Name',name)
    name_data.insert(1,'AV',AV)

    save_excel(name_data, output, name)

def save_excel(name_data, output, name):
    #--- Convert Dataframe to Excel ---#
    writer = ExcelWriter(output)
    name_data.to_excel(writer,sheet_name=name)
    writer.save()