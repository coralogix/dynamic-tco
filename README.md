# TCO Watchdog App
This application is Basically a tool to facilitate the "No data lost philosophy in Coralogix"
This tool will use a change in the TCO functionalities in Coralogix to change the manner in which the account units are counted and allow for much more data to flow in but with less features enabled to it.

This compramise will be reverted every day at 00:00 UTC only to wait for the trigger to become active again.
We do suggest that utilizing this tool would be a second line of defence to a Pay-as-You-Go option enabled on the account.

# Requirements:
- An S3 bucket for the lambda to use
- An IAM role for the lambda execution and the S3 (list, read, write)
- Your aws User should have permissions to deploy lambdas.
- Your User should have AWS CLI and SAM.
- Coralogix audit account access.

# Installation of the solution
## Installing the Lambda function:
This lambda will accept POST calles to API Gateway and will keep the original config and current state on S3.
This will be an alternative to using a Database which will allways cost Somthing, as the rate of IO is rather low here.
S3 is cheaper and robust.

The lambda uses AWS SAM deployment framework.
Below are the steps to install the lambda:
- Clone this repository to the machine you wish to deploy from
- Update the Values on the config file
- Deploy the Lambda.


## Setting the new TCO policies to enforce by the tool.
This lambda uses Coralogix TCO API to enforce the new policies.
In the Body of the request to the API Gateway will have an array of policies.
To know more, please refere to https://coralogix.com/tutorials/tco-optimizer-api/ "Create new Policy" section.

# Comments and Collaboration:
If you have any Comment or Collaboration, please use github issue, create a pull request or just comment us in our Support Chat inside your Coralogix Account
Any suggestion will be much appriciated 


