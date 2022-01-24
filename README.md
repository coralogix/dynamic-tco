# TCO Watchdog App
## Deploy the application

Python 3.9



$ sam build 
$ sam deploy --guided


Add S3 Permission to Lambda Created Role 

Go into the Created lambda and Edit the folling Env Variables from the UI:

PRIVATE_KEY :
    This is the Coralogix Private_key for sending logs
APP_NAME :
    Your application Name in Coralogix.
SUBSYSTEM_NAME:
    Your Subsystem Name in Coralogix.

CORALOGIX_TCO_KEY:
    This is the TCO Api Key. You can find it in API "Access Alerts, Rules and Tags API Key"

AWSBUCKEY
    This is the bucket needed for saving TCO history  and State.
    
POST To ApiGateway must include header  that will be compared with the variable FUNCTION_KEY

  "Function-Key": "thisismysecretkey"

For Other Cluster use Env Variable: CORALOGIX_LOG_URL=https:///api.coralogix.com/v1/logs where is coralogix.com or coralogix.us or app.coralogix.in




The payload to the APIGateway created needs to be with the same syntax as the TCO API Create Policy (https://coralogix.com/tutorials/tco-optimizer-api/)

Example:
[
  {
    "name": "All low",
    "priority": "low",
    "severities": [
      4,
      5,
      6
    ]
  },
  {
    "name": "Policy Creation test new",
    "priority": "medium",
    "severities": [
      1,
      2,
      3
    ]
  }
]


This payload is the  Policy/Policies that will be put in place once the Usage Alert is triggered.



