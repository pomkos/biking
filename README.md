Combine different excel files, reformat it, and clean data appropriately for eventual usage in SPSS/R.

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
* CSV files must be placed in either "dynamic_files" or "static_files" folder, under the same directory that the python scripts are
* Recommended that CSV files be saved in the form of "subject_id.csv"
* Reformatted CSV files will be saved as XLSX files in the "dynamic_new_files" or "static_new_files" folder as appropriate
* The newly created "combined_sheets.xlsx" contains the merged XLSX files, this can be imported into SPSS/R for data analysis

# Default data manipulation: dynamic settings
By default this script will remove all rows where:
* Power is negative or 0 AND cadence is less than 75
* Minute is 0 AND cadence is less than 75
* Minute is 5 AND cadence is less than 75
* Marker is E OR Marker is B
* Heart Rate is < 40 OR > 150

# Default data manipulation: static settings
By default this script will remove all rows where:
* Power is negative or 0 AND cadence is less than 75
* Minute is 0 AND cadence is less than 40
* Minute is 5 AND cadence is less than 40
* Marker is E OR Marker is B
* Heart Rate is < 40 OR > 200

These criteria indicate that the bike is just powering up/down. By default the script will also remove heart rate values that are less than or greater than certain values (but leaves the row intact), indicating a malfunction of the heart rate monitor.

# Output

## Before (raw):
![alt text](https://github.com/pomkos/biking/blob/master/before.png)

## After:
![alt text](https://github.com/pomkos/biking/blob/master/after.png)

## Combined files:
![alt text](https://github.com/pomkos/biking/blob/master/combined.png)
