import requests,getopt
from datetime import datetime
import json
import csv
from io import StringIO

api_url = "https://support.bmcedirect.me/api"
gophish_url = "https://support.bmcedirect.me/account"
header = {
    'Authorization': '6a00607c93b2bddb6825538498940646cfe8cd84810949e26fa8045ee25cfbb9',
    'content-type': "application/json",
    }

proxies = {
   'http': 'http://proxy.eurafric.com:8080',
   'https': 'http://proxy.eurafric.com:8080',
}
group_end_point = "groups/"
csv_file = 'BTI_Users_export_last.csv' #update
csv_file_header = True

def rowCount(csv_file):
    with open(csv_file, 'r',) as csvfile:
        accountsFile = StringIO(csvfile.read().replace(" ;", ";"))
        accounts = csv.reader(accountsFile, delimiter=';')
        return sum(1 for row in accounts)  


""" must be clarified more try:
    opts, args = getopt.getopt(sys.argv[1:], 'h', ['file='])
except getopt.GetoptError:
    print('create_groups.py --file <input file>')
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print('create_groups.py --file <input file>')
        sys.exit()
    elif opt in ("-f", "--file"):
        if arg and arg.strip():
            csv_file = arg
        else
            print('create_groups.py --file <input file>')
            sys.exit() """


# read csv file
#status_code = 201
index = 1
CHUNK_SIZE = 30
group_name = "BTI_GROUP_" #update
new_group = {
        "name": group_name+str(index),
        "targets": []
    }
with open(csv_file, 'r',) as csvfile:
    row_count = rowCount(csv_file)  
    if csv_file_header:
        row_count = row_count - 1
    accountsFile = StringIO(csvfile.read().replace(" ;", ";"))
    accounts = csv.reader(accountsFile, delimiter=';')
    next(accounts)
    count = 0
    for row in accounts:
        print(', '.join(row))
        if row[2].replace(" ", "") != "":
            new_group['targets'].append({
                    "email": row[2],
                    "first_name": row[5],
                    "last_name": row[6],
                    "position": ""
                })
            count+=1
            if count == CHUNK_SIZE or (index*CHUNK_SIZE > row_count and row_count%CHUNK_SIZE == count):
                group_payload = json.dumps(new_group)
                response = requests.post(api_url+"/" + group_end_point, headers=header, verify=False, proxies=proxies, data=group_payload)
                if response.status_code == 201:
                    print(f":) New group [{new_group['name']}, accounts_count:{len(new_group['targets'])}] created successfully")
                else:
                    print(":( Error creating group")
                count = 0
                index+=1
                new_group['name'] = group_name + str(index)
                new_group['targets'] = []    


""" # create the groups
groups = requests.get(api_url+"/" + group_end_point, headers=header, verify=False, proxies=proxies)
groups = groups.json()
print(groups)
for group in groups:
    # create compaign and assign the current group
   
    comapaign_payload = json.dumps(payload)
    print(comapaign_payload)
    #requests.post(api_url+"/" + group_end_point, headers=header, verify=False, proxies=proxies, data=comapaign_payload)
 """

