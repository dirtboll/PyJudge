# PyJudge
Offline gradder helper for SDA using Python 3. For online gradder, visit [alghijudge](https://alghijudge-2020.herokuapp.com/).

## Installation
Clone this repo.
```
git clone https://github.com/dirtboll/PyJudge
cd PyJudge
```
Install requirements.
```
python3 -m pip install -r requirements.txt
#or
pip3 install -r requirements.txt
```
## Usage
```
pyjudge.py [-h] [-t THREADS] javaFile testCaseDir

positional arguments:
  javaFile              Java source code file.
  testCaseDir           Test Case directory. Format test case file: in<i> and out<i>. (e.g. in4 and out4)

optional arguments:
  -h, --help            show this help message and exit
  -t THREADS, --threads THREADS
                        Number of threads to use.
```
Example  
```
# Root directory
# │  tp.java
# │  pyjudge.py
# └─ tc  
#    │  in1  
#    │  in2  
#    │  out1  
#    │  out2  

$ python3 pyjudge.py -t 8 tp.java tc
  TC1: AC |  30.21MB 0.097s | 
  TC2: AC |  30.26MB 0.099s | 
```
## Contribute
1. Clone this repo. 
2. Apply changes.
3. Commit and submit pull request.
4. PM if owner doesn't respond. (line: testaforastuff)

###### Goodluck q(≧▽≦q)