import tcowatchdog
import utcresetter
import json
import os

def lambda_handler(event,context):
    if 'detail-type' in event:
        tcoresetter = utcresetter.UtcResetter()
        tcoresetter.main(event, context)
    else:
        obj = json.loads(json.dumps(event)) 
        if obj["headers"]["Function-Key"] != os.environ.get('FUNCTION_KEY'):
            print("Missing Auth Header !!")
            return {
            'statusCode': 401,
            'body': 'Missing Key!'
            }

            return None
        else:
            tcosetter = tcowatchdog.TcoWatchDog()
            tcosetter.main(event, context)
            return {
                'statusCode': 200,
                'body': 'Success'
            }   

if __name__ == "__main__":
    
    event = {'version': '0', 'id': '60b2a65a-a2b7-58a9-d613-9274d66263b4', 'detail-type': 'Scheduled Event', 'source': 'aws.events', 'account': '771039649440', 'time': '2021-12-03T21:30:37Z', 'region': 'us-east-1', 'resources': ['arn:aws:events:us-east-1:771039649440:rule/cron'], 'detail': {}}
    context = {}
    utcresetter.UtcResetter().main(event, context)