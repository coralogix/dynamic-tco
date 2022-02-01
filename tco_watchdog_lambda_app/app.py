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
    event = {'resource': '/testing', 'path': '/testing', 'httpMethod': 'POST', 'headers': {'Accept': 'application/json, text/plain, */*', 'Content-Type': 'application/json', 'Host': 'igdlr449lh.execute-api.us-east-1.amazonaws.com', 'User-Agent': 'axios/0.21.1', 'X-Amzn-Trace-Id': 'Root=1-61a0ee68-596b607c4c64817277a65eff', 'x-api-key': 'CHOZ2xjpjh8TBibLf8K0rai6O9uUoPcacydKHobg', 'X-Forwarded-For': '54.194.244.111', 'X-Forwarded-Port': '443', 'X-Forwarded-Proto': 'https', "Function-Key": "thisismysecretkey"}, 'multiValueHeaders': {'Accept': ['application/json, text/plain, */*'], 'Content-Type': ['application/json'], 'Host': ['igdlr449lh.execute-api.us-east-1.amazonaws.com'], 'User-Agent': ['axios/0.21.1'], 'X-Amzn-Trace-Id': ['Root=1-61a0ee68-596b607c4c64817277a65eff'], 'x-api-key': ['CHOZ2xjpjh8TBibLf8K0rai6O9uUoPcacydKHobg'], 'X-Forwarded-For': ['54.194.244.111'], 'X-Forwarded-Port': ['443'], 'X-Forwarded-Proto': ['https']}, 'queryStringParameters': None, 'multiValueQueryStringParameters': None, 'pathParameters': None, 'stageVariables': None, 'requestContext': {'resourceId': 'nps8r5', 'resourcePath': '/testing', 'httpMethod': 'POST', 'extendedRequestId': 'JaowZGmFoAMFjmQ=', 'requestTime': '26/Nov/2021:14:25:44 +0000', 'path': '/default/testing', 'accountId': '771039649440', 'protocol': 'HTTP/1.1', 'stage': 'default', 'domainPrefix': 'igdlr449lh', 'requestTimeEpoch': 1637936744716, 'requestId': '2489f10f-a52e-4328-a209-100ca508d4a5', 'identity': {'cognitoIdentityPoolId': None, 'cognitoIdentityId': None, 'apiKey': 'CHOZ2xjpjh8TBibLf8K0rai6O9uUoPcacydKHobg', 'principalOrgId': None, 'cognitoAuthenticationType': None, 'userArn': None, 'apiKeyId': 'pksabr5yp5', 'userAgent': 'axios/0.21.1', 'accountId': None, 'caller': None, 'sourceIp': '54.194.244.111', 'accessKey': None, 'cognitoAuthenticationProvider': None, 'user': None}, 'domainName': 'igdlr449lh.execute-api.us-east-1.amazonaws.com', 'apiId': 'igdlr449lh'}, 'body': '[{"name":"All low","priority":"low","severities":[4,5,6]},{"name":"Policy Creation test new","priority":"medium","severities":[1,2,3]}]', 'isBase64Encoded': False}
    context = {}
    tcowatchdog.TcoWatchDog().main(event, context)
    