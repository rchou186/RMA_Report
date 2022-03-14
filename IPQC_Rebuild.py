
# This program collects Mxx.CSV from IPQC number and draw DCD and Wh charts
# installed module: pandas, mysql_connector, openpyxl, plotly

import glob
import os
import platform
import shutil
import time

import mysql.connector
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots


def ipqc_rebuild(IPQC):
    # get the T number and M number from MySQL Total tabel
    mydb = mysql.connector.connect(
        host="192.168.1.84",
        user="richard",
        password="richardtbts",
        database="TBR_Battery_Test"
    )
    mycursor = mydb.cursor()
    sql = f"SELECT * FROM Total WHERE Out_battery = '{IPQC}' ORDER BY Out_Module ASC"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    IPQC_df = pd.DataFrame(myresult, columns=mycursor.column_names)
    #IPQC_df = pd.read_sql(sql, con=mydb)
    IPQC_df.drop('SEQ', axis=1, inplace=True)
    mydb.close()

    # create IPQC folder for CSV files, which under the current working path
    print("Create folder: {0:s}".format(IPQC))
    os.makedirs(IPQC, exist_ok=True)

    # get the current running path
    current_path = os.getcwd()
    
    # save IPQC table
    print("Save Table: {0:s}.xlsx".format(IPQC))
    IPQC_xlsx = IPQC + '.xlsx'
    #IPQC_file = current_path / IPQC / IPQC_xlsx
    IPQC_df.to_excel(f"{current_path}/{IPQC_xlsx}", index=False, sheet_name='Table')

    # get the correct file Tnumber file path from different os
    if platform.system() == 'Darwin':       # Mac
        if not os.path.exists("/Volumes/Battery Test Data"):
            os.system("open smb://Richard:abcd1234@TBTS-SERVER/'Battery Test Data'")
            time.sleep(5)       # sleep 5 second for disk mount
        Tnumber_path = "/Volumes/Battery Test Data/Grading Test"
    elif platform.system() == 'Windows':    # Windows
        Tnumber_path = "Z:/Grading Test"

    # find the orinigal module csv and copy to destination folder
    for i in range(0, len(IPQC_df)):
        Tnumber = IPQC_df.loc[i, 'Battery']
        Org_Module = IPQC_df.loc[i, 'Org_Module']
        Tnumber_prefix = Tnumber[0:6] + 'xxx'
        destination = "M{0:02d}".format(i+1)
        source_csv = Org_Module + '.csv'
        destination_csv = destination + '.csv'
        source_file = f"{Tnumber_path}/{Tnumber_prefix}/{Tnumber}/{source_csv}"
        destination_file = f"{current_path}/{IPQC}/{destination_csv}"
        #print("Copy {0:s} {1:s}.csv to {2:s}.csv".format(Tnumber, Org_Module, destination))
        shutil.copy(source_file, destination_file)

    destination_path = f"{current_path}/{IPQC}"
    csv_files = sorted(glob.glob(f"{destination_path}/*.csv"))

    # collect all csv files to df_all for ploting charts
    df_all = pd.DataFrame()
    for i, csv_file in enumerate(csv_files):
        df = pd.read_csv(csv_file, header=3, sep=',', encoding='latin-1')
        df.columns = ['Time', 'Voltage', 'Current', 'Ah', 'WH', 'Temp', 'Phase', 'DCIR', 'VMOS', 'VDelta', 'TempMOS']

        # remove last few rows of phase goes back to 0
        if (df.iloc[-4]['Phase'] != 0):
            if (df.iloc[-3]['Phase'] == 0):
                df.drop(df.tail(3).index, inplace=True)
            elif (df.iloc[-2]['Phase'] == 0):
                df.drop(df.tail(2).index, inplace=True)
            elif (df.iloc[-1]['Phase'] == 0):
                df.drop(df.tail(1).index, inplace=True)

        # remove phase 1 and phase 3
        df = df[df.Phase != 1]
        df = df[df.Phase != 3]

        # if phase 2 and phase 4 start not zero, offset it to zero
        time_offset2 = df.loc[df.Phase == 2]['Time'].values[0]
        time_offset4 = df.loc[df.Phase == 4]['Time'].values[0]
        if time_offset2 != 0 or time_offset4 != 0:
            df.loc[df.Phase == 2, 'Time'] = df.loc[df.Phase == 2, 'Time'] - time_offset2
            df.loc[df.Phase == 4, 'Time'] = df.loc[df.Phase == 4, 'Time'] - time_offset4

        df.insert(0, 'Module', 'M{0:02d}'.format(i+1))
        df_all = pd.concat([df_all, df])

    # creat DCD charts
    print(f"Create DCD charts: {IPQC}_DCD.html")
    # change phase name
    df_all.loc[df_all.Phase == 0, 'Phase'] = 'DIS0'
    df_all.loc[df_all.Phase == 2, 'Phase'] = 'CHARGE'
    df_all.loc[df_all.Phase == 4, 'Phase'] = 'DISCHARGE'
    # change time to H:MM:SS
    df_all['Time'] = pd.to_datetime(df_all['Time'], unit='s')
    # generate charts, seperate by Phase
    fig = px.line(df_all, x='Time', y='Voltage', color='Module', facet_col='Phase', title=IPQC+' DCD Chart')
    fig.update_xaxes(tickformat='%M:%S')
    #fig.show()
    fig.write_html(f"{current_path}/{IPQC}_DCD.html")

    # create bar graph chart of CHR_Wh, DIS_Wh and Ratio_Wh
    print(f"Create bar graph chart: {IPQC}_Wh.html")
    fig_bar = make_subplots(rows=1, cols=1, specs=[[{"secondary_y": True}]])
    trace1 = go.Bar(x=IPQC_df['Out_Module'], y=IPQC_df['CHR_Wh'], name='CHR_Wh', marker={'color': 'DodgerBlue'})
    trace2 = go.Bar(x=IPQC_df['Out_Module'], y=IPQC_df['DIS_Wh'], name='DIS_Wh', marker={'color': 'mediumseagreen'})
    trace3 = go.Scatter(x=IPQC_df['Out_Module'], y=IPQC_df['Ratio_Wh'],
                        name='Ratio_Wh', line=dict(color='Red'))
    fig_bar.add_trace(trace1, secondary_y=False)
    fig_bar.add_trace(trace2, secondary_y=False)
    fig_bar.add_trace(trace3, secondary_y=True)
    fig_bar.update_layout(title=f"{IPQC} Wh")
    fig_bar.update_xaxes(title="Module")
    fig_bar.update_yaxes(title='Wh', secondary_y=False)
    fig_bar.update_yaxes(title='DISWh/CHRWh', secondary_y=True, range=[0.5, 1.0])
    #fig_bar.show()
    fig_bar.write_html(f"{current_path}/{IPQC}_Wh.html")


if __name__ == "__main__":
    IPQC = input("Please input IPQC number:")
    ipqc_rebuild(IPQC)
