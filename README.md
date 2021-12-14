# TCO Watchdog App
## Deploy the application

Python 3.9


Please update folloing variables in template.yaml

 PRIVATE_KEY="xxxxx-xxxxx-xxxxx"
 TCO_KEY="xxxxxxx-d05d-4635-a5cb-xxxxxxxxxxx"
 APPLICATION_NAME="TCOWatchdog"
 SUBSYSTEM_NAME="TCOWatchdog"
 AWS_BUCKET_NAME="tcowatchdogbucket"
 FUNCTION_KEY="thisismysecretkey"

$ sam build 
$ sam deploy --guided


Add S3 Permission to Lambda Created Role ##(This should be done by Sam Template)

POST To ApiGateway must include header  that will be compared with the variable FUNCTION_KEY
  "Function-Key": "thisismysecretkey"

For Other Cluster use Env Variable:
CORALOGIX_LOG_URL=https://<Cluster URL>/api/v1/logs
where <Cluster URL> is
coralogix.com	or coralogix.us	or app.coralogix.in