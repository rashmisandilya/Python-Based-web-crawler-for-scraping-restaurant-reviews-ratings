def crawlCsvAndCreateJsonFile(fileName, jsonfile):
	ifile  = open(fileName, "rb")
	jsonFile = open(jsonfile,"w")
	reader = csv.reader(ifile)
	rownum = 0
	mainJson = {}
	jsonArray = []
	for row in reader:
		if rownum == 0:
			header = row
		else:
			url_list = []
			rid = row[0]
			name = 'TEST'
			url_list.append(row[1])
			url_list.append(row[2])
			url_list.append(row[3])
		    	json_data = crawlpage(rid, name, url_list)
			jsonArray.append(json_data)
		rownum += 1
	mainJson['restaurants'] = jsonArray
	print mainJson
	jsondata = json.dumps(mainJson)
	jsonFile.write(jsondata)
	ifile.close()
	jsonFile.close()
