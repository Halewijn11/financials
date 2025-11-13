import streamlit as st
from pygwalker.api.streamlit import StreamlitRenderer
import pandas as pd
st.set_page_config(layout="wide")

st.title('Explore your data')
data_repo_path = '../temp/data/'
core_transaction_df  = pd.read_csv(data_repo_path + 'core_transaction_df.csv')

pyg_app = StreamlitRenderer(core_transaction_df)
pyg_app.explorer()
