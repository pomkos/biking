from biking import extract_df
import pandas as pd
import glob
import os

#--- Options ---#

# csv_file = "Bryan44" #name of csv file from the bike

#---------------#


def reorg_excels():
    path = '/new_files'  # where the csv files are located
    all_files = glob.glob(os.path.join(path, "*.xlsx"))  # make a list of paths

    for files in all_files:
        csv_file = os.path.splitext(os.path.basename(files))[
            0]  # get file name without extension
        extract_df(csv_file)


def combine_excels():
    dataframes = []
    path2 = 'new_files'
    new_files = glob.glob(os.path.join(path2, "*.xlsx"))
    print(new_files)
    # dataframes.append(new_files)
    for f in new_files:
        data = pd.read_excel(f, 'Sheet1').iloc[:-2]
        data.index = [os.path.basename(f)] * len(data)
        dataframes.append(data)

    df = pd.concat(dataframes)
    print(df)


combine_excels()
