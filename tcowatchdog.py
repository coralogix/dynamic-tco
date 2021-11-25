import boto3
import os
import logging
from coralogix.handlers import CoralogixLogger
import requests
import json
import pickle




class TcoWatchDog:
    def __init__(self):
        if not os.environ.get('PRIVATE_KEY'):
            raise Exception("Missing the PRIVATE_KEY environment variable. CANNOT CONTINUE")
        if not os.environ.get('TCO_KEY'):
            raise Exception("Missing the TCO_KEY environment variable. CANNOT CONTINUE")
        
    PRIVATE_KEY = os.environ.get('PRIVATE_KEY')
    APP_NAME = os.environ.get('APPLICATION_NAME', 'NO_APP_NAME')
    SUB_SYSTEM = os.environ.get('SUBSYSTEM_NAME', 'NO_SUB_NAME')
    TCO_KEY = os.environ.get('TCO_KEY')
    AWS_BUCKET_NAME = os.environ.get('AWS_BUCKET_NAME')
    logger = logging.getLogger("Python Logger")
    logger.setLevel(logging.DEBUG)  
    coralogix_handler = CoralogixLogger(PRIVATE_KEY, APP_NAME, SUB_SYSTEM)
    logger.addHandler(coralogix_handler)
    s3_client = boto3.client('s3')

    def settco (self, event):
        #self.logger.info('Hello World')
        #print(event)
        log = {
            "id":"Coralogix TCO WatchDog",
            "event":"Trigger recived"
            }
        self.logger.warn(log)

        listtco = TcoWatchDog.listTCO(self, event).decode('utf8').replace("\"", '\'')
        
        listoverride = TcoWatchDog.listOverride(self, event).decode('utf8').replace("\"", '\'')
        self.s3_client.put_object(Bucket='tcowatchdogbucket',Key='listtco_latest.json', Body=json.dumps(listtco))
        self.s3_client.put_object(Bucket='tcowatchdogbucket',Key='listoverride_latest.json', Body=json.dumps(listoverride))
        CoralogixLogger.flush_messages()

    def listTCO(self, arg):
        
        arg = requests.get('https://api.coralogix.com/api/v1/external/tco/policies',
        headers = {
                        'content-type': 'application/json',
                        'Authorization': "Bearer " + self.TCO_KEY
                    }
        )
        log = {}
        log = {
            "Event" : "List Existing TCO",
            "log" : arg.content.decode('UTF8').replace("\"", '\'')
        }
        self.logger.info(log)
        return (arg.content)
    
    def listOverride(self, arg):
        
        arg = requests.get('https://api.coralogix.com/api/v1/external/tco/overrides',
        headers = {
                        'content-type': 'application/json',
                        'Authorization': "Bearer " + self.TCO_KEY
                    }
        )
        log = {}
        log = {
            "Event":"List Existing TCO Overrides",
            "log":arg.content.decode('UTF8').replace("\"", '\'')
        }
        self.logger.info(log)
        return (arg.content)