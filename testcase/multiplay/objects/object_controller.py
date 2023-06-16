from testcase.multiplay.default import Default
from testcase.multiplay.exec_request import ExecRequest
from testcase.multiplay.objects.fleet import Fleet
from testcase.multiplay.objects.fleet_region import FleetRegion
from testcase.multiplay.objects.fleet_region_provider import FleetRegionProvider
from testcase.multiplay.objects.image import Image
from testcase.multiplay.objects.instance_type import InstanceType
from testcase.multiplay.objects.profile import Profile
from testcase.multiplay.objects.region import Region


def create_instance_type():
    instance_type = InstanceType()
    resp = ExecRequest.send_request('post', Default.instance_type_url, {'Content-Type': 'application/json'},
                                    {'instanceType': instance_type.object2dict()})
    return InstanceType(resp.json()['instanceType'])


def update_instance_type(instance_type):
    resp = ExecRequest.send_request('put', Default.instance_type_url + '/' + instance_type.id,
                                    {'Content-Type': 'application/json'},
                                    {'instanceType': instance_type.object2dict()})
    return InstanceType(resp.json()['instanceType'])


def delete_instance_type(object_id):
    ExecRequest.send_request('delete', Default.instance_type_url + '/' + object_id, None, None)


def create_image():
    image = Image()
    resp = ExecRequest.send_request('post', Default.image_url, {'Content-Type': 'application/json'},
                                    {'image': image.object2dict()})
    return Image(resp.json()['image'])


def delete_image(object_id):
    ExecRequest.send_request('delete', Default.image_url + '/' + object_id, None, None)


def create_fleet(*args):
    fleet = Fleet(*args)
    resp = ExecRequest.send_request('post', Default.fleet_url, {'Content-Type': 'application/json'},
                                    {'fleet': fleet.object2dict()})
    return Fleet(resp.json()['fleet'])


def delete_fleet(object_id):
    ExecRequest.send_request('delete', Default.fleet_url + '/' + object_id, None, None)


def create_profile(*args):
    profile = Profile(*args)
    resp = ExecRequest.send_request('post', Default.profile_url, {'Content-Type': 'application/json'},
                                    {'profile': profile.object2dict()})
    return Profile(resp.json()['profile'])


def delete_profile(object_id):
    ExecRequest.send_request('delete', Default.profile_url + '/' + object_id, None, None)


def create_region(*args):
    region = Region(*args)
    resp = ExecRequest.send_request('post', Default.region_url, {'Content-Type': 'application/json'},
                                    {'region': region.object2dict()})
    return Region(resp.json()['region'])


def update_region(region):
    resp = ExecRequest.send_request('put', Default.region_url + '/' + region.id, {'Content-Type': 'application/json'},
                                    {'region': region.object2dict()})
    return Region(resp.json()['region'])


def delete_region(object_id):
    ExecRequest.send_request('delete', Default.region_url + '/' + object_id, None, None)


def create_fleet_region(*args):
    fleet_region = FleetRegion(*args)
    resp = ExecRequest.send_request('post', Default.fleet_region_url, {'Content-Type': 'application/json'},
                                    {'fleetRegion': fleet_region.object2dict()})
    return FleetRegion(resp.json()['fleetRegion'])


def delete_fleet_region(object_id):
    ExecRequest.send_request('delete', Default.fleet_region_url + '/' + object_id, None, None)


def create_fleet_region_provider(*args):
    fleet_region_provider = FleetRegionProvider(*args)
    resp = ExecRequest.send_request('post', Default.fleet_region_provider_url, {'Content-Type': 'application/json'},
                                    {'fleetRegionProvider': fleet_region_provider.object2dict()})
    return FleetRegionProvider(resp.json()['fleetRegionProvider'])


def delete_fleet_region_provider(object_id):
    ExecRequest.send_request('delete', Default.fleet_region_provider_url + '/' + object_id, None, None)
