from bs4 import BeautifulSoup
import requests

# def get_url():
#     while True:
#         ticker = input('Please enter ticker: ').lower()
#         period = input('Do you want annually or quarterly data? (a/q) ').lower()
#         if period == 'a':
#             url = f"https://stockanalysis.com/stocks/{ticker}/financials/"
#             return url
#         elif period == 'q':
#             url = f"https://stockanalysis.com/stocks/{ticker}/financials/?p=quarterly"
#             return url
#         else:
#             print('Please enter a or q')

url = "https://stockanalysis.com/stocks/zbra/financials/?p=quarterly"
response = requests.get(url).text
data = BeautifulSoup(response, "html.parser")

table = data.table
tr = table.contents
header_row = tr[0]
header_th_elements = header_row.find_all('th')
years_list = []
for th in header_th_elements:
    years_list.append(th.text)
print(years_list)

tablebody = data.tbody
# trs = tablebody.contents

# Find all the table rows within the table body
trs = tablebody.find_all('tr')

revenue_list, net_income_list, share_outstanding_basic_list, share_outstanding_diluted_list, eps_diluted_list, free_cash_flow_list, free_cash_flow_per_share_list = [], [], [], [], [], [], []
# Loop through the rows, excluding the header row
for index, row in enumerate(trs):
    # Find the first cell (td) in each row
    first_cell = row.find('td')

    if 'Revenue' in first_cell.text and len(first_cell.text) < 10:
        print('There is revenue')
        revenue_row = trs[index]
        
        for revenue in revenue_row:
            revenue_list.append(revenue.text)
        print(revenue_list)
    elif 'Net Income' in first_cell.text and len(first_cell.text) < 15:
        print('There is net income')
        net_income_row = trs[index]
        for net_income in net_income_row:
            net_income_list.append(net_income.text)
        print(net_income_list)
    elif 'Shares Outstanding (Basic)' in first_cell.text:
        print('There is shares outstanding basic')
        share_outstanding_basic_row = trs[index]
        for share_outstanding_basic in share_outstanding_basic_row:
            share_outstanding_basic_list.append(share_outstanding_basic.text)
        print(share_outstanding_basic_list)
    elif 'Shares Outstanding (Diluted)' in first_cell.text:
        print('There is shares outstanding diluted')
        share_outstanding_diluted_row = trs[index]
        for share_outstanding_diluted in share_outstanding_diluted_row:
            share_outstanding_diluted_list.append(share_outstanding_diluted.text)
        print(share_outstanding_diluted_list)
    elif 'EPS (Diluted)' in first_cell.text:
        print('There is eps diluted')
        eps_diluted_row = trs[index]
        for eps_diluted in eps_diluted_row:
            eps_diluted_list.append(eps_diluted.text)
        print(eps_diluted_list)
    elif 'Free Cash Flow' in first_cell.text and len(first_cell.text) < 18:
        print('There is free cash flow')
        free_cash_flow_row = trs[index]
        for free_cash_flow in free_cash_flow_row:
            free_cash_flow_list.append(free_cash_flow.text)
        print(free_cash_flow_list)
    elif 'Free Cash Flow Per Share' in first_cell.text:
        print('There is free cash flow per share')
        free_cash_flow_per_share_row = trs[index]
        for free_cash_flow_per_share in free_cash_flow_per_share_row:
            free_cash_flow_per_share_list.append(free_cash_flow_per_share.text)
        print(free_cash_flow_per_share_list)
    
    # Check if a td element is found (to exclude header rows without td)
    
    # print(first_cell.text)