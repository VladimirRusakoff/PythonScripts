#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('matplotlib', 'inline')
import quantstats as qs
import os
import glob
import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt


# In[2]:


def addZero(num):
    if len(str(num)) == 1:
        return '0{0}'.format(num)
    else:
        return str(num)
    
listMonths = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

# получает данные по инструменту на определенную дату (если на указанную дату нет файлика, то берет данные на след.день)
def getData(instrument, dd1):
    foundFile = False
    fileName = r'E:\Date\OptionHistory\{0}\L3_options_{0}{2}{3}.csv'.format(dd1.year, listMonths[dd1.month-1], addZero(dd1.month), addZero(dd1.day))
    if os.path.exists(fileName):
        foundFile = True
    
    if foundFile:
        tabIn = pd.read_csv(fileName, sep=',', header=0)
        #print (dt.datetime.now())
        tabII = tabIn[(tabIn['UnderlyingSymbol']==instrument)]
        tabII['Expiration'] = pd.to_datetime(tabII['Expiration'])
        return tabII 
    else:
        return pd.DataFrame()

# получает данные по инструменту на определенную дату (если на указанную дату нет файлика, то берет данные на след.день)
def getDataUp(instrument, dd1, UpDown):
    foundFile = False
    fileName = r'OptionHistory\L3_{0}_{1}\L3_options_{0}{2}{3}.csv'.format(dd1.year, listMonths[dd1.month-1], addZero(dd1.month), addZero(dd1.day))
    if os.path.exists(fileName):
        foundFile = True
    else:
        if UpDown == 'up':
            for ii in range(1,11):
                dd2 = dd1 + dt.timedelta(days=ii)
                fileName = r'OptionHistory\L3_{0}_{1}\L3_options_{0}{2}{3}.csv'.format(dd2.year, listMonths[dd2.month-1], addZero(dd2.month), addZero(dd2.day))
                if os.path.exists(fileName):
                    foundFile = True
                    break
        else:
            for ii in range(1,11):
                dd2 = dd1 - dt.timedelta(days=ii)
                fileName = r'OptionHistory\L3_{0}_{1}\L3_options_{0}{2}{3}.csv'.format(dd2.year, listMonths[dd2.month-1], addZero(dd2.month), addZero(dd2.day))
                if os.path.exists(fileName):
                    foundFile = True
                    break
    if foundFile:
        tabIn = pd.read_csv(fileName, sep=',', header=0)
        #print (dt.datetime.now())
        tabII = tabIn[(tabIn['UnderlyingSymbol']==instrument)]
        tabII['Expiration'] = pd.to_datetime(tabII['Expiration'])
        return tabII 
    else:
        return pd.DataFrame()
    
def getOptionType(di):
    if di == 1:
        return 'call'
    elif di == -1:
        return 'put'
    
def getExpiration(dd1, expirs):
    dateNew = dd1 + dt.timedelta(days=30)
    expi = pd.to_datetime(expirs.unique()).sort_values()
    for el in expi:
        if el >= dateNew:
            return el
            break
    return 0

def getExpiration111(dd1, expirs):
    dateNew = dd1 + dt.timedelta(days=90)
    expi = pd.to_datetime(expirs.unique()).sort_values()
    for el in expi:
        if el >= dateNew:
            return el
            break
    return 0

def getStrDate(date):
    return str((date).strftime(format='%d.%m.%Y'))

def getATM12(ulPrice, strikes):
    returnStrike = 0.0
    stri = pd.to_numeric(strikes.unique())
    stri.sort()
    for e in np.arange(1, len(stri)):
        if ulPrice >= stri[e-1] and ulPrice <= stri[e]:
            if (ulPrice-stri[e-1]) == (stri[e]-ulPrice):
                returnStrike = stri[e-1]
                break
            elif (ulPrice-stri[e-1]) > (stri[e]-ulPrice):
                returnStrike = stri[e]
                break
            else:
                returnStrike = stri[e-1]
                break
    return returnStrike

def getATM111(ulPrice, strikes, dirr):
    stri = pd.to_numeric(strikes.unique())
    stri.sort()
    ij = 0
    for e in np.arange(1, len(stri)):
        if ulPrice >= stri[e-1] and ulPrice <= stri[e]:
            ij = e
            break
    if dirr == 1:
        if ij+1 < len(stri):
            return stri[ij+1]
    elif dirr == -1:
        if ij-1 >= 0:
            return stri[ij-1]          
    return stri[ij]

def getPrice(Last, Ask, Bid):
    if Last == 0.0:
        return (Bid + Ask) / 2
    else:
        return Last
    
def strDate(date):
    return str(date.strftime(format='%d.%m.%Y'))


# In[3]:


def getDelta(df, dirr, delta, date1):
    df = df[df['Type']==getOptionType(dirr)]
    dd = getNeededDelta(df, delta, date1)
    df1 = df[df['Delta']==dd]
    if len(df1) > 0:
        return df1
    else:
        return pd.DataFrame()
    
def getATM(df, dirr, date1):
    df = df[df['Type']==getOptionType(dirr)]
    df = df[date1 + dt.timedelta(days=30) <= df['Expiration']] 
    ulPrice = df['UnderlyingPrice'].iloc[0]
    strikes = pd.to_numeric(df['Strike'].unique())
    strikes.sort()
    listDiff = list(abs(ulPrice - strikes))
    ii = listDiff.index(min(listDiff))
    df1 = df[(df['Strike']==strikes[ii]) & (df['Expiration']==min(df['Expiration'].unique()))]
    if len(df1) > 0:
        return df1
    else:
        return pd.DataFrame()
    
def getOptionName(df, optionName):
    df1 = df[df['OptionSymbol'] == optionName]
    if len(df1) > 0:
        return df1
    else:
        return pd.DataFrame()
    
def getNeededDelta(df, val, date1):
    df = df[date1 + dt.timedelta(days=30) <= df['Expiration']]
    deltas = df['Delta'].unique()
    qqq = abs(deltas)
    qqq = list(abs(val-qqq))
    ii = qqq.index(min(qqq))
    return deltas[ii]


# In[30]:


# begin new strategy
tabSignals = pd.read_csv(r'Signaly.csv', sep=';', header=0)#, parse_dates=['Date'])
tabSignals['Date'] = pd.to_datetime(tabSignals['Date'], format='%d.%m.%Y')
tabSignals.index = tabSignals['Date']
tabSignals['Date1'] = tabSignals['Date'].shift(-1)
tabSignals = tabSignals[['Date1', 'signal_hsi(china index)', 'signal_mid cap_US_ind', 'signal_bond(Treasures)']]
tabSignals = tabSignals[tabSignals.index.year >= 2004] #== 2006) & (tabSignals.index.month == 12)]


# In[31]:


methodOption = 'Combination'
neededDelta = 0.25
takeProfit = 3
#
takeIsComing = ''
#
chinaIndex = 'FXI'
midCapUS = 'IWS'
bondTreasures = 'IEF'
tabSignals['Ticker'] = 'ticker'
tabSignals['Direction'] = 0.0
#
tabSignals['OptionName'] = ''
tabSignals['Price'] = 0.0
tabSignals['UnderlyingPrice'] = 0.0
tabSignals['Delta'] = 0.0
tabSignals['Expiration'] = ''
tabSignals['Details'] = ''
tabSignals['Strike'] = 0.0
tabSignals['Volume'] = 0.0
tabSignals['OpenInterest'] = 0.0
tabSignals['T1OpenInterest'] = 0.0
tabSignals['PL'] = 0.0
#
priceEnter = 0
ulPriceEnter = 0
indEnter = 0
# 
for ij in range(0,len(tabSignals)-1):
    print ('{0}::{1}'.format(ij, tabSignals['Date1'].iloc[ij]))
    #
    if tabSignals['signal_hsi(china index)'].iloc[ij] != 0:
        tabSignals['Ticker'].iloc[ij] = chinaIndex
        tabSignals['Direction'].iloc[ij] = tabSignals['signal_hsi(china index)'].iloc[ij]
    elif tabSignals['signal_mid cap_US_ind'].iloc[ij] != 0:
        tabSignals['Ticker'].iloc[ij] = midCapUS
        tabSignals['Direction'].iloc[ij] = tabSignals['signal_mid cap_US_ind'].iloc[ij]
    elif tabSignals['signal_bond(Treasures)'].iloc[ij] != 0:
        tabSignals['Ticker'].iloc[ij] = bondTreasures
        tabSignals['Direction'].iloc[ij] = tabSignals['signal_bond(Treasures)'].iloc[ij]
        
    # 
    ddf = getData(tabSignals['Ticker'].iloc[ij], tabSignals['Date1'].iloc[ij])
    if len(ddf) > 0:
        ddf1 = pd.DataFrame()
        if ij != 0:
            if tabSignals['OptionName'].iloc[ij-1] != '':
                ddf1 = ddf[ddf['OptionSymbol'] == tabSignals['OptionName'].iloc[ij-1]]
    
        if len(ddf1) == 0 or tabSignals['Details'].iloc[ij-1].find('Exit') >= 0:
            if methodOption == 'ATM':
                ddf1 = getATM(ddf, tabSignals['Direction'].iloc[ij], tabSignals['Date1'].iloc[ij])
            elif methodOption == 'Combination':
                if tabSignals['Ticker'].iloc[ij] == 'FXI':
                    #ddf1 = getATM(ddf, tabSignals['Direction'].iloc[ij], tabSignals['Date1'].iloc[ij])
                    ddf1 = getDelta(ddf, tabSignals['Direction'].iloc[ij], 0.1, tabSignals['Date1'].iloc[ij])
                else:
                    ddf1 = getDelta(ddf, tabSignals['Direction'].iloc[ij], neededDelta, tabSignals['Date1'].iloc[ij])
            else:
                ddf1 = getDelta(ddf, tabSignals['Direction'].iloc[ij], neededDelta, tabSignals['Date1'].iloc[ij])
                
            #ddf1 = ddf[ddf['Type'] == getOptionType(tabSignals['Direction'].iloc[ij])]
            #dd = 0.1
            #delta = getNeededDelta(dd, ddf1['Delta'].unique())
            #ddf1 = ddf[ddf['Delta']==delta]
            if takeIsComing != '':
                if takeIsComing == tabSignals['Ticker'].iloc[ij]:
                    continue
            #
            if len(ddf1) == 0:
                continue
            
            takeIsComing = ''
            tabSignals['Details'].iloc[ij] = 'Enter'
            tabSignals['Price'].iloc[ij] = getPrice(ddf1['Last'].iloc[0], ddf1['Ask'].iloc[0], ddf1['Bid'].iloc[0])
            priceEnter = tabSignals['Price'].iloc[ij]
            ulPriceEnter = ddf1['UnderlyingPrice'].iloc[0]
            indEnter = ij
            
            if ij != 0:
                if tabSignals['Ticker'].iloc[ij] != tabSignals['Ticker'].iloc[ij-1]:
                    if tabSignals['Details'].iloc[ij-1] == 'Enter':
                        dr = getData(tabSignals['Ticker'].iloc[ij-1], tabSignals['Date1'].iloc[ij])
                        dm = getOptionName(dr, tabSignals['OptionName'].iloc[ij-1])
                        if len(dm) > 0:
                            priceP = getPrice(dm['Last'].iloc[0], dm['Ask'].iloc[0], dm['Bid'].iloc[0])
                            tabSignals['Details'].iloc[ij-1] = 'Enter;Exit_Signal;Price={0}'.format(priceP)
                            tabSignals['PL'].iloc[ij-1] = priceP - tabSignals['Price'].iloc[ij-1]  
                    else:
                        if tabSignals['Details'].iloc[ij-1] != '':
                            tabSignals['Details'].iloc[ij-1] = 'Exit_Signal'
        else:
            tabSignals['Details'].iloc[ij] = 'in'
            tabSignals['Price'].iloc[ij] = getPrice(ddf1['Last'].iloc[0], ddf1['Ask'].iloc[0], ddf1['Bid'].iloc[0])
        
        tabSignals['OptionName'].iloc[ij] = ddf1['OptionSymbol'].iloc[0]
        tabSignals['UnderlyingPrice'].iloc[ij] =  ddf1['UnderlyingPrice'].iloc[0]
        tabSignals['Delta'].iloc[ij] = ddf1['Delta'].iloc[0]
        tabSignals['Expiration'].iloc[ij] = ddf1['Expiration'].iloc[0] 
        tabSignals['Strike'].iloc[ij] = ddf1['Strike'].iloc[0]
        tabSignals['Volume'].iloc[ij] = ddf1['Volume'].iloc[0]
        tabSignals['OpenInterest'].iloc[ij] = ddf1['OpenInterest'].iloc[0]
        tabSignals['T1OpenInterest'].iloc[ij] = ddf1['T1OpenInterest'].iloc[0]
        
        if ij != 0:
            if tabSignals['OptionName'].iloc[ij-1] == tabSignals['OptionName'].iloc[ij]:
                if tabSignals['Price'].iloc[ij] != 0:
                    tabSignals['PL'].iloc[ij] = tabSignals['Price'].iloc[ij] - tabSignals['Price'].iloc[ij-1]
        
        if tabSignals['Details'].iloc[ij] == 'in':
            if tabSignals['Price'].iloc[ij] >= takeProfit * priceEnter:
                tabSignals['Details'].iloc[ij] = 'Exit_TakeP'
                takeIsComing = tabSignals['Ticker'].iloc[ij]
            if ij + 1 < len(tabSignals):
                if tabSignals['Date1'].iloc[ij] <= tabSignals['Expiration'].iloc[ij] and tabSignals['Expiration'].iloc[ij] <= tabSignals['Date1'].iloc[ij+1]:
                    #takeIsComing = tabSignals['Ticker'].iloc[ij] # если не нужно заходить после экспирации
                    tabSignals['Details'].iloc[ij] = 'Exit_Expir'
                    if tabSignals['Direction'].iloc[ij] == 1: 
                        tabSignals['PL'].iloc[ij] = max(tabSignals['UnderlyingPrice'].iloc[ij]-tabSignals['Strike'].iloc[ij],0)-priceEnter
                    elif tabSignals['Direction'].iloc[ij] == -1:
                        tabSignals['PL'].iloc[ij] = max(tabSignals['Strike'].iloc[ij]-tabSignals['UnderlyingPrice'].iloc[ij],0)-priceEnter
                    for el in range(indEnter, ij):
                        tabSignals['PL'].iloc[el] = 0.0
                          
tabSignals.to_csv(r'Delta025TP3_FXIatm.csv', sep=';')


# In[26]:


tabSignals


# In[17]:


tabSignals[tabSignals['Ticker']=='FXI']['PL'].sum()


# In[15]:


tabSignals[tabSignals['Ticker']=='IWS']['PL'].sum()


# In[16]:


tabSignals[tabSignals['Ticker']=='IEF']['PL'].sum()


# In[32]:


tabSignals['PL'].cumsum().plot()


# In[16]:


tabSignals[tabSignals['Ticker']=='FXI']['PL'].mean()


# In[20]:


tabSignals[tabSignals['Ticker']=='IEF']['PL'].sum()


# In[19]:


tabSignals[tabSignals['Ticker']=='IWS']['PL'].sum()


# In[10]:


tabSignals = pd.read_csv(r'D:\rvm\ВК\OptionTesting\tabSignals31.csv', sep=';', header=0)
tabSignals['PL'].cumsum().plot()


# In[4]:


tabSignals = pd.read_csv(r'Delta025TP3.csv', sep=';', header=0)
tabSignals['PL'].cumsum().plot()


# In[7]:


#
chinaIndex = 'FXI'
midCapUS = 'IWS'
bondTreasures = 'IEF'
tabSignals['Ticker'] = 'ticker'
tabSignals['Direction'] = 0.0
#
tabSignals['UnderlyingPrice'] = 0.0
#
priceEnter = 0
ulPriceEnter = 0
indEnter = 0
# 
for ij in range(0,len(tabSignals)-1):
    print ('{0}::{1}'.format(ij, tabSignals['Date1'].iloc[ij]))
    #
    if tabSignals['signal_hsi(china index)'].iloc[ij] != 0:
        tabSignals['Ticker'].iloc[ij] = chinaIndex
        tabSignals['Direction'].iloc[ij] = tabSignals['signal_hsi(china index)'].iloc[ij]
    elif tabSignals['signal_mid cap_US_ind'].iloc[ij] != 0:
        tabSignals['Ticker'].iloc[ij] = midCapUS
        tabSignals['Direction'].iloc[ij] = tabSignals['signal_mid cap_US_ind'].iloc[ij]
    elif tabSignals['signal_bond(Treasures)'].iloc[ij] != 0:
        tabSignals['Ticker'].iloc[ij] = bondTreasures
        tabSignals['Direction'].iloc[ij] = tabSignals['signal_bond(Treasures)'].iloc[ij]
        
    # 
    ddf = getData(tabSignals['Ticker'].iloc[ij], tabSignals['Date1'].iloc[ij])
    if len(ddf) > 0:
        tabSignals['UnderlyingPrice'].iloc[ij] = ddf['UnderlyingPrice'].iloc[0]


# In[9]:


tabSignals['PL'] = 0.0
for i in range(1, len(tabSignals)-1):
    if tabSignals['Ticker'].iloc[i-1] == tabSignals['Ticker'].iloc[i]:
        tabSignals['PL'].iloc[i] = tabSignals['Direction'].iloc[i] * (tabSignals['UnderlyingPrice'].iloc[i] - tabSignals['UnderlyingPrice'].iloc[i-1])


# In[14]:


tabSignals['PL'].cumsum().plot(figsize=(14,7))


# In[115]:


methodOption = 'ATM111'
neededDelta = 0.1
takeProfit = 3   
#
takeIsComing = ''
#
chinaIndex = 'FXI'
midCapUS = 'IWS'
bondTreasures = 'IEF'
tabSignals['Ticker'] = 'ticker'
tabSignals['Direction'] = 0.0
#
tabSignals['OptionName'] = ''
tabSignals['Price'] = 0.0
tabSignals['UnderlyingPrice'] = 0.0
tabSignals['Delta'] = 0.0
tabSignals['Expiration'] = ''
tabSignals['Details'] = ''
tabSignals['Strike'] = 0.0
tabSignals['Volume'] = 0.0
tabSignals['OpenInterest'] = 0.0
tabSignals['T1OpenInterest'] = 0.0
tabSignals['PL'] = 0.0
#
priceEnter = 0
ulPriceEnter = 0
indEnter = 0
# 
for ij in range(0,len(tabSignals)-1):
    print ('{0}::{1}'.format(ij, tabSignals['Date1'].iloc[ij]))
    #
    if tabSignals['signal_hsi(china index)'].iloc[ij] != 0:
        tabSignals['Ticker'].iloc[ij] = chinaIndex
        tabSignals['Direction'].iloc[ij] = tabSignals['signal_hsi(china index)'].iloc[ij]
    elif tabSignals['signal_mid cap_US_ind'].iloc[ij] != 0:
        tabSignals['Ticker'].iloc[ij] = midCapUS
        tabSignals['Direction'].iloc[ij] = tabSignals['signal_mid cap_US_ind'].iloc[ij]
    elif tabSignals['signal_bond(Treasures)'].iloc[ij] != 0:
        tabSignals['Ticker'].iloc[ij] = bondTreasures
        tabSignals['Direction'].iloc[ij] = tabSignals['signal_bond(Treasures)'].iloc[ij]
        
    # 
    ddf = getData(tabSignals['Ticker'].iloc[ij], tabSignals['Date1'].iloc[ij])
    if len(ddf) > 0:
        ddf1 = pd.DataFrame()
        if ij != 0:
            if tabSignals['OptionName'].iloc[ij-1] != '':
                ddf1 = ddf[ddf['OptionSymbol'] == tabSignals['OptionName'].iloc[ij-1]]
    
        if len(ddf1) == 0 or tabSignals['Details'].iloc[ij-1].find('Exit') >= 0:
            if methodOption == 'ATM':
                ddf1 = getATM(ddf, tabSignals['Direction'].iloc[ij])
            else:
                ddf1 = getDelta(ddf, tabSignals['Direction'].iloc[ij], neededDelta, tabSignals['Date1'].iloc[ij])
                
            #ddf1 = ddf[ddf['Type'] == getOptionType(tabSignals['Direction'].iloc[ij])]
            #dd = 0.1
            #delta = getNeededDelta(dd, ddf1['Delta'].unique())
            #ddf1 = ddf[ddf['Delta']==delta]
            if takeIsComing != '':
                if takeIsComing == tabSignals['Ticker'].iloc[ij]:
                    continue
            #
            if len(ddf1) == 0:
                continue
            
            takeIsComing = ''
            tabSignals['Details'].iloc[ij] = 'Enter'
            tabSignals['Price'].iloc[ij] = getPrice(ddf1['Last'].iloc[0], ddf1['Ask'].iloc[0], ddf1['Bid'].iloc[0])
            priceEnter = tabSignals['Price'].iloc[ij]
            ulPriceEnter = ddf1['UnderlyingPrice'].iloc[0]
            indEnter = ij
            
            if ij != 0:
                if tabSignals['Ticker'].iloc[ij] != tabSignals['Ticker'].iloc[ij-1]:
                    if tabSignals['Details'].iloc[ij-1] == 'Enter':
                        dr = getData(tabSignals['Ticker'].iloc[ij-1], tabSignals['Date1'].iloc[ij])
                        dm = getOptionName(dr, tabSignals['OptionName'].iloc[ij-1])
                        if len(dm) > 0:
                            priceP = getPrice(dm['Last'].iloc[0], dm['Ask'].iloc[0], dm['Bid'].iloc[0])
                            tabSignals['Details'].iloc[ij-1] = 'Enter;Exit_Signal;Price={0}'.format(priceP)
                            tabSignals['PL'].iloc[ij-1] = priceP - tabSignals['Price'].iloc[ij-1]  
                    else:
                        if tabSignals['Details'].iloc[ij-1] != '':
                            tabSignals['Details'].iloc[ij-1] = 'Exit_Signal'
        else:
            tabSignals['Details'].iloc[ij] = 'in'
            tabSignals['Price'].iloc[ij] = getPrice(ddf1['Last'].iloc[0], ddf1['Ask'].iloc[0], ddf1['Bid'].iloc[0])
        
        tabSignals['OptionName'].iloc[ij] = ddf1['OptionSymbol'].iloc[0]
        tabSignals['UnderlyingPrice'].iloc[ij] =  ddf1['UnderlyingPrice'].iloc[0]
        tabSignals['Delta'].iloc[ij] = ddf1['Delta'].iloc[0]
        tabSignals['Expiration'].iloc[ij] = ddf1['Expiration'].iloc[0] 
        tabSignals['Strike'].iloc[ij] = ddf1['Strike'].iloc[0]
        tabSignals['Volume'].iloc[ij] = ddf1['Volume'].iloc[0]
        tabSignals['OpenInterest'].iloc[ij] = ddf1['OpenInterest'].iloc[0]
        tabSignals['T1OpenInterest'].iloc[ij] = ddf1['T1OpenInterest'].iloc[0]
        
        if ij != 0:
            if tabSignals['OptionName'].iloc[ij-1] == tabSignals['OptionName'].iloc[ij]:
                tabSignals['PL'].iloc[ij] = tabSignals['Price'].iloc[ij] - tabSignals['Price'].iloc[ij-1]
        
        if tabSignals['Details'].iloc[ij] == 'in':
            if tabSignals['Price'].iloc[ij] >= takeProfit * priceEnter:
                tabSignals['Details'].iloc[ij] = 'Exit_TakeP'
                takeIsComing = tabSignals['Ticker'].iloc[ij]
            if ij + 1 < len(tabSignals):
                if tabSignals['Date1'].iloc[ij] <= tabSignals['Expiration'].iloc[ij] and tabSignals['Expiration'].iloc[ij] <= tabSignals['Date1'].iloc[ij+1]:
                    #takeIsComing = tabSignals['Ticker'].iloc[ij] # если не нужно заходить после экспирации
                    tabSignals['Details'].iloc[ij] = 'Exit_Expir'
                    if tabSignals['Direction'].iloc[ij] == 1: 
                        tabSignals['PL'].iloc[ij] = max(tabSignals['UnderlyingPrice'].iloc[ij]-tabSignals['Strike'].iloc[ij],0)-priceEnter
                    elif tabSignals['Direction'].iloc[ij] == -1:
                        tabSignals['PL'].iloc[ij] = max(tabSignals['Strike'].iloc[ij]-tabSignals['UnderlyingPrice'].iloc[ij],0)-priceEnter
                    for el in range(indEnter, ij):
                        tabSignals['PL'].iloc[el] = 0.0
                        
tabSignals.to_csv(r'tabSignals1.csv', sep=';')


# In[117]:


tabSignals.to_csv(r'tabSignals2.csv', sep=';')


# In[116]:


tabSignals['PL'].cumsum().plot(figsize=(14,7))


# In[78]:


tabSignals[tabSignals['Ticker']=='FXI']['PL'].mean()


# In[80]:


tabSignals[tabSignals['Ticker']=='IWS']['PL'].sum()


# In[81]:


tabSignals[tabSignals['Ticker']=='IEF']['PL'].mean()


# In[ ]:




