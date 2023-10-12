from bs4 import BeautifulSoup
import requests
from openpyxl import Workbook
import datetime

def is_valid_ticker(ticker):
    return ticker.isalpha()

def get_url_and_search_data():
    while True:
        ticker = input('Please enter ticker: ').lower()
        if is_valid_ticker(ticker):
            user_input = input('Do you want annual or quarterly data? (a/q) ').lower()
            if user_input == 'a' or user_input == 'q':
                period = 'annual' if user_input == 'a' else 'quarterly'
                parameter = '' if user_input == 'a' else '?p=quarterly'
                url = f"https://stockanalysis.com/stocks/{ticker}/financials/{parameter}"
                return url, ticker, period
            else:
                print('Please enter "a" for annual or "q" for quarterly.')
        else:
            print('Invalid ticker symbol. Ticker should only contain letters.')


url, ticker, period = get_url_and_search_data()
response = requests.get(url)

# Check if the request was successful
if response.status_code != 200:
    print(f"Failed to fetch data for {ticker} - Check if the ticker is valid or the website structure has changed.")
else:
    data = BeautifulSoup(response.text, "html.parser")

    # Extract years from the table header
    table = data.table
    tr = table.contents
    header_row = tr[0]
    header_th_elements = header_row.find_all('th')
    years_list = []
    for th in header_th_elements:
        years_list.append(th.text)

    # Find the table body
    tablebody = data.tbody

    # Find all the table rows within the table body
    trs = tablebody.find_all('tr')

    # Initialize lists to store data
    revenue_list, net_income_list, share_outstanding_basic_list, share_outstanding_diluted_list, eps_diluted_list, free_cash_flow_list, free_cash_flow_per_share_list = [], [], [], [], [], [], []
    
    for index, row in enumerate(trs):
        # Find the first cell (td) in each row
        first_cell = row.find('td')

        # Check for various data categories
        if 'Revenue' in first_cell.text and len(first_cell.text) < 10:
            revenue_row = trs[index]
            for revenue in revenue_row:
                revenue_list.append(revenue.text)
        elif 'Net Income' in first_cell.text and len(first_cell.text) < 15:
            net_income_row = trs[index]
            for net_income in net_income_row:
                net_income_list.append(net_income.text)
        elif 'Shares Outstanding (Basic)' in first_cell.text:
            share_outstanding_basic_row = trs[index]
            for share_outstanding_basic in share_outstanding_basic_row:
                share_outstanding_basic_list.append(share_outstanding_basic.text)
        elif 'Shares Outstanding (Diluted)' in first_cell.text:
            share_outstanding_diluted_row = trs[index]
            for share_outstanding_diluted in share_outstanding_diluted_row:
                share_outstanding_diluted_list.append(share_outstanding_diluted.text)
        elif 'EPS (Diluted)' in first_cell.text:
            eps_diluted_row = trs[index]
            for eps_diluted in eps_diluted_row:
                eps_diluted_list.append(eps_diluted.text)
        elif 'Free Cash Flow' in first_cell.text and len(first_cell.text) < 18:
            free_cash_flow_row = trs[index]
            for free_cash_flow in free_cash_flow_row:
                free_cash_flow_list.append(free_cash_flow.text)
        elif 'Free Cash Flow Per Share' in first_cell.text:
            free_cash_flow_per_share_row = trs[index]
            for free_cash_flow_per_share in free_cash_flow_per_share_row:
                free_cash_flow_per_share_list.append(free_cash_flow_per_share.text)
        
    # Remove empty spaces from lists
    revenue_list_without_spaces = [i for i in revenue_list if i != ' ']
    net_income_list_without_spaces = [i for i in net_income_list if i != ' ']
    share_outstanding_basic_list_without_spaces = [i for i in share_outstanding_basic_list if i != ' ']
    share_outstanding_diluted_list_without_spaces = [i for i in share_outstanding_diluted_list if i != ' ']
    eps_diluted_list_without_spaces = [i for i in eps_diluted_list if i != ' ']
    free_cash_flow_list_without_spaces = [i for i in free_cash_flow_list if i != ' ']
    free_cash_flow_per_share_list_without_spaces = [i for i in free_cash_flow_per_share_list if i != ' ']

    # Clean the years list (remove the last element)
    clean_years_list = years_list[:-1]
    clean_revenue_list = revenue_list_without_spaces[:-1]
    clean_net_income_list = net_income_list_without_spaces[:-1]
    clean_share_outstanding_basic_list = share_outstanding_basic_list_without_spaces[:-1]
    clean_share_outstanding_diluted_list = share_outstanding_diluted_list_without_spaces[:-1]
    clean_eps_diluted_list = eps_diluted_list_without_spaces[:-1]
    clean_free_cash_flow_list = free_cash_flow_list_without_spaces[:-1]
    clean_free_cash_flow_per_share_list = free_cash_flow_per_share_list_without_spaces[:-1]

    # Create a new Excel workbook and save the data
    wb = Workbook()
    ws = wb.active
    ws.title = f"{ticker.upper()} {period.upper()} ANALYSIS"

    current_time = datetime.datetime.now()
    current_time_to_string = str(current_time)

    ws.append(clean_years_list)
    ws.append(clean_revenue_list)
    ws.append(clean_net_income_list)
    ws.append(clean_share_outstanding_basic_list)
    ws.append(clean_share_outstanding_diluted_list)
    ws.append(clean_eps_diluted_list)
    ws.append(clean_free_cash_flow_list)
    ws.append(clean_free_cash_flow_per_share_list)
    wb.save(f"{ticker}{period}analysis{current_time_to_string}.xlsx")
    print(f"Data for {ticker} ({period}) has been successfully scraped and saved to an Excel file.")