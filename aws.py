import re


import boto3

# for key in sorter:
#     print(key, bigrams[key])

s3 = boto3.resource('s3')

client = boto3.client('ec2')

response = client.describe_instances(
    DryRun=False,
    InstanceIds=[],
    Filters=[],
)

import sys
import socket
import ipwhois


def who(addr):
    # Не юзается "встроенная" whois, тк на unix она встроенная, на винде, говорят, нет
    r = requests.post("http://www.ripn.net/nic/whois/whois.cgi", {'Whois': addr.site, 'Host': 'whois.ripn.net'},
                      headers=addr.headers, allow_redirects=True, ).text.split('(in English).\n')[1].split('</PRE>')[
        0].strip()
    # http://www.ripn.net/about/servpol.html
    if 'You have exceeded allowed connection rate.' in r:
        return 'Вы сделали больше 30 запросов в минуту (лимит). Попробуйте позже'
    elif 'You are not allowed to connect' in r:
        return 'Вы в течении 15 минут превышали лимит (30 запросов в минуту). Восстановление доступа будет ' \
               'не менее, чем через час'
    else:
        return re.compile(r'<.*?>').sub('', r)
addr = '172.15.1.0/24'
who(addr)



def sg_info(sg):
    response_SG = client.describe_security_groups(
        DryRun=False,
        GroupNames=[],
        GroupIds=[
            sg,
        ],
        Filters=[]
    )
    print(response_SG['SecurityGroups'])
    for i in response_SG['SecurityGroups']:
        for c in i['IpPermissions']:
            try:
                print('IpPermissions.', 'From port: ', c['FromPort'], " To port: ", c['ToPort'])
            except:
                print('There are no Inbound rules')
            for d in c['IpRanges']:
                try:
                    print('Inbound IP Ranges:', d['CidrIp'])
                except:
                    print('There are no Inbound IP Ranges')
        for c in i['IpPermissionsEgress']:
            print('IpPermissionsEgress.', 'Protocol: ', c['IpProtocol'])
            try:
                print('From port', c['FromPort'], 'To port', c['ToPort'])
            except:
                print('There are no Outbound rules')
            for d in c['IpRanges']:
                try:
                    print('Outbound IP Ranges:', d['CidrIp'])
                except:
                    print('There are no Outbound IP Ranges')


def run_scan():
    dict_response = dict(response.get('ResponseMetadata'))
    for r in response['Reservations']:
        for i in r['Instances']:
            print('Instance name: ', i['InstanceId'])
            for b in i['SecurityGroups']:
                print('Security group name: ', b['GroupName'], 'Group ID: ', b['GroupId'])
                sg_info(b['GroupId'])
                print('==============')
# run_scan()

# new_bucket = 'amakarov-test'
# file_name = 'test'
# for bucket in s3.buckets.all():
#     a = list()
#     a.append(bucket.name)
#     for i in a:
#         print(i)




def create_bucket(new_bucket):
    for bucket in s3.buckets.all():
        if bucket.name == new_bucket:
            print('Bucket found. No need to create')
            break
        else:
            print("Creating new one")
            status = s3.create_bucket(Bucket=new_bucket, CreateBucketConfiguration={'LocationConstraint': 'us-west-1'})
            print(status)


def upload_file(file_name):
    try:
        f = open(file_name, 'r')
        f.close()
        print('File exists')
    except:
        print('there is no such file:', file_name)
    file_sent_status = s3.Object(new_bucket, file_name).put(Body=open(file_name, 'rb'))
    print('===================')
    print('Checking if file sent')
    sent_status = 2001
    dict_responce = dict(file_sent_status.get('ResponseMetadata'))
    for key, value in dict_responce.items():
        print(key, value)
    if dict_responce.get('HTTPStatusCode') == sent_status:
        print('Sent: Ok')
    else:
        print('Not sent')
    for key, value in dict_responce.get('HTTPHeaders').items():
        print(key, value)

# create_bucket(new_bucket)
# upload_file(file_name)






# # Upload a new file
# s3.Object('new_bucket', 'test').put(Body=open('test', 'rb'))
