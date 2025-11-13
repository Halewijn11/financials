import variables
import numpy as np
import os
import time
import pandas as pd
import subprocess
from montly_expense import Monthly_Expense

class Monthly_Deposit_Expense(Monthly_Expense):
    def __init__(self, month, year):
        """
        Initialize the New_Monthly_Expenses class with the given parameters.

        Parameters:
        download_folder (str): The folder where downloaded files are stored.
        month (int): The month of the expenses.
        year (int): The year of the expenses.
        """
        super().__init__(month, year)

        self.get_deposit_filename()
        self.get_deposit_dataframe()
        self.format_deposit_df()


    def get_deposit_filename(self):
        """
        Retrieve the filename of the deposit file based on the specified criteria.
        """
        sorted_filelist_df = self.sorted_download_file_df
        filter_ = sorted_filelist_df.loc[:, 'filename'].str.contains('BE39 0635 5641 9519')
        
        # filelist_df = filelist_df.sort_values('creation time', ascending=False)
        # filelist_df = filelist_df.loc[filter_]
        # filelist_df = filelist_df.reset_index(drop=True)
        # self.deposit_filename = filelist_df.loc[0, 'filename']


    def get_deposit_dataframe(self):
        self.deposit_df = pd.read_csv(self.download_folder + '/' + self.deposit_filename, sep=';', skiprows=12)
        return self.deposit_df

    def format_deposit_df(self):
        """
        Format the deposit DataFrame for further analysis.
        """

        df = self.deposit_df.copy()
        df['Bedrag'] = df['Bedrag'].str.replace(',', '.')
        df['Bedrag'] = df['Bedrag'].astype('float')
        df['Boekingsdatum'] = pd.to_datetime(df['Boekingsdatum'], format='%d/%m/%Y')

        # omdat sommige mensen geen mededelingen schrijven
        df['Mededelingen'] = df['Mededelingen'].fillna(df['Naam tegenpartij bevat'])
        # Use str.extract to capture everything matching the regex pattern
        df['Mededelingen'] = df['Mededelingen'].str.replace(r'(REF\. : \d+) VAL\. (\d{2}-\d{2})', '', regex=True)
        df['Mededelingen'] = df['Mededelingen'].str.replace(r'REF\. : ([A-Za-z0-9]+) VAL\. (\d{2}-\d{2})', '',
                                                            regex=True)

        # replace'AANKOOP VIA INTERNET MET KAART NR 5169 2010 7988 0753  - Van den Bossche H'
        df['Mededelingen'] = df['Mededelingen'].str.replace(
            'AANKOOP VIA INTERNET MET KAART NR 5169 2010 7988 0753  - Van den Bossche H', 'AVI')
        # delete the extra information aout the time and date in the mededelingen of AVIs
        df['Mededelingen'] = df['Mededelingen'].str.replace(r'(OP \d{2}/\d{2} \d{2}:\d{2})', '', regex=True)
        # replace the google pay sentence
        df['Mededelingen'] = df['Mededelingen'].str.replace(r'(DEBITMASTERCARD-BETALING VIA Google Pay \d{2}/\d{2})',
                                                            'GP', regex=True)
        # change the contactless
        df['Mededelingen'] = df['Mededelingen'].str.replace(
            'AANKOOP BANCONTACT CONTACTLESS MET KAART NR 5169 2010  7988 0753', '')
        df['Mededelingen'] = df['Mededelingen'].str.replace(
            'AANKOOP BANCONTACT CONTACTLESS MET KAART NR 6703 0513  5238 4000', '')
        df['Mededelingen'] = df['Mededelingen'].str.replace('KAART NR 5169 2010 7988 0753', '')
        df['Mededelingen'] = df['Mededelingen'].str.replace(' - Van den Bossche H', '')
        df['Mededelingen'] = df['Mededelingen'].str.replace('BETALING VIA UW MOBILE BANKING APP OF UW BANCONTACT',
                                                            'MOBILE')
        self.formatted_deposit_df = df[self.deposit_interesting_columns]

    def deposit_df_to_excel(self):
        """
        Save the filtered deposit DataFrame to an Excel file.
        """
        time_filt = (self.formatted_deposit_df['Boekingsdatum'].dt.year == self.year) & (
                    self.formatted_deposit_df['Boekingsdatum'].dt.month == self.month)
        time_filt_df = self.formatted_deposit_df[time_filt].copy()

        # filt_select_col_df.loc[:,'Category'] = [np.NaN]*filt_select_col_df.shape[0]
        self.deposit_filepath = self.draft_folder + '/' + self.deposit_filename[:-4] + '.xlsx'
        time_filt_df.to_excel(self.deposit_filepath, index=False)

    def apply_rules(self):
        pass

    def open_deposit_df(self):
        self.get_deposit_filename()
        self.get_deposit_dataframe()
        self.format_deposit_df()
        self.deposit_df_to_excel()
        # Use subprocess to open Excel with the specified file
        subprocess.Popen([self.excel_path, self.deposit_filepath], shell=True)

    def get_categories_for_datavalidation(self):
        """
        Print all categories for data validation purposes.
        """
        concatenated_categories = np.concatenate(
            (self.food_catagories, self.entertainment_categories, self.income_categories, self.remaining_categories))
        for category in concatenated_categories:
            print(category + ',')


if __name__ == "__main__":
    # This code will only run if the file is executed directly.
    deposit_1_2024 = Monthly_Deposit_Expense(1, 2024)
    deposit_1_2024.open_deposit_df()