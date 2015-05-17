"""
a program to find the mean price of a  stock on a given day

url format is http://bigcharts.marketwatch.com/historical/default.asp?symb=MSFT&closeDate=5%2F13%2F10

where s = the stock ticker symbol and date is the 

"""

import urllib2, unicodedata
from bs4 import BeautifulSoup
from Tkinter import *

                



class stock:
    def __init__(self, stockSymbol):
        self.ticker = stockSymbol
        self.dates = []
        self.data = [] #dictionary of stock info on that day
    
    def addDate(self, date):
        if type(date) == list:
            self.dates.append([x for x in date])
        if type(date) == str:    
            self.dates.append(date)
            
    def updateData(date, average):
        self.data.append({date:average})
        
        
    
    def formatDate(self,dateStr):
        """ replaces '/' in datestring with %2F"""
        return "%2F".join(dateStr.split("/"))
    
    
    def average(self, price1, price2):
        return (float(price1) + float(price2))/2.00



    def getData(self):
        """should parse the html of the stock ticking webpage and get the high and low for the day and return a tuple of two floats"""
        
        for date in self.dates:
            
            url = "http://bigcharts.marketwatch.com/historical/default.asp?symb=" + self.ticker + "&closeDate=" + self.formatDate(date)
            
            response = urllib2.urlopen(url)
            html = response.read()    
            
            
            soup = BeautifulSoup(html)
            table = soup.find('table').findAll('th')
    
            stockInfo = {"date": date, "high": 0.0, "low": 0.0}
            
            for th in table:
                if th.getText() == 'High:':
                    stockInfo['high'] = float(th.parent.td.getText())
                if th.getText() == 'Low:':
                    stockInfo['low'] = float(th.parent.td.getText())
                
            stockInfo['average'] = self.average(stockInfo['high'], stockInfo['low'])
            
            self.data.append(stockInfo)
            
    def printResults(self):
        print self.ticker + "\n"
        
        for item in self.data:
            print item["date"]+ ": " + str(item["average"] )
    
def main():
    
    ticker = raw_input("Enter the Stock you want to look up: ")
    date = raw_input("What date: ")
    
    print "looking up data...."
    s = stock(ticker)
    s.addDate(date)
    s.getData()
    s.printResults()