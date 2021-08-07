import streamlit as st
import numpy as np
import pandas as pd
import sqlite3
import time
import requests
import streamlit.components.v1 as components
import plotly.express as px
from datetime import date, datetime
from fnodataupdate import fnodata
import SessionState
from filterdata_fun import filtered_data
from oichart_fun import oi_chart_graph
from coichart_fun import coi_chart_graph
from fiidiidatanalysis import fiidiidata
from streamlit import caching
from get_cmp_fun import get_cmp


st.set_page_config(page_title = 'TraDatAnalytix',layout='wide', page_icon='💹')

session_state1 = SessionState.get(checkboxed=False)
session_state2 = SessionState.get(checkboxed=False)

tday = st.sidebar.date_input('Date Input')

lc, mc, rc = st.columns(3)

button1 = st.sidebar.button("Open Interest")
button2 = st.sidebar.button("FII/DII Data")
button3 = st.sidebar.button("Trading Strategy")


#button1 = lc.button("Open Interest")
#button2 = mc.button("FII/DII Data")
#button3 = rc.button("Trading Strategy")

#tday = st.date_input('Date Input')


if button1 or session_state1.checkboxed:
    session_state1.checkboxed = True

    df = fnodata(tday)
    option = lc.selectbox(
            'Symbol',
            df['SYMBOL'].unique())

    option_exp = mc.selectbox(
            'Expiry DATE',
            df['EXPIRY_DT'].unique())

    option_inst = rc.selectbox(
            'INSTRUMENT',
            df['INSTRUMENT'].unique()) 

    #Getting CMP
    gcmp = get_cmp(df, option)

    # Graph data as per user choice    
    filterdata = filtered_data(df, option, option_exp, option_inst, gcmp)

        
        #md_results = f"**{option}** Futures LTP **{gcmp}**"
        #st.markdown(md_results)
        #lc.markdown(f"<h4 style='text-align: center; color: white; background-color:SlateBlue'>{md_results}</h4>", unsafe_allow_html=True)
        #st.write("Current Future Price" + gcmp)

    
    bb1 = lc.button("Generate OI Graphs")

    if bb1:
        session_state1.checkboxed = False
        
        oi_chart = oi_chart_graph(filterdata)

        coi_chart = coi_chart_graph(filterdata)

        # Plotting OI Graph
        
        st.plotly_chart(oi_chart)

        # Plotting OI Change Graph
        
        st.plotly_chart(coi_chart)


if button2 or session_state2.checkboxed:
    session_state2.checkboxed = True

    bb2 = rc.button("Generate FII Graphs")

    if bb2:
        session_state2.checkboxed = False
        df1 = fiidiidata(tday)
        st.write(df1.head())



