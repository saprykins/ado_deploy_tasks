import pandas as pd



import requests
import json

organization = "g*"
project = "POD_Factory_v5"
workitemtype = "Task"
area_path = "POD_Factory_v5"
pat = "p6*"



def create_task(workitemtype, title):
    url = f"https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/${workitemtype}?api-version=7.0"
    
    headers = {
        "Content-Type": "application/json-patch+json"
    }

    body = [
        {
            "op": "add",
            "path": "/fields/System.Title",
            "value": title  # Set the title to "test wi"
        },
        {
            "op": "add",
            "path": "/fields/System.Description",
            "value": "This is a test work item created via API."  # Set the description
        }
    ]

    response = requests.post(
        url,
        data=json.dumps(body),
        headers=headers,
        auth=("", pat)
    )
    print(response)

    if response.status_code == 200:
        # work_item_id = response.json()['fields']
        print(response.json()['fields'])
        # print(f"Work Item ID: {work_item_id}")
        # print("Task work item created successfully.")
        
    else:
        print(f"Failed to create task work item. Status code: {response.status_code}")
        print(response.text)






# Step 1: Read the CSV file into a Pandas DataFrame
csv_file_path = 'apps.csv'  # Replace with the path to your CSV file
df = pd.read_csv(csv_file_path)

# Group the DataFrame by the 'app' and 'env' columns
grouped = df.groupby(['app', 'env'])

# Iterate through each group and its corresponding VMs
for (app, env), group_data in grouped:
    env_title = app + " - " + env
    env_workitemtype = 'user story'
    create_task(env_workitemtype, env_title)
    '''
    for vm in group_data['vm']:
        server_title = vm
        server_workitem = "server_wi"
        create_task(server_workitem, server_title)
    '''
