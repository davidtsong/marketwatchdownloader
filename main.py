from pandas_datareader import data as web
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import numpy as np
import fix_yahoo_finance as yf
from matplotlib.backends.backend_pdf import PdfPages

def findInList(element, list):
    try:
        for i in range(len(list)):
            if list[i][0] == element:
                print('nop')
                return i
        return None
    except ValueError:
        print("value error")
        return None

def addStockChartYahoo(ticker, start, end):
    global graphNum
    global stockGraphValuesRows
    fig = plt.figure()

    f = web.get_data_yahoo(ticker,start=start,end=end)
    print(f.columns)
    print(f.index)
    print(f)
    print(f.info())
    start = datetime.strptime(start,'%Y-%m-%d')
    end = datetime.strptime(end,'%Y-%m-%d')
    if ((end-start).total_seconds() / 604800 > 1):
        plt.plot(f.index[::7], f['Close'][::7])
        print("more than a week")
        for i in range(len(f.index[::7])):
            stockGraphValuesRows.append([graphNum, ticker + ' ' + start.strftime('%Y-%m-%d') + ' to ' +
            end.strftime('%Y-%m-%d'), f.index[7*i].strftime('%Y-%m-%d'), f['Close'][7*i]])

    else:
        plt.plot(f.index, f['Close'])
        print('less than a week')
        for i in range(len(f.index)):
            stockGraphValuesRows.append([graphNum, ticker + ' ' + start.strftime('%Y-%m-%d') + ' to ' +
            end.strftime('%Y-%m-%d'), f.index[i].strftime('%Y-%m-%d'), f['Close'][i]])


    graphNum = graphNum + 1
    plt.title(str(graphNum) + ": " + ticker + ' Stock Price From ' + start.strftime('%Y-%m-%d') + ' to ' + end.strftime('%Y-%m-%d'))
    plt.xlabel('Date (Y-M-D)')
    plt.ylabel('Closing Price ($)')

    return fig




def addStockChart(ticker, start=(2018,4,1), end=(2018,5,1)):
    global graphNum
    global stockGraphValuesRows

    fig = plt.figure()
    start = datetime(*start)
    end = datetime(*end)

    try:
        f = web.DataReader(ticker, 'morningstar', start, end)
        print(f)
        f.reset_index(level='Date', inplace=True)
        f.time = pd.to_datetime(f['Date'], format='%Y-%m-%d %H:%M:%S')
        f.set_index(['Date'],inplace=True)
        print(f.columns)
        print(f.index)
        print(f.info())
        if ((end-start).total_seconds() / 604800 > 1):
            plt.plot(f.index[::7], f['Close'][::7])
            print("more than a week")
            for i in range(len(f.index[::7])):
                stockGraphValuesRows.append([graphNum, ticker + ' ' + start.strftime('%Y-%m-%d') + ' to ' +
                end.strftime('%Y-%m-%d'), f.index[7*i].strftime('%Y-%m-%d'), f['Close'][7*i]])
        #Add if less than one day to just use the opening and closing values
        else:
            plt.plot(f.index, f['Close'])
            print('less than a week')
            for i in range(len(f.index)):
                stockGraphValuesRows.append([graphNum, ticker + ' ' + start.strftime('%Y-%m-%d') + ' to ' +
                end.strftime('%Y-%m-%d'), f.index[i].strftime('%Y-%m-%d'), f['Close'][i]])


        graphNum = graphNum + 1
        if len(f.index) < 2:
            plt.title(str(graphNum) + ": " + ticker + ' One day buy sell on ' + start.strftime('%Y-%m-%d'))
        else:
            plt.title(str(graphNum) + ": " + ticker + ' Stock Price From ' + start.strftime('%Y-%m-%d') + ' to ' + end.strftime('%Y-%m-%d'))

        plt.xlabel('Date (Y-M-D)')

        plt.ylabel('Closing Price ($)')

        return fig

    except ValueError:
        print('Failed to find')
        return None

if __name__ == "__main__":
    graphNum = 1
    yf.pdr_override()
    #Get CSV Files based on credentials

    stockOverviewColumns= ['Name', '1' , '2', '3', '4', '5','6','7','8','9','10']
    stockOverviewRows = []

    stockGraphValuesColumns = ['GraphNum','Name', 'Date', 'Close']
    stockGraphValuesRows = []

    stockGraphFigures = []

    portfolioColumn = ['Name', 'Number', 'Start', 'End']
    portfolioRows = []
    # plot1 = addStockChart('GOOGL', (2018,4,1), (2018,5,1))
    # plot2 = addStockChart('GOOGL', (2018,4,27), (2018,5,1))

    #Add Portfolio Performance to stockGraph Values and Graph
    overall = pd.read_csv('performance.csv')

    overall.set_index(['Date'],inplace=True)
    #print(overall)
    #print(overall.index)
    for i in range(len(overall.index) // 10):
        stockGraphValuesRows.append(['0', 'Overall Portfolio', overall.index[10*i], overall['Net Worth'][10*i]])
    fig = plt.figure()

    #Reverse order correctly and remove $ signs
    overall = overall[::-1]
    overall['Net Worth'] = overall['Net Worth'].str.replace('$', '')
    overall['Net Worth'] = overall['Net Worth'].str.replace(',', '')
    overall['Net Worth'] = pd.to_numeric(overall['Net Worth'])
    #print(overall.info())

    plt.plot(overall.index[::10], overall['Net Worth'][::10])
    plt.title('0: Overall Portfolio Performance')
    plt.xlabel('Date (Y-M-D)')
    plt.ylabel('Value ($)')

    stockGraphFigures.append(fig)

    #Read from Transactions List and Add to Points and Create Graphs
    transactions = pd.read_csv('transactions.csv')
    # print(transactions)
    #strip hourly time from dates
    transactions['Transaction Date'] = pd.to_datetime(transactions['Transaction Date'])
    transactions['Transaction Date'] = transactions['Transaction Date'].apply(lambda x:x.date().strftime('%m/%d/%y'))
    #flip order again past to now and clean data
    transactions = transactions[::-1]
    transactions['Amount'] = transactions['Amount'].str.replace(',' , '')
    transactions['Amount'] = pd.to_numeric(transactions['Amount'])
    transactions = transactions.reset_index(drop = True)
    # print(transactions)
    # print(transactions.index)

    #Generate the right start and end dates
    for r in range(len(transactions.index)):
        index = findInList(transactions['Symbol'][r], portfolioRows)
        print(index)
        if index != None:
            print('Found one at : ' + str(index))
            if(transactions['Type'][r] == 'Buy' or transactions['Type'][r] == 'Short'):
                portfolioRows[index][1] += transactions['Amount'][r]
            elif(transactions['Type'][r] == 'Sell' or transactions['Type'][r] == 'Cover'):
                portfolioRows[index][1] -= transactions['Amount'][r]
                if(portfolioRows[index][1] < 1):
                    portfolioRows[index][3] = transactions['Transaction Date'][r]
            print(portfolioRows)
        else:
            print('None exists')
            portfolioRows.append([transactions['Symbol'][r], transactions['Amount'][r], transactions['Transaction Date'][r],''])
            print(portfolioRows)

    #Generate and save graphs to pdf
    for stock in portfolioRows:
        print(" Working on : " + stock[0])
        startT = [int(x) for x in stock[2].split('/')]
        startT.insert(0,2000 + startT[2])
        startT = startT[:-1]
        print(startT)

        endT = [int(x) for x in stock[3].split('/')]
        endT.insert(0,2000 + endT[2])
        endT = endT[:-1]
        print(endT)
        chart = addStockChart(stock[0], startT , endT)
        if chart != None and chart != -1:
            stockGraphFigures.append(chart)
        else:
            try:
                stockGraphFigures.append(addStockChartYahoo(stock[0],str(startT[0]) + '-'+ str(format(startT[1], '02d')) +'-' + str(format(startT[2], '02d')),
                str(endT[0]) +'-' + str(format(endT[1], '02d')) +'-' + str(format(endT[2], '02d')) ))
            except KeyError:
                stockGraphFigures.append(addStockChartYahoo(stock[0],str(startT[0]) + '-'+ str(format(startT[1], '02d')) +'-' + str(format(startT[2], '02d')),
                str(endT[0]) +'-' + str(format(endT[1], '02d')) +'-' + str(format(endT[2], '02d')) ))


    print(stockGraphFigures)

    with PdfPages('foo.pdf') as pdf:
        for plot in stockGraphFigures:
            pdf.savefig(plot)
    #Export Datapoints to CSV
    dfstockGraphValues = pd.DataFrame(stockGraphValuesRows, columns = stockGraphValuesColumns)
    dfstockGraphValues.to_csv("stockGraphDataValues.csv", sep=',')

    print("YOU DID IT!")
