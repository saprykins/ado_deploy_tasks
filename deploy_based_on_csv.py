import pandas as pd
import requests
import json

organization = "go*"
project = "P*"
workitemtype = "Task"
area_path = "P*"
pat = "p*"
parent_id = 0


app_csv_file_path = 'apps.csv'  # Replace with the path to your CSV file
tasks_csv_file_path = 'pb.csv'

def create_user_story(workitemtype, title):
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
        work_item_id = response.json()['id']
        print(f"Work Item ID: {work_item_id}")
        return work_item_id  # Return the work_item_id if successful

    else:
        print(f"Failed to create task work item. Status code: {response.status_code}")
        print(response.text)
        return None  # Return None if the creation fails


def get_app_url(parent_id):   
    '''
    Get the link of the parent
    '''

    url = 'https://dev.azure.com/' + organization + '/_apis/wit/workItems/' + str(parent_id) + '?$expand=all'
    
    headers = {
        "Content-Type": "application/json-patch+json"
    }

    response = requests.get(
        url = url,
        headers=headers,
        auth=("", pat), 
    )
    # print(response)
    lnk = response.json()["url"]
    return lnk



def create_child(workitemtype, title, parent_id):
    # parent_id = 0
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
        },
        {
            "op": "add",
            "path": "/fields/System.Parent",
            "value": parent_id  # Set the parent work item ID
        }, 
        {
        "op": "add",
        "path": "/relations/-",
        "value": {
            "rel":"System.LinkTypes.Hierarchy-Reverse",
            "url":get_app_url(parent_id)
            }
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
        work_item_id = response.json()['id']
        print(f"Work Item ID: {work_item_id}")
        print("parent ID is ", parent_id)
        return work_item_id
        
    else:
        print(f"Failed to create task work item. Status code: {response.status_code}")
        print(response.text)
        return None






def create_task(workitemtype, title, parent_id, tags, description, activity, phase):
    # parent_id = 0
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
            "value": description  # Set the description
        },
        {
            "op": "add",
            "path": "/fields/System.Parent",
            "value": parent_id  # Set the parent work item ID
        },
                {
            "op": "add",
            "path": "/fields/System.Tags",
            "value": tags  # Set the title to "test wi"
        },
        {
            "op": "add",
            "path": "/fields/Custom.Mainactivity",
            "value": activity  # Set the description
        },
        {
            "op": "add",
            "path": "/fields/Custom.TPhase",
            "value": phase  # Set the parent work item ID
        }, 
        {
        "op": "add",
        "path": "/relations/-",
        "value": {
            "rel":"System.LinkTypes.Hierarchy-Reverse",
            "url":get_app_url(parent_id)
            }
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
        work_item_id = response.json()['id']
        print(f"Work Item ID: {work_item_id}")
        print("parent ID is ", parent_id)
        return work_item_id
        
    else:
        print(f"Failed to create task work item. Status code: {response.status_code}")
        print(response.text)
        return None





# 
# MAIN 
#

# Step 1: Read the CSV file into a Pandas DataFrame

df = pd.read_csv(app_csv_file_path)

tasks = pd.read_csv(tasks_csv_file_path)

# Group the DataFrame by the 'app' and 'env' columns

app_grouped = df.groupby(['app']) # iterate through applications
grouped = df.groupby(['app', 'env']) # iterate through environments

task_workitem = "task"


# Iterate through each group and its corresponding VMs
for app, group_data in app_grouped: 
    app_workitemtype = "epic"
    app_title = app
    parent_id = create_user_story(app_workitemtype, app_title)
    
    for (app, env), group_data in grouped:    
        if app == app_title:
            env_title = app + " - " + env
            env_workitemtype = 'user story'
            parent_id2 = create_child(env_workitemtype, env_title, parent_id)
        
            # Creating servers
            for vm in group_data['vm']:
                server_title = vm
                server_workitem = "server_wi"
                create_child(server_workitem, server_title, parent_id2)
            
            for index, row in tasks.iterrows():
                task_title = row['task']     # Assuming 'tag' is the column with task titles
                tags = row['tag']
                description = row['description']
                activity = row['activity']
                phase = row['phase']
                create_task(task_workitem, task_title, parent_id2, tags, description, activity, phase)

