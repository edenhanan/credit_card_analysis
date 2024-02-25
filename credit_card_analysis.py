import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os

def clean_data(df):
    df.columns = df.iloc[2]
    df = df[3:]
    df = df[:-3]
    return df

def generate_days_series(month, year):
    start_date = f'{year}-{month}-10'
    if month == 12:
        end_date = f'{year+1}-01-09'
    else:
        end_date = f'{year}-{month+1}-09'
    dates = pd.date_range(start=start_date, end=end_date)
    return dates

def clean_concat_dataframes(dataframes: dict):
    for key in dataframes.keys():
        dataframes[key] = clean_data(dataframes[key])
    return pd.concat(dataframes, ignore_index=True)

def open_excel_file_path():
    root = Tk()
    root.attributes('-topmost', True)
    root.withdraw()
    filename = askopenfilename(filetypes=[("Excel files", "*.xlsx")], initialdir=os.getcwd(), title="Select Excel File")
    return filename

def getcredit_card_data():
    filename = open_excel_file_path()
    dataframes = pd.read_excel(filename, sheet_name=None)
    df = clean_concat_dataframes(dataframes)
    df = add_month_column(df)
    return df

def add_month_column(df):
    
    df['תאריך עסקה'] = pd.to_datetime(df['תאריך עסקה'], format='%d-%m-%Y')
    df['תאריך חיוב'] = pd.to_datetime(df['תאריך חיוב'], format='%d-%m-%Y')
    df['סכום חיוב'] = df['סכום חיוב'].astype(float)
    
    df['month'] = pd.to_datetime(df['תאריך חיוב']).dt.to_period('M') - 1
    # df['month'] = df['תאריך חיוב']
    return df

def calculate_monthly_expenses(df):
    unique_dates = df['month'].unique()
    months = []
    years = []

    for date in unique_dates:
        month = date.month
        year = date.year
        dates = generate_days_series(month, year)
        df_period = df[df['month'] == date]
        month_list = df_period['month'].tolist()
        month_list = month_list[0:len(dates)]
        print(f'{month}-{year}')
        cumulative_sum = [round(df_period[df_period['תאריך עסקה'] <= i]['סכום חיוב'].sum(), 2) for i in dates]
        cumulative_df = pd.DataFrame({'date': dates, 'cumulative_sum': cumulative_sum, 'month': month_list})
        # cumulative_sum = { str(i.date()): }
    return cumulative_df

def plot_monthly_expenses(cumulative_sum):
    pass

if __name__ == '__main__':
    df = getcredit_card_data()
    cumulative_sum = calculate_monthly_expenses(df)
    print(cumulative_sum)