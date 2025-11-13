import pandas as pd
import numpy as np
import os
import random
import seaborn as sns
import importlib
import yaml
import sys
import pygwalker as pyg
import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import pygwalker as pyg
import yaml
from io import StringIO
from pygwalker.api.streamlit import StreamlitRenderer
from streamlit_extras.metric_cards import style_metric_cards
sys.path.append('../')



import multipage_app.functions as functions
importlib.reload(functions)

# print('hello')

# st.write("Hello World")

import multipage_app.functions as functions
importlib.reload(functions)


settings = functions.load_settings('../dashboard_config.yaml')
print(settings)

#--------------------- setting the theme -----------------------------
# functions.set_theme(settings)

#--------------------- reading dataframes -----------------------------
# temp_dir = settings['tempdir']
# data_repo_path = temp_dir + 'data/'

# transaction_df  = pd.read_csv(data_repo_path + 'transaction_df.csv')
# core_transaction_df  = pd.read_csv(data_repo_path + 'core_transaction_df.csv')
# montly_balance_df  = pd.read_csv(data_repo_path + 'montly_balance_df.csv')
# net_balance_df  = pd.read_csv(data_repo_path + 'net_balance_df.csv')
# refund_df = pd.read_csv(data_repo_path + 'refund_df.csv')
# monthly_spend_by_category_summary_df  = pd.read_csv(data_repo_path + 'monthly_spend_by_category_summary_df.csv')

# ---- Load settings ----
if 'settings' not in st.session_state:
    settings = functions.load_settings('../dashboard_config.yaml')
    st.session_state.settings = settings
if 'plot_settings' not in st.session_state:
    st.session_state.plot_settings = settings['plots']


settings = st.session_state.settings
data_repo_path = settings['tempdir'] + 'data/'

# ---- Load DataFrames only once ----
if 'dataframes_loaded' not in st.session_state:
    st.session_state.transaction_df = pd.read_csv(data_repo_path + 'transaction_df.csv')
    st.session_state.core_transaction_df = pd.read_csv(data_repo_path + 'core_transaction_df.csv')
    st.session_state.montly_balance_df = pd.read_csv(data_repo_path + 'montly_balance_df.csv')
    st.session_state.net_balance_df = pd.read_csv(data_repo_path + 'net_balance_df.csv')
    st.session_state.refund_df = pd.read_csv(data_repo_path + 'refund_df.csv')
    st.session_state.core_transaction_df = pd.read_csv(data_repo_path + 'core_transaction_df.csv')
    st.session_state.monthly_spend_by_category_summary_df = pd.read_csv(data_repo_path + 'monthly_spend_by_category_summary_df.csv')
    st.session_state.monthly_spend_by_category_summary_df = pd.read_csv(
        data_repo_path + 'monthly_spend_by_category_summary_df.csv'
    )
    st.session_state.dataframes_loaded = True



# #--------------------- setup streamlit -----------------------------
# st.set_page_config(layout = 'wide')

# #--------------------- plot the balance figure -----------------------------
# plot_settings = settings['plots']
# balance_fig = functions.plot_income_spending(montly_balance_df,net_balance_df, settings['plots']['spending_income_plot'])
# monthly_spend_percentage_fig = functions.plot_monthly_spend_percentage(monthly_spend_by_category_summary_df, 
#                                                                        settings['plots']['percentage_spend_by_category_plot'])
# treemap_fig = functions.treemap_df(core_transaction_df,
#         settings['plots']['treemap_plot'])


# #--------------------- calculate some metrics -----------------------------

# avg_saving_per_month = int(net_balance_df['amount'].mean())

# avg_saving_spending_df = montly_balance_df.groupby(['is_income_category'],as_index = False)['amount'].mean()
# avg_income_per_month = avg_saving_spending_df[avg_saving_spending_df['is_income_category'] == True].iloc[0]['amount']
# avg_spending_per_month = avg_saving_spending_df[avg_saving_spending_df['is_income_category'] == False].iloc[0]['amount']

# refund_summary_df = refund_df.groupby(['main_tag'],as_index=False)['amount'].sum()
# parental_refund = refund_summary_df[refund_summary_df['main_tag'] == 'parental_refund'].iloc[0]['amount']
# pending_refund = refund_summary_df[refund_summary_df['main_tag'] == 'pending_refund'].iloc[0]['amount']
# loan = refund_summary_df[refund_summary_df['main_tag'] == 'loan'].iloc[0]['amount']


# #--------------------- building the streamlit app -----------------------------

# # with top_cols[2]:
# #     pyg_app = StreamlitRenderer(transaction_df)
# #     pyg_app.explorer()
# st.set_page_config(
#     page_title="pages",
# )
# st.sidebar.success('seelect a page')

# metric_card_settings = plot_settings['metric_cards']
# top_cols = st.columns(6)
# top_cols[0].metric(
#     label = "avg_income_per_month",
#     value = int(avg_income_per_month),
#     border=metric_card_settings['border']
# )
# top_cols[1].metric(
#     label = "avg_spending_per_month",
#     value = np.abs(int(avg_spending_per_month)),
#     border=metric_card_settings['border']
# )
# top_cols[2].metric(
#     label = "avg_saving_spending_df",
#     value = int(avg_saving_per_month),
#     border=metric_card_settings['border']
# )
# top_cols[3].metric(
#     label = "parental_refund",
#     value = int(parental_refund),
#     border=metric_card_settings['border']
# )
# top_cols[4].metric(
#     label = "pending_refund",
#     value = int(pending_refund),
#     border=metric_card_settings['border']
# )
# top_cols[5].metric(
#     label = "loan",
#     value = int(loan),
#     border=metric_card_settings['border'],
    
# )

# style_metric_cards(box_shadow=metric_card_settings['box_shadow'],
#                    border_left_color=metric_card_settings['border_left_color'],
#                    background_color=metric_card_settings['background_color'])
# # top_cols = st.columns([1,1,1])

# with top_cols[0]:
#     st.plotly_chart(balance_fig, use_container_width=True)
# with top_cols[1]:
#     st.plotly_chart(monthly_spend_percentage_fig, use_container_width=True)

summary_page = st.Page(
    page='pages/summary_page.py',
    title='Summary',
    default=True,
    icon='📄'  # example icon for summary
)

dataframe_page = st.Page(
    page='pages/dataframe_page.py',
    title='Dataframes',
    icon='📊'  # example icon for dataframes
)

pygwalker_page = st.Page(
    page='pages/pygwalker_page.py',
    title='Pygwalker',
    icon='🧩'  # example icon for pygwalker
)
# page_2 = st.Page(
#     page='pages/projects.py',
#     title = 'page1',
# )
# st.plotly_chart(treemap_fig, use_container_width=True)
# st.plotly_chart(monthly_spend_percentage_fig, use_container_width=True)

pg = st.navigation({
    "Info": [summary_page],
    "Data Exploration": [dataframe_page, pygwalker_page]
})

pg.run()