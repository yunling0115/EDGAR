# Download all NSAR- forms (Investment Advisement Outsourcing)

import os
import ftplib
from ftplib import FTP
import urllib
import urllib2
import csv

path = "F:\EDGAR\Investment Adviser\N-forms\NSAR series mapping\\"
filepath = "F:\EDGAR\Investment Adviser\N-forms\NSAR series mapping\NSAR\\"
filepath_new = "F:\EDGAR\Investment Adviser\N-forms\NSAR series mapping\NSAR-cleaned\\"

c = csv.reader(open(path+"NSAR.csv", "r"))
httplist =[]
filename =[]
formtype =[]
for row in c:
    httplist.append(row[-1])
    filename.append(row[-2])
    formtype.append(row[-3])
# filename: 1000069-96-000012
# httplist: /edgar/data/1000056/9999999997-02-057366.txt
'''
ftp = FTP("ftp.sec.gov")
ftp.login(user="",passwd="yling@usc.edu")
if not os.path.exists(filepath): os.makedirs(filepath)
#for i in range(0,5):
for i in range(0, httplist.__len__()):
    print i
    f = open(filepath+filename[i]+".txt","w")
    cmd = "RETR "+httplist[i].replace("ftp://ftp.sec.gov","")
    ftp.retrbinary(cmd, f.write)
    f.close()
'''

# Extract firm name
name_N = []
cik_N = []
cdate_N = []
fdate_N = []
formtype_N = []
#
series_ID = []
series_NAME = []
contract_ID = []
contract_NAME = []
contract_TICKER = []
'''  
#example: 10866415-10-000790
#i=85,31
#for i in range(0,100):
for i in range(0, httplist.__len__()):
    #print i
    f = open(filepath+filename[i]+".txt","r")
    source = f.read()    
    #
    SEC_begin = source.find("COMPANY CONFORMED NAME:\t")
    SEC_end = source.find("\n", SEC_begin)
    CIK_begin = source.find("CENTRAL INDEX KEY:\t")
    CIK_end = source.find("\n",CIK_begin)
    CDATE_begin = source.find("CONFORMED PERIOD OF REPORT:\t")
    CDATE_end = source.find("\n", CDATE_begin)
    FDATE_begin = source.find("FILED AS OF DATE:\t")
    FDATE_end = source.find("\n", FDATE_begin)
    FTYPE_begin = source.find("CONFORMED SUBMISSION TYPE:\t")
    FTYPE_end = source.find("\n", FTYPE_begin)
    name_N.insert(i,source[SEC_begin+24:SEC_end].strip())
    cik_N.insert(i,source[CIK_begin+21:CIK_end].strip())
    cdate_N.insert(i,source[CDATE_begin+28:CDATE_end].strip())
    fdate_N.insert(i,source[FDATE_begin+18:FDATE_end].strip())
    formtype_N.insert(i,source[FTYPE_begin+26:FTYPE_end].strip())
  
    # Loop start with <SERIES>, end with </SERIES>
    series = source.find("<SERIES>")
    series_E = source.find("</SERIES>", series)
    contract = source.find("<CLASS-CONTRACT>", series, series_E)
    contract_E = source.find("</CLASS-CONTRACT>", contract, series_E)
    #print series
    #print contract
    j = 0 # j is for each contract
    while series>0:
        #print series
        #print series_E
        #contract = source.find("<CLASS-CONTRACT>", series, series_E)
        #contract_E = source.find("</CLASS-CONTRACT>", contract, series_E)
        if contract==-1:
            contract = source.find("<CLASS-CONTRACT>", series, series_E)
            contract_E = source.find("</CLASS-CONTRACT>", contract, series_E)
        while contract>0:
            #print "j: "
            #print j
            #print contract
            #print contract_E
            # <SERIES-ID>, <SERIES-NAME>
            series_id_begin = source.find("<SERIES-ID>", series)
            series_id_end = source.find("\n", series_id_begin)
            series_name_begin = source.find("<SERIES-NAME>", series)
            series_name_end = source.find("\n", series_name_begin)
            series_ID.insert(j,source[series_id_begin+11:series_id_end])
            series_NAME.insert(j,source[series_name_begin+13:series_name_end])
            # Loop start with <CLASS-CONTRACT>, end with </CLASS-CONTRACT>          
            # <CLASS-CONTRACT-ID>, <CLASS-CONTRACT-NAME>, <CLASS-CONTRACT-TICKER-SYMBOL>
            contract_id_begin = source.find("<CLASS-CONTRACT-ID>", contract, series_E)
            contract_id_end = source.find("\n", contract_id_begin, series_E)
            contract_name_begin = source.find("<CLASS-CONTRACT-NAME>", contract, series_E)
            contract_name_end = source.find("\n", contract_name_begin, series_E)
            contract_ticker_begin = source.find("<CLASS-CONTRACT-TICKER-SYMBOL>", contract, series_E)
            contract_ticker_end = source.find("\n", contract_ticker_begin, series_E)                       
            if contract_id_begin==-1:
                contract_ID.insert(j,"")
            else:
                contract_ID.insert(j,source[contract_id_begin+19:contract_id_end])
            if contract_name_begin==-1:
                contract_NAME.insert(j,"")
            else:
                contract_NAME.insert(j,source[contract_name_begin+21:contract_name_end])
            if contract_ticker_begin==-1:
                contract_TICKER.insert(j,"")
            else:
                contract_TICKER.insert(j,source[contract_ticker_begin+30:contract_ticker_end])
            # End Contract 
            contract = source.find("<CLASS-CONTRACT>", contract_E, series_E)
            contract_E = source.find("</CLASS-CONTRACT>", contract, series_E)
            j = j+1
        # End Series    
        series = source.find("<SERIES>", series_E)
        series_E = source.find("</SERIES>", series)
    #
    g = open(filepath+filename[i]+".csv","w")
    g.write("series_ID, series_NAME, contract_ID, contract_NAME, contract_TICKER, \n")
    for k in range(0,j):
        g.write(series_ID[k]+",")
        g.write(series_NAME[k].replace(",","'")+",")
        g.write(contract_ID[k]+",")
        g.write(contract_NAME[k].replace(",","'")+",")
        g.write(contract_TICKER[k]+"\n")
    g.close()
   

    f.close()

# summary of NSAR-1
g = open(path+"NSAR-1.csv","w")
g.write("CIK, Name, Conformed Date, Filing Date, Form Type, \n")
#for i in range(0,5):
for i in range(0, httplist.__len__()):
    g.write(cik_N[i]+",")
    g.write(name_N[i].replace(",","'")+",")
    g.write(cdate_N[i]+",")
    g.write(fdate_N[i]+",")
    g.write(formtype_N[i]+"\n")
g.close()

# Combine tickers
LINES = []
for i in range(0,httplist.__len__()):
    print i
    f = open(filepath+filename[i]+".csv","r")
    source = f.readlines()
    print source.__len__()
    if source.__len__()>1:
        for k in range(1,source.__len__()):
            #source[k]=cik_N[i]+","+fdate_N[i]+","+source[k]
            LINES.append(cik_N[i]+","+fdate_N[i]+","+source[k])
g = open(path+"Map-Contract.csv","w")
g.write("CIK, Filing Date, series_ID, series_NAME, contract_ID, contract_NAME, contract_TICKER,\n")
g.writelines(LINES)
g.close()

# Delete csv files
for i in range(0,httplist.__len__()):
    if os.path.isfile(filepath+filename[i]+".csv")==True:
        os.remove(filepath+filename[i]+".csv")
'''

'''
# Extract information - (text - /text)
# 42101, 112146, 112380, 112641, 113158, 116716 (exception - need to look into details)
# 91690 (exception - contain both parts)
for i in range(116716, 116717):
#for i in range(113157, 112641, -1):
    print i
    if formtype[i] not in ["NT-NSAR", "NSAR-U", "NSAR-U/A"]:
        f = open(filepath+filename[i]+".txt","r")
        source = f.read()
        f.close()
        b = source.find("<TEXT>")
        b = source.find("\n",b)
        e = source.find("</TEXT>")   
        p = source.find("<PAGE>",b,e)
        j = source.find("\n",p,e)
        source = source[b+1:p]+source[j+1:e]
        while p>0:
            p = source.find("<PAGE>")
            j = source.find("\n",p)
            source = source[0:p]+source[j+1:source.__len__()]
        p = source.find("SIGNATURE")
        source = source[0:p]
        g = open(filepath_new+filename[i]+".txt","w")
        g.write(source)
        g.close()
'''
# exception: 38341
for i in range(8811, httplist.__len__()):
    if formtype[i] not in ["NT-NSAR", "NSAR-U", "NSAR-U/A"]:
        #only extract lines starting with "0":
        print i
        f = open(filepath+filename[i]+".txt","r")
        source = f.readlines()
        f.close()
        source_new = []
        for j in range(0,source.__len__()):
            string = source[j]
            if string[0]=="0":
                source_new.append(source[j])
        g = open(filepath_new+filename[i]+".txt","w")
        g.writelines(source_new)
        g.close()
        

    
