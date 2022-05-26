# This program input SN to get the following:
# 1. Test Number and the AFTER table and charts
# 2. IPQC Number and the BEFORE table and charts
# Module to be installed: pandas, openpyxl, mysql_connector, plotly

import os

import mysql.connector
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots


from IPQC_Rebuild import ipqc_rebuild
from TEST_Build import test_build

VERSION = '22.0324.01'

if __name__ == '__main__':

    mydb = mysql.connector.connect(
        host="192.168.1.84",
        user="richard",
        password="richardtbts",
        database="TBR_Battery_Test"
    )
    mycursor = mydb.cursor()

    # input the SN of an RMA battery
    serial_no = input(f"V{VERSION}, Please Enter the SN of an RMA battery:")

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

    print(f"\nBattery SN ({serial_no}) = IPQC number ({ipqc_no}) ----- after {mileage} mile and {mis} MIS -----> TEST number ({test_no})")

    # create SN folder
    os.makedirs(serial_no, exist_ok=True)

    # get the current working path
    current_path = os.getcwd()
    # change working path to current_path/serial_no
    os.chdir(f"{current_path}/{serial_no}")

    # Before

    # search the Total to get the IPQC data and its original CSV file
    IPQC_df, IPQC_df_all = ipqc_rebuild(ipqc_no)

    # After

    # serach the Total to get the TEST data and its CSV file
    TEST_df, TEST_df_all = test_build(test_no)

    # make RMA excel file of IPQC and TEST together
    print(f"\nCreate RMA total table: {serial_no}.xlsx ---> ", end='')
    output_df = pd.concat([IPQC_df, TEST_df], axis=1)
    output_df.to_excel(f"{serial_no}.xlsx")

    # change phase name
    IPQC_df_all.loc[IPQC_df_all.Phase == 'DIS0', 'Phase'] = 'Before_DIS0'
    IPQC_df_all.loc[IPQC_df_all.Phase == 'CHARGE', 'Phase'] = 'Before_CHARGE'
    IPQC_df_all.loc[IPQC_df_all.Phase == 'DISCHARGE', 'Phase'] = 'Before_DISCHARGE'
    TEST_df_all.loc[TEST_df_all.Phase == 'DIS0', 'Phase'] = 'After_DIS0'
    TEST_df_all.loc[TEST_df_all.Phase == 'CHARGE', 'Phase'] = 'After_CHARGE'
    TEST_df_all.loc[TEST_df_all.Phase == 'DISCHARGE', 'Phase'] = 'After_DISCHARGE'

    # combine IPQC and TEST df_all dataframes
    df_allall = pd.concat([IPQC_df_all, TEST_df_all])

    # make RMA DCD chart of both IPQC and TEST together (6 charts)
    print(f"Create RMA DCD charts: {serial_no}_DCD.html ---> ", end='')
    # change time to H:MM:SS
    #df_allall['Time'] = pd.to_datetime(df_allall['Time'], unit='s')
    # generate charts, seperate by Phase
    color_map = {'M01':'#AA0DFE', 'M02':'#3283FE', 'M03':'#85660D', 'M04':'#782AB6', 'M05':'#565656',
                 'M06':'#1C8356', 'M07':'#16FF32', 'M08':'#F7E1A0', 'M09':'#E2E2E2', 'M10':'#1CBE4F',
                 'M11':'#C4451C', 'M12':'#DEA0FD', 'M13':'#FE00FA', 'M14':'#325A9B', 'M15':'#FEAF16', 
                 'M16':'#F8A19F', 'M17':'#90AD1C', 'M18':'#F6222E', 'M19':'#1CFFCE', 'M20':'#2ED9FF',
                 'M21':'#B10DA1', 'M22':'#C075A6', 'M23':'#FC1CBF', 'M24':'#B00068', 'M25':'#FBE426',
                 'M26':'#FA0087', 'M27':'#2E91E5', 'M28':'#222A2A', 'M29':'#B68100', 'M30':'#511CFB',
                 'M31':'#778AAE', 'M32':'#620042', 'M33':'#FF9616', 'M34':'#00B5F7'
                } # the color_map is choose from Alphabet and some Dark24, Light23
    fig = px.line(df_allall, x='Time', y='Voltage', color='Module', facet_col='Phase', title=serial_no+' DCD Chart', color_discrete_map=color_map)
    fig.update_xaxes(tickformat='%M:%S')
    fig.show()
    fig.write_html(f"{serial_no}_DCD.html")

    # make RMA Wh bar chart of both IPQC and TEST together (2 charts)
    # create bar graph chart of CHR_Wh, DIS_Wh and Ratio_Wh
    print(f"Create bar graph chart: {serial_no}_Wh.html")
    fig_bar = make_subplots(rows=2, cols=1, specs=[[{"secondary_y": True}], [{"secondary_y": True}]])

    trace1 = go.Bar(x=IPQC_df['Out_Module'], y=IPQC_df['CHR_Wh'], name='Before_CHR_Wh', marker={'color': 'DodgerBlue'})
    trace2 = go.Bar(x=IPQC_df['Out_Module'], y=IPQC_df['DIS_Wh'], name='Before_DIS_Wh', marker={'color': 'mediumseagreen'})
    trace3 = go.Scatter(x=IPQC_df['Out_Module'], y=IPQC_df['Ratio_Wh'],
                        name='Before_Ratio_Wh', line=dict(color='Red'))
    fig_bar.add_trace(trace1, row=1, col=1, secondary_y=False)
    fig_bar.add_trace(trace2, row=1, col=1, secondary_y=False)
    fig_bar.add_trace(trace3, row=1, col=1, secondary_y=True)

    trace4 = go.Bar(x=TEST_df['Org_Module'], y=TEST_df['CHR_Wh'], name='After_CHR_Wh', marker={'color': 'blue'})
    trace5 = go.Bar(x=TEST_df['Org_Module'], y=TEST_df['DIS_Wh'], name='After_DIS_Wh', marker={'color': 'green'})
    trace6 = go.Scatter(x=TEST_df['Org_Module'], y=TEST_df['Ratio_Wh'],
                        name='After_Ratio_Wh', line=dict(color='orange'))
    fig_bar.add_trace(trace4, row=2, col=1, secondary_y=False)
    fig_bar.add_trace(trace5, row=2, col=1, secondary_y=False)
    fig_bar.add_trace(trace6, row=2, col=1, secondary_y=True)

    fig_bar.update_layout(title=f"{serial_no} Wh")
    fig_bar.update_xaxes(title="Module")
    fig_bar.update_yaxes(title='Wh', secondary_y=False)
    fig_bar.update_yaxes(title='DISWh/CHRWh', secondary_y=True, range=[0.5, 1.0])
    fig_bar.show()
    fig_bar.write_html(f"{serial_no}_Wh.html")