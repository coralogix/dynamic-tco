import boto3
import os
import logging
from coralogix.handlers import CoralogixLogger
import requests
import json
import datetime

class UtcResetter():
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
            "id":"Coralogix TCO Resetter",
            "event":"Triggered"
            }
        self.logger.info(log)
        
        UtcResetter.restoreTCO(self, event, context)
        UtcResetter.restoreOverride(self, event, context)
    CoralogixLogger.flush_messages()

    def restoreTCO(self, event, context):
        listtco = json.loads(self.s3_client.get_object(Bucket='tcowatchdogbucket',Key='listtco_latest.json')['Body'].read())
        for element in listtco:
            del element['id']
            arg = requests.post('https://api.coralogix.com/api/v1/external/tco/policies',
            headers = {
                            'content-type': 'application/json',
                            'Authorization': "Bearer " + self.TCO_KEY
                        },
            json = element
            )
            log = {}
            log = {
                "Event" : "Restoring  TCO",
                "status_code" : arg.status_code,
                "log" : arg.text,
                "tco_policy" : element
            }
            self.logger.info(log)
    
    def restoreOverride(self, event, context):
        listoverride = json.loads(self.s3_client.get_object(Bucket='tcowatchdogbucket',Key='listoverride_latest.json')['Body'].read())
        for element in listoverride:
            del element['id']
            arg = requests.post('https://api.coralogix.com/api/v1/external/tco/overrides',
            headers = {
                            'content-type': 'application/json',
                            'Authorization': "Bearer " + self.TCO_KEY
                        },
            json = element
            )
            log = {}
            log = {
                "Event" : "Restoring  Overrides",
                "status_code" : arg.status_code,
                "log" : arg.text,
                "tco_policy" : element
            }
            self.logger.info(log)