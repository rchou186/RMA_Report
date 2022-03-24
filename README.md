RMA reporting program

This program shows DCD chart and Wh chart of both BEFORE (IPQC) and AFTER
(TEST). Inputs the battery SN to get IPQC and TEST data from SQL server and
csv raw data directories.

This program generate the following output result folders and files:
  1. Folder Tyymddxxxx       The folder of the RMA battery SN, all the
                             following result files will be in this folder
  2. Folder JxxQxxxxx        IPQC csv raw data (BEFORE data)
  3. Folder JxxTxxxxx        TEST csv raw data (AFTER data)
  3. JxxQxxxxx.xlsx          IPQC DCD table
  4. JxxQxxxxx_DCD.html      IPQC DCD chart of 34 modules
  5. JxxQxxxxx_Wh.html       IPQC Wh bar graph chart of 34 modules
  6. JxxTxxxxx.xlsx          TEST DCD table
  7. JxxTxxxxx_DCD.html      TEST DCD chart of 34 modules
  8. JXXTXXXXX_Wh.html       TEST Wh bar graph chart of 34 modules
  9. Tyymddxxxx.xlsx         DCD table of both IPQC and TEST together
 10. Tyymddxxxx_DCD.html     DCD chart of both IPQC and TEST
 11. Tyymddxxxx_Wh.html      Wh bar graph of both IPQC and TEST

The files contained in this program:

RMA_Report.py       Main program to call IPQC_Rebuild and TEST_Build and 
                    generate the combined excel and html files 
IPQC_Rebuild.py     Program to collect IPQC data from SQL and raw data
                    directory and generate correcponding excel and html files
TEST_Build.py       Program to collect TEST data from SQL and raw data
                    directory and generate correcponding excel and html files
README.md           This file

Python modules to be installed:
pandas, openpyxl, plotly, mysql_connector, 
pyinstaller

Versions:

V22.0314.01
Date: 2022/03/14
 1. Initial Release
 
 V22.0321.01
Date: 2022/03/21
 1. Add DCD comparision chart and Wh comparision chart of both BEFORE and AFTER

 V22.0334.01
Date: 2022/03/24
 1. Fix the bug in Windows directory, need to remove the "/Battery Test Data "