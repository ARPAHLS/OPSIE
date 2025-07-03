import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
from colorama import Fore, Style
import re
import time
import statsmodels.api as sm  # New import for ARIMA model
from pytz import timezone

# Native Modules
from markets_mappings import keyword_mapping

# Create a reverse mapping for case-insensitive lookup
reverse_mapping = {ticker.lower(): name for name, ticker in keyword_mapping['companies'].items()}

def handle_markets_command(command):
    # Ensure the command starts with /markets and extract the rest
    if not command.lower().startswith('/markets'):
        return Fore.RED + "Error: Command must start with '/markets'."

    # Remove the '/markets' prefix and strip any extra whitespace
    command = command[len('/markets'):].strip()
    
    sectors = keyword_mapping['sectors']
    companies = keyword_mapping['companies']
    currencies = keyword_mapping['currencies']
    cryptocurrencies = keyword_mapping['cryptocurrencies']

    # Split the remaining command into parts
    parts = command.lower().split()

    # Check if at least one keyword is provided
    if len(parts) < 1:
        return Fore.YELLOW + "Please provide a company, sector, currency, or crypto after '/markets'."

    keyword = parts[0]
    extra = parts[1] if len(parts) > 1 else None

    # Handle compare command
    if keyword == 'compare' and len(parts) == 3:
        stock1_input = parts[1]
        stock2_input = parts[2]
        return stock_compare(stock1_input, stock2_input)
    
    # Handle the new oil full report
    if keyword == 'oil' and extra == 'full':
        return generate_oil_market_report()

    # Handle sector commands
    if keyword in sectors:
        tickers = sectors[keyword]
        return display_sector_data(keyword, tickers)
    
    # Handle currency and cryptocurrency commands
    if keyword in currencies:
        return display_currency_data(keyword, currencies[keyword])
    elif keyword in cryptocurrencies:
        return display_crypto_data(keyword, cryptocurrencies[keyword])
    
    # Handle company commands
    elif keyword in companies:
        ticker = companies[keyword]
        # Check if there's an extra command
        if extra:
            return handle_company_extra(keyword, ticker, extra)
        return display_company_data(keyword, ticker)
    
    # If the keyword is not recognized, return an error message
    return Fore.RED + f"Error: The company, sector, currency, or crypto '{keyword}' is not recognized. Please check the name and try again."

def handle_company_extra(company_name, ticker, extra):
    if not extra:
        return display_company_data(company_name, ticker)
    else:
        extra = extra.lower()
        try:
            if extra == 'statistics':
                return display_statistics(ticker)
            elif extra == 'history':
                return display_history(ticker)
            elif extra == 'profile':
                return display_profile(ticker)
            elif extra == 'financials':
                return display_financials(ticker)
            elif extra == 'analysis':
                return display_analysis(ticker)
            elif extra == 'options':
                return display_options(ticker)
            elif extra == 'holders':
                return display_holders(ticker)
            elif extra == 'sustainability':
                return display_sustainability(ticker)
            else:
                return Fore.RED + f"Invalid extra command: {extra}"
        except Exception as e:
            return Fore.RED + f"An error occurred while processing the command: {str(e)}"

def display_sector_data(sector_name, tickers):
    output = f"\nTop stocks in the {Fore.LIGHTYELLOW_EX}{sector_name.capitalize()} sector{Fore.RESET}:\n\n"
    for idx, ticker in enumerate(tickers, start=1):
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1y")
        data = {
            '1D': get_percentage_change(hist, days=1),
            '5D': get_percentage_change(hist, days=5),
            '1M': get_percentage_change(hist, days=30),
            '1Y': get_percentage_change(hist, days=365)
        }
        # Company name in light yellow
        output += Fore.LIGHTYELLOW_EX + f"{idx}. {stock.info.get('shortName', ticker)} ({ticker}){Fore.RESET}\n"
        # Performance data
        performance_line = (
            Fore.WHITE + f"   1D: {format_percentage_change(data['1D'])} | " +
            Fore.WHITE + f"5D: {format_percentage_change(data['5D'])} | " +
            Fore.WHITE + f"1M: {format_percentage_change(data['1M'])} | " +
            Fore.WHITE + f"1Y: {format_percentage_change(data['1Y'])}"
        )
        output += performance_line + '\n'
        # Generate ASCII chart
        hist_chart = stock.history(period="1mo")  # last 1 month data
        prices = hist_chart['Close'].tolist()
        if len(prices) >= 2:
            chart = generate_sparkline(prices)
            # Determine the color based on last month's percentage change
            if data['1M'] > 0:
                chart_color = Fore.LIGHTGREEN_EX
            elif data['1M'] < 0:
                chart_color = Fore.RED
            else:
                chart_color = Fore.CYAN
            output += Fore.WHITE + f"   Price Chart (Last 1 Month):\n"
            output += f"   {chart_color}{chart}{Fore.RESET}\n"
        else:
            output += Fore.RED + "   Not enough data to generate chart.\n"
        output += "\n"
    return output

def display_company_data(company_name, ticker):
    output = ''
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1y")
    data = {
        '1D': get_percentage_change(hist, days=1),
        '5D': get_percentage_change(hist, days=5),
        '1M': get_percentage_change(hist, days=30),
        '1Y': get_percentage_change(hist, days=365)
    }
    # Company name in light yellow
    output += f"\nMarket data for {Fore.LIGHTYELLOW_EX}{stock.info.get('shortName', company_name.capitalize())} ({ticker}):{Fore.RESET}\n\n"
    # Current price
    current_price = stock.info.get('regularMarketPrice', 'N/A')
    if current_price != 'N/A':
        current_price = f"${current_price:.2f}"
    # Performance data
    performance_line = (
        f"   {Fore.LIGHTCYAN_EX}Current Price:{Fore.RESET} {Fore.LIGHTGREEN_EX}{current_price}{Fore.RESET}\n" +
        Fore.WHITE + f"   1D: {format_percentage_change(data['1D'])} | " +
        Fore.WHITE + f"5D: {format_percentage_change(data['5D'])} | " +
        Fore.WHITE + f"1M: {format_percentage_change(data['1M'])} | " +
        Fore.WHITE + f"1Y: {format_percentage_change(data['1Y'])}"
    )
    output += performance_line + '\n'
    # Generate ASCII chart
    hist_chart = stock.history(period="1mo")  # last 1 month data
    prices = hist_chart['Close'].tolist()
    if len(prices) >= 2:
        chart = generate_sparkline(prices)
        # Determine the color based on last month's percentage change
        if data['1M'] > 0:
            chart_color = Fore.LIGHTGREEN_EX
        elif data['1M'] < 0:
            chart_color = Fore.RED
        else:
            chart_color = Fore.CYAN
        output += Fore.WHITE + f"\n   Price Chart (Last 1 Month):\n"
        output += f"   {chart_color}{chart}{Fore.RESET}\n"
    else:
        output += Fore.RED + "\n   Not enough data to generate chart.\n"
    # Top News
    news = stock.news[:5]
    if news:
        output += Fore.WHITE + "\n   Top News:\n\n"
        for article in news:
            output += Fore.LIGHTBLUE_EX + f"     - {article['title']}\n"
            output += Fore.WHITE + f"       {article['link']}\n"
        output += '\n'
    else:
        output += Fore.RED + "   No recent news articles found.\n\n"
    return output

def display_statistics(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    output = f"\nKey Statistics for {Fore.LIGHTYELLOW_EX}{info.get('shortName', ticker)} ({ticker}):{Fore.RESET}\n\n"
    try:
        # Valuation Measures
        output += Fore.LIGHTYELLOW_EX + "Valuation Measures:\n" + Fore.RESET
        valuation_keys = [
            'marketCap', 'enterpriseValue', 'trailingPE', 'forwardPE',
            'priceToSalesTrailing12Months', 'priceToBook', 'enterpriseToRevenue',
            'enterpriseToEbitda'
        ]
        for key in valuation_keys:
            value = info.get(key, 'N/A')
            if value != 'N/A':
                if key in ['marketCap', 'enterpriseValue']:
                    value = format_currency(value)
                else:
                    value = f"{value:.2f}"
            output += f"   {Fore.LIGHTCYAN_EX}{key}:{Fore.RESET} {value}\n"
        output += "\n"
        # Financial Highlights
        output += Fore.LIGHTYELLOW_EX + "Financial Highlights:\n" + Fore.RESET
        financial_keys = [
            'ebitdaMargins', 'profitMargins', 'grossMargins', 'operatingMargins',
            'returnOnAssets', 'returnOnEquity', 'revenue', 'revenuePerShare',
            'quarterlyRevenueGrowth', 'grossProfits', 'ebitda', 'netIncomeToCommon'
        ]
        for key in financial_keys:
            value = info.get(key, 'N/A')
            if value != 'N/A':
                if 'Margins' in key or 'returnOn' in key or 'quarterlyRevenueGrowth' in key:
                    value = format_percentage(value)
                elif key in ['revenue', 'revenuePerShare', 'grossProfits', 'ebitda', 'netIncomeToCommon']:
                    value = format_currency(value)
                else:
                    value = f"{value:.2f}"
            output += f"   {Fore.LIGHTCYAN_EX}{key}:{Fore.RESET} {value}\n"
    except Exception as e:
        output += Fore.RED + "   Unable to retrieve key statistics.\n"
    return output

def display_history(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1y")
    output = f"\nHistorical Data for {Fore.LIGHTYELLOW_EX}{stock.info.get('shortName', ticker)} ({ticker}):{Fore.RESET}\n\n"
    if not hist.empty:
        # Select relevant columns and format index
        hist = hist[['Open', 'High', 'Low', 'Close', 'Volume']]
        hist.index = hist.index.strftime('%Y-%m-%d')
        output += hist.tail(10).to_string()
    else:
        output += Fore.RED + "   No historical data available.\n"
    return output

def display_profile(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    output = f"\nProfile for {Fore.LIGHTYELLOW_EX}{info.get('shortName', ticker)} ({ticker}):{Fore.RESET}\n\n"
    output += f"   {Fore.LIGHTCYAN_EX}Industry:{Fore.RESET} {info.get('industry', 'N/A')}\n"
    output += f"   {Fore.LIGHTCYAN_EX}Sector:{Fore.RESET} {info.get('sector', 'N/A')}\n"
    output += f"   {Fore.LIGHTCYAN_EX}Full Time Employees:{Fore.RESET} {info.get('fullTimeEmployees', 'N/A')}\n"
    output += f"   {Fore.LIGHTCYAN_EX}Website:{Fore.RESET} {info.get('website', 'N/A')}\n"
    output += f"\n   {Fore.LIGHTYELLOW_EX}Description:{Fore.RESET}\n\n"
    output += f"   {info.get('longBusinessSummary', 'N/A')}\n"
    return output

def display_financials(ticker):
    stock = yf.Ticker(ticker)
    output = f"\nFinancials for {Fore.LIGHTYELLOW_EX}{stock.info.get('shortName', ticker)} ({ticker}):{Fore.RESET}\n"

    # Income Statement
    income_stmt = stock.financials
    if not income_stmt.empty:
        output += f"\n{Fore.LIGHTYELLOW_EX}Income Statement (in thousands):{Fore.RESET}\n"
        income_stmt = income_stmt / 1000  # Convert to thousands for readability
        income_stmt = income_stmt.transpose()
        income_stmt.index = income_stmt.index.strftime('%Y-%m-%d')
        # Ensure the required columns are present
        income_columns = ['Total Revenue', 'Cost Of Revenue', 'Gross Profit', 'Operating Income', 'Net Income']
        existing_columns = [col for col in income_columns if col in income_stmt.columns]
        income_stmt = income_stmt[existing_columns]
        output += income_stmt.to_string()
    else:
        output += Fore.RED + "\n   No income statement data available.\n"

    # Balance Sheet
    balance_sheet = stock.balance_sheet
    if not balance_sheet.empty:
        output += f"\n\n{Fore.LIGHTYELLOW_EX}Balance Sheet (in thousands):{Fore.RESET}\n"
        balance_sheet = balance_sheet / 1000  # Convert to thousands
        balance_sheet = balance_sheet.transpose()
        balance_sheet.index = balance_sheet.index.strftime('%Y-%m-%d')
        # Ensure the required columns are present
        balance_columns = ['Total Assets', 'Total Liab', 'Total Stockholder Equity']
        existing_columns = [col for col in balance_columns if col in balance_sheet.columns]
        balance_sheet = balance_sheet[existing_columns]
        output += balance_sheet.to_string()
    else:
        output += Fore.RED + "\n   No balance sheet data available.\n"

    # Cash Flow Statement
    cash_flow = stock.cashflow
    if not cash_flow.empty:
        output += f"\n\n{Fore.LIGHTYELLOW_EX}Cash Flow Statement (in thousands):{Fore.RESET}\n"
        cash_flow = cash_flow / 1000  # Convert to thousands
        cash_flow = cash_flow.transpose()
        cash_flow.index = cash_flow.index.strftime('%Y-%m-%d')
        # Ensure the required columns are present
        cash_flow_columns = ['Total Cash From Operating Activities', 'Total Cashflows From Investing Activities', 'Total Cash From Financing Activities']
        existing_columns = [col for col in cash_flow_columns if col in cash_flow.columns]
        cash_flow = cash_flow[existing_columns]
        output += cash_flow.to_string()
    else:
        output += Fore.RED + "\n   No cash flow data available.\n"

    return output

def display_analysis(ticker):
    stock = yf.Ticker(ticker)
    company_name = stock.info.get('shortName', ticker)
    output = f"\nAnalysis for {Fore.LIGHTYELLOW_EX}{company_name} ({ticker}):{Fore.RESET}\n"

    # Analyst Recommendations
    recommendations = stock.recommendations

    if recommendations is not None and not recommendations.empty:
        output += Fore.LIGHTYELLOW_EX + "\nRecent Analyst Recommendations:\n" + Fore.RESET

        # Take the last 5 recommendations and create a copy
        recs = recommendations.tail(5).copy()

        # Reset index to include 'Date' as a column
        recs.reset_index(inplace=True)

        # Format 'Date' column
        if 'Date' in recs.columns:
            recs['Date'] = recs['Date'].dt.strftime('%Y-%m-%d')
        else:
            recs.rename(columns={'index': 'Date'}, inplace=True)
            recs['Date'] = recs['Date'].astype(str)

        # Ensure required columns are present
        required_columns = ['Date', 'Firm', 'To Grade', 'From Grade', 'Action']
        for col in required_columns:
            if col not in recs.columns:
                recs.loc[:, col] = 'N/A'

        # Select required columns
        recs_display = recs[required_columns]
        output += recs_display.to_string(index=False)
    else:
        output += Fore.RED + "\n   No analyst recommendations available.\n"

    output += "\n\n"

    # Price Target
    price_target = stock.info.get('targetMeanPrice', 'N/A')
    number_of_analysts = stock.info.get('numberOfAnalystOpinions', 'N/A')

    output += Fore.LIGHTYELLOW_EX + "Analyst Price Target:\n" + Fore.RESET
    output += f"   {Fore.LIGHTCYAN_EX}Target Mean Price:{Fore.RESET} {price_target}\n"
    output += f"   {Fore.LIGHTCYAN_EX}Number of Analysts:{Fore.RESET} {number_of_analysts}\n"

    return output

def display_options(ticker):
    stock = yf.Ticker(ticker)
    options_dates = stock.options
    output = f"\nOptions for {Fore.LIGHTYELLOW_EX}{stock.info.get('shortName', ticker)} ({ticker}):{Fore.RESET}\n\n"
    if options_dates:
        output += Fore.LIGHTYELLOW_EX + "Available Options Expiration Dates:\n" + Fore.RESET
        for date in options_dates:
            output += f"   {date}\n"
        nearest_date = options_dates[0]
        options_chain = stock.option_chain(nearest_date)
        output += f"\nOptions Chain for {nearest_date} (Showing top 5 calls and puts):\n\n"
        output += Fore.LIGHTYELLOW_EX + "Calls:\n" + Fore.RESET
        calls = options_chain.calls.head(5)
        output += calls.to_string(index=False)
        output += "\n\n" + Fore.LIGHTYELLOW_EX + "Puts:\n" + Fore.RESET
        puts = options_chain.puts.head(5)
        output += puts.to_string(index=False)
    else:
        output += Fore.RED + "   No options data available.\n"
    return output

def display_holders(ticker):
    stock = yf.Ticker(ticker)
    major_holders = stock.major_holders
    institutional_holders = stock.institutional_holders
    output = f"\nHolders for {Fore.LIGHTYELLOW_EX}{stock.info.get('shortName', ticker)} ({ticker}):{Fore.RESET}\n\n"
    if major_holders is not None and not major_holders.empty:
        output += Fore.LIGHTYELLOW_EX + "Major Holders:\n" + Fore.RESET
        output += major_holders.to_string(index=False, header=False)
    else:
        output += Fore.RED + "   No major holders data available.\n"
    output += "\n\n"
    if institutional_holders is not None and not institutional_holders.empty:
        output += Fore.LIGHTYELLOW_EX + "Top Institutional Holders:\n" + Fore.RESET
        output += institutional_holders.head(10).to_string(index=False)
    else:
        output += Fore.RED + "   No institutional holders data available.\n"
    return output

def display_sustainability(ticker):
    stock = yf.Ticker(ticker)
    sustainability = stock.sustainability
    output = f"\nSustainability for {Fore.LIGHTYELLOW_EX}{stock.info.get('shortName', ticker)} ({ticker}):{Fore.RESET}\n"
    if sustainability is not None and not sustainability.empty:
        # Reset index to turn metrics into a column
        sus = sustainability.reset_index()
        sus.columns = ['Metric', 'Value']
        # Format the DataFrame for display
        output += "\n" + Fore.LIGHTYELLOW_EX + "Sustainability Metrics:\n" + Fore.RESET
        output += sus.to_string(index=False)
    else:
        output += Fore.RED + "\n   No sustainability data available.\n"
    return output

def get_percentage_change(hist, days):
    try:
        end_price = hist['Close'][-1]
        if len(hist) >= days:
            start_price = hist['Close'][-days]
        else:
            start_price = hist['Close'][0]
        return ((end_price - start_price) / start_price) * 100
    except Exception:
        return 0.0

def format_percentage_change(value):
    if value > 0:
        return Fore.LIGHTGREEN_EX + f"+{value:.2f}%" + Fore.RESET
    elif value < 0:
        return Fore.RED + f"{value:.2f}%" + Fore.RESET
    else:
        return Fore.WHITE + "0.00%" + Fore.RESET

def format_percentage(value):
    try:
        value = float(value) * 100
        if value > 0:
            return Fore.LIGHTGREEN_EX + f"{value:.2f}%" + Fore.RESET
        elif value < 0:
            return Fore.RED + f"{value:.2f}%" + Fore.RESET
        else:
            return Fore.WHITE + "0.00%" + Fore.RESET
    except:
        return 'N/A'

def format_currency(value):
    try:
        value = float(value)
        if value >= 1e12:
            return f"${value/1e12:.2f}T"
        elif value >= 1e9:
            return f"${value/1e9:.2f}B"
        elif value >= 1e6:
            return f"${value/1e6:.2f}M"
        elif value >= 1e3:
            return f"${value/1e3:.2f}K"
        else:
            return f"${value:.2f}"
    except:
        return 'N/A'

def generate_sparkline(data):
    if not data:
        return ''
    
    # Remove NaN values from the data
    data = [x for x in data if x == x]  # Simple NaN check: NaN is the only value that doesn't equal itself
    
    if not data:  # Check again if data is empty after removing NaNs
        return ''
    
    min_data = min(data)
    max_data = max(data)
    data_range = max_data - min_data if max_data - min_data != 0 else 1
    scaled_data = [(x - min_data) / data_range for x in data]
    spark_chars = '▁▂▃▄▅▆▇█'
    result = ''
    
    for x in scaled_data:
        index = int(x * (len(spark_chars) - 1))
        result += spark_chars[index]
    
    return result

# Function to strip ANSI color codes for width calculation
def strip_ansi_codes(text):
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)

# Utility Functions for formatting
def format_percentage_no_color(value):
    try:
        value = float(value) * 100
        return f"{value:.2f}%"
    except:
        return 'N/A'

def format_currency_no_color(value):
    try:
        value = float(value)
        if value >= 1e12:
            return f"${value/1e12:.2f}T"
        elif value >= 1e9:
            return f"${value/1e9:.2f}B"
        elif value >= 1e6:
            return f"${value/1e6:.2f}M"
        elif value >= 1e3:
            return f"${value/1e3:.2f}K"
        else:
            return f"${value:.2f}"
    except:
        return 'N/A'
    
def format_number(value):
    try:
        return f"{value:,.0f}"
    except:
        return 'N/A'
    
def display_currency_data(keyword, currency_code):
    try:
        currency_pair = f"{currency_code}=X"
        currency = yf.Ticker(currency_pair)
        hist = currency.history(period="1y")

        data = {
            '1D': get_percentage_change(hist, days=1),
            '5D': get_percentage_change(hist, days=5),
            '1M': get_percentage_change(hist, days=30),
            '1Y': get_percentage_change(hist, days=365)
        }

        output = f"\nMarket data for {Fore.LIGHTYELLOW_EX}{currency_code} (Currency):{Fore.RESET}\n\n"
        current_price = currency.info.get('regularMarketPrice', 'N/A')
        if current_price != 'N/A':
            current_price = f"${current_price:,.2f}"

        performance_line = (
            f"{Fore.LIGHTCYAN_EX}   Current Price:{Fore.RESET} {Fore.LIGHTGREEN_EX}{current_price}{Fore.RESET}\n" +
            Fore.WHITE + f"   1D: {format_percentage_change(data['1D'])} | " +
            f"5D: {format_percentage_change(data['5D'])} | " +
            f"1M: {format_percentage_change(data['1M'])} | " +
            f"1Y: {format_percentage_change(data['1Y'])}"
        )
        output += performance_line + "\n"
        hist_chart = currency.history(period="1mo")
        prices = hist_chart['Close'].tolist()
        if len(prices) >= 2:
            chart = generate_sparkline(prices)
            chart_color = Fore.LIGHTGREEN_EX if data['1M'] > 0 else Fore.RED if data['1M'] < 0 else Fore.CYAN
            output += Fore.WHITE + "   Price Chart (Last 1 Month):\n"
            output += f"   {chart_color}{chart}{Fore.RESET}\n"
        else:
            output += Fore.RED + "   Not enough data to generate chart.\n"

        output += Fore.WHITE + "\nAdditional Data:\n\n"
        output += f"{Fore.LIGHTCYAN_EX}   52 Week Range:{Fore.RESET} {currency.info.get('fiftyTwoWeekLow', 'N/A')} - {currency.info.get('fiftyTwoWeekHigh', 'N/A')}\n"
        output += f"{Fore.LIGHTCYAN_EX}   Volume (24hr):{Fore.RESET} {format_number(currency.info.get('volume', 'N/A'))} (units)\n"
        output += f"{Fore.LIGHTCYAN_EX}   Market Cap:{Fore.RESET} {format_number(currency.info.get('marketCap', 'N/A'))} USD\n"

        return output
    except Exception as e:
        return Fore.RED + f"Error fetching data for {currency_code}: {str(e)}"

def display_crypto_data(keyword, crypto_code):
    try:
        crypto = yf.Ticker(crypto_code)
        hist = crypto.history(period="1y")

        data = {
            '1D': get_percentage_change(hist, days=1),
            '5D': get_percentage_change(hist, days=5),
            '1M': get_percentage_change(hist, days=30),
            '1Y': get_percentage_change(hist, days=365)
        }

        crypto_name = crypto_code.split('-')[0].upper()
        output = f"\nMarket data for {Fore.LIGHTYELLOW_EX}{crypto_name} (Crypto):{Fore.RESET}\n\n"
        current_price = crypto.info.get('regularMarketPrice', 'N/A')
        if current_price != 'N/A':
            current_price = f"${current_price:,.2f}"

        performance_line = (
            f"{Fore.LIGHTCYAN_EX}   Current Price:{Fore.RESET} {Fore.LIGHTGREEN_EX}{current_price}{Fore.RESET}\n" +
            Fore.WHITE + f"   1D: {format_percentage_change(data['1D'])} | " +
            f"5D: {format_percentage_change(data['5D'])} | " +
            f"1M: {format_percentage_change(data['1M'])} | " +
            f"1Y: {format_percentage_change(data['1Y'])}"
        )
        output += performance_line + "\n"
        hist_chart = crypto.history(period="1mo")
        prices = hist_chart['Close'].tolist()
        if len(prices) >= 2:
            chart = generate_sparkline(prices)
            chart_color = Fore.LIGHTGREEN_EX if data['1M'] > 0 else Fore.RED if data['1M'] < 0 else Fore.CYAN
            output += Fore.WHITE + "   Price Chart (Last 1 Month):\n"
            output += f"   {chart_color}{chart}{Fore.RESET}\n"
        else:
            output += Fore.RED + "   Not enough data to generate chart.\n"

        output += Fore.WHITE + "\nAdditional Data:\n\n"
        output += f"{Fore.LIGHTCYAN_EX}   52 Week Range:{Fore.RESET} {crypto.info.get('fiftyTwoWeekLow', 'N/A')} - {crypto.info.get('fiftyTwoWeekHigh', 'N/A')}\n"
        output += f"{Fore.LIGHTCYAN_EX}   Volume (24hr):{Fore.RESET} {format_number(crypto.info.get('volume', 'N/A'))} USD\n"
        output += f"{Fore.LIGHTCYAN_EX}   Market Cap:{Fore.RESET} {format_number(crypto.info.get('marketCap', 'N/A'))} USD\n"
        output += f"{Fore.LIGHTCYAN_EX}   Circulating Supply:{Fore.RESET} {format_number(crypto.info.get('circulatingSupply', 'N/A'))} coins\n"

        return output
    except Exception as e:
        return Fore.RED + f"Error fetching data for {crypto_code}: {str(e)}"

# Fetch stock data with error handling
def fetch_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        if not stock.info or stock.info == {}:
            raise ValueError(Fore.RED + f"No data available for {ticker}")
        return stock
    except Exception as e:
        print(f"{Fore.RED}Error fetching data for {ticker}: {e}{Fore.RESET}")
        return None

# Main function to compare stocks
def stock_compare(stock1_input, stock2_input):
    # First, normalize the inputs to tickers using the keyword_mapping dictionary
    stock1_ticker = keyword_mapping['companies'].get(stock1_input.lower(), stock1_input.upper())
    stock2_ticker = keyword_mapping['companies'].get(stock2_input.lower(), stock2_input.upper())

    # Fetch data for both stocks
    stock1 = fetch_stock_data(stock1_ticker)
    if not stock1:
        return Fore.RED + f"No data available for {stock1_ticker}."
    
    time.sleep(2)  # Adding delay to avoid throttling
    
    stock2 = fetch_stock_data(stock2_ticker)
    if not stock2:
        return Fore.RED + f"No data available for {stock2_ticker}."

    # Get company names from the stock data or fallback to ticker
    company_name1 = stock1.info.get('shortName', stock1_ticker)
    company_name2 = stock2.info.get('shortName', stock2_ticker)

    # Metrics to compare
    metrics = {
        'Market Cap': ('marketCap', format_currency_no_color),
        'Total Revenue': ('totalRevenue', format_currency_no_color),
        'Revenue Growth': ('revenueGrowth', format_percentage_no_color),
        'Gross Profit Margin': ('grossMargins', format_percentage_no_color),
        'Operating Margin': ('operatingMargins', format_percentage_no_color),
        'Net Income': ('netIncomeToCommon', format_currency_no_color),
        'EPS (TTM)': ('trailingEps', lambda x: f"{x:.2f}" if x is not None else 'N/A'),
        'P/E Ratio (TTM)': ('trailingPE', lambda x: f"{x:.2f}" if x is not None else 'N/A'),
        'Return on Equity': ('returnOnEquity', format_percentage_no_color),
        'Debt to Equity Ratio': (None, None)  # Will calculate manually if needed
    }

    # Collect data
    data = {}
    for metric, (key, formatter) in metrics.items():
        if key:
            value1 = stock1.info.get(key, None)
            value2 = stock2.info.get(key, None)
            formatted_value1 = formatter(value1) if value1 is not None else 'N/A'
            formatted_value2 = formatter(value2) if value2 is not None else 'N/A'
        else:
            # Debt to Equity Ratio
            total_debt1 = stock1.info.get('totalDebt', None)
            equity1 = stock1.info.get('totalStockholderEquity', None)
            ratio1 = total_debt1 / equity1 if total_debt1 and equity1 else None

            total_debt2 = stock2.info.get('totalDebt', None)
            equity2 = stock2.info.get('totalStockholderEquity', None)
            ratio2 = total_debt2 / equity2 if total_debt2 and equity2 else None

            formatted_value1 = f"{ratio1:.2f}" if ratio1 is not None else 'N/A'
            formatted_value2 = f"{ratio2:.2f}" if ratio2 is not None else 'N/A'

        # Apply color coding for comparison
        try:
            value1_num = float(strip_ansi_codes(formatted_value1).replace('%', '').replace('$', '').replace('B', ''))
            value2_num = float(strip_ansi_codes(formatted_value2).replace('%', '').replace('$', '').replace('B', ''))
            if value1_num > value2_num:
                formatted_value1 = Fore.LIGHTGREEN_EX + formatted_value1 + Fore.RESET
                formatted_value2 = Fore.RED + formatted_value2 + Fore.RESET
            elif value1_num < value2_num:
                formatted_value1 = Fore.RED + formatted_value1 + Fore.RESET
                formatted_value2 = Fore.LIGHTGREEN_EX + formatted_value2 + Fore.RESET
        except ValueError:
            pass  # In case value is not numeric (e.g., 'N/A')

        data[metric] = [formatted_value1, formatted_value2]

    # Fixed-width column setup
    metric_width = 25
    company1_width = max(20, len(company_name1) + 5)
    company2_width = max(20, len(company_name2) + 5)

    # Header
    output = f"\nComparison between {Fore.LIGHTYELLOW_EX}{company_name1} ({stock1_ticker}){Fore.RESET} and {Fore.LIGHTYELLOW_EX}{company_name2} ({stock2_ticker}):\n"
    output += f"{'Metric':<{metric_width}} {company_name1:<{company1_width}} {company_name2:<{company2_width}}\n"
    output += "-" * (metric_width + company1_width + company2_width) + "\n"

    # Rows with proper padding
    for metric, values in data.items():
        metric_name = metric.ljust(metric_width)
        company1_value = strip_ansi_codes(values[0]).ljust(company1_width)
        company2_value = strip_ansi_codes(values[1]).ljust(company2_width)

        # Apply color after padding
        colored_value1 = values[0].replace(strip_ansi_codes(values[0]), company1_value)
        colored_value2 = values[1].replace(strip_ansi_codes(values[1]), company2_value)

        output += f"{metric_name} {colored_value1} {colored_value2}\n"

    return output

# Add these new functions after the existing functions but before handle_markets_command

def generate_oil_market_report():
    # Get Athens time
    athens_time = datetime.now(timezone('Europe/Athens')).strftime("%Y-%m-%d %H:%M:%S Athens")
    
    output = f"""
{Fore.MAGENTA}╔═════════════════════════════════════════════════════════════╗
║     {Fore.CYAN}█▀▀ █   █▀█ █▄▄ ▄▀█ █   █▀█ █ █   {Fore.MAGENTA}& {Fore.CYAN}█▀▀ ▄▀█ █▀{Fore.MAGENTA}     ║
║     {Fore.CYAN}█▄█ █▄▄ █▄█ █▄█ █▀█ █▄▄ █▄█ █ █▄▄ {Fore.MAGENTA}& {Fore.CYAN}█▄█ █▀█ ▄█{Fore.MAGENTA}     ║
║                 MARKET INTELLIGENCE SYSTEM                    ║
║              By ARPA HELLENIC LOGICAL SYSTEMS                ║
║                     {athens_time}                 ║
╚══════════════════════════════════════════════════════════════╝{Fore.RESET}
"""
    try:
        output += generate_market_overview()
        output += predict_oil_prices()
        output += analyze_industry_news()
        output += analyze_top_players()
        output += analyze_global_supply()
        output += analyze_industry_trends()
    except Exception as e:
        output += f"\n{Fore.RED}Error generating market report: {str(e)}{Fore.RESET}"
    
    return output

def predict_oil_prices():
    output = f"\n{Fore.LIGHTMAGENTA_EX}■ OIL PRICE PREDICTION{Fore.RESET}\n"
    try:
        wti = yf.Ticker("CL=F")
        hist = wti.history(period="1y")
        
        if hist.empty:
            output += f"{Fore.RED}Not enough data to make predictions.{Fore.RESET}\n"
            return output

        prices = hist['Close'].dropna().values
        
        if len(prices) < 30:
            return f"{Fore.RED}Insufficient data for prediction.{Fore.RESET}\n"

        log_prices = np.log(prices)
        model = sm.tsa.ARIMA(log_prices, order=(5,1,0))
        model_fit = model.fit()
        
        # Get forecast values as a numpy array
        forecast = model_fit.forecast(steps=7)
        forecast_values = np.exp(forecast)
        
        # Convert current price to scalar
        current_price = prices[-1]
        output += f"\n{Fore.CYAN}Current WTI Price: ${current_price:.2f}{Fore.RESET}\n"
        output += f"{Fore.CYAN}7-Day Price Forecast:{Fore.RESET}\n"

        # Generate dates
        last_date = hist.index[-1]
        forecast_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=7)

        # Process each forecast value individually
        for i, date in enumerate(forecast_dates):
            price = forecast_values[i]  # Get single value from array
            change = ((price - current_price) / current_price) * 100
            change_color = Fore.LIGHTGREEN_EX if price > current_price else Fore.RED
            output += f"{date.strftime('%Y-%m-%d')}: ${price:.2f} ({change_color}{change:+.2f}%{Fore.RESET})\n"

        # Generate trend visualization
        sparkline = generate_sparkline(forecast_values)
        
        # Compare first and last values directly
        trend_up = forecast_values[-1] > forecast_values[0]
        trend_color = Fore.LIGHTGREEN_EX if trend_up else Fore.RED
        
        output += f"\n{Fore.CYAN}Forecasted Price Trend:{Fore.RESET}\n"
        output += f"   {trend_color}{sparkline}{Fore.RESET}  "
        output += f"[Range: ${np.min(forecast_values):.2f} - ${np.max(forecast_values):.2f}]\n"
        
        # Calculate trend percentage using scalar values
        trend_pct = ((forecast_values[-1] - forecast_values[0]) / forecast_values[0]) * 100
        if trend_up:  # Use the boolean we already calculated
            output += f"   Upward trend expected: {Fore.LIGHTGREEN_EX}+{trend_pct:.1f}%{Fore.RESET} over 7 days\n"
        else:
            output += f"   Downward trend expected: {Fore.RED}{trend_pct:.1f}%{Fore.RESET} over 7 days\n"

    except Exception as e:
        output += f"{Fore.RED}Error making price prediction: {str(e)}{Fore.RESET}\n"

    return output

def analyze_industry_news():
    output = f"\n{Fore.LIGHTMAGENTA_EX}■ INDUSTRY NEWS ANALYSIS{Fore.RESET}\n"
    try:
        # Use multiple news sources and APIs
        news_sources = [
            {'ticker': 'CL=F', 'type': 'Oil Futures'},
            {'ticker': 'XLE', 'type': 'Energy Sector'},
            {'ticker': 'XOM', 'type': 'Oil & Gas'},
            {'ticker': 'CVX', 'type': 'Oil & Gas'}
        ]
        
        all_news = []
        for source in news_sources:
            ticker_obj = yf.Ticker(source['ticker'])
            news = ticker_obj.news
            for article in news:
                # Extract the actual source from the article URL
                domain = article['link'].split('/')[2]
                if 'yahoo' in domain:
                    actual_source = 'Yahoo Finance'
                elif 'reuters' in domain:
                    actual_source = 'Reuters'
                elif 'bloomberg' in domain:
                    actual_source = 'Bloomberg'
                elif 'ft.com' in domain:
                    actual_source = 'Financial Times'
                else:
                    actual_source = domain.replace('www.', '').capitalize()
                
                article['source'] = actual_source
                article['sector'] = source['type']
                all_news.append(article)
        
        # Sort by publication date
        all_news.sort(key=lambda x: x.get('providerPublishTime', 0), reverse=True)
        
        # Take unique articles
        seen_titles = set()
        unique_news = []
        for article in all_news:
            if article['title'] not in seen_titles:
                seen_titles.add(article['title'])
                unique_news.append(article)
        
        output += f"\n{Fore.WHITE}Latest Market Intelligence:{Fore.RESET}\n"
        
        # Display top 5 unique news with enhanced analysis
        for article in unique_news[:5]:
            title = article['title']
            source = article['source']
            sector = article['sector']
            link = article['link']
            
            output += f"\n{Fore.LIGHTBLUE_EX}{title}{Fore.RESET}\n"
            output += f"Source: {source} | Sector: {sector}\n"
            output += f"{link}\n"
            output += f"Analysis: {analyze_sentiment(title)}\n"

        # Overall market sentiment
        positive = sum(1 for a in unique_news[:5] if 'Positive' in analyze_sentiment(a['title']))
        negative = sum(1 for a in unique_news[:5] if 'Negative' in analyze_sentiment(a['title']))
        
        output += f"\n{Fore.WHITE}Market Sentiment Summary:{Fore.RESET} "
        if positive > negative:
            output += f"{Fore.LIGHTGREEN_EX}Predominantly Positive{Fore.RESET}\n"
        elif negative > positive:
            output += f"{Fore.RED}Predominantly Negative{Fore.RESET}\n"
        else:
            output += f"{Fore.YELLOW}Mixed/Neutral{Fore.RESET}\n"

    except Exception as e:
        output += f"{Fore.RED}Error fetching or analyzing news: {str(e)}{Fore.RESET}\n"

    return output

def analyze_sentiment(text):
    # Simple sentiment analysis based on keywords
    positive_keywords = ['gain', 'rise', 'up', 'increase', 'positive', 'surge', 'growth', 'profit']
    negative_keywords = ['fall', 'drop', 'down', 'decrease', 'negative', 'decline', 'loss', 'plunge']

    text = text.lower()
    positive_score = sum([text.count(word) for word in positive_keywords])
    negative_score = sum([text.count(word) for word in negative_keywords])

    if positive_score > negative_score:
        return f"{Fore.LIGHTGREEN_EX}Positive{Fore.RESET}"
    elif negative_score > positive_score:
        return f"{Fore.RED}Negative{Fore.RESET}"
    else:
        return f"{Fore.YELLOW}Neutral{Fore.RESET}"

def generate_market_overview():
    output = f"\n{Fore.LIGHTMAGENTA_EX}■ MARKET OVERVIEW{Fore.RESET}\n"
    try:
        # Get data for each commodity
        commodities = {
            'WTI': yf.Ticker("CL=F"),
            'Brent': yf.Ticker("BZ=F"),
            'Gas': yf.Ticker("NG=F")
        }
        
        output += f"\n{Fore.CYAN}Price Trends (30-Day):{Fore.RESET}\n"
        
        for name, ticker in commodities.items():
            hist = ticker.history(period="1mo")
            if not hist.empty:
                prices = hist['Close']
                change_30d = ((prices[-1] - prices[0]) / prices[0]) * 100
                sparkline = generate_sparkline(prices.tolist())
                
                # Color based on performance
                chart_color = Fore.LIGHTGREEN_EX if change_30d >= 0 else Fore.RED
                
                # Format the line with price range and percentage
                output += f"{name:<6} {chart_color}{sparkline}{Fore.RESET}  "
                output += f"[${min(prices):.2f} - ${max(prices):.2f}] "
                output += f"({chart_color}{change_30d:+.2f}%{Fore.RESET})\n"
            else:
                output += f"{name:<6} {Fore.RED}No data available{Fore.RESET}\n"

    except Exception as e:
        output += f"{Fore.RED}Error generating market overview: {str(e)}{Fore.RESET}\n"
    
    return output

def analyze_top_players():
    output = f"\n{Fore.LIGHTMAGENTA_EX}■ TOP PLAYERS ANALYSIS{Fore.RESET}\n"
    try:
        companies = [
            ('XOM', 'ExxonMobil'), ('CVX', 'Chevron'), 
            ('SHEL', 'Shell'), ('TTE', 'TotalEnergies'),
            ('BP', 'BP'), ('COP', 'ConocoPhillips')
        ]

        # Financial metrics table (keep as is)
        output += "\n╔════════════════╦══════════════╦══════════════╦═══════════╦═══════╗\n"
        output += "║ Company        ║ Market Cap   ║ Revenue      ║ Margin    ║ P/E   ║\n"
        output += "╠════════════════╬══════════════╬══════════════╬═══════════╬═══════╣\n"

        for ticker, name in companies:
            try:
                stock = yf.Ticker(ticker)
                info = stock.info

                market_cap = format_currency(info.get('marketCap', 'N/A'))
                revenue = format_currency(info.get('totalRevenue', 'N/A'))
                margin = format_percentage(info.get('operatingMargins', 'N/A'))
                pe = f"{info.get('trailingPE', 'N/A'):.2f}" if info.get('trailingPE') else 'N/A'

                output += f"║ {name:<14} ║ {market_cap:<12} ║ {revenue:<12} ║ {margin:<9} ║ {pe:<6} ║\n"
            except:
                output += f"║ {name:<14} ║ {'N/A':<12} ║ {'N/A':<12} ║ {'N/A':<9} ║ {'N/A':<6} ║\n"

        output += "╚════════════════╩══════════════╩══════════════╩═══════════╩═══════╝\n"

        # Performance Comparison section with fixed formatting
        output += f"\n{Fore.WHITE}Performance Comparison (YTD):{Fore.RESET}\n"
        for ticker, name in companies:
            try:
                stock = yf.Ticker(ticker)
                hist = stock.history(period="ytd")
                
                # Calculate YTD change
                ytd_change = ((hist['Close'][-1] - hist['Close'][0]) / hist['Close'][0]) * 100
                
                # Get 30-point sample for sparkline
                prices = hist['Close'].tolist()
                sample_size = min(30, len(prices))
                sampled_prices = prices[::len(prices)//sample_size][:sample_size]
                
                # Generate sparkline and determine color
                chart = generate_sparkline(sampled_prices)
                chart_color = Fore.LIGHTGREEN_EX if ytd_change >= 0 else Fore.RED
                
                # Format the line with fixed spacing
                output += f"{name:<15} "
                output += f"{chart_color}{chart}{Fore.RESET}  "
                output += f"[${min(prices):.2f} - ${max(prices):.2f}] "
                output += f"({chart_color}{ytd_change:+.2f}%{Fore.RESET})\n"
            except Exception as e:
                continue

    except Exception as e:
        output += f"{Fore.RED}Error analyzing top players: {str(e)}{Fore.RESET}\n"
    
    return output

def analyze_global_supply():
    output = f"\n{Fore.LIGHTMAGENTA_EX}■ GLOBAL SUPPLY & DEMAND ANALYSIS{Fore.RESET}\n"
    try:
        oil_etfs = ['USO', 'BNO', 'OIL', 'DBO']
        
        output += f"\n{Fore.WHITE}Market ETF Performance:{Fore.RESET}\n"
        for etf in oil_etfs:
            try:
                fund = yf.Ticker(etf)
                hist = fund.history(period="1mo")
                
                # Calculate monthly change
                monthly_change = ((hist['Close'][-1] - hist['Close'][0]) / hist['Close'][0]) * 100
                
                # Generate colored sparkline
                chart = generate_sparkline(hist['Close'].tolist())
                chart_color = Fore.LIGHTGREEN_EX if monthly_change >= 0 else Fore.RED
                
                # Add price range and percentage change
                output += f"{etf:<6} "
                output += f"{chart_color}{chart}{Fore.RESET}  "
                output += f"[${min(hist['Close']):.2f} - ${max(hist['Close']):.2f}] "
                output += f"({chart_color}{monthly_change:+.2f}%{Fore.RESET})\n"
            except:
                continue

        wti = yf.Ticker("CL=F")
        hist = wti.history(period="1mo")
        avg_volume = hist['Volume'].mean()
        current_volume = hist['Volume'][-1]
        volume_ratio = current_volume / avg_volume if avg_volume else 0

        output += f"\n{Fore.WHITE}Trading Volume Analysis:{Fore.RESET}\n"
        output += f"Average Daily Volume: {format_number(avg_volume)} barrels/day\n"
        output += f"Current Volume: {format_number(current_volume)} barrels/day\n"
        output += f"Volume Ratio: {volume_ratio:.2f}x average "
        
        # Add volume interpretation
        if volume_ratio > 1.2:
            output += f"{Fore.GREEN}(High trading activity){Fore.RESET}\n"
        elif volume_ratio < 0.8:
            output += f"{Fore.YELLOW}(Low trading activity){Fore.RESET}\n"
        else:
            output += f"{Fore.WHITE}(Normal trading activity){Fore.RESET}\n"

    except Exception as e:
        output += f"{Fore.RED}Error analyzing global supply: {str(e)}{Fore.RESET}\n"
    
    return output

def analyze_industry_trends():
    output = f"\n{Fore.LIGHTMAGENTA_EX}■ INDUSTRY TRENDS & RISK ANALYSIS{Fore.RESET}\n\n"
    try:
        energy_etf = yf.Ticker("XLE")
        hist = energy_etf.history(period="1mo")

        output += f"{Fore.WHITE}Risk Indicators:{Fore.RESET}\n"
        output += f"Volatility:     {generate_risk_meter(calculate_volatility(hist))}\n"
        output += f"Volume Trend:   {generate_risk_meter(calculate_volume_trend(hist))}\n"
        output += f"Price Trend:    {generate_risk_meter(calculate_price_trend(hist))}\n"

    except Exception as e:
        output += f"{Fore.RED}Error analyzing industry trends: {str(e)}{Fore.RESET}\n"
    
    return output

def calculate_volatility(hist):
    try:
        returns = hist['Close'].pct_change()
        return min(returns.std() * np.sqrt(252), 1.0)  # Annualized volatility, capped at 1.0
    except:
        return 0.5

def calculate_volume_trend(hist):
    try:
        current_vol = hist['Volume'][-5:].mean()
        past_vol = hist['Volume'][:-5].mean()
        return min(max(current_vol / past_vol - 0.5, 0), 1)
    except:
        return 0.5

def calculate_price_trend(hist):
    try:
        prices = hist['Close']
        return min(max((prices[-1] / prices[0] - 0.9) / 0.2, 0), 1)
    except:
        return 0.5

def generate_risk_meter(value):
    meter_length = 10
    filled = int(value * meter_length)
    if value < 0.3:
        color = Fore.GREEN
        level = "Low"
    elif value < 0.7:
        color = Fore.YELLOW
        level = "Medium"
    else:
        color = Fore.RED
        level = "High"
    return f"{color}{'█' * filled}{'░' * (meter_length - filled)}{Fore.RESET} {level}"
    
def generate_market_sentiment():
    try:
        # Get WTI data for sentiment analysis
        wti = yf.Ticker("CL=F")
        hist = wti.history(period="5d")
        
        # Calculate basic technical indicators using proper indexing
        volatility = hist['Close'].std()
        momentum = (hist['Close'].values[-1] - hist['Close'].values[0]) / hist['Close'].values[0]
        
        # Calculate volume trend using values instead of iloc
        first_volume = hist['Volume'].values[0]
        last_volume = hist['Volume'].values[-1]
        volume_trend = (last_volume - first_volume) / first_volume if first_volume else 0
        
        # Determine sentiment based on multiple factors
        if momentum > 0.02 and volume_trend > 0:
            return f"{Fore.LIGHTGREEN_EX}Bullish{Fore.RESET}"
        elif momentum < -0.02 and volume_trend < 0:
            return f"{Fore.RED}Bearish{Fore.RESET}"
        elif volatility > hist['Close'].mean() * 0.02:
            return f"{Fore.YELLOW}Volatile{Fore.RESET}"
        else:
            return f"{Fore.LIGHTCYAN_EX}Neutral{Fore.RESET}"
    except Exception as e:
        return f"{Fore.YELLOW}Neutral{Fore.RESET}"
    
#Example usage
#if __name__ == "__main__":
#    command = input("Enter command: ")
#    print(handle_markets_command(command))