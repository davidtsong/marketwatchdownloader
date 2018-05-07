from pandas_datareader import data as web
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import numpy as np
import fix_yahoo_finance as yf
import glob
from app import app

from matplotlib.backends.backend_pdf import PdfPages
class GenGraphs:
    key = ''
    stockOverviewColumns= ['Name', '1' , '2', '3', '4', '5','6','7','8','9','10']
    stockOverviewRows = []

    stockGraphValuesColumns = ['GraphNum','Name', 'Date', 'Close']
    stockGraphValuesRows = []

    stockGraphFigures = []

    portfolioColumn = ['Name', 'Number', 'Start', 'End']
    portfolioRows = []

    files = []
    graphNum = 0
    def __init__(self, files, key):
        self.files = files
        self.key = key

    def findInList(self, element, list):
        try:
            for i in range(len(list)):
                if list[i][0] == element:
                    print('nop')
                    return i
            return None
        except ValueError:
            print("value error")
            return None
    def appendStockChart(self, ticker, start, end):
        try:
            self.stockGraphFigures.append(self.addStockChartYahoo(ticker, start, end))
        except KeyError:
            appendStockChart(ticker,start,end)
        except:
            print("Couldn't find stock : " + ticker)

    def addStockChartYahoo(self, ticker, start, end):
        fig = plt.figure()
        plt.xticks(rotation=70, fontsize=5)

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
                self.stockGraphValuesRows.append([self.graphNum, ticker + ' ' + start.strftime('%Y-%m-%d') + ' to ' +
                end.strftime('%Y-%m-%d'), f.index[7*i].strftime('%Y-%m-%d'), f['Close'][7*i]])

        else:
            plt.plot(f.index, f['Close'])
            print('less than a week')
            for i in range(len(f.index)):
                self.stockGraphValuesRows.append([self.graphNum, ticker + ' ' + start.strftime('%Y-%m-%d') + ' to ' +
                end.strftime('%Y-%m-%d'), f.index[i].strftime('%Y-%m-%d'), f['Close'][i]])


        self.graphNum = self.graphNum + 1
        plt.title(str(self.graphNum) + ": " + ticker + ' Stock Price From ' + start.strftime('%Y-%m-%d') + ' to ' + end.strftime('%Y-%m-%d'))
        plt.xlabel('Date (Y-M-D)')

        plt.ylabel('Closing Price ($)')

        return fig




    def addStockChart(self, ticker, start=(2018,4,1), end=(2018,5,1)):

        fig = plt.figure()
        start = datetime(*start)
        end = datetime(*end)

        try:
            f = web.DataReader(ticker, 'morningstar', start, end)
            print(f)
            f.reset_index(level='Date', inplace=True)
            f.time = pd.to_datetime(f['Date'], format='%Y-%m-%d %H:%M:%S')
            f.set_index(['Date'],inplace=True)
            plt.xticks(rotation=70, fontsize=5)
            print(f.columns)
            print(f.index)
            print(f.info())
            if ((end-start).total_seconds() / 604800 > 1):
                plt.plot(f.index[::7], f['Close'][::7])
                print("more than a week")
                for i in range(len(f.index[::7])):
                    self.stockGraphValuesRows.append([self.graphNum, ticker + ' ' + start.strftime('%Y-%m-%d') + ' to ' +
                    end.strftime('%Y-%m-%d'), f.index[7*i].strftime('%Y-%m-%d'), f['Close'][7*i]])
            #Add if less than one day to just use the opening and closing values
            else:
                plt.plot(f.index, f['Close'])
                print('less than a week')
                for i in range(len(f.index)):
                    self.stockGraphValuesRows.append([self.graphNum, ticker + ' ' + start.strftime('%Y-%m-%d') + ' to ' +
                    end.strftime('%Y-%m-%d'), f.index[i].strftime('%Y-%m-%d'), f['Close'][i]])


            self.graphNum = self.graphNum + 1
            if len(f.index) < 2:
                plt.title(str(self.graphNum) + ": " + ticker + ' One day buy sell on ' + start.strftime('%Y-%m-%d'))
            else:
                plt.title(str(self.graphNum) + ": " + ticker + ' Stock Price From ' + start.strftime('%Y-%m-%d') + ' to ' + end.strftime('%Y-%m-%d'))

            plt.xlabel('Date (Y-M-D)')

            plt.ylabel('Closing Price ($)')

            return fig

        except ValueError:
            print('Failed to find')
            return None

    def run(self):
        yf.pdr_override()
        #Get CSV Files based on credentials

        # plot1 = addStockChart('GOOGL', (2018,4,1), (2018,5,1))
        # plot2 = addStockChart('GOOGL', (2018,4,27), (2018,5,1))

        #Add Portfolio Performance to stockGraph Values and Graph
        overall = self.files[0]

        overall.set_index(['Date'],inplace=True)
        #print(overall)
        #print(overall.index)
        for i in range(len(overall.index) // 10):
            self.stockGraphValuesRows.append(['0', 'Overall Portfolio', overall.index[10*i], overall['Net Worth'][10*i]])
        fig = plt.figure()
        plt.xticks(rotation=70, fontsize=5)
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

        self.stockGraphFigures.append(fig)

        #Read from Transactions List and Add to Points and Create Graphs
        transactions = self.files[1]
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
            index = self.findInList(transactions['Symbol'][r], self.portfolioRows)
            print(index)
            if index != None:
                print('Found one at : ' + str(index))
                if(transactions['Type'][r] == 'Buy' or transactions['Type'][r] == 'Short'):
                    self.portfolioRows[index][1] += transactions['Amount'][r]
                elif(transactions['Type'][r] == 'Sell' or transactions['Type'][r] == 'Cover'):
                    self.portfolioRows[index][1] -= transactions['Amount'][r]
                    if(self.portfolioRows[index][1] < 1):
                        self.portfolioRows[index][3] = transactions['Transaction Date'][r]
            else:
                print('None exists')
                self.portfolioRows.append([transactions['Symbol'][r], transactions['Amount'][r], transactions['Transaction Date'][r],''])

        #Generate and save graphs to pdf
        for stock in self.portfolioRows:
            print(" Working on : " + stock[0])
            startT = [int(x) for x in stock[2].split('/')]
            startT.insert(0,2000 + startT[2])
            startT = startT[:-1]
            print(startT)

            endT = [int(x) for x in stock[3].split('/')]
            endT.insert(0,2000 + endT[2])
            endT = endT[:-1]
            print(endT)
            chart = self.addStockChart(stock[0], startT , endT)
            if chart != None and chart != -1:
                self.stockGraphFigures.append(chart)
            else:
                self.appendStockChart(stock[0],str(startT[0]) + '-'+ str(format(startT[1], '02d')) +'-' + str(format(startT[2], '02d')),
                str(endT[0]) +'-' + str(format(endT[1], '02d')) +'-' + str(format(endT[2], '02d')) )


        pdfFileName= 'app/upload/' + self.key + ' Graphs.pdf'

        with PdfPages(pdfFileName) as pdf:
            for plot in self.stockGraphFigures:
                pdf.savefig(plot)


        #Export Datapoints to CSV
        dfstockGraphValues = pd.DataFrame(self.stockGraphValuesRows, columns = self.stockGraphValuesColumns)
        dfstockGraphValues.to_csv('app/upload/' + self.key + ' datapoints.csv', sep=',')

        print("YOU DID IT!")

        return ['app/' + app.config['UPLOAD_FOLDER'] + self.key + ' Graphs.pdf', 'app/' + app.config['UPLOAD_FOLDER'] + self.key + ' datapoints.csv']
