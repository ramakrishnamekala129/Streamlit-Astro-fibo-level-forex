# -*- coding: utf-8 -*-
"""
Created on Tue May 31 07:49:19 2022

@author: ramak
"""

import pandas as pd

class Gann:
    def __init__(self,entry):
        self.entry=entry
    def Gansquare9(self):
        collect=[]
        load=[]
        tol=2
        _entry=self.entry
        fin=_entry+tol
        sqeul=0
        for start in range(1,fin+1):
            #global sqeul
            if start < 2:
                _0=start+start
                _45=start+_0
                _90=_45+start
                _135=_90+start
                _180=_135+start
                _225=_180+start
                _270=_225+start
                _315=_270+start
                sqeul=_315
                k=[start,_0,_45,_90,_135,_180,_225,_270,_315]
                collect.append(k)
                #print(k)
            else:
                _0=start+sqeul
                _45=start+_0
                _90=_45+start
                _135=_90+start
                _180=_135+start
                _225=_180+start
                _270=_225+start
                _315=_270+start
                sqeul=_315
                k=[start,_0,_45,_90,_135,_180,_225,_270,_315]
                collect.append(k)
                #print(k)
        
        df=pd.DataFrame(collect)
        df.columns=['Index','0','45','90','135','180','225','270','315']
        df=df.set_index('Index')
        df['360']=df['0'].shift(-1)
        df=df.dropna()
        
        return df
    def jupiter_kethu(self):
        df=self.Gansquare9()
        df1=df
        df1=df[['0','45','90','135','180','225','270','315']]
        df1.columns=['Buy_0','Notrade_45','Notrade_90','Sell_135','Buy_180','Notrade_225','Notrade_270','Sell_315']
        df1['SL1']=(df1['Sell_135']+df1['Buy_180'])/2
        df1['SL2']=(df1['Sell_315']+df1['Buy_0'].shift(-1))/2
        df1=df1[['Buy_0','Notrade_45','Notrade_90','Sell_135','SL1','Buy_180','Notrade_225','Notrade_270','Sell_315','SL2']]
        print(df1)
        df1.to_csv('jupiter_kethu.csv')
        return df1
    def mercury_mars(self):
        df=self.Gansquare9()
        df1=df
        df1=df[['90','135','180','225','270','315','360','45']]
        df1['_45']=df1['45'].shift(-1)
        del df1['45']
        df1=df1.dropna()
        df1.columns=['Buy_90','Notrade_135','Notrade_180','Sell_225','Buy_270','Notrade_315','Notrade_360','Sell_45']
        df1['SL1']=(df1['Sell_225']+df1['Buy_270'])/2
        df1['SL2']=(df1['Sell_45']+df1['Buy_90'].shift(-1))/2
        df1=df1[['Buy_90','Notrade_135','Notrade_180','Sell_225','SL1','Buy_270','Notrade_315','Notrade_360','Sell_45','SL2']]
        print(df1)
        df1.to_csv('mercury_mars.csv')
        return df1
    def rahu_saturn(self):
        df=self.Gansquare9()
        df1=df
        df1=df[['45','90','135','180','225','270','315','360']]
        df1.columns=['Buy_45','Notrade_90','Notrade_135','Sell_180','Buy_225','Notrade_270','Notrade_315','Sell_360']
        df1['SL1']=(df1['Sell_180']+df1['Buy_225'])/2
        df1['SL2']=(df1['Sell_360']+df1['Buy_45'].shift(-1))/2
        df1=df1[['Buy_45','Notrade_90','Notrade_135','Sell_180','SL1','Buy_225','Notrade_270','Notrade_315','Sell_360','SL2']]
        
        
        print(df1)
        df1.to_csv('rahu_saturn.csv')
        return df1
    def moon_venus(self):
        df=self.Gansquare9()
        df1=df
        df1=df[['315','0','45','90','135','180','225','270']]
        df1['_315']=df1['315'].shift(1)
        del df1['315']
        df1=df1[['_315','0','45','90','135','180','225','270']]
        df1.columns=['Buy_315','Notrade_0','Notrade_45','Sell_90','Buy_135','Notrade_180','Notrade_225','Sell_270']
        df1['SL1']=(df1['Sell_90']+df1['Buy_135'])/2
        df1['SL2']=(df1['Sell_270']+df1['Buy_315'].shift(-1))/2
        df1=df1[['Buy_315','Notrade_0','Notrade_45','Sell_90','SL1','Buy_135','Notrade_180','Notrade_225','Sell_270','SL2']]
        print(df1)
        df1.to_csv('moon_venus.csv')
        return df1



entry=500
d=Gann(entry).moon_venus()

