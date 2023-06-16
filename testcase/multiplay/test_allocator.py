import uuid

from testcase.multiplay.default import Default
from testcase.multiplay.exec_request import ExecRequest
from testcase.multiplay.objects import object_controller
from testcase.multiplay.objects.allocation import Allocation


def test_allocation():
    try:
        instance_type = object_controller.create_instance_type()
        instance_type.nameInProvider = 'tpl_gpu'
        object_controller.update_instance_type(instance_type)
        image = object_controller.create_image()
        fleet = object_controller.create_fleet(instance_type.id, image.id)
        profile = object_controller.create_profile(fleet.id)
        region = object_controller.create_region()
        region.nameInProvider = '5000'
        region.regionConfig = '{"Endpoint": "http://10.33.201.222:18229"}'
        object_controller.update_region(region)
        fleet_region = object_controller.create_fleet_region(fleet.id, region.id)
        # fleet_region_provider = object_controller.create_fleet_region_provider(fleet.id, region.id)

        fleet_region.minAvailableInstances = 1
        ExecRequest.send_request('put', Default.fleet_region_url + '/' + fleet_region.id,
                                 {'Content-Type': 'application/json'},
                                 {'fleetRegion': fleet_region.object2dict()})
        allocation_uuid = str(uuid.uuid4())
        resp = ExecRequest.send_request('post', Default.allocation_url + '/' + fleet.id + '/allocations',
                                        {'Content-Type': 'application/json'},
                                        {'uuid': allocation_uuid, 'regionId': region.id, 'profileId': profile.id})
        result = Allocation(resp.json()['allocation'])

        resp1 = ExecRequest.send_request('get',
                                         Default.allocation_url + '/' + result.fleetId +
                                         '/allocations/' + allocation_uuid, None, None)
        result1 = Allocation(resp1.json()['allocation'])
        assert result1.fleetId == result.fleetId

        resp2 = ExecRequest.send_request('get',
                                         Default.allocation_url + '/' + result.fleetId +
                                         '/allocations?pageSize=5',
                                         None, None)
        result2 = Allocation(resp2.json()['allocations'][0])
        assert result2.fleetId == result.fleetId
    finally:
        ExecRequest.send_request('delete', Default.allocation_url + '/' + result.fleetId +
                                 '/allocations/' + allocation_uuid, None, None)
        resp3 = ExecRequest.send_request('get',
                                         Default.allocation_url + '/' + result.fleetId +
                                         '/allocations', None, None)
        assert str(resp3.json()['totalCount']) == '0'
        fleet_region.minAvailableInstances = 0
        ExecRequest.send_request('put', Default.fleet_region_url + '/' + fleet_region.id,
                                 {'Content-Type': 'application/json'},
                                 {'fleetRegion': fleet_region.object2dict()})
        # object_controller.delete_fleet_region_provider(str(fleet_region_provider.id))
        object_controller.delete_fleet_region(fleet_region.id)
        object_controller.delete_region(region.id)
        object_controller.delete_profile(profile.id)
        object_controller.delete_fleet(fleet.id)
        object_controller.delete_image(image.id)
        object_controller.delete_instance_type(instance_type.id)


def test_reservation():
    try:
        instance_type = object_controller.create_instance_type()
        instance_type.nameInProvider = 'tpl_gpu'
        object_controller.update_instance_type(instance_type)
        image = object_controller.create_image()
        fleet = object_controller.create_fleet(instance_type.id, image.id)
        profile = object_controller.create_profile(fleet.id)
        region = object_controller.create_region()
        region.nameInProvider = '5000'
        region.regionConfig = '{"Endpoint": "http://10.33.201.222:18229"}'
        object_controller.update_region(region)
        fleet_region = object_controller.create_fleet_region(fleet.id, region.id)

        allocation_uuid = str(uuid.uuid4())
        resp1 = ExecRequest.send_request('post', Default.reservation_url, {'Content-Type': 'application/json'},
                                         {'uuid': allocation_uuid,
                                          'allocations': [
                                              {'fleetId': fleet.id, 'regionId': region.id, 'profileId': profile.id,
                                               'quantity': '1'}]})
        assert str(resp1.json()['status']) == 'Created'

        resp2 = ExecRequest.send_request('get', Default.reservation_url + '/' + allocation_uuid, None, None)
        if str(resp2.json()['status']) == 'Failed':
            ExecRequest.send_request('delete', Default.reservation_url + '/' + allocation_uuid, None, None, 400)
    finally:
        # ExecRequest.send_request('delete', Default.reservation_url + '/' + allocation_uuid, None, None)
        object_controller.delete_fleet_region(fleet_region.id)
        object_controller.delete_region(region.id)
        object_controller.delete_profile(profile.id)
        object_controller.delete_fleet(fleet.id)
        object_controller.delete_image(image.id)
        object_controller.delete_instance_type(instance_type.id)
