import boto3
from datetime import datetime, timedelta

ws_client = boto3.client('workspaces')
cw_client = boto3.client('cloudwatch')
ws_paginator = ws_client.get_paginator('describe_workspaces')

def return_workspaces_list():
    # Get list of WorkSpaces
    response_iterator = ws_paginator.paginate()
    full_wsid_list = []
    for ws_page in response_iterator:
        ws_list = ws_page['Workspaces']
        for ws in ws_list:
            full_wsid_list.append(ws['WorkspaceId'])
    return full_wsid_list

def check_session_launch_time():
    full_wsid_list = return_workspaces_list()
    print('\n From inside the check_session_launch_time function \n')
    number = 0
    for wsid in full_wsid_list:
        response = cw_client.get_metric_data(
            MetricDataQueries=[
                {
                    'Id': 'someid',
                    'MetricStat': {
                        'Metric': {
                            'Namespace': 'AWS/WorkSpaces',
                            'MetricName': 'SessionLaunchTime',
                            'Dimensions': [
                                {
                                    "Name": "WorkspaceId",
                                    "Value": wsid
                                },
                            ]
                        },
                        'Period': 3600,  # 1 hour (3600 seconds)
                        'Stat': 'Average',
                     },
                },
            ],
            StartTime=datetime.now() - timedelta(hours=1),
            EndTime=datetime.now(),
        )
        metric_data_results = response['MetricDataResults']
        workspace_id = wsid
        for item in metric_data_results:
            values = item['Values']
            for value in values:
                if value > 60:
                    number += 1
                    print(f"The SessionLaunchTime of WorkSpace {workspace_id} is {value} s, which is more than 60 s")
    
    return number


def lambda_handler(event, context):
    number = check_session_launch_time()
    message = 'There are ' + str(number) + ' Amazon WorkSpaces with launch times of more than one minute'
    return message
