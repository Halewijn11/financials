import variables
import numpy as np
import os
import time
import pandas as pd
import subprocess
import PyPDF2
import re
from montly_expense import Monthly_Expense

class Monthly_MasterCard_Expense(Monthly_Expense):
    def __init__(self, month, year):
        """
        Initialize the New_Monthly_Expenses class with the given parameters.

        Parameters:
        download_folder (str): The folder where downloaded files are stored.
        month (int): The month of the expenses.
        year (int): The year of the expenses.
        """
        super().__init__(month, year)

        #get the filename for the mastercard
        self.get_mastercard_filename()

    def get_mastercard_filename(self):
        """
        Retrieve the filename of the Mastercard file based on the specified criteria.
        """
        filelist_df = self.sorted_download_file_df
        filter_ = filelist_df.loc[:, 'filename'].str.contains('6285990591')
        filelist_df = filelist_df.sort_values('creation time', ascending=False)
        filelist_df = filelist_df.loc[filter_]
        filelist_df = filelist_df.reset_index(drop=True)
        self.mastercard_filename = filelist_df.loc[0, 'filename']
        return self.mastercard_filename

    def get_date(self, splitted_array):
        string = [element for element in splitted_array if 'Afsluitingsdatum' in element][0]
        # Use regular expression to extract the date from the string
        date_match = re.search(r'\d{2}/\d{2}/\d{4}', string)
        self.date = date_match.group()

    def format_mastercard_df(self, df, date):
        df = df.copy()
        df['Boekingsdatum'] = [date] * df.shape[0]
        df['Boekingsdatum'] = pd.to_datetime(df['Boekingsdatum'], format='%d/%m/%Y')
        df = df[['Boekingsdatum', 'Mededelingen', 'Bedrag']]
        df['Bedrag'] = df['Bedrag'].str.replace(',', '.')
        df['Bedrag'] = df['Bedrag'].astype('float')
        # df['Boekingsdatum'] = pd.to_datetime(df['Boekingsdatum'], format = '%d/%m/%Y')
        return df

    def get_mastercard_df(self):
        pdf_filename = self.get_mastercard_filename()
        pdf_file_path = self.download_folder + '/' + pdf_filename
        # stores the text of the pages
        text_array = []
        # Open the PDF file in binary mode
        with open(pdf_file_path, 'rb') as pdf_file:
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(pdf_file_path)
            num_pages = len(pdf_reader.pages)
            # Extract text from each page
            for page_num in range(num_pages):
                # Get a specific page
                page = pdf_reader.pages[page_num]
                # Extract text from the page
                page_text = page.extract_text()
                text_array += [page_text]
        splitted_array = []
        for ii in range(len(text_array)):
            splitted_array += text_array[ii].split('\n')

        # Regex pattern to match expressions with dates and "EUR"
        pattern = r'\b\d{2}/\d{2}\b.*?EUR\b'
        # Select expressions that match the pattern
        selected_expressions = [expr for expr in splitted_array if re.search(pattern, expr)]
        # Regex pattern to extract date, description, and amount
        pattern = r'(\d{2}/\d{2}) (\d{2}/\d{2}) (.+?) (\d+,\d+) EUR'
        # Extracting data using regex
        extracted_data = [re.match(pattern, entry).groups() for entry in selected_expressions]
        # Creating DataFrame
        mastercard_df = pd.DataFrame(extracted_data,
                                     columns=['Transactiedatum', 'Boekingsdatum', 'Mededelingen', 'Bedrag'])
        date = self.get_date(splitted_array)
        # Print the DataFrame
        mastercard_df = self.format_mastercard_df(mastercard_df, date)
        return mastercard_df


    #     self.month = month
    #     self.year = year
    #     self.download_folder = r'C:\Users\User\Downloads'
    #
    #     self.excel_path = variables.excel_path
    #     self.draft_folder = variables.draft_folder
    #     self.deposit_interesting_columns = np.array(['Boekingsdatum', 'Mededelingen', 'Bedrag'])
    #     self.food_catagories = variables.food_categories
    #     self.entertainment_categories = variables.entertainment_categories
    #     self.income_categories = variables.income_categories
    #     self.remaining_categories = variables.remaining_categories
    #
    #     # for the deposit
    #     self.get_sorted_download_folder_file_df()
    #     self.get_deposit_filename()
    #     self.get_deposit_dataframe()
    #     self.format_deposit_df()
    #     self.deposit_df_to_excel()
    #
    #     # for the mastercard
    #     self.get_mastercard_filename()
    #
    # def get_sorted_download_folder_file_df(self):
    #     filelist = os.listdir(self.download_folder)
    #     time_array = []
    #     for ii in range(len(filelist)):
    #         path = self.download_folder + '\\' + filelist[ii]
    #         creation_time = os.path.getctime(path)
    #         creation_time = time.ctime(creation_time)
    #         time_array += [creation_time]
    #     filelist_df = pd.DataFrame(filelist)
    #     filelist_df = filelist_df.rename(columns={0: 'filename'})
    #     filelist_df['creation time'] = time_array
    #     filelist_df['creation time'] = pd.to_datetime(filelist_df.loc[:, 'creation time'])
    #     self.sorted_download_file_df = filelist_df
    #
    # def get_deposit_filename(self):
    #     """
    #     Retrieve the filename of the deposit file based on the specified criteria.
    #     """
    #     filelist_df = self.sorted_download_file_df
    #     filter_ = filelist_df.loc[:, 'filename'].str.contains('BE39 0635 5641 9519')
    #     filelist_df = filelist_df.sort_values('creation time', ascending=False)
    #     filelist_df = filelist_df.loc[filter_]
    #     filelist_df = filelist_df.reset_index(drop=True)
    #     self.deposit_filename = filelist_df.loc[0, 'filename']
    #
    # def get_mastercard_filename(self):
    #     """
    #     Retrieve the filename of the Mastercard file based on the specified criteria.
    #     """
    #     filelist_df = self.sorted_download_file_df
    #     filter_ = filelist_df.loc[:, 'filename'].str.contains('6285990591')
    #     filelist_df = filelist_df.sort_values('creation time', ascending=False)
    #     filelist_df = filelist_df.loc[filter_]
    #     filelist_df = filelist_df.reset_index(drop=True)
    #     self.mastercard_filename = filelist_df.loc[0, 'filename']
    #
    # def get_deposit_dataframe(self):
    #     self.deposit_df = pd.read_csv(self.download_folder + '/' + self.deposit_filename, sep=';', skiprows=12)
    #     return self.deposit_df
    #
    # def format_deposit_df(self):
    #     """
    #     Format the deposit DataFrame for further analysis.
    #     """
    #
    #     df = self.deposit_df.copy()
    #     df['Bedrag'] = df['Bedrag'].str.replace(',', '.')
    #     df['Bedrag'] = df['Bedrag'].astype('float')
    #     df['Boekingsdatum'] = pd.to_datetime(df['Boekingsdatum'], format='%d/%m/%Y')
    #
    #     # omdat sommige mensen geen mededelingen schrijven
    #     df['Mededelingen'] = df['Mededelingen'].fillna(df['Naam tegenpartij bevat'])
    #     # Use str.extract to capture everything matching the regex pattern
    #     df['Mededelingen'] = df['Mededelingen'].str.replace(r'(REF\. : \d+) VAL\. (\d{2}-\d{2})', '', regex=True)
    #     df['Mededelingen'] = df['Mededelingen'].str.replace(r'REF\. : ([A-Za-z0-9]+) VAL\. (\d{2}-\d{2})', '',
    #                                                         regex=True)
    #
    #     # replace'AANKOOP VIA INTERNET MET KAART NR 5169 2010 7988 0753  - Van den Bossche H'
    #     df['Mededelingen'] = df['Mededelingen'].str.replace(
    #         'AANKOOP VIA INTERNET MET KAART NR 5169 2010 7988 0753  - Van den Bossche H', 'AVI')
    #     # delete the extra information aout the time and date in the mededelingen of AVIs
    #     df['Mededelingen'] = df['Mededelingen'].str.replace(r'(OP \d{2}/\d{2} \d{2}:\d{2})', '', regex=True)
    #     # replace the google pay sentence
    #     df['Mededelingen'] = df['Mededelingen'].str.replace(r'(DEBITMASTERCARD-BETALING VIA Google Pay \d{2}/\d{2})',
    #                                                         'GP', regex=True)
    #     # change the contactless
    #     df['Mededelingen'] = df['Mededelingen'].str.replace(
    #         'AANKOOP BANCONTACT CONTACTLESS MET KAART NR 5169 2010  7988 0753', '')
    #     df['Mededelingen'] = df['Mededelingen'].str.replace(
    #         'AANKOOP BANCONTACT CONTACTLESS MET KAART NR 6703 0513  5238 4000', '')
    #     df['Mededelingen'] = df['Mededelingen'].str.replace('KAART NR 5169 2010 7988 0753', '')
    #     df['Mededelingen'] = df['Mededelingen'].str.replace(' - Van den Bossche H', '')
    #     df['Mededelingen'] = df['Mededelingen'].str.replace('BETALING VIA UW MOBILE BANKING APP OF UW BANCONTACT',
    #                                                         'MOBILE')
    #     self.formatted_deposit_df = df[self.deposit_interesting_columns]
    #
    # def deposit_df_to_excel(self):
    #     """
    #     Save the filtered deposit DataFrame to an Excel file.
    #     """
    #     time_filt = (self.formatted_deposit_df['Boekingsdatum'].dt.year == self.year) & (
    #                 self.formatted_deposit_df['Boekingsdatum'].dt.month == self.month)
    #     time_filt_df = self.formatted_deposit_df[time_filt].copy()
    #
    #     # filt_select_col_df.loc[:,'Category'] = [np.NaN]*filt_select_col_df.shape[0]
    #     self.deposit_filepath = self.draft_folder + '/' + self.deposit_filename[:-4] + '.xlsx'
    #     time_filt_df.to_excel(self.deposit_filepath, index=False)
    #
    # def apply_rules(self):
    #     pass
    #
    # def open_deposit_df(self):
    #     self.get_deposit_filename()
    #     self.get_deposit_dataframe()
    #     self.format_deposit_df()
    #     # Use subprocess to open Excel with the specified file
    #     subprocess.Popen([self.excel_path, self.deposit_filepath], shell=True)
    #
    # def get_categories_for_datavalidation(self):
    #     """
    #     Print all categories for data validation purposes.
    #     """
    #     concatenated_categories = np.concatenate(
    #         (self.food_catagories, self.entertainment_categories, self.income_categories, self.remaining_categories))
    #     for category in concatenated_categories:
    #         print(category + ',')


if __name__ == "__main__":
    # This code will only run if the file is executed directly.
    mastercard_1_2024 = Monthly_MasterCard_Expense(1, 2025)
    print(mastercard_1_2024.mastercard_filename)