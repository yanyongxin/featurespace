'''
Created on Apr 30, 2023

@author: yan yongxin
'''

import pandas as pd
from sklearn.preprocessing import StandardScaler
import time
import matplotlib.pyplot as plt
import numpy as np
from numpy.lib.arraysetops import _ediff1d_dispatcher
from pandas._libs.algos import diff_2d

df1 = pd.read_csv('transactions_obf.csv')
df2 = pd.read_csv('labels_obf.csv')
pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', None)
# convert the Time Stamp column to a datetime object
df1['transactionTime'] = pd.to_datetime(df1['transactionTime'])
print(df1.head(100))
sorted_df1 = df1.sort_values(by=['accountNumber', 'transactionTime'])
#sdf = sorted_df1.groupby('accountNumber')
sorted_df1['duration'] = pd.Timedelta(-1, unit='D')
sorted_df1['loca'] = 'loca'

sorted_df1 = sorted_df1.reset_index(drop=True)

print(sorted_df1.head(100))

total = len(sorted_df1)

row_prev = sorted_df1.loc(0)
for i in range(1, total-1):
    row_prev = sorted_df1.loc[i-1]
    row = sorted_df1.loc[i]
    row_next = sorted_df1.loc[i+1]
    diff_1 = pd.Timedelta(-1, unit='D')
    if row.accountNumber == row_prev.accountNumber:
        diff_1 = row.transactionTime - row_prev.transactionTime
    diff_2 = pd.Timedelta(-1, unit='D')
    if row.accountNumber == row_next.accountNumber:
        diff_2 = row_next.transactionTime - row.transactionTime
    
    diff = pd.Timedelta(-1, unit='D')
    if diff_1 > pd.Timedelta(0):
        diff = diff_1
    if diff_2 > pd.Timedelta(0):
        if diff < pd.Timedelta(0):
            diff = diff_2
        else:
            diff = min(diff, diff_2)
    sorted_df1.loc[i, 'duration'] = diff
    
sorted_df1.loc[total -1, 'duration'] = sorted_df1.loc[total -1, 'transactionTime'] - sorted_df1.loc[total -2, 'transactionTime']


print(sorted_df1.head(100))

fraud_df = sorted_df1[sorted_df1['eventId'].isin(df2['eventId'])]
good_df = sorted_df1[~sorted_df1['eventId'].isin(df2['eventId'])]

good_size = len(good_df)
fraud_size = len(fraud_df)

print(f"good: {good_size}, fraud: {fraud_size}")

accounts = {}

fraud_accounts = {}

def get_account(acct_num):
    acct = accounts.get(acct_num)
    if acct is None:
        acct = Acct(acct_num)
        accounts.update({acct_num: acct})
    return acct

def get_fraud_account(acct_num):
    acct = fraud_accounts.get(acct_num)
    if acct is None:
        acct = Acct(acct_num)
        fraud_accounts.update({acct_num: acct})
    return acct

class Event:

    def __init__(self, transactionTime,merchantId,mcc,merchantCountry,merchantZip,posEntryMode,transactionAmount,availableCash):
        self.time = transactionTime
        self.mid = merchantId
        self.mcc = mcc
        self.country = merchantCountry
        self.zip = merchantZip
        self.pos = posEntryMode
        self.amount = transactionAmount
        self.avail = availableCash
    
    def printEvent(self):
        print(f"\tTime:{self.time}, mid:{self.mid}, mcc:{self.mcc}, country:{self.country}, zip:{self.zip}, pos:{self.pos}, amount:{self.amount}, avail:{self.avail}")
        
    def getLocTimeAmt(self):
        loc = str(self.country) + "_" + str(self.zip)
        return loc, self.time, self.amount
    
# Define a class
class Acct:
    # Class property

    def __init__(self, acctnum):
        self.acctnum = acctnum
        self.events = []
        self.locations = {}
        self.durations = []
        self.amounts = []

    def add_event(self, event):
        self.events.append(event)
        
    def printAcct(self):
        sz = len(self.events)
        print(f"Account:{self.acctnum}, events:{sz}" )
        
    def findDistributions(self):
        oldtime = None
        
        for ev in self.events:
            loc,tim,amt = ev.getLocTimeAmt()
            if oldtime != None:
                dur = tim - oldtime
                self.durations.append(dur)
            oldtime = tim
            
            old_value = self.locations.get(loc)
            if old_value == None:
                self.locations.update({loc:1})
            else:
                old_value += 1
                self.locations.update({loc: old_value})
            
            self.amounts.append(amt)
            

for row in good_df.itertuples(index=False):
    event = Event(row.transactionTime,row.merchantId,row.mcc,row.merchantCountry,row.merchantZip,row.posEntryMode,row.transactionAmount,row.availableCash)
    acct = get_account(row.accountNumber)
    acct.add_event(event)

for row in fraud_df.itertuples(index=False):
    event = Event(row.transactionTime,row.merchantId,row.mcc,row.merchantCountry,row.merchantZip,row.posEntryMode,row.transactionAmount,row.availableCash)
    acct = get_fraud_account(row.accountNumber)
    acct.add_event(event)
    

print("Good Accounts: ", len(accounts))
print("Fraud_Accounts: ", len(fraud_accounts))

for key, acct in fraud_accounts.items():
    g_acct = accounts.get(key)
    if g_acct is None:
        print("account: ", key, " not exist")
        continue
    g_acct.findDistributions()
    keys = g_acct.locations.keys()
    values = g_acct.locations.values()
    
    
    # Create a bar plot with the keys on the x-axis and the values on the y-axis
#    plt.bar(keys, values)
    
    # Add a title and labels to the plot
#    plt.title('Dictionary Plot')
#    plt.xlabel('Keys')
#    plt.ylabel('Values')
    
    # Show the plot
#    plt.show()


    # Create a bar plot with the keys on the x-axis and the values on the y-axis
#    plt.bar(keys, values)
    acct.findDistributions()
    keys_f = acct.locations.keys()
    values_f = acct.locations.values()
    # Create a bar plot with the keys on the x-axis and the values on the y-axis
    width = 0.4
    
    # Create a figure and axis object
    fig, ax = plt.subplots()
    
    # Plot the first bar chart
    ax.bar(keys, values, width, label='Good', color='red')
    
    # Shift the x-coordinates of the bars to the right
    x2 = [i + width for i in range(len(keys))]
    
    # Plot the second bar chart
    ax.bar(keys_f, values_f, width, label='Fraud', color='blue')
    
    # Add a title and labels to the plot
    ax.set_title('Bar Chart Comparison')
    ax.set_xlabel('Locations')
    ax.set_ylabel('Times')
    
    # Add a legend to the plot
    ax.legend()
    
    # Show the plot
    plt.show()
    break

#    plt.bar(keys_f, values_f)
#    plt.show()


'''
for key, act in accounts.items():
    act.printAcct()
    

print("transaction:")
print(sorted_df1.head(10))
print("labels:")
#print(filtered_df.head(10))

# convert the Time Stamp column to a datetime object
#filtered_df['transactionTime'] = pd.to_datetime(filtered_df['transactionTime'])

# sort the DataFrame in terms of increasing time stamp
#sorted_df = filtered_df.sort_values('transactionTime')

#print("filtered:")
#print(filtered_df.head())

#sorted_df.to_csv('fraud.csv', index=False)
'''
