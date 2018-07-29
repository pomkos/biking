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

# Default data manipulation
By default this script will remove all rows where:
* Power is negative or 0 AND cadence is less than 75
* Minute is 0 AND cadence is less than 75
* Minute is 5 AND cadence is less than 75
* Marker is E OR Marker is B

These criteria indicate that the bike is just powering up/down. By default the script will also remove heart rate values that are less than 50 or greater than 200 (but leaves the row intact), indicating a malfunction of the heart rate monitor.

# Output

Before:
![alt text](https://github.com/pomkos/biking/blob/master/before.png)

After:
![alt text](https://github.com/pomkos/biking/blob/master/after.png)

Combined files:
![alt text](https://github.com/pomkos/biking/blob/master/combined.png)
