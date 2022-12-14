'''import json
import urllib.parse
import boto3
import io
import gzip

print('Loading function')

s3 = boto3.resource('s3')


def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    obj=s3.Object(bucket,key)
    #print(obj.get()['BODY'])
    #print(key)
    #bucket="aws-cloudtrail-logs-881731855274-a0e6075b"
    #key="AWSLogs/881731855274/CloudTrail/ap-south-1/2021/12/23/881731855274_CloudTrail_ap-south-1_20211223T0530Z_mukjLm6uIEafCS0D.json.gz"
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        #print("CONTENT TYPE: " + response['ContentType'])
        #return response
        content = response['Body'].read()
        with gzip.GzipFile(fileobj=io.BytesIO(content), mode='rb') as fh:
            event_json = json.load(fh)
            output_dict = [record for record in event_json['Records']]
        return(output_dict)
    except Exception as e:
        print(e)
        #print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e

'''
import json
import boto3
import gzip
import urllib.parse

def lambda_handler(event, context):
    #message = event['Records'][0]['s3']['bucket']['name']
    # print(event)
    #key=event['detail']['requestParameters']['key']
    # print(key)
    
    
    
   
    #bucket_name = event['detail']['requestParameters']['bucketName']
    # # print(bucket_name)
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    s3 = boto3.resource("s3")
    obj = s3.Object(bucket, key)
    with gzip.GzipFile(fileobj=obj.get()["Body"]) as gzipfile:
        
        
        content = gzipfile.read()
        print(content)
    
    print("got access from 1318")
    
    