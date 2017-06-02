import json

import boto3
import sys
import socket
import ipwhois
import time
import whois
import requests
import os
from netaddr import *
import pprint
from ipwhois import *

# AAAS-4574-deploy-services-needs-to-have-a

def test():
    for i in range(0, 30):
        while True:
            try:
                print(i/0)
            except:
                print("lalala", i)
            break
        if i==29:
            print("Too many requests. Limit is 30 times")







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
                if d['CidrIp'] != '0.0.0.0/0':
                    # d['CidrIp'] = '216.70.7.11/32'
                    print('Inbound IP Ranges:', d['CidrIp'])
                    print('All the IPs:')
                    xz = d['CidrIp']
                    ips = IPNetwork(xz)
                    print('!!!!!!!!!!!!!!!!!!!')
                    print(ips.ip)
                    obj = IPWhois(ips.ip)
                    results = obj.lookup_rdap(depth=1)
                    pp = pprint.PrettyPrinter(indent=2)
                    print('Whois results: ', pp.pprint(results))
                    print('OLOLOLOLO')
                else:
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
                    ni_responce = ''.join(['Instance is Running. Public IP:', i['Association']['PublicIp']])
            else:
                ni_responce = 'Instance is not running'
    return ni_responce


# network_interfaces('i-0c803ff127917a6df')


def run_scan():
    # s3 = boto3.resource('s3')
    client = boto3.client('ec2', region_name='us-west-2')
    response = client.describe_instances(
        DryRun=False,
        InstanceIds=[],
        Filters=[],
    )
    case_list1 = []
    case_list2 = []
    for_email = []
    info1 = []
    for r in response['Reservations']:
        for i in r['Instances']:
            info1 = ['\n', 'Instance name: ', i['InstanceId'], 'Type:', i['InstanceType'], 'Image ID:', i['ImageId'], '\n', network_interfaces(i['InstanceId']), '\n', '==============']
            for_email.append(info1)
            case1 = i['InstanceId']
            case_list1.append(case1)
            case2 = i['InstanceType']
            case_list2.append(case2)
            # inst_id_dict = {'InstanceId': i['InstanceId'], 'InstanceType': i['InstanceType']}
            # inst_id_dict.update({'InstanceId': i['InstanceId'], 'InstanceType': i['InstanceType']})
            for b in i['SecurityGroups']:
                print('Security group name: ', b['GroupName'], 'Group ID: ', b['GroupId'])
                sg_info(b['GroupId'])
                print('==============')
            # dict1 = zip(case_list1, case_list2)
            # for case_list1, case_list2 in dict1:
            #     print(case_list1, case_list2)
            # return dict1
            # json1 = json.dump({"InstanceId": i['InstanceId'], "InstanceType": i['InstanceType'], }, sort_keys=True,
            #                   indent=4, separators=(',', ': '), fp=f_json)

    for_db = json.dumps({"InstanceId": case_list1, "InstanceType": case_list2}, sort_keys=False,
                           indent=4, separators=(',', ': '))
    message = ''
    client = boto3.client("ses")
    for i in for_email:
        # ''.join(list(i[7]))
        ii = ''.join(list(i))
        message += ii
    # message = repr(for_email)
    print(message)
    info = 'Email Address			aws-acs-prod@entrustdatacard.com,\nAWS AccountId: 771749627727,\nSubmitterName: ' \
           'Howard Wang,\nCompanyName: EntrustDatacard Corp,' \
           '\nEmailAddress: howard.wang@entrustdatacard.com,\n AdditionalEmail1: Duncan.Stirling@entrust.com, ' \
           '\n AdditionalEmail2#: tim.clarke@entrust.com \n'
    rowMess = 'From: AndreyMakarov@coherentsolutions.com\nTo: AndreyMakarov@coherentsolutions.com\nSubject: Your AWS Penetration Testing Inquiry\nMIME-Version: 1.0\n\n{0}\n{1}\n\nBandwidth\t\t\t1\nRegion\t\t    \tVirginia\nTimezone\t\t\tgmt--3\nStartDate\t\t\t\nEndDate\t\t\t\nComments\t\t\t\nTermsAgreement\t\t\ti-agree\nPolicy\t    \t\ti-agree\nAWS Account ID\t\t\t771749627727\nAWS Account ID\t\t\t771749627727\nIAM Account\t\t\tNo\nEmail Address\t\t\taws-acs-prod@entrustdatacard.com\nName\t\t\tacs_production '.format(
        info, message)

    response = client.send_raw_email(
        Destinations=[
        ],
        FromArn='',
        RawMessage={
            'Data': rowMess,
        },
        SourceArn='arn:aws:ses:us-west-2:242906888793:identity/AndreyMakarov@coherentsolutions.com',
    )

    print(response)

    return for_db


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
