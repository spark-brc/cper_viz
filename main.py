import logging
import plotly.express as px
import geopandas as gpd
import streamlit as st
import os
import pandas as pd
import base64
import numpy as np
import glob
import datetime
# import utils
import time
from io import StringIO
from shapely.geometry import shape
import json
import xmltodict
import utils

pd.options.mode.chained_assignment = None

LINE = """<style>
.vl {
  border-left: 2px solid gray;
  height: 100px;
  position: absolute;
  left: 50%;
  margin-left: -3px;
  top: 0;
}
</style>
<div class="vl"></div>"""

st.set_page_config(
    layout="wide",
    initial_sidebar_state='collapsed',
    page_title='APEX Visualization',
    page_icon='icon2.png' 
    )
st.title('APEX Model - Biomass Analysis')
st.markdown("## User Inputs:")
col1, line, col2, line2, col3 = st.beta_columns([0.3,0.05,0.3,0.05,0.3])


with col1:
    shp = st.selectbox('Select Shapefile:', ['AGM', 'TGM'])
with line:
    st.markdown(LINE, unsafe_allow_html=True)
with col2:
    output_df = st.selectbox('Select Output file:', ['ACY', 'AGZ'])


def main(dff, dfmin, dfmax, yrmin, yrmax, sel_yr):
    with line2:
        st.markdown(LINE, unsafe_allow_html=True)
    tdf01 = st.beta_expander('{} Dataframe from {} output'.format(sel_var, output_df))
    with tdf01:
        st.dataframe(dff, height=500)
        st.markdown(utils.filedownload(dff), unsafe_allow_html=True)
    st.write('___')
    st.write('## Spatio-temporal variation')
    sel_yr = st.slider(
        "Select Time:", int(yrmin), int(yrmax))
    st.write('### Example 1 of map layout')
    utils.viz_biomap2(shp, dff, dfmin, dfmax, sel_yr)
    st.write('### Example 2 of map layout')
    mcol1, mcol2 = st.beta_columns([0.5, 0.5])    
    with mcol1:
        utils.viz_biomap2('AGM', dff, dfmin, dfmax, sel_yr)
    with mcol2:
        utils.viz_biomap2('TGM', dff, dfmin, dfmax, sel_yr)
    st.write('___')
    st.write('## Check correlation between variables')
    vcol1, vcol2 = st.beta_columns([0.5, 0.5])
    with vcol1:
        v1 = st.multiselect('Select Reach Vars on X-axis:', ot_vars)
    with vcol2:
        v2 = st.multiselect('Select Reach Vars on Y-axis:', ot_vars)
    st.plotly_chart(utils.get_corr_plot(df, v1, v2), use_container_width=True)

    


@st.cache
def load_data():
    if output_df == 'ACY':
        df = pd.read_csv(
                    "./resources/CONUNN_AGM.ACY",
                    delim_whitespace=True,
                    skiprows=8,
                    header=0,
                    )
    elif output_df == 'AGZ':
        df = pd.read_csv(
                    "./resources/CONUNN_AGM.AGZ",
                    delim_whitespace=True,
                    skiprows=8,
                    header=0,
                    )
    return df



if __name__ == '__main__':
    logging.basicConfig(level=logging.CRITICAL)
    df = load_data()
    tdf02 = st.beta_expander('Dataframe from {} output'.format(output_df))
    with tdf02:
        st.dataframe(df)
    if output_df == 'ACY':
        ot_vars = utils.get_acy_vars()
    elif output_df == 'AGZ':
        ot_vars = utils.get_agz_vars()
    with col3:
        sel_var = st.selectbox('Select Output Variable:', ot_vars, index=2)    
    dff, dfmin, dfmax, yrmin, yrmax = utils.read_acy(df, sel_var)
    




    # if rchids2 and obsids2 and wnam:
    main(dff, dfmin, dfmax, yrmin, yrmax, yrmin)

