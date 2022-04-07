# Dynamic TCO App
This application is a tool to facilitate the "No data lost philosophy in Coralogix"
This tool will use a change in the TCO functionalities in Coralogix to change the manner in which the account units are counted and allow for much more data to flow in but with less features enabled to it.

This compromise will be reverted every day at 00:00 UTC only to wait for the trigger to become active again.
We do suggest that utilizing this tool would be a second line of defence to a Pay-as-You-Go option enabled on the account.

# Requirements:
- An S3 bucket for the lambda to use
- Your aws User should have permissions to deploy lambdas.
- Your User should have AWS CLI and SAM.
- Coralogix audit account access.

# Installation of the solution
## Installing the Lambda function:
This lambda will accept POST calles to API Gateway and will keep the original config and current state on S3.
This will be an alternative to using a Database which will allways cost somthing, as the rate of IO is rather low here.
S3 is cheaper and robust.

The lambda uses AWS SAM deployment framework.
Below are the steps to install the lambda:
- Clone this repository to the machine you wish to deploy from
- Deploy the Lambda.
```
# sam build
# sam deploy --guided
```
- Go to the created Lambda function and add AmazonS3FullAccess Policy to the Excecution Role.
- Update Lambdas Environmental Variables from AWS Console.

Variable |Description
----------|------------
APPLICATION_NAME |Application Name in Coralogix.
AWS_BUCKET_NAME |Bucket the function will use to save tco status. Created in the requirements.
FUNCTION_KEY |Secret key that is used to authenticate against the lambda function.
PRIVATE_KEY |Coralogix Send your logs Api Key. Data Flow->ApiKeys
SUBSYSTEM_NAME |Subsystem name in Coralogix
TCO_KEY |Coralogix TCO Api Key. Data Flow->ApiKeys


If your Account is not in the EU region (the account url does not have a .com suffix)
you will need to add this environment variable:
```
CORALOGIX_LOG_URL=https://<coralogix_cluster_url>/api/v1/logs
```
Cluster location | coralogix_cluster_url
-----------------| --------------------
US| api.coralogix.us
IN| api.app.coralogix.in
Singapore| api.coralogixsg.com
EU2| api.eu2.coralogix.com

## Setting the new TCO policies to enforce by the tool.
This lambda uses Coralogix TCO API to enforce the new policies.
In the Body of the request to the API Gateway will have an array of policies.
To know more, please refere to https://coralogix.com/tutorials/tco-optimizer-api/ "Create new Policy" section.

# Comments and Collaboration:
If you have any Comment or Collaboration, please use github issue, create a pull request or just comment us in our Support Chat inside your Coralogix Account
Any suggestion will be much appriciated 
