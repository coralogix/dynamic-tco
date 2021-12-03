import tcowatchdog
import utcresetter

def lambda_handler(event,context):
    if 'detail-type' in event:
        tcoresetter = utcresetter.UtcResetter()
        tcoresetter.main(event, context)
    else:
        tcosetter = tcowatchdog.TcoWatchDog()
        tcosetter.main(event, context)


if __name__ == "__main__":
    #event = {'resource': '/testing', 'path': '/testing', 'httpMethod': 'POST', 'headers': {'Accept': 'application/json, text/plain, */*', 'Content-Type': 'application/json', 'Host': 'igdlr449lh.execute-api.us-east-1.amazonaws.com', 'User-Agent': 'axios/0.21.1', 'X-Amzn-Trace-Id': 'Root=1-61a0ee68-596b607c4c64817277a65eff', 'x-api-key': 'CHOZ2xjpjh8TBibLf8K0rai6O9uUoPcacydKHobg', 'X-Forwarded-For': '54.194.244.111', 'X-Forwarded-Port': '443', 'X-Forwarded-Proto': 'https'}, 'multiValueHeaders': {'Accept': ['application/json, text/plain, */*'], 'Content-Type': ['application/json'], 'Host': ['igdlr449lh.execute-api.us-east-1.amazonaws.com'], 'User-Agent': ['axios/0.21.1'], 'X-Amzn-Trace-Id': ['Root=1-61a0ee68-596b607c4c64817277a65eff'], 'x-api-key': ['CHOZ2xjpjh8TBibLf8K0rai6O9uUoPcacydKHobg'], 'X-Forwarded-For': ['54.194.244.111'], 'X-Forwarded-Port': ['443'], 'X-Forwarded-Proto': ['https']}, 'queryStringParameters': None, 'multiValueQueryStringParameters': None, 'pathParameters': None, 'stageVariables': None, 'requestContext': {'resourceId': 'nps8r5', 'resourcePath': '/testing', 'httpMethod': 'POST', 'extendedRequestId': 'JaowZGmFoAMFjmQ=', 'requestTime': '26/Nov/2021:14:25:44 +0000', 'path': '/default/testing', 'accountId': '771039649440', 'protocol': 'HTTP/1.1', 'stage': 'default', 'domainPrefix': 'igdlr449lh', 'requestTimeEpoch': 1637936744716, 'requestId': '2489f10f-a52e-4328-a209-100ca508d4a5', 'identity': {'cognitoIdentityPoolId': None, 'cognitoIdentityId': None, 'apiKey': 'CHOZ2xjpjh8TBibLf8K0rai6O9uUoPcacydKHobg', 'principalOrgId': None, 'cognitoAuthenticationType': None, 'userArn': None, 'apiKeyId': 'pksabr5yp5', 'userAgent': 'axios/0.21.1', 'accountId': None, 'caller': None, 'sourceIp': '54.194.244.111', 'accessKey': None, 'cognitoAuthenticationProvider': None, 'user': None}, 'domainName': 'igdlr449lh.execute-api.us-east-1.amazonaws.com', 'apiId': 'igdlr449lh'}, 'body': '[{"appname":["app1"],"subsystem":[],"tcolevel":"low"},{"appname":["app1"],"subsystem":["sub1"],"tcolevel":"medium"},{"appname":["app2"],"subsystem":["sub2","sub3","sub4"],"tcolevel":"low"},{"appname":["app3","app4"],"subsystem":[],"tcolevel":"low"}]', 'isBase64Encoded': False}
    event = {'version': '0', 'id': '60b2a65a-a2b7-58a9-d613-9274d66263b4', 'detail-type': 'Scheduled Event', 'source': 'aws.events', 'account': '771039649440', 'time': '2021-12-03T21:30:37Z', 'region': 'us-east-1', 'resources': ['arn:aws:events:us-east-1:771039649440:rule/cron'], 'detail': {}}
    context = {}
    #tcowatchdog.TcoWatchDog().main(event, context)
    utcresetter.UtcResetter().main(event, context)