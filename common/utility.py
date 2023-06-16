import getopt
import hashlib
import logging
import random
import string
import sys
import time
import base64
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA

import conf.config_parser as config_parser
import conf.property_parser as property_parser


def random_str(length, charset=None):
    if charset is None:
        charset = string.ascii_lowercase + string.digits
    return ''.join(random.choice(charset) for _ in range(length))


def random_mail():
    return 'silkcloudtest+' + random_str(20) + '@gmail.com'


def random_number(length, charset=None):
    if charset is None:
        charset = string.digits
    return ''.join(random.choice(charset) for _ in range(length))


def random_pwd():
    return random_str(4, string.ascii_uppercase) + random_str(4, string.ascii_lowercase) + random_str(4, string.digits)


def random_phone_number(length, charset=None):
    if charset is None:
        charset = string.digits
    pre_list = ['130', '131', '132', '133', '134', '135', '136', '137', '138', '139', '147', '150', '151', '152',
                '153', '155', '156', '157', '158', '159', '186', '187', '188']
    random_pre = random.choice(pre_list)
    number = ''.join(random.choice(charset) for i in range(length))
    return random_pre + number


def random_int(start, end):
    return random.randint(start, end)


def get_file_md5(data):
    md5 = hashlib.md5(data).hexdigest()
    return md5


def get_timestamp_millisecond():
    time_stamp = time.time()
    return int(round(time_stamp * 1000))


def get_signature(url, query_string, req_body, timestamp, dynamic_salt):
    md5_str = url
    if query_string is not None:
        md5_str = md5_str + query_string

    if req_body is not None:
        md5_str = md5_str + req_body

    md5_str = md5_str + str(timestamp) + dynamic_salt

    hl = hashlib.md5()
    hl.update(md5_str.encode())

    return hl.hexdigest()


# The following are about config reading
def get_env():
    env = ''
    try:
        # start from the 3rd parameter
        # pytest -q testcase/test_gamestart.py --alluredir ${WORKSPACE}/allure_report --env=migu -m daily
        opts, args = getopt.getopt(sys.argv, 'alluredir:env:-m-q', ['env=', 'alluredir=', 'm', 'q'])
    except getopt.GetoptError:
        sys.exit(1)

    for arg in args:
        if '-env=' in arg or '--env=' in arg:
            env = str(arg).split('=')[1]
            # if env.endswith("]"):
            #     env = env[0:env.index(']')]
            break

    if env == '':
        logging.info('No environment file is set, please double check')
        sys.exit(1)
    else:
        logging.info('The environment is ' + env)
        return env


def read_config():
    env = get_env()

    parser = config_parser.ConfigLoader(env)
    default_genesis_url = parser.get_setting('endpoint', 'defaultGenesisEndpoint')
    default_cloud_platform_url = parser.get_setting('endpoint', 'defaultCloudPlatformEndpoint')
    default_play_platform_url = parser.get_setting('endpoint', 'defaultPlayPlatformEndpoint')
    additional_properties = property_parser.parse(parser.get_setting('additionalProperties', 'path'))
    resource_file_path = parser.get_setting('additionalProperties', 'resourceFilePath')

    return default_genesis_url, default_cloud_platform_url, default_play_platform_url, additional_properties, \
        resource_file_path


def get_admin_user_name_password():
    env = get_env()
    parser = config_parser.ConfigLoader(env)
    additional_properties = property_parser.parse(parser.get_setting('additionalProperties', 'path'))
    return additional_properties.get('admin_user_name'), additional_properties.get('admin_user_pw')


def get_org_admin_user_name_password():
    env = get_env()
    parser = config_parser.ConfigLoader(env)
    additional_properties = property_parser.parse(parser.get_setting('additionalProperties', 'path'))

    logging.info(f"OrgAdminUser Name: {additional_properties.get('org_admin_name')} "
                 f"Password: {additional_properties.get('org_admin_pw')} "
                 f"OrgId: {additional_properties.get('org_id')}")

    return additional_properties.get('org_admin_name'), \
           additional_properties.get('org_admin_pw'),


def get_org_user_name_password():
    env = get_env()
    parser = config_parser.ConfigLoader(env)
    additional_properties = property_parser.parse(parser.get_setting('additionalProperties', 'path'))
    return additional_properties.get('org_user_name'), additional_properties.get('org_user_pw')


def get_encrypt_password(public_key, original_password):
    public_key = base64.b64decode(public_key)
    rsa_key = RSA.importKey(public_key)
    cipher_rsa = PKCS1_v1_5.new(rsa_key)
    encrypt_password = cipher_rsa.encrypt(original_password.encode('utf-8'))
    encrypt_password = base64.b64encode(encrypt_password).decode('utf-8')
    return encrypt_password


def get_pre_configured_org():
    env = get_env()
    parser = config_parser.ConfigLoader(env)
    additional_properties = property_parser.parse(parser.get_setting('additionalProperties', 'path'))
    return additional_properties.get('automation_org_admin'), additional_properties.get('automation_org_dev')


def get_pre_created_resource():
    env = get_env()
    parser = config_parser.ConfigLoader(env)
    additional_properties = property_parser.parse(parser.get_setting('additionalProperties', 'path'))
    resource_name = additional_properties.get("pre_created_resource_name")
    resource_type = additional_properties.get("pre_created_resource_type")
    spec_id = additional_properties.get("pre_created_resource_spec_id")
    return resource_name, int(resource_type), spec_id


def get_automation_org_admin():
    env = get_env()
    parser = config_parser.ConfigLoader(env)
    additional_properties = property_parser.parse(parser.get_setting('additionalProperties', 'path'))

    auto_org_admin = additional_properties.get("automation_org_admin")
    return auto_org_admin


def get_automation_org_dev():
    env = get_env()
    parser = config_parser.ConfigLoader(env)
    additional_properties = property_parser.parse(parser.get_setting('additionalProperties', 'path'))

    auto_org_dev = additional_properties.get("automation_org_dev")
    return auto_org_dev
