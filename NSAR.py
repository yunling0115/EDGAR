# Parsing Forms

import xlrd
import xlwt
import os
import ftplib
from ftplib import FTP
import urllib
import urllib2
import csv

path = "F:\EDGAR\Investment Adviser\N-forms\NSAR series mapping\\"
filepath = "F:\EDGAR\Investment Adviser\N-forms\NSAR series mapping\NSAR\\"
filepath_new = "F:\EDGAR\Investment Adviser\N-forms\NSAR series mapping\NSAR-cleaned\\"
bookpath = "F:\EDGAR\Investment Adviser\N-forms\NSAR series mapping\Tables\\"

c = csv.reader(open(path+"NSAR.csv", "r"))
httplist =[]
filename =[]
formtype =[]
for row in c:
    httplist.append(row[-1])
    filename.append(row[-2])
    formtype.append(row[-3])

# I. Tabulate Cleaned from (no "NT-NSAR", "NSAR-U", "NSAR-U/A")

# Load Map of Table
# - Table 1: Registrant's short panel
varlist1 = {} #dictionary of lists (indexed by i)
namelist1 = [] #dictionary name - no letter to substitute
book = xlrd.open_workbook(bookpath+"Master Vars - 1.xls")
sh = book.sheet_by_index(0)
for rx in range(sh.nrows):
    #print rx
    if sh.cell_value(rowx=rx,colx=1).strip().__len__()<7:
        namelist1.append(str(sh.cell_value(rowx=rx,colx=0).strip()+"  "+sh.cell_value(rowx=rx,colx=1).strip()))
    else:
        namelist1.append(str(sh.cell_value(rowx=rx,colx=0).strip()+" "+sh.cell_value(rowx=rx,colx=1).strip()))    
h1 = namelist1
h1.insert(0,"ID")
varlist1[0] = h1    

# - Table 1b: Registrant's short panel -- need to look further into individual files
varlist1b = {} #dictionary of lists (indexed by i)
namelist1b = [] #dictionary name - no letter to substitute
book = xlrd.open_workbook(bookpath+"Master Vars - 1b.xls")
sh = book.sheet_by_index(0)
for rx in range(sh.nrows):
    #print rx
    if sh.cell_value(rowx=rx,colx=1).strip().__len__()<7:
        namelist1b.append(str(sh.cell_value(rowx=rx,colx=0).strip()+"  "+sh.cell_value(rowx=rx,colx=1).strip()))
    else:
        namelist1b.append(str(sh.cell_value(rowx=rx,colx=0).strip()+" "+sh.cell_value(rowx=rx,colx=1).strip()))  
h1b = namelist1b
h1b.insert(0,"ID")
varlist1b[0] = h1b

# - Table 2: Series' short panel
varlist2 = {} #dictionary of lists
namelist2 = [] #dictionary name
book = xlrd.open_workbook(bookpath+"Master Vars - 2.xls")
sh = book.sheet_by_index(0)
for rx in range(sh.nrows):
    #print rx
    if sh.cell_value(rowx=rx,colx=1).strip().__len__()<7:
        namelist2.append(str(sh.cell_value(rowx=rx,colx=0).strip()+"  "+sh.cell_value(rowx=rx,colx=1).strip()))
    else:
        if sh.cell_value(rowx=rx,colx=1).strip().__len__()>7:
            namelist2.append(str(sh.cell_value(rowx=rx,colx=0).strip()+sh.cell_value(rowx=rx,colx=1).strip()))
        else:
            namelist2.append(str(sh.cell_value(rowx=rx,colx=0).strip()+" "+sh.cell_value(rowx=rx,colx=1).strip()))
          
h2 = namelist2
h2.insert(0,"ID")
varlist2[0] = h2

# - Table 3: Registrant's long panel
varlist3 = {} #dictionary of lists
namelist3 = [] #dictionary name
book = xlrd.open_workbook(bookpath+"Master Vars - 3.xls")
sh = book.sheet_by_index(0)
for rx in range(sh.nrows):
    #print rx
    if sh.cell_value(rowx=rx,colx=1).strip().__len__()<7:
        namelist3.append(str(sh.cell_value(rowx=rx,colx=0).strip()+"  "+sh.cell_value(rowx=rx,colx=1).strip()))
    else:
        namelist3.append(str(sh.cell_value(rowx=rx,colx=0).strip()+" "+sh.cell_value(rowx=rx,colx=1).strip()))
h3 = namelist3
h3.insert(0,"ID")
varlist3[0] = h3

# - Table 4: Series' long panel
varlist4 = {} #dictionary of lists
namelist4 = [] #dictionary name
book = xlrd.open_workbook(bookpath+"Master Vars - 4.xls")
sh = book.sheet_by_index(0)
for rx in range(sh.nrows):
    #print rx
    if sh.cell_value(rowx=rx,colx=1).strip().__len__()<7:
        namelist4.append(str(sh.cell_value(rowx=rx,colx=0).strip()+"  "+sh.cell_value(rowx=rx,colx=1).strip()))
    else:
        namelist4.append(str(sh.cell_value(rowx=rx,colx=0).strip()+" "+sh.cell_value(rowx=rx,colx=1).strip()))  
h4 = namelist4
h4.insert(0,"ID")
varlist4[0] = h4

# ------------------------------------------------------------------------------

#BN = 100
BN = httplist.__len__()

print "Parsing Table 1&1b"
# II. Table 1&1b (registrant's short panel)
'''
# - Parsing:
m = 1 #index of observation (0 for varname)
for i in range(0,BN):
    if formtype[i] not in ["NT-NSAR", "NSAR-U", "NSAR-U/A"]:
        print i
        f = open(filepath_new+filename[i]+".txt","r")
        source = f.readlines()
        f.close()
        # index is the index in the namelist (containing variable name)
        # , the list of index(of the namelist) is one-to-one mapped to the value
        list_index1 = []
        list_value1 = []
        list_index1b = []
        list_value1b = []
        # find string and take value
        for j in range(0,source.__len__()):
            string = source[j]
            # for table 1
            if string[0:11] in namelist1:
                list_index1.append(namelist1.index(string[0:11]))
                list_value1.append(string[11:string.__len__()].strip())
            # for table 1b
            if string[0:11] in namelist1b:
                list_index1b.append(namelist1b.index(string[0:11]))
                list_value1b.append(string[11:string.__len__()].strip())
        # write into separate lists of the master dictionary 1
        #varlist1[0].append(str(i))
        varlist1[m] = [str(i)]
        for k in range(1,namelist1.__len__()):
            if k in list_index1:
                varlist1[m].append(list_value1[list_index1.index(k)])
            else:
                varlist1[m].append("")
        # write into separate lists of the master dictionary 1b
        #varlist1b[0].append(str(i))
        varlist1b[m] = [str(i)]
        for k in range(1,namelist1b.__len__()):
            if k in list_index1b:
                # note: no repetitive index
                varlist1b[m].append(list_value1b[list_index1b.index(k)])
            else:
                varlist1b[m].append("")
        m = m+1
        
# Write into CSV files (1 and 1b)
with open(bookpath+"Consolidated Table 1.csv", "wb") as f:
    writer = csv.writer(f)
    for key, value in varlist1.items():
        writer.writerow([key]+value)
with open(bookpath+"Consolidated Table 1b.csv", "wb") as f:
    writer = csv.writer(f)
    for key, value in varlist1b.items():
        writer.writerow([key]+value)
'''

print "Parsing Table 3"       
# III. Table 3 #### Could be series long-panel (not registrant long-panel, 5/5/2013)
'''
# - Table 3: - split into N=sub subtables (subdictionary) according the first 3 digits
# -- A list of list
# -- A list of dictionaries? Iterate one dictionary for each list (XXX) to save space
# Detect the position of **
for i in range(1,namelist3.__len__()):
    namelist3[i] = namelist3[i][0:9]
    #s3.append(namelist3[i].index("*")) # ** are always the last two characters
# Generate subdictionaries varlist3_sub and sublists namelist3_sub
sub = 0
string_prior = namelist3[1]
Namelist3 = [[namelist3[1]]]
for i in range(2,namelist3.__len__()):
    string = namelist3[i]
    if string[0:3]==string_prior[0:3]:
        Namelist3[sub].append(string)
    else:
        Namelist3.append([])
        Namelist3[sub+1].append(string)
        sub = sub+1
    string_prior=string
for i in range(sub):
    Namelist3[i].insert(0,"subid")
    
sub = sub+1
# Parsing and Writing into CSV files in each loop of list - save space lower speed
for n in range(7,sub):
    varlist3 = {}
    varlist3[0] = Namelist3[n]
    varlist3[0].insert(0,"id") # Another variable to take into account multiple obs for each ID
    m = 1 # index of observation! (0 for varname)
    for i in range(0,BN):
    #for i in range(0,httplist.__len__()):
        if formtype[i] not in ["NT-NSAR", "NSAR-U", "NSAR-U/A"]:
            print i # ID, one ID corresponds to multiple m's
            f = open(filepath_new+filename[i]+".txt","r")
            source = f.readlines()
            f.close()
            # Refresh for each i
            list_index3 = []
            list_value3 = []
            list_var3 = [] # to take the ** value
            # find string and take value
            for j in range(0,source.__len__()):
                string = source[j]
                if string[0:9] in Namelist3[n]:
                    list_index3.append(Namelist3[n].index(string[0:9]))
                    list_value3.append(string[11:string.__len__()].strip())
                    list_var3.append(string[9:11])
            # group list_var3 into different groups
            if list_var3.__len__()==0:
                continue
            else:
                ssub = 0
                List_index3 = [[list_index3[0]]]
                List_value3 = [[list_value3[0]]]
                List_var3 = [[list_var3[0]]]
                #### note: no need to split value since index have been splitted
                if list_var3.__len__()>1:                    
                    string_prior = list_var3[0]
                    for nn in range(1,list_var3.__len__()):
                        string = list_var3[nn]
                        if string==string_prior:
                            List_index3[ssub].append(list_index3[nn])
                            List_value3[ssub].append(list_value3[nn])
                            List_var3[ssub].append(string)                            
                        else:
                            List_index3.append([])
                            List_value3.append([])
                            List_var3.append([])
                            List_index3[ssub+1].append(list_index3[nn])
                            List_value3[ssub+1].append(list_value3[nn])
                            List_var3[ssub+1].append(string)
                            string_prior = string
                            ssub = ssub+1
                ssub = ssub+1
                # ss now becomes the number of obs within each i                    
                # write into separate lists of the sub dictionary n with m=[0:ssub] as the observation                
                for nn in range(ssub):
                    templist3 = [str(i)]
                    templist3.append(List_var3[nn][0]) # repetition of id
                    for k in range(2,Namelist3[n].__len__()): # Note: 0 for ID, 1 for id
                        if k in List_index3[nn]:
                            #### Note: we have repetitive index here, value need to map one-to-one to index
                            templist3.append(List_value3[nn][List_index3[nn].index(k)])
                        else:
                            templist3.append("")
                    varlist3[m] = templist3
                    m = m+1 # note here
    with open(bookpath+"Consolidated Table 3-"+str(n)+".csv", "wb") as f:
        writer = csv.writer(f)
        for key, value in varlist3.items():
            writer.writerow([key]+value)
'''

print "Parsing Table 2" 
# IV. Table 2 (series identification - series short panel)
'''
# - Series-level Short Panel - Each series as an observation
# - some similar to III, but no outgrouping but yes ingrouping
# cut namelist3 in half
namelist2_s = []
for i in range(0, namelist2.__len__()):
    if "**" in namelist2[i]:
        namelist2_s.append(namelist2[i][0:7]) # ** always start from the 7th digit
varlist2[0] = namelist2_s
varlist2[0].insert(0,"series")
varlist2[0].insert(0,"ID")
# Parsing and Writing into CSV files
m = 1 # indexing observation
for i in range(0,BN):
#for i in range(0,httplist__len__()):
    if formtype[i] not in ["NT-NSAR", "NSAR-U", "NSAR-U/A"]:
        print i
        f = open(filepath_new+filename[i]+".txt","r")
        source = f.readlines()
        f.close()
        # Refresh for each i
        list_index2 = []
        list_value2 = []
        list_var2 = [] # to take the ** value
        # find string and take value
        for j in range(0, source.__len__()):
            string = source[j]
            if string[0:7] in namelist2_s:
                list_index2.append(namelist2_s.index(string[0:7]))
                list_value2.append(string[11:string.__len__()].strip())
                list_var2.append(string[7:9])
        # group list_var2 into different groups
        if list_var2.__len__()==0:
            continue
        else:
            ssub = 0
            List_index2 = [[list_index2[0]]]
            List_value2 = [[list_value2[0]]]
            List_var2 = [[list_var2[0]]]
            #### note: need to split value too
            if list_var2.__len__()>1:
                string_prior = list_var2[0]
                for nn in range(1,list_var2.__len__()):
                    string = list_var2[nn]
                    if string==string_prior:
                        List_index2[ssub].append(list_index2[nn])
                        List_value2[ssub].append(list_value2[nn])
                        List_var2[ssub].append(string)
                    else:
                        List_index2.append([])
                        List_value2.append([])
                        List_var2.append([])
                        List_index2[ssub+1].append(list_index2[nn])
                        List_value2[ssub+1].append(list_value2[nn])
                        List_var2[ssub+1].append(string)
                        string_prior = string
                        ssub = ssub+1
            ssub = ssub+1
            # ssub are the number of series that are reported in the form with List_var2 contains the key
            # write into csv with m=[0:ssub]
            for nn in range(ssub):
                templist2 = [str(i)]
                templist2.append(List_var2[nn][0])
                for k in range(2,namelist2_s.__len__()):
                    if k in List_index2[nn]:
                        templist2.append(List_value2[nn][List_index2[nn].index(k)])
                    else:
                        templist2.append("")
                varlist2[m] = templist2
                m = m+1
with open(bookpath+"Consolidated Table 2.csv", "wb") as f:
    writer = csv.writer(f)
    for key, value in varlist2.items():
        writer.writerow([key]+value)
'''

print "Parsing Table 4" 
# V. Table 4 (series long-panel)
'''
# Long panel of series
# Need subgrouping! - both take two digits and take four digits
# Some similar to VI, no outgrouping but double-ingrouping
namelist4_s = namelist4[5:9]
# A00**--: ** series, could be AA,01,02; --: broker
for i in range(0, namelist4_s.__len__()):
    if "**" in namelist4_s[i]:
        namelist4_s[i]=namelist4_s[i][0:7] # start with 7th digit
varlist4[0] = namelist4_s
varlist4[0].insert(0,"id")
varlist4[0].insert(0,"series")
varlist4[0].insert(0,"ID")
# Parsing and Writing into CSV files
m = 1 # indexing observation - put into the inner loop
for i in range(0,BN):
#for i in range(0,httplist.__len__()):
    if formtype[i] not in ["NT-NSAR", "NSAR-U", "NSAR-U/A"]:
        print i
        f = open(filepath_new+filename[i]+".txt","r")
        source = f.readlines()
        f.close()
        # Refresh for each i
        list_index4 = []
        list_value4 = []
        # double index
        list_var4 = [] # double-index
        list_var4_seires = []
        list_var4_id = []
        for j in range(0, source.__len__()):
            string = source[j]
            if string[0:7] in namelist4_s:
                list_index4.append(namelist4_s.index(string[0:7]))
                list_value4.append(string[11:string.__len__()].strip())
                list_var4.append(string[7:11])
                #list_var4_series.append(string[7:9])
                #list_var4_id.append(string[9:11])
        # group list_var4 (double-index) into different groups
        if list_var4.__len__()==0:
            continue
        else:
            ssub = 0
            List_index4 = [[list_index4[0]]]
            List_value4 = [[list_value4[0]]]
            List_var4 = [[list_var4[0]]]
            #List_var4_series = [[list_var4_series[0]]]
            #List_var4_id = [[list_var4_id[0]]]
            if list_var4.__len__()>1:
                string_prior = list_var4[0]
                for nn in range(1,list_var4.__len__()):
                    string = list_var4[nn]
                    if string==string_prior:
                        List_index4[ssub].append(list_index4[nn])
                        List_value4[ssub].append(list_value4[nn])
                        List_var4[ssub].append(list_var4[nn])
                        #List_var4_series[ssub].append(list_var4_series[nn])
                        #List_var4_id[ssub].append(list_var4_id[nn])
                    else:
                        List_index4.append([])
                        List_value4.append([])
                        List_var4.append([])
                        #List_var4_series.append([])
                        #List_var4_id.append([])
                        List_index4[ssub+1].append(list_index4[nn])
                        List_value4[ssub+1].append(list_value4[nn])
                        List_var4[ssub+1].append(list_var4[nn])
                        #List_var4_series[ssub+1].append(list_var4_series[nn])
                        #List_var4_id[ssub+1].append(list_var4_id[nn])
                        string_prior = string
                        ssub = ssub+1
                ssub = ssub+1 
                # ssub are the number of (series x id)
                # write into csv with m=[0:ssub]
                for nn in range(ssub):
                    templist4 = [str(i)]
                    templist4.append(List_var4[nn][0][0:2])
                    templist4.append(List_var4[nn][0][2:4])
                    for k in range(3, namelist4_s.__len__()): # note: namelist4_s's real value start from the 3rd
                        if k in List_index4[nn]:
                            templist4.append(List_value4[nn][List_index4[nn].index(k)])
                        else:
                            templist4.append("")
                    varlist4[m] = templist4
                    m = m+1
with open(bookpath+"Consolidated Table 4.csv", "wb") as f:
    writer = csv.writer(f)
    for key, value in varlist4.items():
        writer.writerow([key]+value)
'''                                         
# ------------------------------------------------------------------------------



