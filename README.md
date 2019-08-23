Combine different excel files, reformat it, and clean data appropriately for eventual usage in SPSS/R!

# Features:

* Use GUI to designate input/output folders, customize settings
* Option to clean data by designating Cadence and HR limits
* Option to obtain how many seconds participants were in negative power
* Option to merge all new bike files into one excel sheet, for SPSS analysis
* Reorganizes all raw bike files into a readable format
* Reorganized files are ready to use with MatLab analysis

# To Do:

* Static GUI
* One GUI for all options
* Immediate basic statistical analysis
* Entropy analysis, possibly via MatLab

# How to

## Start the script:

Install all requirements
```
pip install -r requirements.txt
```
Then start the script
```
python start_biking.py
```
## Compile using pyinstaller
### Automatic:
Run pyinstaller on the .spec file.
```
pyinstaller start_biking.spec -wF
```

### Manual:
```
pyinstaller start_biking.py -wF
```
Pyinstaller does not compile pandas in full, the .exe will not work. Edit the start_sbiking.spec and add the following AFTER "block_cipher = None":
```
def get_pandas_path():
    import pandas
    pandas_path = pandas.__path__[0]
    return pandas_path
```
Then add the following BEFORE "pyz = PYZ(a.pure, a.zipped_data,":
```
dict_tree = Tree(get_pandas_path(), prefix='pandas', excludes=["*.pyc"])
a.datas += dict_tree
a.binaries = filter(lambda x: 'pandas' not in x[0], a.binaries)
```
As of Numpy 1.16.0 you also need to modify:
```
hiddenimports=['numpy.core._dtype_ctypes']
```

And then recompile:
```
pyinstaller start_biking.spec -wF
```

# Output

## Before (raw):
![alt text](https://github.com/pomkos/biking/blob/master/before.png)

## After:
![alt text](https://github.com/pomkos/biking/blob/master/after.png)

## Matlab Analysis:
![alt text](https://github.com/pomkos/biking/blob/master/matlab.png)
