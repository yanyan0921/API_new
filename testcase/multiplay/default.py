import base64
import random
import string

from testcase.multiplay.config.config_loader import ConfigLoader
from testcase.multiplay.config.property_loader import PropertyLoader


class Default:
    config_loader = ConfigLoader('multiplay')
    endpoint = config_loader.get_setting('endpoints', 'mp_endpoint')
    property_loader = PropertyLoader(config_loader.get_setting('additional', 'property_file'))
    master_token = property_loader.get_property('master_token')
    basic_access = property_loader.get_property('basic_access')
    basic_secret = property_loader.get_property('basic_secret')
    instance_type_url = endpoint + '/v1/fleet-manager/instance-types'
    image_url = endpoint + '/v1/fleet-manager/images'
    fleet_url = endpoint + '/v1/fleet-manager/fleets'
    profile_url = endpoint + '/v1/fleet-manager/profile'
    region_url = endpoint + '/v1/fleet-manager/regions'
    fleet_region_url = endpoint + '/v1/fleet-manager/fleet-regions'
    fleet_region_provider_url = endpoint + '/v1/fleet-manager/fleet-region-providers'
    allocation_url = endpoint + '/v1/allocator/fleets'
    reservation_url = endpoint + '/v1/allocator/reservation'

    @staticmethod
    def random_letters(rand_size=10):
        letters = string.ascii_letters
        return 'test-' + ''.join(random.choice(letters) for i in range(rand_size))

    @staticmethod
    def random_int(start=0, end=100):
        return random.randint(start, end)

    @staticmethod
    def get_basic_auth():
        userpass = Default.basic_access + ':' + Default.basic_secret
        encoded_u = base64.b64encode(userpass.encode()).decode()
        return {"Authorization": "Basic %s" % encoded_u}

    @staticmethod
    def get_master_auth():
        return {"Authorization-Internal": "Internal %s" % Default.master_token}
