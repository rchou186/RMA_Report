This RMA_Report program collects and generates the BEFORE and AFTER data from
MySQL database. Enter the desired battery SN to find the IPQC number and TEST
number as well.

This program generate the following output directory and result files:
  1. Directory Txxxxxxxx/    The folder to put result files of IPQC and TEST 
                             table and chart
  2. Directory JxxQxxxxx/    Under the 1. Directory, this folder stores the 
                             original CSV files from IPQC number (BEFORE)
  3. Directory JxxTxxxxx/    Under the 1. Directory, this folder stores the 
                             CSV files from TEST number (AFTER)
  4. ipqcnumber.xlsx         The DCD table of IPQC number (BEFORE) 
  5. ipqcnumber_DCD.html     The DCD chart of IPQC number
  6. ipqcnumber_Wh.html      The Wh bar chart of IPQC number 
  7. testnumber.xlsx         The DCD table of TEST number (AFTER)
  8. testnumber_DCD.html     The DCD chart of TEST number
  9. testnumber_Wh.html      The Wh bar chart of TEST number   

The files contained in this program:

RMA_Reportpy        Main program to entey the battery SN for generate reports
IPQC_Rebuild.py     Generate IPQC table and charts from IPQC number
TEST_Build.py       Generate TEST table and charts from TEST number
README.md           This file

Python modules to be installed:
pandas, openpyxl, plotly, mysql_connector, pyinstaller

Versions:

V22.0314.01
Date: 2022/03/14
 1. Initial Release
