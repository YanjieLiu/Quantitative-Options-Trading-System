
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import *


cpu = pd.read_excel("50ETF.xlsx","underlyingclose30")
cpo = pd.read_excel("50ETF.xlsx","close")

###  日期转换函数
def returnYear(date):
    a=date.year
    return a

def returnMonth(date):
    a=date.month
    return a

def yearMonth(date):
    a = date.year
    b = date.month
    c=str(a)+"-"+str(b)
    return(c)
    
def yearMonthDay(date):
    a=date.year
    b=date.month
    c=date.day
    d=str(a)+"-"+str(b)+"-"+str(c)
    return(d)
    
def callorput(x):
    if(x==1):
        a='购'
        return(a)
    else:
        b='沽'
        return (b)
    
def outMoneyPrice(callput, strikeprice):  #
    #print(strikeprice)
    if(callput == 1):
        if (strikeprice <= 3):
            interval =np.arange(0, 3.05, 0.05)
            for j in interval:
                if j>=strikeprice:
                    str_prc=j
                    break
        elif(strikeprice > 3):
            interval =np.arange(3, 5, 0.1)
            for j in interval:
                if j>strikeprice:
                    str_prc=j
                    break
    elif (callput == -1):
        if (strikeprice <= 3):
            interval =np.arange(0, 3.05, 0.05)
            for i,j in enumerate(interval):
                if j>=strikeprice:
                    str_prc=interval[i-1]
                    break
        elif (strikeprice > 3):
            interval =np.arange(3, 5, 0.1)
            for i,j in enumerate(interval):
                if j>=strikeprice:
                    str_prc=interval[i-1]
                    break
    return (str_prc)

def atMoneyPrice(strikeprice):   #
    if strikeprice<=3:
        a=round(round((strikeprice+0.0001)/0.05)*0.05,2)#-0.0001是为了将价格2.375平值视作2.35
    if strikeprice>3:
        a = round(round(strikeprice / 0.1) * 0.1,2)
    return a

#####  统计过去高低平均


a=[]
for i in np.arange(15,len(cpu['close'])+1,1):
    #if i<=len(cpu['close'])-120:
        a.append(np.mean(cpu['close'][i-15:i]))
        
#### 计算过去50ETF收盘价的高、低、均值        
high=[]
low=[]
avg=[]
for i in np.arange(120,len(cpu['close'])+1,1):
    avg.append(np.mean(cpu['close'][i-120:i]))

for i in np.arange(24,len(cpu['close'])+1,1):
    #if i<=(len(cpu['close'])-20):
        high.append(np.max(cpu['close'][i-24:i]))
        low.append(np.min(cpu['close'][i-24:i]))
        
        
        
"""high=filter(None,high)
low=filter(None,low)
avg=filter(None,avg)"""
######expiration date summary#####
exp_store=['2015-3-25',
             '2015-4-22',
             '2015-5-27',
             '2015-6-24',
             '2015-7-22',
             '2015-8-26',
             '2015-9-30',
             '2015-10-28',
             '2015-11-25',
             '2015-12-23',
             '2016-1-27',
             '2016-2-24',
             '2016-3-23',
             '2016-4-27',
             '2016-5-25',
             '2016-6-22',
             '2016-7-27',
             '2016-8-24',
             '2016-9-28',
             '2016-10-26',
             '2016-11-23',
             '2016-12-28',
             '2017-1-25',
             '2017-2-22',
             '2017-3-22',
             '2017-4-26',
             '2017-5-24',
             '2017-6-28',
             '2017-7-26',
             '2017-8-23',
             '2017-9-27',
             '2017-10-25',
             '2017-11-22',
             '2017-12-27',
             '2018-1-24',
             '2018-2-28',
             '2018-3-28',
             '2018-4-25',
             '2018-5-23',
             '2018-6-27',
             '2018-7-25',
             '2018-8-22',
             '2018-9-26'
             ]
######
def isexp(date):#判断日期是否超过到期日
    global t2
    t1=yearMonthDay(date)
    #print(t1)
    year=returnYear(date)
    month=returnMonth(date)
    expiration=str(year)+'-'+ str(month)+'-'
    for exp in exp_store:
        if expiration in exp:
            t2=yearMonthDay(datetime.strptime(exp,'%Y-%m-%d'))
    if t1<t2:
        return(-1)
    if t1>=t2:
        return(1)
def onexpday(date):#判断日期是否是到期日
    global t2
    t1=yearMonthDay(date)
    #print(t1)
    year=returnYear(date)
    month=returnMonth(date)
    expiration=str(year)+'-'+ str(month)+'-'
    for exp in exp_store:
        if expiration in exp:
            t2=yearMonthDay(datetime.strptime(exp,'%Y-%m-%d'))
    if t1==t2:
        return(1)
    else:
        return (-1)
    
####  这个是对日期价格找出下个月期权合约,用于到期后    
def exp_option(date, strikeprice, callput):
    type = callorput(callput)
    year = returnYear(date)
    month = returnMonth(date)
    price = str("%.2f" % ( strikeprice))
    NAME = [column for column in cpo]
    # set position
    if month < 12:
        month = month + 1
        string = str(type)+str(year)+"年"+str(month)+"月"+str(price)
        for i,j in enumerate(NAME):
            if string in j:
                column=i
                return (column)
    if month == 12:
        year = year + 1
        month = 1
        string = str(type)+str(year)+"年"+str(month)+"月"+str(price)
        for i,name in enumerate(NAME):
            if string in name:
                column=i
                return (column)
    # offset position
    string=string = type+str(year)+"年"+str(month)+"月"+str(price)
    for i, name in enumerate(NAME):
        if string in name:
            column = i
            
def findOption(situation, date, strikeprice, callput):
    type = callorput(callput)
    year = returnYear(date)
    month = returnMonth(date)
    #price = round(outMoneyPrice(callput, strikeprice) ,2)
    price=str("%.2f" % (outMoneyPrice(callput,strikeprice)))
 
    NAME = [column for column in cpo]
    # before expiration date,到期日前
    if situation == -1:
        string = str(type)+str(year)+"年"+str(month)+"月"+str(price)
        #print(string)
        for i,j in enumerate(NAME):
            if string in j:
                column=i
                break
        if column!= None and len(str(column))<5:
            return (column)
        else:
            return (None)
    # equal or surpass expiration date,到到期日
    if situation == 1:
        column=exp_option(date, strikeprice, callput)
        if column != None:
            return (column)
        else:
            return(None)


#######################################position##########################################
day2=[]
flag =0
set =0
shut1 = -1 #put option
shut2 = 1#call option
shut3=2#日内交易
cost=None
revenue=None
column=None
Return =[]#return for strategy
documentTime=[]
j=0

date_infor = []
posit_infor = []
i_infor = []
revenue_infor = []
column_infor = []
row_infor = []
##

#### 这里是用30分钟线
for i in np.arange(120,len(cpu['date'])-1,1):
    try:
        date = datetime.strptime(str(cpu['date'][i]), '%d/%m/%Y %H:%M')
    except:
        date = datetime.strptime(str(cpu['date'][i]), '%Y-%m-%d %H:%M:%S')
    strikeprice=cpu['close'][i]
    nowday = yearMonthDay(date)
    
    
######################################set position################## 开仓
    ### 上升趋势 ###  过去ma15大于ma120，价格
    if onexpday(date)==-1  and a[i-15] > avg[i-120] and  cpu['close'][i] >1.001*high[i-24] and flag != shut1 and flag != shut2 :
        for k, day in enumerate(cpo['date']):
            day = yearMonthDay(day)
            if nowday == day:
                rowIndex = k
        column = findOption(situation=isexp(date), date=date, strikeprice=outMoneyPrice(1,strikeprice), callput=-1)
        # no contract needed
        if column is None:
            revenue=None
        else:
            revenue=cpo.iat[rowIndex, column]
        flag = shut1
        #print(a[i-119],high[i-119])
        date_infor.append(str(cpu['date'][i]))
        posit_infor.append(' short put ')
        i_infor.append(str(i))
        revenue_infor.append(revenue)
        column_infor.append(str(column))
        row_infor.append(str(rowIndex))
    
        ####down trend####
    elif onexpday(date)== -1  and a[i-15] < avg[i-120] and cpu['close'][i] <0.999*low[i-24] and flag != shut1 and flag != shut2 :
        for k, day in enumerate(cpo['date']):
            day = yearMonthDay(day)
            if nowday == day:
                rowIndex = k
        column = findOption(situation=isexp(date), date=date, strikeprice=outMoneyPrice(-1,strikeprice), callput=1)

        if column is None:
            revenue=None
        else:
            revenue=cpo.iat[rowIndex, column]
        flag = shut2

        date_infor.append(str(cpu['date'][i]))
        posit_infor.append(' short call ')
        i_infor.append(str(i))
        revenue_infor.append(revenue)
        column_infor.append(str(column))
        row_infor.append(str(rowIndex))
        
    #####################offset position##################
    #####到期平仓#####
    elif onexpday(date)==1 and flag==shut1:
        for k, day in enumerate(cpo['date']):
            day = yearMonthDay(day)
            if nowday == day:
                rowIndex = k - 1
        
        if column is None:
            cost=None
        else:
            cost=cpo.iat[rowIndex, column]
        try:
            Return.append(revenue - cost-0.0015)
            day2.append(yearMonthDay(date))
        except:
            Return.append(None)
            day2.append(None)
        j=j+1
        date_infor.append(str(cpu['date'][i]))
        posit_infor.append(' buy put back ')
        i_infor.append(str(i))
        revenue_infor.append(cost)
        column_infor.append(str(column))
        row_infor.append(str(rowIndex))
        
        flag = set
    elif onexpday(date)==1 and flag==shut2:
        for k, day in enumerate(cpo['date']):
            day = yearMonthDay(day)
            if nowday == day:
                rowIndex = k - 1
        
        if column is None:
            cost=None
        else:
            cost=cpo.iat[rowIndex, column]
        try:
            Return.append(revenue - cost-0.0015)
            day2.append(yearMonthDay(date))
        except:
            Return.append(None)
            day2.append(None)
        j = j + 1
        date_infor.append(str(cpu['date'][i]))
        posit_infor.append(' buy call back ')
        i_infor.append(str(i))
        revenue_infor.append(cost)
        column_infor.append(str(column))
        row_infor.append(str(rowIndex))
        
        flag = set
    ####未到期平仓###############################
    
    elif (onexpday(date)==-1) :
        for k, day in enumerate(cpo['date']):
            day = yearMonthDay(day)
            if nowday == day:
                rowIndex = k
        if column is None:
            cost = None
            Return.append(None)
            day2.append(None)
        else:
            cost = cpo.iat[rowIndex, column]  ### 止盈止损
            if (revenue - cost - 0.0015 < -0.04 or revenue - cost - 0.0015 > 0.04) and flag == shut1:
                Return.append(revenue - cost - 0.0015)
                day2.append(yearMonthDay(date))
                j = j + 1
                date_infor.append(str(cpu['date'][i]))
                posit_infor.append(' buy put back ')
                i_infor.append(str(i))
                revenue_infor.append(cost)
                column_infor.append(str(column))
                row_infor.append(str(rowIndex))
                flag = set
            elif (cpu['close'][i] < avg[i-120] and flag == shut1):
                Return.append(revenue - cost - 0.0015)
                day2.append(yearMonthDay(date))
                j = j + 1
                date_infor.append(str(cpu['date'][i]))
                posit_infor.append(' buy put back ')
                i_infor.append(str(i))
                revenue_infor.append(cost)
                column_infor.append(str(column))
                row_infor.append(str(rowIndex))
                flag = set
            elif (revenue - cost - 0.0015 < -0.04 or revenue - cost - 0.0015 > 0.04) and flag == shut2:
                Return.append(revenue - cost - 0.0015)
                day2.append(yearMonthDay(date))
                j = j + 1
                date_infor.append(str(cpu['date'][i]))
                posit_infor.append(' buy call back ')
                i_infor.append(str(i))
                revenue_infor.append(cost)
                column_infor.append(str(column))
                row_infor.append(str(rowIndex))
                flag = set
            elif (cpu['close'][i] > avg[i-120] and flag == shut2):
                Return.append(revenue - cost - 0.0015)
                day2.append(yearMonthDay(date))
                j = j + 1
                date_infor.append(str(cpu['date'][i]))
                posit_infor.append(' buy call back ')
                i_infor.append(str(i))
                revenue_infor.append(cost)
                column_infor.append(str(column))
                row_infor.append(str(rowIndex))
                flag = set
            else:
                continue
        
     
        
from math import isnan     


R=[]
for r in Return:
    if r is  None:
        continue
    elif isnan(r):
        R.append(0)
    elif r is not None:
        R.append(round(r,4))
Return=R

time=[]
for j in day2:
    if j is not None:
        time.append(datetime.strptime(j,'%Y-%m-%d'))
#index 1 annualized return rate
#年化收益率（Annualized Returns)
#(策略最终价值 / 策略初始价值 - 1) / 回测交易日数量 × 250
tradetimes=len(Return)*2
fee=10.0
amount=1000000.0
marginRate=0.12
assuranceFactor=1.2
maxPrice=np.max(cpu['close'])
annualizedFactor=250.0/795.0
sum_return=np.sum(Return)*amount #fee:10/time
#margin=maxPrice*amount*marginRate*assuranceFactor
margin=1000000
# margin rate:12%;assurance factor:1.2
annualRate_1=round(((sum_return/margin))*annualizedFactor,7)
#index 2 annualized sharpe ratio
feeEach=2.0*fee/amount
return_ret_1=[]
for r in Return:
    return_ret_1.append((r*amount)/(margin))
rf=0.04 #annualized riskfree rate
#cum_return_ret_1=cumsum(return_ret_1)
annual_sharpe_Ratio_1=(annualRate_1-rf)/(np.std(return_ret_1,ddof=1)*np.sqrt(len(Return)/2.83))#python算标准差除以n-1
#index 3 annualized volatility
annual_volatility_1=(annualRate_1-rf)/annual_sharpe_Ratio_1

#index 4 maxdrawdown
#maxdrawdown_ret_1<-maxdrawdown(return_ret_1)
cum_Return=[]
sum=0
for k in Return:
    sum=sum+k
    cum_Return.append(sum)

money=[]
for i in cum_Return:
    money.append(amount*i+1000000)
max_drawdown =0
for e, i in enumerate(money):
    for f, j in enumerate(money):
        if f > e and float(j - i)  < max_drawdown:
            max_drawdown = float(j - i)

max_drawdownratio =0
try:
    for e, i in enumerate(money):
        for f, j in enumerate(money):
            if f > e and float(j - i)/i  < max_drawdownratio:
                max_drawdownratio = float(j - i)/i
except:
    max_drawdownratio=None


#index 5 winning rate
win_1=0
for i in return_ret_1:
    if i>0:
        win_1=win_1+1
win_rate_1=win_1/float(len(Return))

#summary
print('Return')
print(Return)
print('win_rate_1','annualRate_1','annual_sharpe_Ratio_1','annual_volatility_1','max_drawdown','max_drawdownratio')
print(win_rate_1, annualRate_1, annual_sharpe_Ratio_1, annual_volatility_1, max_drawdown, max_drawdownratio)
plt.figure(figsize=(10, 5))
plt.plot(time, money)
plt.xlabel('Date')
plt.ylabel('Money')
plt.title('Money Curve')
plt.grid(True) 
plt.savefig("Result.png")
plt.show()





 











