from core import Remediate


@Remediate
def lambda_handler(session, restApiId):
    client = session.client('apigateway')
    print(f"Declaring API as private")
    client.update_rest_api(restApiId=restApiId,patchOperations=[{'op':'replace','path':'/endpointConfiguration/types/REGIONAL','value':'PRIVATE'}])
    print(f"Adding api policy to only allow traffic from VPCs")
    client.update_rest_api(restApiId=restApiId,patchOperations=[{'op':'replace','path':'/policy','value':'{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":"*","Action":"execute-api:Invoke","Resource":"arn:aws:execute-api:::/*"},{"Effect":"Deny","Principal":"*","Action":"execute-api:Invoke","Resource":"arn:aws:execute-api:::/*","Condition":{"StringNotEquals":{"aws:SourceVpce":""}}}]}'}])
    print('Auditing...')
    response=client.get_rest_api(restApiId=restApiId)
    if 'PRIVATE' not in response['endpointConfiguration']['types']:
        return False,'Remediation failed'
    print("Remediation Complete!")
    return True
