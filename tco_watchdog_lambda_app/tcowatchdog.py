import boto3
import os
import logging
from coralogix.handlers import CoralogixLogger
import requests
import json
import datetime


class TcoWatchDog:
    def __init__(self):
        if not os.environ.get('PRIVATE_KEY'):
            raise Exception("Missing the PRIVATE_KEY environment variable. CANNOT CONTINUE")
        if not os.environ.get('TCO_KEY'):
            raise Exception("Missing the TCO_KEY environment variable. CANNOT CONTINUE")
    
    #Take variables from environment    
    PRIVATE_KEY = os.environ.get('PRIVATE_KEY')
    APP_NAME = os.environ.get('APPLICATION_NAME', 'NO_APP_NAME')
    SUB_SYSTEM = os.environ.get('SUBSYSTEM_NAME', 'NO_SUB_NAME')
    TCO_KEY = os.environ.get('TCO_KEY')
    AWS_BUCKET_NAME = os.environ.get('AWS_BUCKET_NAME')

    #Set up logger objects
    logger = logging.getLogger("Python Logger")
    logger.setLevel(logging.DEBUG)  
    coralogix_handler = CoralogixLogger(PRIVATE_KEY, APP_NAME, SUB_SYSTEM)
    logger.addHandler(coralogix_handler)
    s3_client = boto3.client('s3')

    def main (self, event, context):
        log = {
            "id":"Coralogix TCO WatchDog",
            "event":"Triggered"
            }
        self.logger.info(log)
        #get current status of TCO Policy and override

        listtco = TcoWatchDog.listTCO(self, event)
        listoverride = TcoWatchDog.listOverride(self, event)
        #Save Current status of TCO and Override to S3
        self.s3_client.put_object(Bucket='tcowatchdogbucket',Key='listtco_latest.json', Body=json.dumps(json.loads(listtco)))
        self.s3_client.put_object(Bucket='tcowatchdogbucket',Key='listtco_'+datetime.datetime.now().isoformat()+'.json', Body=json.dumps(json.loads(listtco)))
        self.s3_client.put_object(Bucket='tcowatchdogbucket',Key='listoverride_latest.json', Body=json.dumps(json.loads(listoverride)))
        self.s3_client.put_object(Bucket='tcowatchdogbucket',Key='listoverride_'+datetime.datetime.now().isoformat()+'.json', Body=json.dumps(json.loads(listoverride)))
        


        TcoWatchDog.delTCO(self, listtco)

        TcoWatchDog.delOverride(self, listoverride)

        CoralogixLogger.flush_messages()

    def delOverride(self, str_override):
        overrides = json.loads(str_override)
        if len(overrides) == 0:
            log = {}
            log = {
                "Event" : " Deleting Override",
                "log" : "No Override to Delete"
                }
            self.logger.info(log)
        #print(overrides)
        for element in overrides:
            arg = requests.delete('https://api.coralogix.com/api/v1/external/tco/overrides/'+element["id"],
        headers = {
                        'content-type': 'application/json',
                        'Authorization': "Bearer " + self.TCO_KEY
                    }
        )
            
            if arg.status_code != 200:
                print('Error Deleting Override')
                log = {}
                log = {
                "Event" : "Error Deleting Override",
                "log" : element
                }
                self.logger.error(log)

    def delTCO(self, str_tcos):
        tcos = json.loads(str_tcos)
        if len(tcos) == 0:
            log = {}
            log = {
                "Event" : " Deleting Policy",
                "log" : "No Policy to Delete"
                }
            self.logger.info(log)
        
        for element in tcos:
            arg = requests.delete('https://api.coralogix.com/api/v1/external/tco/policies/'+element["id"],
        headers = {
                        'content-type': 'application/json',
                        'Authorization': "Bearer " + self.TCO_KEY
                    }
        )
            log = {}
            log = {
                "Event" : " Deleting Policy",
                "log" : element
                }
            self.logger.info(log)
            if arg.status_code != 200:
                print('Error Deleting Policy')
                log = {}
                log = {
                "Event" : "Error Deleting Policy",
                "log" : element
                }
                self.logger.error(log)
            

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
        #self.logger.info(log)
        #print(type(arg.content))
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
        #print(log)
        #self.logger.info(log)
        return (arg.content)