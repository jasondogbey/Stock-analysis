from bs4 import BeautifulSoup
import requests
from openpyxl import Workbook

# Function to validate tickers
def is_valid_ticker(ticker):
    ticker_without_space = ticker.replace(" ", "")
    ticker_list = ticker_without_space.split(",")
    for ticker in ticker_list:
        if not ticker.isalpha():
            return False
    return ticker_list

# Function to get URLs and search data
def get_url_and_search_data():
    while True:
        ticker = input('Please enter tickers separated by a comma: ').lower()
        if is_valid_ticker(ticker):
            ticker_list = is_valid_ticker(ticker)
            break
        else:
            print('Invalid ticker symbol. Ticker should only contain letters.')

    while True:
        user_input = input('Do you want annual or quarterly data? (a/q) ').lower()
        if user_input == 'a' or user_input == 'q':
            parameter = '' if user_input == 'a' else '?p=quarterly'
            url_list = []
            for ticker in ticker_list:
                url = f"https://stockanalysis.com/stocks/{ticker}/financials/{parameter}"
                url_list.append(url)
            return url_list, ticker_list
        else:
            print('Please enter "a" for annual or "q" for quarterly.')
        
# Function to fetch data from a URL
def fetch_data(ticker, url):
    response = requests.get(url)
    result = []
    # Check if the request was successful
    if response.status_code != 200:
        error_message = f"Failed to fetch data for {ticker} - Check if the ticker is valid or the website structure has changed."
        result.append([error_message])
        return result
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

        result.append(clean_years_list)
        result.append(clean_revenue_list)
        result.append(clean_net_income_list)
        result.append(clean_share_outstanding_basic_list)
        result.append(clean_share_outstanding_diluted_list)
        result.append(clean_eps_diluted_list)
        result.append(clean_free_cash_flow_list)
        result.append(clean_free_cash_flow_per_share_list)
    return result

# Function to save data to an Excel file
def save_to_excel_file(results):
    # Create a new Excel workbook and save the data
    wb = Workbook()
    for sheet_data in results:
        for sheet_name, data in sheet_data.items():
            ws = wb.create_sheet(title=sheet_name)
            
            for item in data:
                ws.append(item)
               
    # Remove the default "Sheet" that is created by default
    default_sheet = wb["Sheet"]
    wb.remove(default_sheet)
    file_name = input("Please enter a name for the excel file: ")
    wb.save(f"{file_name}.xlsx")
    print(f"Your data has been saved to an Excel file with filename {file_name}.xlsx")

# Main function
def main():
    url_list, ticker_list = get_url_and_search_data()
    url_ticker_dict = dict(zip(ticker_list, url_list))
    results = []
    for ticker, url in url_ticker_dict.items():
        result = fetch_data(ticker, url)
        result_dict = {ticker: result}
        results.append(result_dict)
    
    save_to_excel_file(results)

if __name__ == "__main__":
    main()