import logging
import plotly.express as px
import streamlit as st
import os
import pandas as pd
import base64
import numpy as np
import glob
import datetime
# import utils
import time

pd.options.mode.chained_assignment = None


st.set_page_config(
    layout="wide",
    initial_sidebar_state='collapsed',
    page_title='APEX Visualization',
    page_icon='icon2.png' 
    )
st.write(os.getcwd())

st.title('APEX Model - Streamflow Analysis')
st.markdown("## User Inputs:")

wd_path = st.text_input("Provid the path of project directory:")
st.write(type(wd_path))
os.chdir(wd_path)

# def find_rch_files(wd):
#     rch_files = []
#     for filename in glob.glob(str(wd)+"/*.RCH"):
#         rch_files.append(os.path.basename(filename))
#     return rch_files
# dd = find_rch_files(wd_path)
# st.write(dd)
st.write(os.getcwd())
