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
  