#!/usr/bin/env python3

import requests
import sys
import datetime
from confirm import confirm
from gsheets import gSheets

pdf_id = sys.argv[1]

# Set Authentication Token
token = [YOUR_COURTLISTENER_ACCESS_TOKEN]
headers = {'Authorization': 'Token ' + token}

# Build docket query for docket number
docQuery = 'https://www.courtlistener.com/api/rest/v3/dockets/?docket_number='
docketNum = sys.argv[2]
docketNum = docketNum.replace(' ', '%20')  # encode white space for URL
docketNum = docketNum.replace('\"', '')  # strip quotation marks
docQuery += docketNum

# Check for second argument; if found, add to query as court_id
if len(sys.argv) > 3:
    docQuery += '&court__id=' + sys.argv[3]

# Search for docket
docRequest = requests.get(docQuery, headers=headers)
parsedDocket = docRequest.json()

# If no matches, return error message
if len(parsedDocket['results']) < 1:
    print('\nNo cases match this docket number.\n')
    exit()

# If more than one case returned and court arg present, parse first result
elif (len(parsedDocket['results']) > 1) and (len(sys.argv) > 2):
    for doc in parsedDocket['results']:
        caseName = doc['case_name']
        caseCourt = doc['court']
        caseCluster = doc['clusters']
        for clus in caseCluster:
            caseCluster = clus

# if more than one case returned and no court arg, alert user to add court id
elif len(parsedDocket['results']) > 1:
    output = '\nMore than one case matches your docket number:\n'
    for doc in parsedDocket['results']:
        caseName = doc['case_name']
        caseCourt = doc['court']
        courtPre = 'https://www.courtlistener.com/api/rest/v3/courts/'
        caseCourt = caseCourt.replace(courtPre, '')
        caseCourt = caseCourt.replace('/', '')
        output += '\n' + caseName + ' (' + caseCourt + ')'
    output += '\n\nSearch again and add the court code as a second argument.\n'
    print(output)
    exit()

# If only one result, parse docket object for case names and cluster
else:
    for doc in parsedDocket['results']:
        caseName = doc['case_name']
        if doc['case_name_full']:
            caseFull = doc['case_name_full']
        else:
            caseFull = caseName
        caseCluster = doc['clusters']
        caseDocket = doc['docket_number']
        for clus in caseCluster:
            caseCluster = clus

# Get cluster object
clusterRequest = requests.get(caseCluster, headers=headers)
parsedCluster = clusterRequest.json()

# Get cluster year
caseDate = parsedCluster['date_filed']
caseYear = datetime.datetime.strptime(caseDate, '%Y-%m-%d')
caseYear = caseYear.year
caseYear = str(caseYear)

# Display citation
output = '\nThe following information will be added to Google Sheets:'
output += '\n\npdf#:\n' + pdf_id
output += '\n\nDocket #:\n' + caseDocket
output += '\n\nYear:\n' + caseYear
output += '\n\nCase citation (Bluebook):\n' + caseName
output += '\n\nFull Case Name:\n' + caseFull
output += '\n'

print(output)

if confirm() is False:
    print('\nNo data was added to Google Sheets\n')
    exit()
else:
    gSheets(pdf_id, caseDocket, caseYear, caseName, caseFull)
    print('\nThe data was added to Google Sheets\n')
    exit()
