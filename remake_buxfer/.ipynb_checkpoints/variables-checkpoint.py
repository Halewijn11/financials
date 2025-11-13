import numpy as np

excel_path = r'C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE'
draft_folder = r'C:\Users\User\OneDrive\Documenten\financials\remake_buxfer\draft_folder'
food_categories = np.array(['food/groceries', 'food/restaurants', 'food/studentenrestaurant'])
entertainment_categories = np.array(['entertainment', 'entertainment/drinks'])
income_categories = np.array(['income', 'parental income'])
remaining_categories = np.array(['sports','trips', 'parental refund', 'transportation', 'gifts', 'unforesceen expenses'])
download_folder = r'C:\Users\User\Downloads'
interesting_columns = np.array(['date', 'description', 'amount'])

remake_buxfer_path = r'C:\Users\User\OneDrive\Documenten\financials\remake_buxfer'
deposit_folder_path = remake_buxfer_path + '/' + 'deposit_folder'
mastercard_folder_path = remake_buxfer_path + '/' + 'mastercard_folder'

raw_deposit_csv_path = deposit_folder_path + '/' + 'raw_csv_files'
deposit_excel_path = deposit_folder_path + '/' + 'excel_files'

raw_mastercard_pdf_path = mastercard_folder_path + '/' + 'raw_pdf_files'
mastercard_excel_path = mastercard_folder_path + '/' + 'excel_files'


# raw_belfius_csv_path = r'C:\Users\User\OneDrive\Documenten\financials\remake_buxfer\deposit_folder\raw_belfius_csv_files'