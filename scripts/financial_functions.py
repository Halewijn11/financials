import pandas as pd
import numpy as np
import os
import random
import seaborn as sns
import matplotlib.pyplot as plt
import time
import subprocess
#from openpyxl.worksheet.datavalidation import DataValidation
import re
# import variables
import importlib
# variables = importlib.reload(variables)
# import PyPDF2
import yaml


def reload_libraries(): 
    import variables
    variables = importlib.reload(variables)
    print('done')

# with open("./config.yml", "r") as f:
#     config = yaml.safe_load(f)
# rule_config = config['rules']

def get_deposit_filename(filelist_df):
    """
    Retrieve the filename of the deposit file based on the specified criteria.
    """
    filter_ = filelist_df.loc[:, 'filename'].str.contains('BE39 0635 5641 9519')
    filelist_df = filelist_df.sort_values('creation time', ascending=False)
    filelist_df = filelist_df.loc[filter_]
    filelist_df = filelist_df.reset_index(drop=True)
    deposit_filename = filelist_df.loc[0, 'filename']
    return deposit_filename

def get_sorted_download_folder_file_df(): 
    filelist = os.listdir(variables.download_folder)
    time_array = []
    for ii in range(len(filelist)):
        path = variables.download_folder + '\\' + filelist[ii]
        creation_time = os.path.getctime(path)
        creation_time = time.ctime(creation_time)
        time_array += [creation_time]
    filelist_df = pd.DataFrame(filelist)
    filelist_df = filelist_df.rename(columns={0: 'filename'})
    filelist_df['creation time'] = time_array
    filelist_df['creation time'] = pd.to_datetime(filelist_df.loc[:, 'creation time'])
    sorted_download_file_df = filelist_df
    return sorted_download_file_df

def get_deposit_df(filepath):
    deposit_df = pd.read_csv(filepath, sep = ';', skiprows=12)
    return deposit_df

def format_deposit_df(deposit_df):
    """
    Format the deposit DataFrame for further analysis.
    """
    

    df = deposit_df.copy()
    df = df.rename(columns = {'Bedrag': 'amount',
                        'Mededelingen': 'description',
                             'Boekingsdatum': 'date'})
    df['amount'] =  df['amount'].str.replace(',', '.')
    df['amount'] = df['amount'].astype('float')
    df['date'] = pd.to_datetime(df['date'], format = '%d/%m/%Y')
    
    # omdat sommige mensen geen description schrijven
    df['description'] = df['description'].fillna(df['Naam tegenpartij bevat'])
    # Use str.extract to capture everything matching the regex pattern
    df['description'] = df['description'].str.replace(r'(REF\. : \d+) VAL\. (\d{2}-\d{2})', '', regex=True)
    df['description'] = df['description'].str.replace(r'REF\. : ([A-Za-z0-9]+) VAL\. (\d{2}-\d{2})', '', regex=True)
    
    #replace'AANKOOP VIA INTERNET MET KAART NR 5169 2010 7988 0753  - Van den Bossche H'
    df['description'] = df['description'].str.replace('AANKOOP VIA INTERNET MET KAART NR 5169 2010 7988 0753  - Van den Bossche H', 'AVI')
    #delete the extra information aout the time and date in the description of AVIs
    df['description'] = df['description'].str.replace(r'(OP \d{2}/\d{2} \d{2}:\d{2})', '', regex = True)
    #replace the google pay sentence
    df['description'] = df['description'].str.replace(r'(DEBITMASTERCARD-BETALING VIA Apple Pay \d{2}/\d{2})', 'AP', regex = True)
    #replace the apple pay sentence
    df['description'] = df['description'].str.replace(r'(DEBITMASTERCARD-BETALING VIA Google Pay \d{2}/\d{2})', 'GP', regex = True)
    df['description'] = df['description'].str.replace(r'(DEBITMASTERCARD-BETALING \d{2}/\d{2})', 'MC', regex = True)
    #change the contactless
    df['description'] = df['description'].str.replace('AANKOOP BANCONTACT CONTACTLESS MET KAART NR 5169 2010  7988 0753', '')
    df['description'] = df['description'].str.replace('AANKOOP BANCONTACT CONTACTLESS MET KAART NR 6703 0513  5238 4000', '')
    df['description'] = df['description'].str.replace('KAART NR 5169 2010 7988 0753', '')
    df['description'] = df['description'].str.replace(' - Van den Bossche H', '')
    df['description'] = df['description'].str.replace('BETALING VIA UW MOBILE BANKING APP OF UW BANCONTACT', 'MOBILE')
    df['description'] = df['description'].str.replace(r'\s+', ' ', regex=True).str.strip()

    formatted_deposit_df = df
    formatted_deposit_df['card'] = ['belfius_deposit']*formatted_deposit_df.shape[0]


    return formatted_deposit_df

# def apply_rules(deposit_df):
#     for 
    


def df_to_excel(formatted_deposit_df, filename, output_filepath): 
    """
    Save the filtered deposit DataFrame to an Excel file.
    """
    
    #filt_select_col_df.loc[:,'Category'] = [np.NaN]*filt_select_col_df.shape[0]
    formatted_deposit_df.to_excel(output_filepath, index = False)

def open_deposit_df(filepath):
    # Use subprocess to open Excel with the specified file
    subprocess.Popen([variables.excel_path, filepath], shell=True)

def open_mastercard_df(filepath):
    # Use subprocess to open Excel with the specified file
    subprocess.Popen([variables.excel_path, filepath], shell=True)



def update_row(row):
    matched = False
    local_row = row.copy()

    for rule in rule_config:
        matching_col_name = rule.get('matching_col_name')
        updated_col_name = rule.get('updated_col_name')
        mapped_text = rule.get('mapped_text')
        query = str(rule.get('query')).lower()
        target = str(local_row[matching_col_name]).lower()
        if query in target:
            local_row[updated_col_name] = mapped_text
    
    return local_row

def get_categories_for_datavalidation():
    """
    Print all categories for data validation purposes.
    """
    concatenated_categories = np.concatenate((variables.food_categories, variables.entertainment_categories, variables.income_categories, variables.remaining_categories))
    for category in concatenated_categories:
        print(category + ',')


def overwrite_description(df):
    """
    Overwrites the 'description' column with 'short_description' 
    when 'short_description' is not NaN.

    Parameters:
    df (pd.DataFrame): DataFrame with 'description' and 'short_description' columns.

    Returns:
    pd.DataFrame: New DataFrame with updated 'description' column.
    """
    df = df.copy()  # avoid modifying the original df
    df['description'] = np.where(df['short_description'].notna(), 
                                 df['short_description'], 
                                 df['description'])
    # print(df.columns)
    # df = df.drop('short_description',axis = 1)
    return df

def open_formatted_montly_deposit_in_excel(input_path, filename, output_path, open_excel): 
    input_filepath = input_path + '/' + filename
    deposit_df = get_deposit_df(input_filepath)
    formatted_deposit_df = format_deposit_df(deposit_df)
    ruled_formatted_deposit_df = formatted_deposit_df.apply(update_row, axis = 1)
    ruled_formatted_deposit_df = overwrite_description(ruled_formatted_deposit_df)
    # display(ruled_formatted_deposit_df)
    # print(ruled_formatted_deposit_df.columns)
    # ruled_formatted_deposit_df = ruled_formatted_deposit_df.drop('short_description', axis =1)
    ruled_formatted_deposit_df = ruled_formatted_deposit_df[['date', 'card', 'description', 'amount', 'tag']]
    
    output_filepath = output_path + '/' + filename[:-4] + '.xlsx'
    if open_excel == True:
        df_to_excel(ruled_formatted_deposit_df, filename, output_filepath)
        open_deposit_df(output_filepath)
    return ruled_formatted_deposit_df