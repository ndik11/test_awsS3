import json

import boto3
import sys
import socket
import ipwhois
import time
import whois
import requests
import os


# for key in sorter:
#     print(key, bigrams[key])


def sg_info(sg):
    client = boto3.client('ec2')
    response_SG = client.describe_security_groups(
        DryRun=False,
        GroupNames=[],
        GroupIds=[
            sg,
        ],
        Filters=[]
    )
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


def network_interfaces(instance):
    s3 = boto3.resource('s3')
    client = boto3.client('ec2')
    response = client.describe_instances(
        DryRun=False,
        InstanceIds=[
            instance,
        ],
        Filters=[],
    )
    for r in response['Reservations']:
        for k in r['Instances']:
            if k['State']['Name'] == 'running':
                for i in k['NetworkInterfaces']:
                    ni_responce = 'Instance is Running. Public IP:', i['Association']['PublicIp']
            else:
                ni_responce = 'Instance is not running'
    return ni_responce


# network_interfaces('i-0c803ff127917a6df')


def run_scan():
    s3 = boto3.resource('s3')
    client = boto3.client('ec2')
    response = client.describe_instances(
        DryRun=False,
        InstanceIds=[],
        Filters=[],
    )
    case_list1 = []
    case_list2 = []
    f_json = open('wow.json', 'w', encoding='utf-8')
    f = open('file.txt', 'w', encoding='utf-8')
    # inst_id_dict = {}.fromkeys(['InstanceId', 'InstanceType'])
    print('AWS AccountId 771749627727', '\n', file=f)
    print('SubmitterName Howard Wang', '\n', file=f)
    print('CompanyName Entrust Datacard Corp.', '\n', file=f)
    print('EmailAddress howard.wang@entrustdatacard.com', '\n', file=f)
    print('AdditionalEmail1 Duncan.Stirling@entrust.com', '\n', file=f)
    print('AdditionalEmail2# tim.clarke@entrust.com', '\n', file=f)
    # print(response)
    for r in response['Reservations']:
        for i in r['Instances']:
            print('Instance name: ', i['InstanceId'], 'Type:', i['InstanceType'], 'Image ID:', i['ImageId'], '\n', file=f)
            print(network_interfaces(i['InstanceId']), '\n', file=f)
            print('==============', file=f)
            case1 = i['InstanceId']
            case_list1.append(case1)
            case2 = i['InstanceType']
            case_list2.append(case2)
            # inst_id_dict = {'InstanceId': i['InstanceId'], 'InstanceType': i['InstanceType']}
            # inst_id_dict.update({'InstanceId': i['InstanceId'], 'InstanceType': i['InstanceType']})
            # for b in i['SecurityGroups']:
            #     print('Security group name: ', b['GroupName'], 'Group ID: ', b['GroupId'])
            #     sg_info(b['GroupId'])
            #     print('==============')
            # dict1 = zip(case_list1, case_list2)
            # for case_list1, case_list2 in dict1:
            #     print(case_list1, case_list2)
            # return dict1
            # json1 = json.dump({"InstanceId": i['InstanceId'], "InstanceType": i['InstanceType'], }, sort_keys=True,
            #                   indent=4, separators=(',', ': '), fp=f_json)

    # for i in case_list1:
    #     case3 = json.dump({"InstanceId": i},
    #                       indent=4, separators=(',', ': '), fp=f_json)
    #     for k in case_list2:
    #         case3 = json.dump({"InstanceType": k},
    #                        indent=4, separators=(',', ': '), fp=f_json)
    #         break
    case_list1 = json.dump({"InstanceId": case_list1, "InstanceType": case_list2}, sort_keys=True,
                           indent=4, separators=(',', ': '), fp=f_json)
    f.close()
    f_json.close()
    # print(case_list1)
    # print(case_list1, case_list2)
    return case_list1, case_list2


# run_scan()


def create_table():
    dynamodb = boto3.resource('dynamodb')
    response = dynamodb.create_table(
        AttributeDefinitions=[
            {
                'AttributeName': 'TimeStamp',
                'AttributeType': 'S',
            },
            {
                'AttributeName': 'InstanceId',
                'AttributeType': 'S',
            },
        ],
        KeySchema=[
            {
                'AttributeName': 'TimeStamp',
                'KeyType': 'HASH',
            },
            {
                'AttributeName': 'InstanceId',
                'KeyType': 'RANGE',
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5,
        },
        TableName='Instances',
    )
    print("Table status:", response.table_status)
# create_table()


def load_data():
    import json
    import decimal
    dynamodb = boto3.resource('dynamodb')
    import datetime
    my_time = str(datetime.datetime.now())
    print(my_time)
    table = dynamodb.Table('Instances')

    with open("wow.json") as json_file:
        opened_json = json.load(json_file, parse_float=decimal.Decimal)
        for i in opened_json['InstanceId']:
            InstanceId = i
            InstanceId = str(InstanceId)
            for k in opened_json['InstanceType']:
                InstanceType = k
                InstanceType = str(InstanceType)
            print("Adding InstanceId:", InstanceId, InstanceType)


            status = table.put_item(
                Item={
                    'TimeStamp': my_time,
                    'InstanceId': InstanceId,
                    'InstanceType': InstanceType,
                }
            )
            print(status)
load_data()



def send_11email():
    client = boto3.client("ses")
    f = open('file.txt', 'r', encoding='utf-8')
    message = f.read()
    rowMess = 'From: @.com\nTo: @\nSubject: Test ' \
              'email (contains an attachment)\nMIME-Version: 1.0\nContent-type: Multipart/Mixed; ' \
              'boundary="NextPart"\n\n--NextPart\nContent-Type: text/plain\n\n' + message \
              + '\n\n--NextPart\nContent-Type: text/plain;\nContent-Disposition: attachment; ' \
                'filename="attachment.txt"\n\nThis is the text in the attachment.\n\n--NextPart-- '

    response = client.send_raw_email(
        Destinations=[
        ],
        FromArn='',
        RawMessage={
            'Data': rowMess,
        },
        SourceArn='arn:aws:ses:us-west-2:2429:identity/@.com',
    )

    print(response)


# send_11email()


def create_bucket(new_bucket):
    s3 = boto3.resource('s3')
    for bucket in s3.buckets.all():
        if bucket.name == new_bucket:
            print('Bucket found. No need to create')
            break
        else:
            print("Creating new one")
            status = s3.create_bucket(Bucket=new_bucket, CreateBucketConfiguration={'LocationConstraint': 'us-west-1'})
            print(status)


def upload_file(file_name):
    s3 = boto3.resource('s3')
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
