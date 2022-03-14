# This program input SN to get the following:
# 1. Test Number and the AFTER table and charts
# 2. IPQC Number and the BEFORE table and charts
# Module to be installed: pandas, openpyxl, mysql_connector, plotly

import os

import mysql.connector
import pandas as pd

from IPQC_Rebuild import ipqc_rebuild
from TEST_Build import test_build

program_version = "22.0314.01"

if __name__ == '__main__':

    mydb = mysql.connector.connect(
        host="192.168.1.84",
        user="richard",
        password="richardtbts",
        database="TBR_Battery_Test"
    )
    mycursor = mydb.cursor()

    # input the SN of an RMA battery
    serial_no = input(f"(Version {program_version})  Please Enter the SN of an RMA battery: ")

    # search the SN_Table to get the IPQC number
    sql = f"SELECT IPQC_No, Mileage, MIS FROM SN_Table WHERE Serial_no = '{serial_no}'"
    mycursor.execute(sql)
    try:
        sql_get = mycursor.fetchone()
        ipqc_no = sql_get[0]
        mileage = sql_get[1]
        mis = sql_get[2]
    except:  # not found
        print("IPQC number not found!")
        exit()

    sql = f"SELECT Battery FROM Total WHERE B_SN = '{serial_no}'"
    mycursor.execute(sql)
    try:
        test_no = mycursor.fetchone()[0]
    except:
        print("TEST number not found! Battery not tested!")
        exit()

    print(f"Battery SN ({serial_no}) = IPQC number ({ipqc_no}) ----- after {mileage} mile and {mis} MIS -----> TEST number ({test_no})")

    # create SN folder
    os.makedirs(serial_no, exist_ok=True)

    # get the current working path
    current_path = os.getcwd()
    # change working path to current_path/serial_no
    os.chdir(f"{current_path}/{serial_no}")

    # Before

    # search the Total to get the IPQC data and its original CSV file
    ipqc_rebuild(ipqc_no)

    # After

    # serach the Total to get the TEST data and its CSV file
    test_build(test_no)
