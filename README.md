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

For Other Cluster use Env Variable:
CORALOGIX_LOG_URL=https://<Cluster URL>/api/v1/logs
where <Cluster URL> is
coralogix.com	or coralogix.us	or app.coralogix.in

