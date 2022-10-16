# -*- coding: utf-8 -*-
"""
Created on Tue May 31 11:13:46 2022

@author: ramak
"""

import yfinance as yf
import streamlit as st
import math
import pandas as pd
from datetime import datetime, timedelta,date
import investpy
import numpy as np
from streamlit_autorefresh import st_autorefresh
from investiny import historical_data, search_assets

m=st.sidebar.text_input('Option Range',value=5)

import requests

headers = {

    'authority': 'api.stocksrin.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'origin': 'https://www.stocksrin.com',
    'referer': 'https://www.stocksrin.com/',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="104", "Opera GX";v="90"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.100',
}

params = (
    ('symbol', 'BankNifty'),
    ('expiry', '2022-10-20'),
    ('lastTimeStamp', ''),
    ('forcedDataLoad', 'true'),
)

response = requests.get('https://api.stocksrin.com/srOptionChain/chain', headers=headers, params=params)

import requests

headers = {
    'authority': 'api.stocksrin.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'origin': 'https://www.stocksrin.com',
    'referer': 'https://www.stocksrin.com/',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="104", "Opera GX";v="90"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.100',
}

params = (
    ('symbol', 'BankNifty'),
)

r = requests.get('https://api.stocksrin.com/srOptionChain/expiry', headers=headers, params=params)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://api.stocksrin.com/srOptionChain/expiry?symbol=BankNifty', headers=headers)



r=r.json()



def chaindata(expiry):
	import requests

	headers = {
	    'authority': 'api.stocksrin.com',
	    'accept': 'application/json, text/plain, */*',
	    'accept-language': 'en-US,en;q=0.9',
	    'origin': 'https://www.stocksrin.com',
	    'referer': 'https://www.stocksrin.com/',
	    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="104", "Opera GX";v="90"',
	    'sec-ch-ua-mobile': '?0',
	    'sec-ch-ua-platform': '"Windows"',
	    'sec-fetch-dest': 'empty',
	    'sec-fetch-mode': 'cors',
	    'sec-fetch-site': 'same-site',
	    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.100',
	}

	params = (
	    ('symbol', 'BankNifty'),
	    ('expiry', expiry),
	    #('lastTimeStamp', '07-Oct-22 15:31:39'),
	    ('forcedDataLoad', 'true'),
	)

	response = requests.get('https://api.stocksrin.com/srOptionChain/chain', headers=headers, params=params)

	#NB. Original query string below. It seems impossible to parse and
	#reproduce query strings 100% accurately so the one below is given
	#in case the reproduced version is not "correct".
	# response = requests.get('https://api.stocksrin.com/srOptionChain/chain?symbol=BankNifty&expiry=2022-10-27&lastTimeStamp=07-Oct-22%2015:31:39&forcedDataLoad=true', headers=headers)
	k=response
	return k
st_autorefresh(interval=1000, key="dataframerefresh")
k=response.json()
indexltp=k['srIndexQuote']['openValue']
mod=int(indexltp)%50
if mod <25:
    atmstrike = int(math.floor(indexltp/100))*100
else:
    atmstrike = int(math.ceil(indexltp/100))*100
#print(math.floor(k['srIndexQuote']['openValue']))
print(atmstrike)
strikelvl=[]
nextlvl={}
for i in range(0,int(m)):
    strikelvl.append(atmstrike + (i*100))
    strikelvl.append(atmstrike - (i*100))


for i in k['strikeDataModel']['strikes']:
    print()
    if i['strikePrice'] in strikelvl:
        nextlvl[str(i['strikePrice'])]={'CE':0,
        'PE':0,
        'CE_change':0,'PE_change':0}


for expiry in r:

	k=chaindata(expiry)
	print(expiry)
	if k.status_code==200:
		print(k)
		k=k.json()
		for i in k['strikeDataModel']['strikes']:
			#print()
			if i['strikePrice'] in strikelvl:
				print(nextlvl[str(i['strikePrice'])])
				if i['CE']==None:
					i['CE']={'oi':0
					,'oic':0
					}


				if (i['PE'])==None:
					i['PE']={'oi':0
					,'oic':0
					}
				nextlvl[str(i['strikePrice'])]={'CE': (nextlvl[str(i['strikePrice'])]['CE']+i['CE']['oi']),
				'PE':(nextlvl[str(i['strikePrice'])]['PE']+i['PE']['oi']),
				'CE_change':(nextlvl[str(i['strikePrice'])]['CE_change']+i['CE']['oic']),'PE_change':(nextlvl[str(i['strikePrice'])]['PE_change']+i['PE']['oic'])}





st.sidebar.title("Fibo Level Maker")
#st.markdown("This application is a Share Price dashboard for Top 5 Gainers and Losers:")
st.sidebar.markdown("This application is a which gives Fibo entry levels")
def CurrencyDivider(select):
    if 'JPY' in select:
       return 1000
    elif 'XAU/USD' in select:
    	return 100
    elif 'USD' in select:
        return 100000
    elif 'INR' in select:
        return 10000
    else:
    	return 1

select=1
#st.sidebar.title("Pairs")
#select = st.sidebar.selectbox('Select a Pair', pairs, key='1')
#currency = st.sidebar.checkbox('Currency')
#st.json(response.json())


print(pd.DataFrame(nextlvl).T)
st.bar_chart(pd.DataFrame(nextlvl).T)


import plotly.express as px 


fig=px.bar(pd.DataFrame(nextlvl).T, orientation='h' ,text_auto=True,barmode='group')


st.write(fig)


currentfibo = st.sidebar.checkbox('Todays')
currentfiboweek = st.sidebar.checkbox('Weeks')
varcurrentfiboweek = st.sidebar.checkbox('Custom Weeks')
varcurrentfibomonth = st.sidebar.checkbox('Custom Months')

gann = st.sidebar.checkbox('Astro Levels')
fullgann = st.sidebar.checkbox('Complete Astro Levels')


h=st.text_input('Type Instrument',value='nsebank')
search_results = search_assets(query=h, limit=100)
if not pd.DataFrame(search_results).empty:
	st.dataframe(pd.DataFrame(search_results))

k=st.sidebar.text_input('Instrument Token',value='18217')
mu=st.sidebar.text_input('Multipier',value=1)
if not mu==(1) :
	if not mu =="":
		select=int(mu)
	else:
		select=1


d = st.date_input("Todays Date",date.today())
d=d+timedelta(days=1)
todate=d-timedelta(days=25)
todate=todate.strftime('%m/%d/%Y')
d=d.strftime('%m/%d/%Y')
data = historical_data(investing_id=int(k), from_date=str(todate), to_date=str(d))
print(data)
t=pd.DataFrame(data)
t['date']=pd.to_datetime(t['date'])
#t=t.set_index(['date'])
t['Date']=t['date']
t['Open']=t['open']
t['Low']=t['low']
t['High']=t['high']
t['Close']=t['close']
#print(t)


if not t.empty:
	j=t
	Divide=(select)
	if currentfibo:
		takeinput = st.number_input(label="Input Today Open Price",step=1.,format="%.2f")
		#if not currency:Divide=1
		
		t=pd.DataFrame(t)
		test1=t
		#print(test1)
		t=t['Open']
		todayprice=int((list(t)[-1])*Divide)
		if takeinput >0:
			todayprice=int(takeinput*Divide)
		t=test1['Close']
		t=t[-11:-1].values
		print("Today price back date")
		test1=test1.iloc[-12:-2,:]
		print(len(test1))
		t=t*Divide
		t=pd.to_numeric(t, downcast='integer')
		k=[]
		for i in t:
		    k.append(int(i))
		t=k
		

		avglst=[]
		for i in range(1,len(t)):
		    avglst.append(np.log(t[i]/t[i-1]))
		lnsq=[]
		for i in avglst:
		    lnsq.append(i**2)

		avg=np.mean(avglst)
		ln=np.mean(lnsq)
		variance=ln-(avg**2)
		volatility=math.sqrt(variance)
		pricerange=t[-1]*volatility

		D0236B=todayprice+(0.236*pricerange)
		D0236S=todayprice-(0.236*pricerange)
		D0382B=(0.382*pricerange)+todayprice
		D0382S=todayprice-(0.382*pricerange)
		D05B=todayprice+(0.5*pricerange)
		D05S=todayprice-(0.5*pricerange)
		D0618B=todayprice+(0.618*pricerange)
		D0618S=todayprice-(0.618*pricerange)
		D0786B=todayprice+(0.786*pricerange)
		D0786S=todayprice-(0.786*pricerange)
		D0888B=todayprice+(0.888*pricerange)
		D0888S=todayprice-(0.888*pricerange)
		D01B=todayprice+(1*pricerange)
		D01S=todayprice-(1*pricerange)
		D1236B=todayprice+(1.236*pricerange)
		D1236S=todayprice-(1.236*pricerange)
		D1272B=todayprice+(1.272*pricerange)
		D1272S=todayprice-(1.272*pricerange)
		D1618B=todayprice+(1.618*pricerange)
		D1618S=todayprice-(1.618*pricerange)
		l1=[int(D0236B)/Divide,int(D0236S)/Divide]
		l2=[int(D0382B)/Divide,int(D0382S)/Divide]
		l3=[int(D05B)/Divide,int(D05S)/Divide]
		l4=[int(D0618B)/Divide,int(D0618S)/Divide]
		l5=[int(D0786B)/Divide,int(D0786S)/Divide]
		l6=[int(D0888B)/Divide,int(D0888S)/Divide]
		l7=[int(D01B)/Divide,int(D01S)/Divide]
		l8=[int(D1236B)/Divide,int(D1236S)/Divide]
		l9=[int(D1272B)/Divide,int(D1272S)/Divide]
		l10=[int(D1618B)/Divide,int(D1618S)/Divide]
		ls=[l1,l2,l3,l4,l5,l6,l7,l8,l9,l10]
		df=pd.DataFrame(ls,columns=['Buy','Sell'],index=['0.236','0.382','0.5','0.618','0.786','0.888','1','1.236','1.272','1.618'])
		st.dataframe(df)
		st.text('Open Price for Calculation is '+str(float(todayprice/Divide)))
	if currentfiboweek:
		st.text('Week Fibo Level')
		st.text('Table')
		tw=j
		test1=tw
		tw=tw.reset_index()
		tw['Date']=pd.to_datetime(tw['Date'])
		print("Week price back date")
		test1=test1.iloc[-11:-1,:]
		print(test1)
		backdate=tw['Date'].dt.weekday
		backdate=list(backdate)[-1]
		if backdate!=0:
		    tw=tw.iloc[:-backdate,:]
		    #print(t)
		ktw=list(tw['Close']*Divide)
		tw=list(tw['Open'])
		todaypricew=int(tw[-1]*Divide)
		#t=test1['Close']
		tw=ktw
		tw=tw[-12:-2]#.values
		print(tw)
		
		kw=[]
		for i in tw:
		    kw.append(int(i))
		tw=kw
			

		avglstw=[]
		for i in range(1,len(tw)):
			if (tw[i-1] or tw[i-1])==0:
				avglstw.append(0)
			else:
				k12=np.log(tw[i]/tw[i-1])
				avglstw.append(k12)
		lnsqw=[]
		for i in avglstw:
		    lnsqw.append(i**2)

		avgw=np.mean(avglstw)
		lnw=np.mean(lnsqw)
		variancew=lnw-(avgw**2)
		volatilityw=math.sqrt(variancew)
		print('volatility'+str(volatilityw))
		yvolatilityw=volatilityw*100*(math.sqrt(365))
		print('yearvolatility'+str(yvolatilityw))
		pricerangew=todaypricew*volatilityw
		print('pricerange'+str(pricerangew))
		print('todayprice'+str(todaypricew))
		pricerangew=((todaypricew*yvolatilityw)/100*(math.sqrt(8)))/math.sqrt(365)
		print('pricerange'+str(pricerangew))
		D0236Bw=todaypricew+(0.236*pricerangew)
		D0236Sw=todaypricew-(0.236*pricerangew)
		D0382Bw=(0.382*pricerangew)+todaypricew
		D0382Sw=todaypricew-(0.382*pricerangew)
		D05Bw=todaypricew+(0.5*pricerangew)
		D05Sw=todaypricew-(0.5*pricerangew)
		D0618Bw=todaypricew+(0.618*pricerangew)
		D0618Sw=todaypricew-(0.618*pricerangew)
		D0786Bw=todaypricew+(0.786*pricerangew)
		D0786Sw=todaypricew-(0.786*pricerangew)
		D0888Bw=todaypricew+(0.888*pricerangew)
		D0888Sw=todaypricew-(0.888*pricerangew)
		D01Bw=todaypricew+(1*pricerangew)
		D01Sw=todaypricew-(1*pricerangew)
		D1236Bw=todaypricew+(1.236*pricerangew)
		D1236Sw=todaypricew-(1.236*pricerangew)
		D1272Bw=todaypricew+(1.272*pricerangew)
		D1272Sw=todaypricew-(1.272*pricerangew)
		D1618Bw=todaypricew+(1.618*pricerangew)
		D1618Sw=todaypricew-(1.618*pricerangew)
		l1w=[int(D0236Bw)/Divide,int(D0236Sw)/Divide]
		l2w=[int(D0382Bw)/Divide,int(D0382Sw)/Divide]
		l3w=[int(D05Bw)/Divide,int(D05Sw)/Divide]
		l4w=[int(D0618Bw)/Divide,int(D0618Sw)/Divide]
		l5w=[int(D0786Bw)/Divide,int(D0786Sw)/Divide]
		l6w=[int(D0888Bw)/Divide,int(D0888Sw)/Divide]
		l7w=[int(D01Bw)/Divide,int(D01Sw)/Divide]
		l8w=[int(D1236Bw)/Divide,int(D1236Sw)/Divide]
		l9w=[int(D1272Bw)/Divide,int(D1272Sw)/Divide]
		l10w=[int(D1618Bw)/Divide,int(D1618Sw)/Divide]
		lsw=[l1w,l2w,l3w,l4w,l5w,l6w,l7w,l8w,l9w,l10w]
		dfw=pd.DataFrame(lsw,columns=['Buy','Sell'],index=['0.236','0.382','0.5','0.618','0.786','0.888','1','1.236','1.272','1.618'])
		print(dfw)
		st.dataframe(dfw)
		st.text('Week Open Price for Calculation is '+str(float(todaypricew/Divide)))

	if varcurrentfiboweek:
		takeinput = st.number_input(label="Input Custom Week Open Price",step=1.,format="%.2f")
		st.text(' Custom Week Fibo Level')
		st.text('Table')

		tw=j#pd.DataFrame(j)
		test1=tw
		tw=tw.reset_index()
		tw['Date']=pd.to_datetime(tw['Date'])
		print("Custom Week price back date")
		test1=test1.iloc[-12:-2,:]
		#print(test1)
		#print(t)
		ktw1=list(tw['Close']*Divide)
		tw=list(tw['Open'])
		todaypricew=int(tw[-1]*Divide)
		tw=ktw1
		tw=tw[-11:-1]#.values
		if takeinput > 1:
			todaypricew=takeinput
		#tw=tw*Divide
		#t=pd.to_numeric(t, downcast='integer')
		#print(tw)
		kw=[]
		for i in tw:
		    kw.append(int(i))
		tw=kw
		

		avglstw=[]
		for i in range(1,len(tw)):
			if (tw[i-1] or tw[i-1])==0:
				avglstw.append(0)
			else:
				k12=np.log(tw[i]/tw[i-1])
				avglstw.append(k12)
		lnsqw=[]
		for i in avglstw:
		    lnsqw.append(i**2)

		avgw=np.mean(avglstw)
		lnw=np.mean(lnsqw)
		variancew=lnw-(avgw**2)
		volatilityw=math.sqrt(variancew)
		print('volatility'+str(volatilityw))
		yvolatilityw=volatilityw*100*(math.sqrt(365))
		print('yearvolatility'+str(yvolatilityw))
		pricerangew=todaypricew*volatilityw
		print('pricerange'+str(pricerangew))
		print('todayprice'+str(todaypricew))
		pricerangew=((todaypricew*yvolatilityw)/100*(math.sqrt(8)))/math.sqrt(365)
		print('pricerange'+str(pricerangew))
		D0236Bw=todaypricew+(0.236*pricerangew)
		D0236Sw=todaypricew-(0.236*pricerangew)
		D0382Bw=(0.382*pricerangew)+todaypricew
		D0382Sw=todaypricew-(0.382*pricerangew)
		D05Bw=todaypricew+(0.5*pricerangew)
		D05Sw=todaypricew-(0.5*pricerangew)
		D0618Bw=todaypricew+(0.618*pricerangew)
		D0618Sw=todaypricew-(0.618*pricerangew)
		D0786Bw=todaypricew+(0.786*pricerangew)
		D0786Sw=todaypricew-(0.786*pricerangew)
		D0888Bw=todaypricew+(0.888*pricerangew)
		D0888Sw=todaypricew-(0.888*pricerangew)
		D01Bw=todaypricew+(1*pricerangew)
		D01Sw=todaypricew-(1*pricerangew)
		D1236Bw=todaypricew+(1.236*pricerangew)
		D1236Sw=todaypricew-(1.236*pricerangew)
		D1272Bw=todaypricew+(1.272*pricerangew)
		D1272Sw=todaypricew-(1.272*pricerangew)
		D1618Bw=todaypricew+(1.618*pricerangew)
		D1618Sw=todaypricew-(1.618*pricerangew)
		l1w=[int(D0236Bw)/Divide,int(D0236Sw)/Divide]
		l2w=[int(D0382Bw)/Divide,int(D0382Sw)/Divide]
		l3w=[int(D05Bw)/Divide,int(D05Sw)/Divide]
		l4w=[int(D0618Bw)/Divide,int(D0618Sw)/Divide]
		l5w=[int(D0786Bw)/Divide,int(D0786Sw)/Divide]
		l6w=[int(D0888Bw)/Divide,int(D0888Sw)/Divide]
		l7w=[int(D01Bw)/Divide,int(D01Sw)/Divide]
		l8w=[int(D1236Bw)/Divide,int(D1236Sw)/Divide]
		l9w=[int(D1272Bw)/Divide,int(D1272Sw)/Divide]
		l10w=[int(D1618Bw)/Divide,int(D1618Sw)/Divide]
		lsw=[l1w,l2w,l3w,l4w,l5w,l6w,l7w,l8w,l9w,l10w]
		dfw=pd.DataFrame(lsw,columns=['Buy','Sell'],index=['0.236','0.382','0.5','0.618','0.786','0.888','1','1.236','1.272','1.618'])
		print(dfw)
		st.dataframe(dfw)
		st.text('Custom Week Open Price for Calculation is '+str(float(todaypricew/Divide)))

	if varcurrentfibomonth:
	    takeinput = st.number_input(label="Input Custom Month Open Price",step=1.,format="%.2f")
	    takeinput1 = st.number_input(label="Input Custom Month Range Day")
	    st.text('Custom Month Fibo Level')
	    st.text('Table')

	    tw=j#pd.DataFrame(j)
	    test1=tw
	    tw=tw.reset_index()
	    tw['Date']=pd.to_datetime(tw['Date'])
	    print("Custom Month price back date")
	    test1=test1.iloc[-11:-1,:]
	    print(test1)
	    #print(t)
	    ktw1=list(tw['Close']*Divide)
	    tw=list(tw['Open'])
	    todaypricew=int(tw[-1]*Divide)
	    tw=ktw1
	    tw=tw[-11:-1]#.values
	    if takeinput > 1:
	        todaypricew=takeinput
	    #tw=tw*Divide
	    #t=pd.to_numeric(t, downcast='integer')
	    kw=[]
	    for i in tw:
	        kw.append(int(i))
	    tw=kw


	    avglstw=[]
	    for i in range(1,len(tw)):
	        avglstw.append(np.log(tw[i]/tw[i-1]))
	    lnsqw=[]
	    for i in avglstw:
	        lnsqw.append(i**2)

	    avgw=np.mean(avglstw)
	    lnw=np.mean(lnsqw)
	    variancew=lnw-(avgw**2)
	    volatilityw=math.sqrt(variancew)
	    print('volatility'+str(volatilityw))
	    yvolatilityw=volatilityw*100*(math.sqrt(365))
	    print('yearvolatility'+str(yvolatilityw))
	    pricerangew=todaypricew*volatilityw
	    print('pricerange'+str(pricerangew))
	    print('todayprice'+str(todaypricew))
	    pricerangew=((todaypricew*yvolatilityw)/100*(math.sqrt(30)))/math.sqrt(365)
	    if takeinput1 > 1:
	        pricerangew=((todaypricew*yvolatilityw)/100*(math.sqrt(int(takeinput1))))/math.sqrt(365)
	    print('pricerange'+str(pricerangew))
	    D0236Bw=todaypricew+(0.236*pricerangew)
	    D0236Sw=todaypricew-(0.236*pricerangew)
	    D0382Bw=(0.382*pricerangew)+todaypricew
	    D0382Sw=todaypricew-(0.382*pricerangew)
	    D05Bw=todaypricew+(0.5*pricerangew)
	    D05Sw=todaypricew-(0.5*pricerangew)
	    D0618Bw=todaypricew+(0.618*pricerangew)
	    D0618Sw=todaypricew-(0.618*pricerangew)
	    D0786Bw=todaypricew+(0.786*pricerangew)
	    D0786Sw=todaypricew-(0.786*pricerangew)
	    D0888Bw=todaypricew+(0.888*pricerangew)
	    D0888Sw=todaypricew-(0.888*pricerangew)
	    D01Bw=todaypricew+(1*pricerangew)
	    D01Sw=todaypricew-(1*pricerangew)
	    D1236Bw=todaypricew+(1.236*pricerangew)
	    D1236Sw=todaypricew-(1.236*pricerangew)
	    D1272Bw=todaypricew+(1.272*pricerangew)
	    D1272Sw=todaypricew-(1.272*pricerangew)
	    D1618Bw=todaypricew+(1.618*pricerangew)
	    D1618Sw=todaypricew-(1.618*pricerangew)
	    l1w=[int(D0236Bw)/Divide,int(D0236Sw)/Divide]
	    l2w=[int(D0382Bw)/Divide,int(D0382Sw)/Divide]
	    l3w=[int(D05Bw)/Divide,int(D05Sw)/Divide]
	    l4w=[int(D0618Bw)/Divide,int(D0618Sw)/Divide]
	    l5w=[int(D0786Bw)/Divide,int(D0786Sw)/Divide]
	    l6w=[int(D0888Bw)/Divide,int(D0888Sw)/Divide]
	    l7w=[int(D01Bw)/Divide,int(D01Sw)/Divide]
	    l8w=[int(D1236Bw)/Divide,int(D1236Sw)/Divide]
	    l9w=[int(D1272Bw)/Divide,int(D1272Sw)/Divide]
	    l10w=[int(D1618Bw)/Divide,int(D1618Sw)/Divide]
	    lsw=[l1w,l2w,l3w,l4w,l5w,l6w,l7w,l8w,l9w,l10w]
	    lsw=[l1w,l2w,l3w,l4w,l5w,l6w,l7w,l8w,l9w,l10w]
	    dfw=pd.DataFrame(lsw,columns=['Buy','Sell'],index=['0.236','0.382','0.5','0.618','0.786','0.888','1','1.236','1.272','1.618'])
	    print(dfw)
	    st.dataframe(dfw)
	    st.text('Custom Months Open Price for Calculation is '+str(float(todaypricew/Divide)))

	if gann:
		t=j
		todayprice_12=list(t['Open'])[-1]
		print('astro today price {}'.format(todayprice_12))
		takeinput = st.number_input(label="Input Price For Astro",step=1.,format="%.6f")
		takeinput=takeinput*Divide
		selectbox=st.selectbox('Select Planet Aspects',('Jupiter/Kethu','Mercury/Mars','Rahu/Saturn','Moon/Venus'))
		if selectbox == 'Jupiter/Kethu':
			df=pd.read_csv('jupiter_kethu.csv')
			df=df.dropna()
			df=df.astype(int)
		elif selectbox == 'Mercury/Mars':
			df=pd.read_csv('mercury_mars.csv')
			df=df.dropna()
			df=df.astype(int)
		elif selectbox == 'Rahu/Saturn':
			df=pd.read_csv('rahu_saturn.csv')
			df=df.dropna()
			df=df.astype(int)
		elif selectbox == 'Moon/Venus':
			df=pd.read_csv('moon_venus.csv')
			df=df.dropna()
			df=df.astype(int)
		df=df.iloc[:,1:]
		df1=df
		takeinput1=takeinput
		if takeinput ==0:
			takeinput1=todayprice_12*Divide
		if takeinput1 !=0:
			if selectbox == 'Jupiter/Kethu':
			    #df=pd.read_csv('jupiter_kethu.csv')
			    df_sort = df.iloc[(df['Sell_315']-takeinput1).abs().argsort()[:5]]
			    df1=df_sort.sort_index(axis=0, level=None, ascending=True, inplace=False, kind='quicksort', na_position='last', sort_remaining=True)
			    df1=df1.reset_index()
			    df1=df1.iloc[:,1:]
			elif selectbox == 'Mercury/Mars':
			    #df=pd.read_csv('mercury_mars.csv')
			    df_sort = df.iloc[(df['Buy_90']-takeinput1).abs().argsort()[:5]]
			    df1=df_sort.sort_index(axis=0, level=None, ascending=True, inplace=False, kind='quicksort', na_position='last', sort_remaining=True)
			    df1=df1.reset_index()
			    df1=df1.iloc[:,1:]
			elif selectbox == 'Rahu/Saturn':
			    #df=pd.read_csv('rahu_saturn.csv')
			    df_sort = df.iloc[(df['Buy_45']-takeinput1).abs().argsort()[:5]]
			    df1=df_sort.sort_index(axis=0, level=None, ascending=True, inplace=False, kind='quicksort', na_position='last', sort_remaining=True)
			    df1=df1.reset_index()
			    df1=df1.iloc[:,1:]
			elif selectbox == 'Moon/Venus':
			    #df=pd.read_csv('moon_venus.csv')
			    df_sort = df.iloc[(df['Buy_315']-takeinput1).abs().argsort()[:5]]
			    df1=df_sort.sort_index(axis=0, level=None, ascending=True, inplace=False, kind='quicksort', na_position='last', sort_remaining=True)
			    df1=df1.reset_index()
			    df1=df1.iloc[:,1:]
		df1=df1.div(Divide)
		if Divide ==1:
			st.dataframe(df1.style.format("{:.2f}"))
		elif Divide ==100:
			st.dataframe(df1.style.format("{:.2f}"))
		elif Divide ==1000:
			st.dataframe(df1.style.format("{:.3f}"))
		elif Divide ==100000:
			st.dataframe(df1.style.format("{:.5f}"))

	if fullgann:
	    selectbox=st.selectbox('Select Planet Aspects Full Sheet',('Jupiter/Kethu','Mercury/Mars','Rahu/Saturn','Moon/Venus'))
	    if selectbox == 'Jupiter/Kethu':
	        df=pd.read_csv('jupiter_kethu.csv')
	        df=df.dropna()
	        df=df.astype(int)
	    elif selectbox == 'Mercury/Mars':
	        
	        df=pd.read_csv('mercury_mars.csv')
	        df=df.dropna()
	        df=df.astype(int)
	    elif selectbox == 'Rahu/Saturn':
	        df=pd.read_csv('rahu_saturn.csv')
	        df=df.dropna()
	        df=df.astype(int)
	    elif selectbox == 'Moon/Venus':
	        df=pd.read_csv('moon_venus.csv')
	        df=df.dropna()
	        df=df.astype(int)
	    df=df.iloc[:,1:]
	    df1=df
	    
	    st.dataframe(df1)
		
