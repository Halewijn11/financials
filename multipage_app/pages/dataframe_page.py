# import streamlit as st
# import functions
# import pandas as pd

# settings = functions.load_settings('../dashboard_config.yaml')
# print(settings)

# #--------------------- setting the theme -----------------------------
# # functions.set_theme(settings)

# #--------------------- reading dataframes -----------------------------
# temp_dir = settings['tempdir']
# data_repo_path = temp_dir + 'data/'

# transaction_df  = pd.read_csv(data_repo_path + 'transaction_df.csv')
# core_transaction_df  = pd.read_csv(data_repo_path + 'core_transaction_df.csv')
# montly_balance_df  = pd.read_csv(data_repo_path + 'montly_balance_df.csv')
# net_balance_df  = pd.read_csv(data_repo_path + 'net_balance_df.csv')
# refund_df = pd.read_csv(data_repo_path + 'refund_df.csv')
# monthly_spend_by_category_summary_df  = pd.read_csv(data_repo_path + 'monthly_spend_by_category_summary_df.csv')

# balance_fig = functions.plot_income_spending(montly_balance_df,net_balance_df, settings['plots']['spending_income_plot'])

# st.plotly_chart(balance_fig, use_container_width=True)

import streamlit as st

st.write('test')
