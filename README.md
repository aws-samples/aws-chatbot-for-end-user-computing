Monitor and automate AWS End User Computing(EUC) with AWS Chatbot
--------------------------------------
This serves as README for the blogpost [Monitor and automate Amazon EUC with AWS Chatbot](https://amazon.awsapps.com/workdocs/index.html#/document/4dbd3e580cefb02d50341ce3bb6944c75b636c8d391e2ba614750a681d91fa7f) on the AWS Desktop and Application Streaming channel.

![Architecture diagram](/images/architecture.png "Architecture")

Prerequisites 
-------------
1. AWS account access with permissions to create CloudFormation stack, Lambda functions, SNS topic, IAM role and policies.
2. Microsoft Teams or Slack information.
   1. **Microsoft Teams**
      - Note down the Tenant ID, Team ID and Channel ID. Refer to the screenshots below. 
      ![Channel Link](/images/teams1.jpg "Channel Link")
      ![IDs](/images/teams2.jpg "Tenant, Team and Channel ID")
   2. **Slack**
      - Note down the Slack Workspace and Channel ID from browser. Refer to the screenshots below. 
      ![Slack IDs](/images/slack.jpg "Slack IDs")

Setup Process 
-------------
1. To configure a Slack client, 
follow the instructions in Step 1: Setting up AWS Chatbot with Slack. https://docs.aws.amazon.com/chatbot/latest/adminguide/slack-setup.html
   1. Follow steps 1 to 5 in the link. 
   2. Add AWS Chatbot to the Slack channel. Refer to step14 in the previous link.
2. To configure a Microsoft Teams client, follow the instructions in Step 1: Setting up AWS Chatbot with Microsoft Teams. https://docs.aws.amazon.com/chatbot/latest/adminguide/teams-setup.html#teams-client-setup
   1. Follow steps 1 to 5 in the link.
   2. Add AWS Chatbot to your team. Refer to step 14 in the link. 
3. Create Lambda deployment packages.
   1. Download and create zip files of the python files in the source directory https://gitlab.aws.dev/appc/eucchatbot/-/tree/main/source
   2. You may use the zip command in Linux to do so. 
   `zip chatbot_cost_explorer01.py.zip chatbot_cost_explorer01.py && zip chatbot_launchtime_checks01.py.zip chatbot_launchtime_checks01.py && zip chatbot_unhealthy_workspace_checks01.py.zip chatbot_unhealthy_workspace_checks01.py && zip chatbot_workspace_latency_checks01.py.zip chatbot_workspace_latency_checks01.py`
   3. The zip files **must** be named as chatbot_cost_explorer01.py.zip, chatbot_launchtime_checks01.py.zip, chatbot_unhealthy_workspace_checks01.py.zip and chatbot_workspace_latency_checks01.py.zip. 
4. Create an S3 bucket in the EUC account and upload zip files you created in the previous step with the chatbot.yaml file. The files should appear in the bucket as S3BucketName/chatbot_cost_explorer01.py.zip.
![Contents in S3 Bucket](/images/s3bucket.jpg "Contents of S3 Bucket")
5. Take note of the S3 Object URL of the chatbot.yaml cloudformation template and the name of the bucket. For example: https://euc-chatbot-bucket.s3.ap-southeast-1.amazonaws.com/chatbot.yaml is the S3 Object URL of the CloudFormation template and euc-chatbot-bucket is the S3 bucket name.   
6. In the EUC AWS account, navigate to the CloudFormation console and create a new stack using the S3 Object URL of the chatbot.yaml file and the S3 bucket name.
7. The required resources for the Chatbot service, such as the SNS topic, IAM role, IAM policy, and Lambda functions, will be created.

The template creates the following resources:
| Resource Name | Type |
| ------ | ------ |
|      ChatbotServicePolicy  |    AWS::IAM::ManagedPolicy    |
|     ChatbotServiceRole   |  AWS::IAM::Role      |
|     EUCChatbotExecutionRole | AWS::IAM::Role       |
|     EUCChatbotTopic       |    AWS::SNS::Topic    |
|     LatencyCheckFunction   |    AWS::Lambda::Function     |
|     LaunchTimeCheckFunction   |    AWS::Lambda::Function    |
|     UnHealthyWorkSpacesCheckFunction   |     AWS::Lambda::Function   |
|     CurrentEUCBillCheckFunction   |  AWS::Lambda::Function      |

Understanding AWS chabot permissions
--------
This solution creates an IAM role and policy for the AWS chatbot to interact with resources in your account. Please review and make amendments to IAM and guardrail policies if required to adhere to your organisation's security posture. Refer https://docs.aws.amazon.com/chatbot/latest/adminguide/understanding-permissions.html

LICENSE
-------------
This library is licensed under the MIT-0 License. See the LICENSE file.
