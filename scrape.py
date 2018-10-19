'''
Author: Daniel Frederick
Date: October 18, 2018
'''

from lxml import html
import requests
import datetime
import csv
import os

'''
filepath = os.path.join('c:/your/full/path', 'filename')
if not os.path.exists('c:/your/full/path'):
    os.makedirs('c:/your/full/path')
f = open(filepath, "a")
'''

'''
print('Getting site code... ')
page = requests.get('https://eve-marketdata.com/industry/ore')
print('Parsing site code... ')
tree = html.fromstring(page.content)
'''

names = ['Arkonor', 'Bistot', 'Crokite', 'Dark Ochre', 'Gneiss', 'Hedbergite', 'Hemorphite', 'Jaspet', 'Kernite', 'Mercoxit', 'Omber', 'Plagioclase', 'Pyroxeres', 'Scordite', 'Spodumain', 'Veldspar']

class scrape:
    def __init__(self):
        print('Getting site code... ')
        self.page = requests.get('https://eve-marketdata.com/industry/ore')
        print('Parsing site code... ')
        self.tree = html.fromstring(self.page.content)

    #returns an array of prices
    def getPrices(self):
        print('Scraping https://eve-marketdata.com/industry/ore for market data... ')
        return self.tree.xpath('//td[@class="price"]/text()')

    #returns a combined array of the word ore, volume, isk/m3, and isk/h
    def getOre(self):
        return self.tree.xpath('//span[@class="ore"]/text()')

    def imm(self):
        im = self.tree.xpath('//span[@class="ore"]/text()')
        a=[] #the word ore
        b=[] #volume
        c=[] #isk/m3
        d=[] #isk/h
        ans=[]
        x=1
        i=0
        while i < len(im):
            n=True
            if x == 1 and n == True:
                a.append(im[i])
                x+=1
                n=False
            if x == 2 and n == True:
                b.append(im[i])
                x+=1
                n=False
            if x == 3 and n == True:
                c.append(im[i])
                x+=1
                n=False
            if x == 4 and n == True:
                d.append(im[i])
                x = 1
            i += 1
        ans.append(c)
        ans.append(d)
        return ans

    def estIsk(self, holdCap):
        ans = []
        temp = self.imm()
        iskm3 = temp[0]
        for i in iskm3:
            ans.append(int(i)*int(holdCap))
        return ans

    #outputs a text file with results
    def output(self, path):
        print('Creating output file... ')
        now = datetime.datetime.now()

        
        filename = 'output' + now.strftime(' %Y-%m-%d %H %M') + '.csv'
        filepath = os.path.join(path, filename)
        if not os.path.exists(path):
            print('Path does not exist, creating directory now... ')
            os.makedirs(path)
        f = open(filepath, "w")
        
        writer = csv.writer(f, delimiter=',', quotechar='"',quoting=csv.QUOTE_MINIMAL)
        names.insert(0, 'NAMES')
        writer.writerow(names)      #write names row
        prices = self.getPrices()
        prices.insert(0, 'PRICES')
        writer.writerow(prices)     #write prices row
        k = self.imm()
        iskm3 = k[0]
        iskh = k[1]
        iskm3.insert(0, 'ISK/m3')
        writer.writerow(iskm3)      #write isk/m3 row
        #hold = input('Enter hold capacity --> ')
        #eIsk = self.estIsk(hold)
        #eIsk.insert(0, 'EST PROFIT')
        #writer.writerow(eIsk)       #write est profit row
        iskh.insert(0, 'ISK/h')
        writer.writerow(iskh)       #write isk/h row
        f.close()
        print('Succesfully outputed ' + 'output' + now.strftime(' %Y-%m-%d %H %M') + '.csv')
        #i=input('Press any key to exit --> ')

class server:
    def __init__(self):
        self.h = self.currentHour()
        self.m = self.currentMin()

    #asks user how often the program should update, and how many times
    def run(self):
        self.path = input('Enter desired output files (ex. C:/your/full/path) --> ')
        print('Would you like to program to update every minute or every hour? ')
        while True:
            j = str(input('h or m --> '))
            if j == 'h' or j == 'm':
                break
            elif j != 'h':
                if j != 'm':
                    print('Unrecognized answer. Please try again. ')

        while True:
            its = input('How many times would you like the program to update after the initial update? --> ')
            #try:
            #    its = int(its)
            #except ValueError
            #    print('Please enter an integer greater than 0. Try again. ')
            if its.isdigit() == False:
                print('Please try again. ')
            else:
                break

        #initial update
        t = scrape()
        t.output(self.path)
        print('Initial iteration concluded. \n')

        if j == 'h':
            print('Updating every hour, ' + str(its) + ' times.\n ')
            self.updateH(int(its))
        if j == 'm':
            print('Updating every minute, ' + str(its) + ' times.\n ')
            self.updateM(int(its))

    #updates every minute, up to its iterations
    def updateM(self, its):
        i = 0
        while True:
            if self.currentMin() != self.m:
                t = scrape()
                t.output(self.path)
                print('Iteration ' + str(i + 1) + ' concluded. '+ str(its - i) + ' remaining.\n')
                self.m = self.currentMin()
                i += 1
            if i >= its:
                temp = input('Operation concluded. Press any key to exit -->')
                exit()

    #updates every hour, up to its iterations
    def updateH(self, its):
        i = 0
        while True:
            if self.currentHour() != self.h:
                t = scrape()
                t.output(self.path)
                print('Iteration ' + str(i + 1) + ' concluded. '+ str(its - i) + ' remaining.\n')
                self.h = self.currentHour()
                i += 1
            if i >= its:
                temp = input('Operation concluded. Press any key to exit -->')
                exit()

    #checks current hour
    def currentHour(self):
        now = datetime.datetime.now()
        ans = now.hour
        return ans

    #checks current minute
    def currentMin(self):
        now = datetime.datetime.now()
        ans = now.minute
        return ans

#inst = scrape()
#inst.outputCsv()

temp = server()
temp.run()
            
