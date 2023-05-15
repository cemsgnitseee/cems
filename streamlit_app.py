from datetime import date, timedelta
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import plotly.express as px
scope = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_service_account_file("keys.json", scopes=scope)
client = gspread.authorize(creds)
today = date.today()
default_date_yesterday = (today - timedelta(days=1))
selected_date = st.date_input("Date", default_date_yesterday)
selected_date=str(selected_date)
year=selected_date[:4]
month=selected_date[5:7]
day=selected_date[8:]
str_month=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov','Dec']
sheetname=str_month[int(month)-1]+year
names_sheet_id="1XI3LK_NCQsWch7dbLmckAWsQfxzW--I4-e1VXBox3oQ"
spreadsheet = client.open_by_key(names_sheet_id)
sheet1=spreadsheet.worksheet("Sheet1")
df = pd.DataFrame(data=sheet1.get_all_records())
for index, row in df.iterrows():
    if(row['month_year']==sheetname):
        workbookid=row['id']
spreadsheet1 = client.open_by_key(workbookid)
exactdate=month+"/"+day+"/"+year[2:]
daybefore=month+"/"+str(int(day)-1).zfill(2)+"/"+year[2:]
if st.button("energy consumed"):
    meters=['Admin_1_250','Admin_2_250','IT_250','EEE_ECE_CSE_HOSTEL_800','GEN_BYPASS_600','IT_400','Auditorium_E-Block_250','Canteen_Motors_125','Capacitors_800','Main_Incoming_1250']
    for i in meters:
        try:
            h=str(sheetname+i)
            sheet1=spreadsheet1.worksheet(h)
            df = pd.DataFrame(data=sheet1.get_all_records())
            grouped_df = df.groupby("date").agg(list)
            grouped_lists = grouped_df.reset_index()
            present=(grouped_lists.loc[grouped_lists["date"]==exactdate])
            present = present.reset_index()
            past=(grouped_lists.loc[grouped_lists["date"]==daybefore])
            past = past.reset_index()
            present=int(present["Energy"][len(present)-1][-1])
            past=int(past["Energy"][len(past)-1][-1])
            st.write("energy consumed by "+i+" "+str(present-past))
        except Exception as er:
            pass

metername= st.multiselect(
    'select meters',['GPR_Memorial_250','Admin_1_250','Admin_2_250','IT_250','EEE_ECE_CSE_HOSTEL_800','GEN_BYPASS_600','IT_400','Auditorium_E-Block_250','Canteen_Motors_125','Capacitors_800','Main_Incoming_1250'])
s=[]
for i in range(len(metername)):
    s.append(sheetname+metername[i])
values_to_plot= st.multiselect('values to be plotted',["P_total","P_r","P_y","P_b","Pf_avg","Pf_r","Pf_y","Pf_b","S_t","S_r","S_y","S_b","Vl_avg","V_ry","V_yb","V_br","Vln_avg","V_r","V_y","V_b","I_t","I_r","I_y","I_b","freq","Energy","Vah"])

if st.button("plot"):
    for i in s:
            sheet1=spreadsheet1.worksheet(i)
            df = pd.DataFrame(data=sheet1.get_all_records())
            grouped_df = df.groupby("date").agg(list)
            grouped_lists = grouped_df.reset_index()
            p=(grouped_lists.loc[grouped_lists["date"]==exactdate])
            p = p.reset_index()
            for j in values_to_plot:
                fig = px.line(p, x=p.iloc[0]["time"], y=p.iloc[0][j],title=i+j+' vs time')#perfect one day plot
                st.plotly_chart(fig)

