from __future__ import print_function
from awslimitchecker.checker import AwsLimitChecker
import boto3
import os

''' This function is to run the limitchecker api and alert on any limits which are seen to be close to their limits.
- The limitchecker has several drawbacks. We can't check all the limits due Amazon don't have API to check almost 60% of them. So now we check just the limits that can be validated through API or Trusted Advisor API.
- The variables below are set when the lambda function is run.
'''
print('Loading function')
#email to send from
email_from = os.environ['email_from']
#email send to
email_to = os.environ['email_to']
#arn to send from
email_from_arn = os.environ['email_from_arn']
#list of emails
email_cc_for_case = os.environ['email_cc_for_case']

def lambda_handler(event, context):
    limit_checker()


def limit_checker():
    c = AwsLimitChecker()
    result = c.check_thresholds()
    warning_message = ''
    critical_message = ''

    for service, svc_limits in result.items():
        for limit_name, limit in svc_limits.items():
            if (limit.api_limit is not None) or (limit.ta_limit is not None):
                for warn in limit.get_warnings():
                    warning_notice = ("\n{service} '{limit_name}' usage ({u}) exceeds "
                                      "warning threshold (limit={l})".format(
                            service=service,
                            limit_name=limit_name,
                            u=str(warn),
                            l=limit.get_limit(),
                        )
                    )
                    if limit.get_limit() < 100:
                        warning_message += ''.join(list(warning_notice)) + " . Please raise it up to five times more\n"
                    elif limit.get_limit() < 1000:
                        warning_message += ''.join(list(warning_notice)) + ". Please raise it up to 50%\n"
                    elif limit.get_limit() > 1000:
                        warning_message += ''.join(list(warning_notice)) + ". Please raise it up to 20%\n"

                for crit in limit.get_criticals():
                    if not crit:
                        have_critical = False
                        print(have_critical)
                    critical_notice = ("{service} '{limit_name}' usage ({u}) exceeds "
                                       "critical threshold (limit={l})".format(
                            service=service,
                            limit_name=limit_name,
                            u=str(crit),
                            l=limit.get_limit(),
                        )
                    )
                    if limit.get_limit() < 100:
                        critical_message += ''.join(list(critical_notice)) + ". Please raise it up to five times more\n"
                    elif limit.get_limit() < 1000:
                        critical_message += ''.join(list(critical_notice)) + ". Please raise it up to 50%\n"
                    elif limit.get_limit() > 1000:
                        critical_message += ''.join(list(critical_notice)) + ". Please raise it up to 20%\n"


    print("WARNING MESSAGE:", warning_message, "CRITICAL MESSAGE:\n", critical_message)
    if len(critical_message) > 10:
        print('Critical found')
        case_id = case_creation(warning_message, critical_message)
        email_send(case_id, warning_message, critical_message)
    else:
        print("No limit criticals")


def case_creation(warning_message, critical_message):
    client_support = boto3.client('support')
    response = client_support.create_case(
        subject='Limits',
        serviceCode='aws-identity-and-access-management',
        severityCode='low',
        categoryCode='other',
        communicationBody='Hello\n' + warning_message + critical_message,
        ccEmailAddresses=[
            ''+ email_cc_for_case
        ],
        language='en',
        issueType='customer-service',
    )
    case_id = response['caseId']
    print(case_id, response['caseId'])
    return case_id




# email!!!!!!!!!!!!!!!!!!!!!!!!!!
def email_send(case_id, warning_message, critical_message):
    client = boto3.client("ses")
    info = 'We have some warnings:  '
    case_created = '\nCase#' + case_id
    rowMess = 'From: {0}\nTo: {1}'.format(email_from, email_to) + '\nSubject: AWS limits checker' \
              'check\nMIME-Version: 1.0\n\n' + info + warning_message + critical_message + case_created
    response = client.send_raw_email(
        Destinations=[
        ],
        FromArn='',
        RawMessage={
            'Data': rowMess,
        },
        SourceArn='' + email_from_arn,
    )
    print('Email info:', response)
