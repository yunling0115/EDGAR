#-------------------------------------------------------------------------------
#  To extract forecast earnings information: use desktop to run
#-------------------------------------------------------------------------------
# 1. First to download all txt files

# stdlib module for reading page source
import ftplib
from ftplib import FTP
import urllib
import urllib2
import csv
import os.path 

f = open("E:\EDGAR\s4\\ftp.csv","r")
# note: \f = x0
flist = f.readlines()
f.close()
length = flist.__len__()

# 9pm - 6am (EST)
for i in range(0,length):
    print i
    name = flist[i].strip("\"" "\n" "ftp://ftp.sec.gov/edgar/data/" ".txt")
    fname = name.replace("/","-")
    cmd = "RETR /edgar/data/"+name+".txt"
    address = flist[i].strip("\"" "\n" "ftp://ftp.sec.gov" ".txt")
    file = open("G:\EDGAR\s4\\raw s4\\"+fname+".txt", "wb")
    ftp.retrbinary(cmd, file.write)
    file.close()
	
#-------------------------------------------------------------------------------

# 2. Next to extract tables
f = open("G:\EDGAR\s4\\ftp.csv","r")
flist = f.readlines()
f.close()
length = flist.__len__()

# Print the list of files not exist
flist2 = []
g = open("G:\EDGAR\s4\\File Not Exist.csv","w")
for i in range(0,length):
    fname = flist[i].strip("\"" "\n" "ftp://ftp.sec.gov/edgar/data/" ".txt").replace("/","-")
    if os.path.exists("G:\EDGAR\s4\\raw s4\\"+fname+".txt")=="False":
        g.write(fname)
    else:
        flist2.insert(i,fname)
g.close()
       
# b) all tables (case insensitive)
table_ix1 = source.lower().find("TABLE OF CONTENTS".lower())
table_beg = source.lower().find("<TABLE>".lower(), table_ix1)
table_end = source.lower().find("</TABLE>".lower(), table_beg)
while table_beg>0:
    table_beg = source.lower().find("<TABLE>".lower(), table_end)
    table_end = source.lower().find("</TABLE>".lower(), table_beg)
    g.write(source[table_beg:table_end])

g.close()
f.close()

for i in range(0,length):
    print i
    fname = flist2[i].strip("\"" "\n" "ftp://ftp.sec.gov/edgar/data/" ".txt").replace("/","-")
    f = open("G:\EDGAR\s4\\raw s4\\"+fname+".txt","r")
    source = f.read()
    # a) filedate
    date_ix1 = source.find("FILED AS OF DATE:")
    date_beg = date_ix1+19
    date_end = date_beg+8
    fdate = source[date_beg:date_end]
    g = open("G:\EDGAR\s4\\s4 tables\\"+fname+".txt","w")
    g.write(fdate+"\n")
    # b) all tables (case insensitive)
    table_ix1 = source.lower().find("TABLE OF CONTENTS".lower())
    table_beg = source.lower().find("<TABLE>".lower(), table_ix1)
    table_end = source.lower().find("</TABLE>".lower(), table_beg)
    while table_beg>0:
        table_beg = source.lower().find("<TABLE>".lower(), table_end)
        table_end = source.lower().find("</TABLE>".lower(), table_beg)
        g.write(source[table_beg:table_end])

    g.close()
    f.close()

#-------------------------------------------------------------------------------

# 3. Last to extract disclosure measure

f = open("G:\EDGAR\s4\\ftp.csv","r")
flist = f.readlines()
f.close()
length = flist.__len__()

#-------------------------------------------------------------------------------

# a). size of the file serves as the first level of disclosure

fsize = []
g = open("G:\EDGAR\\Disc\\Disc1.csv", "w")
g.write("Filename, Size, \n")
for i in range(0,length):
    fname = flist[i].strip("\"" "\n" "ftp://ftp.sec.gov/edgar/data/" ".txt").replace("/","-")
    size = os.path.getsize("G:\EDGAR\s4\\s4 tables\\"+fname+".txt")
    g.write(fname.strip()+",")
    g.write(size.bit_length().__str__()+"\n")
g.close()

#-------------------------------------------------------------------------------

# b). If " futureyear " contained in any table, there's more disclosure

g = open("G:\EDGAR\\Disc\\Disc2.csv", "w")
g.write("Filename,Fileyear, Year +1,Year +2,Year +3,Year +4,Year +5,Year +6,Year +7,Year +8,Year +9,Year +10,Year +11,Year +12,Year +13,Year +14,Year +15, \n")
for i in range(0,length):
    # print i
    fname = flist[i].strip("\"" "\n" "ftp://ftp.sec.gov/edgar/data/" ".txt").replace("/","-")
    h = fname.find("-")
    h1 = fname.find("-",h+1)
    h2 = fname.find("-",h1+1)
    fyear = int(fname[h1+1:h2])
    if fyear>50:
        fyear = fyear+1900
    else:
        fyear = fyear+2000
    # print fyear
    f = open("G:\EDGAR\s4\\s4 tables\\"+fname+".txt","r")
    tables = f.read()
    f.close()
    g.write(fname+","+fyear.__str__()+",")
    for j in range(1,16): # looking forward 15 years, estimate for thereafter not counted
        year_txt1 = " "+(fyear+j).__str__()+" " # adding blanks to make sure it's a year (year serves as column name)
        year_txt2 = (fyear+j).__str__()+"..." # most form: 2000.......... (year serves as row name)
        find1 = tables.find(year_txt1)
        find2 = tables.find(year_txt2)
        find = max(find1,find2)
        if find<0:
            true = 0
        else:
            true = 1
        g.write(true.__str__()+",")
    g.write("\n")
g.close()
    

#-------------------------------------------------------------------------------
"""
# c). If " futureyear " and "earning" simultaneously contained in any table, there's more disclosure

g = open("G:\EDGAR\\Disc\\Disc2.csv", "w")
g.write("Filename,Year +1,Year +2,Year +3,Year +4,Year +5,Year +6,Year +7,Year +8,Year +9,Year +10,Year +11,Year +12,Year +13,Year +14,Year +15, \n")
for i in range(0,length):
    print i
    fname = flist[i].strip("\"" "\n" "ftp://ftp.sec.gov/edgar/data/" ".txt").replace("/","-")
    h = fname.find("-")
    h1 = fname.find("-",h+1)
    h2 = fname.find("-",h1+1)
    fyear = int(fname[h1+1:h2])
    if fyear>50:
        fyear = fyear+1900
    else:
        fyear = fyear+2000
    f = open("G:\EDGAR\s4\\s4 tables\\"+fname+".txt","r")
    tables = f.read()
    f.close()
    g.write(fname+","+fyear.__str__()+",")
    table_beg = tables.lower().find("<TABLE>".lower())
    table_end = tables.lower().find("<TABLE>".lower(),table_beg+1)
    for j in range(1,16): # looking forward 15 years
        year_txt1 = " "+(fyear+j).__str__()+" " # adding blanks to make sure it's a year (year serves as column name)
        year_txt2 = (fyear+j).__str__()+"..." # most form: 2000.......... (year serves as row name)
        # need earnings and specified year appear in one table
        true = 0
        while table_beg>0:
            year_find1 = tables[table_beg:table_end].find(year_txt1)
            year_find2 = tables[table_beg:table_end].find(year_txt2)
            earnings_find = tables[table_beg:table_end].lower().find("earning".lower()) # "estimated earnings, earnings per share..."
            find = min(earnings_find,max(year_find1,year_find2))
            if find>0:
                true = 1
            break
            table_beg = tables.lower().find("<TABLE>".lower(),table_end)
            table_end = tables.lower().find("<TABLE>".lower(),table_beg+1)
        g.write(true.__str__()+",")
    g.write("\n")
g.close()
"""
