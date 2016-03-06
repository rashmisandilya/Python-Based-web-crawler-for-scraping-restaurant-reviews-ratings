import csv

ifile  = open('test.csv', "rb")
reader = csv.reader(ifile, delimiter='\t')

rownum = 0
#for row in reader:
    # Save header row.
    #if rownum == 0:
     #   header = row
    #else:
        #colnum = 0
	#print row[2]
       # for col in row:
	    
        #    print col
         #   colnum += 1
            
   # rownum += 1

for row in reader:
	if rownum == 0:
		header = row
	else:
		url_list = []
		restaurant_id = row[0]
		restaurant_name = row[1]
		url_list.append(row[2])
		url_list.append(row[3])
		url_list.append(row[4])
	    
	rownum += 1
print restaurant_id
print restaurant_name
print url_list
ifile.close()
