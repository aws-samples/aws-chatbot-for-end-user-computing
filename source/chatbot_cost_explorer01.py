import os
import boto3
from datetime import date, timedelta

REGION = os.environ.get('WorkSpacesRegion')
ce_client = boto3.client('ce', REGION)

def get_cost_and_usage(start_date, end_date):
    response = ce_client.get_cost_and_usage(
        TimePeriod={
            'Start': start_date,
            'End': end_date
        },
        Granularity='MONTHLY',
        Metrics=['BlendedCost'],
        Filter={
            'Dimensions': {
                'Key': 'SERVICE',
                'Values': ['Amazon WorkSpaces', 'Amazon AppStream']
            }
        },
        GroupBy=[
            {
                'Type': 'DIMENSION',
                'Key': 'SERVICE'
            }
        ]
    )
    return response['ResultsByTime']

def calculate_total_cost(results):
    total_workspaces_cost = 0
    total_appstream_cost = 0

    for result in results:
        groups = result['Groups']
        for group in groups:
            keys = group['Keys']
            bill = group['Metrics']['BlendedCost']['Amount']
            
            if keys == ['Amazon AppStream']:
                total_appstream_cost += float(bill)
            elif keys == ['Amazon WorkSpaces']:
                total_workspaces_cost += float(bill)
    
    return total_workspaces_cost, total_appstream_cost

def lambda_handler(event, context):
    today = date.today()
    yesterday = today - timedelta(days=1)
    start_of_month = today.replace(day=1)
    
    try:
        if start_of_month == today:
            end_date = yesterday
        else:
            end_date = today
        
        results = get_cost_and_usage(str(start_of_month), str(end_date))
        
        total_workspaces_cost, total_appstream_cost = calculate_total_cost(results)
        
        euc_charges_for_this_month = total_workspaces_cost + total_appstream_cost
        
        euc_charges_for_this_month = round(euc_charges_for_this_month, 2)
        
        total_euc_cost = f'EUC charges for this month is {euc_charges_for_this_month} USD of which'
        total_workspaces_cost = f' WorkSpaces charges are {total_workspaces_cost} USD'
        total_appstream_cost = f' and AppStream charges are {total_appstream_cost} USD'
        
        return total_euc_cost + total_workspaces_cost + total_appstream_cost
    
    except (boto3.exceptions.Boto3Error, ValueError) as error:
        raise ValueError(f'An error occurred: {str(error)}')
