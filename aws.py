import boto3

# Let's use Amazon S3
s3 = boto3.resource('s3')
new_bucket = 'amakarov-test1'
file_name ='test'


def create_bucket(new_bucket):
    for bucket in s3.buckets.all():
        if bucket.name ==new_bucket:
            print 'Bucket found. No need to create'
            break
        else:
            print "Creating new one"
            s3.create_bucket(Bucket='new_bucket', CreateBucketConfiguration={'LocationConstraint': 'us-west-1'})


def upload_file(file_name):
    try:
        f = open(file_name,'r')
        f.close()
        print 'File exists'
    except:
        print 'there is no such file:', file_name
    file_sent_status = s3.Object(new_bucket, file_name).put(Body=open(file_name, 'rb'))
    print '==================='
    print 'Checking if file sent'
    sent_status = 200
    dict_responce = dict(file_sent_status.get('ResponseMetadata'))
    for key, value in dict_responce.items():
        print key, value
    if dict_responce.get('HTTPStatusCode') == sent_status:
        print 'Sent: Ok'
    else:
        print 'Not sent'



create_bucket(new_bucket)
upload_file(file_name)






# # Upload a new file
# s3.Object('new_bucket', 'test').put(Body=open('test', 'rb'))