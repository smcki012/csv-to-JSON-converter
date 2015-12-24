import json
import csv
import sys

jsonOutput = [];
mapCatToList = {}
listIssues = []

def loadCSV(Workbook1):
	with open(Workbook1, 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', dialect=csv.excel_tab)
		for row in reader:
			catObj = getCategory(row[0])

			issueName = row[1]
			issueType = row[2]

			if isNewIssue(issueName):
				issueObj = {}
				issueObj["name"] = issueName
				issueObj["include_keywords"] = []
				issueObj["include_type"] = issueType
				issueObj["exclude_keywords"] = []

				for i in range(3, len(row)):
					if row[i] != "":
						issueObj["include_keywords"].append(row[i])

				catObj["issues"].append(issueObj)
				listIssues.append(issueName.lower())

	print "Done !"

def getCategory(categoryName):
	if categoryName in mapCatToList:
		return jsonOutput[mapCatToList[categoryName]]
	else:
		catObj = {}
		catObj["name"] = categoryName
		catObj["issues"] = []
		jsonOutput.append(catObj)
		mapCatToList[categoryName] = len(jsonOutput)-1

		return catObj

def isNewIssue(issueName):
	if issueName.lower() in listIssues:
		print "Processing Error - You already have an issue with that name - " + issueName
		sys.exit(0)

	return True

def saveJson():
	json_file = open('output.json','wb')
	json_file.write(json.dumps(jsonOutput))
	json_file.close()

if len(sys.argv) < 2:
	print "Usage is - python csv2json.py <input_file.csv>"
	print "Make sure the input_file.csv has been saved as Windows Comma Separated Files CSV in Excel"
else:
	loadCSV(sys.argv[1])
	saveJson()
	print "Done! See file output.json"
