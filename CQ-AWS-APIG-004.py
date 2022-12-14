from urllib import response
from core import Remediate


@Remediate
def lambda_handler(session, restApiId,stageName):
    client = session.client('apigateway')
    print(f"Updating stage {stageName} for API {restApiId}")
    client.update_stage(restApiId=restApiId,stageName=stageName,patchOperations=[{"op":"replace","path":"/*/*/metrics/enabled","value":"true"}])
    print("Auditing...")
    try:
        response=client.get_stage(restApiId=restApiId,stageName=stageName)['methodSettings']['*/*']['metricsEnabled']
        if response==False:
            return False,'Remediation Failed'    
    except KeyError:
        return False,'Remediation Failed'
    print("Remediation Complete!")
    return True
