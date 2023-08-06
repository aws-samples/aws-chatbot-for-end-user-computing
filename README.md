Monitor and automate AWS End User Computing(EUC) with AWS Chatbot
--------------------------------------
This serves as README for the blogpost **Monitor and automate Amazon EUC with AWS Chatbot** on the AWS Desktop and Application Streaming channel.

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
1. To configure a Slack chat client, 
follow the instructions in Step 1: Setting up AWS Chatbot with Slack. **https://docs.aws.amazon.com/chatbot/latest/adminguide/slack-setup.html**
   1. Follow steps 1–5. 
   2. Add AWS Chatbot to the Slack channel by following step 14.
2. To configure a Microsoft Teams client, follow the instructions in Step 1: Setting up AWS Chatbot with Microsoft Teams. **https://docs.aws.amazon.com/chatbot/latest/adminguide/teams-setup.html#teams-client-setup**
   1. Follow steps 1 to 5.
   2. Add AWS Chatbot to your team by following step 14. 
3. Create Lambda deployment packages by creating zip archives of the four python files in the source directory.
   1. Download the hour python files in the source directory [https://github.com/aws-samples/aws-chatbot-for-end-user-computing/tree/main/source](https://github.com/aws-samples/aws-chatbot-for-end-user-computing/tree/main/source)
   2. Create zip archives. If you are using Linux or MacOS you may use the following command to do so.
   `zip chatbot_cost_explorer01.py.zip chatbot_cost_explorer01.py && zip chatbot_launchtime_checks01.py.zip chatbot_launchtime_checks01.py && zip chatbot_unhealthy_workspace_checks01.py.zip chatbot_unhealthy_workspace_checks01.py && zip chatbot_workspace_latency_checks01.py.zip chatbot_workspace_latency_checks01.py`
   3. The zip archives **must** be named as chatbot_cost_explorer01.py.zip, chatbot_launchtime_checks01.py.zip, chatbot_unhealthy_workspace_checks01.py.zip and chatbot_workspace_latency_checks01.py.zip. 
4. Create an S3 bucket in the EUC account and upload zip archives you created in the previous step along with the chatbot.yaml file. The files should appear in the bucket as S3BucketName/chatbot_cost_explorer01.py.zip.
![Contents in S3 Bucket](/images/s3bucket.jpg "Contents of S3 Bucket")
5. Take note of the S3 Object URL of the chatbot.yaml cloudformation template and the name of the bucket. For example: https://BucketName.s3.Region.amazonaws.com/chatbot.yaml
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
