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
    APP_NAME = os.environ.get('APPLICATION_NAME', 'TCOWATCHDOG')
    SUB_SYSTEM = os.environ.get('SUBSYSTEM_NAME', 'TCOWATCHDOG')
    TCO_KEY = os.environ.get('TCO_KEY')
    AWS_BUCKET_NAME = os.environ.get('AWS_BUCKET_NAME')
    coralogix_domain = os.environ.get('CORALOGIX_LOG_URL', 'https://api.coralogix.com/api/v1/logs').split("/")[2]
    #Set up logger objects
    logger = logging.getLogger("Python Logger")
    logger.setLevel(logging.DEBUG)  
    if not logger.handlers:
        coralogix_handler = CoralogixLogger(PRIVATE_KEY, APP_NAME, SUB_SYSTEM)
        logger.addHandler(coralogix_handler)
    s3_client = boto3.client('s3')

    def main (self, event, context, bucket_name = AWS_BUCKET_NAME):
        log = {
            "id":"Coralogix TCO WatchDog",
            "event":"Triggered"
            }
        self.logger.info(log)
        #Get current status of TCO Policy and override
        listtco = TcoWatchDog.listTCO(self, event)
        listoverride = TcoWatchDog.listOverride(self, event)
        #Save Current status of TCO and Override to S3 
        self.s3_client.put_object(Bucket=bucket_name,Key='listtco_latest.json', Body=listtco) 
        self.s3_client.put_object(Bucket=bucket_name,Key='listtco_'+datetime.datetime.now().isoformat()+'.json', Body=listtco)
        self.s3_client.put_object(Bucket=bucket_name,Key='listoverride_latest.json', Body=listoverride)
        self.s3_client.put_object(Bucket=bucket_name,Key='listoverride_'+datetime.datetime.now().isoformat()+'.json', Body=listoverride)
        TcoWatchDog.delTCO(self, listtco)
        TcoWatchDog.delOverride(self, listoverride)        
        TcoWatchDog.applyTco(self, event, context)
        self.s3_client.put_object(Bucket=bucket_name,Key='tcowatchdog.active', Body="True")        
        CoralogixLogger.flush_messages()
        
    def applyTco(self,event,context):
        new_rules=json.loads(event["body"])
        for element in new_rules:
            arg = requests.post('https://'+self.coralogix_domain+'/api/v1/external/tco/policies',
            headers = {'content-type': 'application/json', 'Authorization': "Bearer " + self.TCO_KEY}, json = element)
            log = {
                "Event" : "Apply TCO",
                "status_code" : arg.status_code,
                "log" : arg.text,
                "tco_policy" : element
            }
            self.logger.info(log)
    
    def delOverride(self, str_override):
        overrides = json.loads(str_override)
        if len(overrides) == 0:
            log = {
                "Event" : " Deleting Override",
                "log" : "No Override to Delete"
                }
            self.logger.info(log)
            return None        
        arg = requests.delete('https://'+self.coralogix_domain+'/api/v1/external/tco/overrides/bulk',
        headers = {'content-type': 'application/json', 'Authorization': "Bearer " + self.TCO_KEY}, json = overrides)            
        if arg.status_code != 200:
            print('Error Deleting Override')
            print(overrides)
            log = {
            "Event" : "Error Deleting Override",
            "log" : overrides
            }
            self.logger.error(log)        
        log = {
            "Event" : " Deleting Override",
            "log" : overrides
        }
        self.logger.error(log)
    
    def delTCO(self, str_tcos):
        tcos = json.loads(str_tcos)
        if len(tcos) == 0:
            log = {
                "Event" : " Deleting Policy",
                "log" : "No Policy to Delete"
                }
            self.logger.info(log)        
        for element in tcos:
            arg = requests.delete('https://'+self.coralogix_domain+'/api/v1/external/tco/policies/'+element["id"],
                    headers = {'content-type': 'application/json', 'Authorization': "Bearer " + self.TCO_KEY}
                )
            log = {
                "Event" : " Deleting Policy",
                "log" : element
                }
            self.logger.info(log)
            if arg.status_code != 200:
                print('Error Deleting Policy')
                log = {
                "Event" : "Error Deleting Policy",
                "log" : element
                }
                self.logger.error(log)
            
    def listTCO(self, arg):
        arg = requests.get('https://'+self.coralogix_domain+'/api/v1/external/tco/policies',
                    headers = { 'content-type': 'application/json', 'Authorization': "Bearer " + self.TCO_KEY}
                    )
        new_content = json.loads(arg.content)
        log = {
            "Event" : "List Existing TCO",
            "log" : new_content
        }
        self.logger.info(log)
        return (arg.content)
    
    def listOverride(self, arg):
        arg = requests.get('https://'+self.coralogix_domain+'/api/v1/external/tco/overrides',
        headers = {
                        'content-type': 'application/json',
                        'Authorization': "Bearer " + self.TCO_KEY}
        )        
        new_content = json.loads(arg.content)
        log = {
            "Event":"List Existing TCO Overrides",
            "log":new_content
        }
        self.logger.info(log)
        return (arg.content)
