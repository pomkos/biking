import pandas as pd
from pandas import ExcelWriter

#--- Options ---#
name = 'Alaina'
AV = '11'
excel_file = "Alaina11.xlsx"
output = "bike_data.xlsx"


#--- Manipulate an Excel File ---#
def extract_df(name, AV, excel_file, output):
    writer = ExcelWriter(output)
    sheet = pd.read_excel(excel_file, sheet_name=0,) #sheetname refers to sheet in file
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

    merge_df(Power, Torque, HR, Minute, Second, Cadence, writer)

def merge_df(*args):
    #--- Merge Dataframes ---#
    #dfs=[Power,Torque,HR,Minute,Second,Cadence]
    bigdata = pd.merge(args[1],
                    args[2][['Time','Torque']],
                    on='Time')
    bigdata = pd.merge(bigdata, #left dataframe to merge to
                    args[3][['Time','Heart Rate']], #Right dataframe: select two columns 
                    on='Time') #merge based on matching "Time" column
    bigdata = pd.merge(bigdata,
                    args[4][['Time','Minute']],
                    on='Time')
    bigdata = pd.merge(bigdata,
                    args[5][['Time','Second']],
                    on='Time')
    bigdata = pd.merge(bigdata,
                    args[6][['Time','Cadence']],
                    on='Time')

    bigdata.insert(0,'Name',name)
    bigdata.insert(1,'AV',AV)

    save_excel(bigdata, args[7])

def save_excel(*args):
    #--- Convert Dataframe to Excel ---#
    args[1].to_excel(args[2],sheet_name=name)
    args[2].save()