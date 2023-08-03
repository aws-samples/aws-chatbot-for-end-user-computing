import boto3
ws_client = boto3.client('workspaces')
def check_workspaces_health_status():
    print('\nFrom inside the check_workspaces_health_status function \n')
    paginator = ws_client.get_paginator('describe_workspaces')
    response_iterator = paginator.paginate()
    unhealthy_count = 0
    for response in response_iterator:
        workspaces = response['Workspaces']
        for workspace in workspaces:
            workspace_id = workspace['WorkspaceId']
            username = workspace['UserName']
            state = workspace['State']
            # print('WorkSpaces health status:', workspace_id, username, state)
            if state == 'UNHEALTHY':
                unhealthy_count += 1
                print('WorkSpaces health status:', workspace_id, username, state)
    return unhealthy_count

def lambda_handler(event, context):
    number = check_workspaces_health_status()
    message = f'There are {number} unhealthy Amazon WorkSpaces'
    return message
