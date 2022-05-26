## RMA reporting program
***
This program shows DCD chart and Wh chart of both BEFORE (IPQC) and AFTER (TEST). Inputs the battery SN to get IPQC and TEST data from SQL server and csv raw data directories.

This program generate the following output result folders and files:

|File                    |Description                                                                            |
|------------------------|---------------------------------------------------------------------------------------|
|1. Folder Tyymddxxxx    |The folder of the RMA battery SN, all the following result files will be in this folder|
|2. Folder JxxQxxxxx     |IPQC csv raw data (BEFORE data)                                                        |
|3. Folder JxxTxxxxx     |TEST csv raw data (AFTER data)                                                         |
|4. JxxQxxxxx.xlsx       |IPQC DCD table                                                                         |
|5. JxxQxxxxx_DCD.html   |IPQC DCD chart of 34 modules                                                           |
|6. JxxQxxxxx_Wh.html    |IPQC Wh bar graph chart of 34 modules                                                  |
|7. JxxTxxxxx.xlsx       |TEST DCD table                                                                         |
|8. JxxTxxxxx_DCD.html   |TEST DCD chart of 34 modules                                                           |
|9. JXXTXXXXX_Wh.html    |TEST Wh bar graph chart of 34 modules                                                  |
|10. Tyymddxxxx.xlsx     |DCD table of both IPQC and TEST together                                               |
|11. Tyymddxxxx_DCD.html |DCD chart of both IPQC and TEST                                                        |
|12. Tyymddxxxx_Wh.html  |Wh bar graph of both IPQC and TEST                                                     |

***

The files contained in this program:

|File           |Description                                                                                                  |
|---------------|-------------------------------------------------------------------------------------------------------------|     
|RMA_Report.py  |Main program to call IPQC_Rebuild and TEST_Build and generate the combined excel and html files              |
|IPQC_Rebuild.py|Program to collect IPQC data from SQL and raw data directory and generate correcponding excel and html files |
|TEST_Build.py  |Program to collect TEST data from SQL and raw data directory and generate correcponding excel and html files |
|README.md      |This file                                                                                                    |

Python modules to be installed:

pandas, openpyxl, plotly, mysql_connector, pyinstaller

### Versions:

V22.0314.01 Date: 2022/03/14

 1. Initial Release

V22.0321.01 Date: 2022/03/21

 1. Add DCD comparision chart and Wh comparision chart of both BEFORE and AFTER

V22.0334.01 Date: 2022/03/24

 1. Fix the bug in Windows directory, need to remove the "/Battery Test Data"

V22.0511.01 Date: 2022/05/11

 1. Change the raw data path in /ChiBackup/Grading Test/
 2. Add *.csv and *.xlsx in .gitignore
 3. Change this README.md file into markdown format

V22.0526.01 Date: 2022/05/26
 1. Add color_map for DCD curve in IPQC_Rebuild, TEST_Build, and RMA_Report