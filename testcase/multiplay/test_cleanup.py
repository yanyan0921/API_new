from testcase.multiplay.default import Default
from testcase.multiplay.exec_request import ExecRequest
from testcase.multiplay.objects import object_controller
from testcase.multiplay.objects.fleet import Fleet
from testcase.multiplay.objects.instance_type import InstanceType
from testcase.multiplay.objects.region import Region


def test_cleanup_fleet_region():
    resp = ExecRequest.send_request('get', Default.fleet_url, None, None)
    for fleet in resp.json()['fleets']:
        if str(Fleet(fleet).name).startswith('test-'):
            resp1 = ExecRequest.send_request('get', Default.fleet_region_url + '/' + Fleet(fleet).id + '/regions', None,
                                             None)
            for fleet_region in resp1.json()['fleetRegionVos']:
                if fleet_region['regionName'].startswith('test-'):
                    object_controller.delete_fleet_region(fleet_region['id'])


def test_cleanup_fleet():
    resp = ExecRequest.send_request('get', Default.fleet_url, None, None)
    for fleet in resp.json()['fleets']:
        if str(Fleet(fleet).name).startswith('test-'):
            object_controller.delete_fleet(Fleet(fleet).id)


def test_cleanup_region():
    resp = ExecRequest.send_request('get', Default.region_url, None, None)
    for region in resp.json()['regions']:
        if str(Region(region).name).startswith('test-'):
            object_controller.delete_region(Region(region).id)


def test_cleanup_instance_type():
    resp = ExecRequest.send_request('get', Default.instance_type_url, None, None)
    for instance_type in resp.json()['instanceTypes']:
        if str(InstanceType(instance_type).name).startswith('test-'):
            object_controller.delete_instance_type(InstanceType(instance_type).id)
