import boto3
from datetime import datetime, timedelta

ws_client = boto3.client('workspaces')
cw_client = boto3.client('cloudwatch')
ws_paginator = ws_client.get_paginator('describe_workspaces')
WORKPSACES_LATENCY = 60

def return_workspaces_list():
    # Get list of WorkSpaces
    response_iterator = ws_paginator.paginate()
    full_wsid_list = []
    for ws_page in response_iterator:
        ws_list = ws_page['Workspaces']
        for ws in ws_list:
            full_wsid_list.append(ws['WorkspaceId'])
    return full_wsid_list

def check_insession_latency():
    full_wsid_list = return_workspaces_list()
    print('\n From inside the check_insession_latency function \n')
    workspaces_bad_latency_number = 0
    for wsid in full_wsid_list:
        response = cw_client.get_metric_data(
            MetricDataQueries=[
                {
                    'Id': 'someid',
                    'MetricStat': {
                        'Metric': {
                            'Namespace': 'AWS/WorkSpaces',
                            'MetricName': 'InSessionLatency',
                            'Dimensions': [
                                {
                                    "Name": "WorkspaceId",
                                    "Value": wsid
                                },
                            ]
                        },
                        'Period': 43200,  # 12 hours (43200 seconds)
                        'Stat': 'Average',
                     },
                },
            ],
            StartTime=datetime.now() - timedelta(hours=12),
            EndTime=datetime.now(),
        )
        metric_data_results = response['MetricDataResults']
        workspace_id = wsid
        for item in metric_data_results:
            values = item['Values']
            for value in values:
                if value > WORKPSACES_LATENCY:
                    print(f"The latency of WorkSpace {workspace_id} is {value} ms, which is greater than 10 ms")
                    workspaces_bad_latency_number += 1
    
    return workspaces_bad_latency_number

def lambda_handler(event, context):
    # TODO implement
    number = check_insession_latency()
    message = 'There are ' + str(number) + ' Amazon WorkSpaces reporting high in-session latency'
    return message
