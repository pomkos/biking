Combine different excel files and reformat them appropriately, for eventual usage in SPSS/R.

# How to

Prereqs:
```
pip install -r requirements.txt
```
To start the script:
```
pip start_biking.py
```
# Notes
* CSV files must be placed in a "files" folder, under the same directory that the python scripts are
* Recommended that CSV files be saved in the form of "subject_id.csv"
* Reformatted CSV files will be saved as XLSX files in the new_files folder
* The newly created "combined_sheets.xlsx" contains the merged XLSX files, this can be imported into SPSS/R for data analysis
