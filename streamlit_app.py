import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import plotly.express as px
scope = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_service_account_file("keys.json", scopes=scope)
client = gspread.authorize(creds)
spreadsheet = client.open_by_key("1nDom83EY4IDsEGSOGu-_ZchimSxBvV6NqlcXG9zqAcM")
s=[]
month = st.selectbox(
    'Select month',
    ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov','Dec'))
sheetname=month+"2023"
metername= st.multiselect(
    'select meters',['GPR_Memorial_250','Admin_1_250','Admin_2_250','IT_250','EEE_ECE_CSE_HOSTEL_800','GEN_BYPASS_600','IT_400','Auditorium_E-Block_250','Canteen_Motors_125','Capacitors_800','Main_Incoming_1250'])
for i in range(len(metername)):
    s.append(sheetname+metername[i])
values_to_plot= st.multiselect('values to be plotted',["P_total","P_r","P_y","P_b","Pf_avg","Pf_r","Pf_y","Pf_b","S_t","S_r","S_y","S_b","Vl_avg","V_ry","V_yb","V_br","Vln_avg","V_r","V_y","V_b","I_t","I_r","I_y","I_b","freq","Energy","Vah"])
if st.button('plot'):
    for i in s:
        sheet1=spreadsheet.worksheet(i)
        df = pd.DataFrame(data=sheet1.get_all_records())
        for j in range(len(values_to_plot)):
            fig = px.line(df, x="time", y=values_to_plot[j], color='date',title=str(i+" "+values_to_plot[j]+' vs time'))
            st.plotly_chart(fig, use_container_width=True)
else:
    st.write("select options to plot")
