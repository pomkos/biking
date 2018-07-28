from biking import extract_df

#--- Options ---#

name_data = 'Alaina' #Name of subject
AV = '11' #Acceleration/Velocity settings
csv_file = "Alaina11.xlsx" #name of csv file from the bike
output = "Alaina11_new.xlsx"#name for new, reorganized file

#---------------#

extract_df(name_data, AV, csv_file, output)
