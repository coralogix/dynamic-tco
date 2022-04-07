import boto3
from botocore.exceptions import ClientError
import os
import logging
from coralogix.handlers import CoralogixLogger
import requests
import json
import datetime
import dynamictco

class UtcResetter():
    def __init__(self):
        if not os.environ.get('PRIVATE_KEY'):
            raise Exception("Missing the PRIVATE_KEY environment variable. CANNOT CONTINUE")
        if not os.environ.get('TCO_KEY'):
            raise Exception("Missing the TCO_KEY environment variable. CANNOT CONTINUE")  
    #Take variables from environment           
    PRIVATE_KEY = os.environ.get('PRIVATE_KEY')
    APP_NAME = os.environ.get('APPLICATION_NAME', 'DYNAMICTCO')
    SUB_SYSTEM = os.environ.get('SUBSYSTEM_NAME', 'DYNAMICTCO')
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
        try:
            run_status = self.s3_client.get_object(Bucket=bucket_name,Key='DynamicTCO.active')['Body'].read()
            log = {
                "id":"Coralogix TCO Resetter",
                "event":"Triggered"
                }
            self.logger.info(log)       
            listtco = dynamictco.DynamicTCO.listTCO(self, event)
            listoverride = dynamictco.DynamicTCO.listOverride(self, event)
            dynamictco.DynamicTCO.delTCO(self, listtco)
            dynamictco.DynamicTCO.delOverride(self, listoverride)
            UtcResetter.restoreTCO(self, event, context)
            UtcResetter.restoreOverride(self, event, context)
            self.s3_client.delete_object(Bucket=bucket_name,Key='DynamicTCO.active')
        
        except ClientError as e: #When the flag is not found, there is no Action taken against TCO API
            log = {
                "id":"Coralogix TCO Resetter",
                "event":"No Action Taken. Flag Not Found"
            }
            self.logger.info(log)
        
        CoralogixLogger.flush_messages()

    def restoreTCO(self, event, context, bucket_name = AWS_BUCKET_NAME):
        listtco = json.loads(self.s3_client.get_object(Bucket=bucket_name,Key='listtco_latest.json')['Body'].read())
        for element in listtco:
            del element['id']
            arg = requests.post('https://'+self.coralogix_domain+'/api/v1/external/tco/policies',
                    headers = {'content-type': 'application/json', 'Authorization': "Bearer " + self.TCO_KEY}, json = element)
            log = {
                "Event" : "Restoring  TCO",
                "status_code" : arg.status_code,
                "log" : arg.text,
                "tco_policy" : element
            }
            self.logger.info(log)

    def restoreOverride(self, event, context, bucket_name = AWS_BUCKET_NAME):
        listoverride = json.loads(self.s3_client.get_object(Bucket=bucket_name,Key='listoverride_latest.json')['Body'].read())
        if len(listoverride) == 0:
            log = {
                "Event" : " Restoring Override",
                "log" : "No Override to Restore"
                }
            self.logger.info(log)
            return None    
        for element in listoverride:
            del element['id']
        arg = requests.post('https://'+self.coralogix_domain+'/api/v1/external/tco/overrides/bulk',
            headers = {'content-type': 'application/json', 'Authorization': "Bearer " + self.TCO_KEY}, json = listoverride)
        log = {
            "Event" : "Restoring  Overrides",
            "status_code" : arg.status_code,
            "log" : arg.text,
            "tco_policy" : listoverride
            }
        self.logger.info(log)
