import pytest

from testcase.multiplay.default import Default
from testcase.multiplay.exec_request import ExecRequest
from testcase.multiplay.objects import object_controller
from testcase.multiplay.objects.fleet import Fleet
from testcase.multiplay.objects.fleet_log_collector_config import FleetLogCollectorConfig
from testcase.multiplay.objects.fleet_region import FleetRegion
from testcase.multiplay.objects.fleet_region_provider import FleetRegionProvider
from testcase.multiplay.objects.image import Image
from testcase.multiplay.objects.instance_type import InstanceType
from testcase.multiplay.objects.profile import Profile
from testcase.multiplay.objects.region import Region


# POST   /v1/fleet-manager/instance-types
# PUT    /v1/fleet-manager/instance-types/{id}
# GET    /v1/fleet-manager/instance-types/{id}
# GET    /v1/fleet-manager/instance-types
# DELETE /v1/fleet-manager/instance-types/{id}
def test_instance_type():
    try:
        instance_type_url = Default.instance_type_url
        instance_type = InstanceType()
        resp = ExecRequest.send_request('post', instance_type_url,
                                        {'Content-Type': 'application/json'},
                                        {'instanceType': instance_type.object2dict()})
        result = InstanceType(resp.json()['instanceType'])
        assert result.name == instance_type.name
        # assert result.createdBy == instance_type.createdBy
        assert not result.isDeleted

        new_name = Default.random_letters()
        new_name_in_provider = Default.random_letters()
        new_cpu_type = Default.random_letters()
        new_cores = Default.random_int(8, 12)
        new_cpu_frequency = Default.random_int(4000, 5000)
        new_ram = str(Default.random_int(9000, 10000))
        new_network_bandwidth = Default.random_int(2000, 3000)
        new_gpu_type = Default.random_letters()
        modified = Default.random_letters()
        result.name = new_name
        result.nameInProvider = new_name_in_provider
        result.cpuType = new_cpu_type
        result.cores = new_cores
        result.cpuFrequency = new_cpu_frequency
        result.ram = new_ram
        result.networkBandwidth = new_network_bandwidth
        result.gpuType = new_gpu_type
        result.modifiedBy = modified
        resp1 = ExecRequest.send_request('put', instance_type_url + '/' + result.id,
                                         {'Content-Type': 'application/json'},
                                         {'instanceType': result.object2dict()})
        result1 = InstanceType(resp1.json()['instanceType'])
        assert result1.name == new_name
        assert result1.nameInProvider == new_name_in_provider
        assert result1.cpuType == new_cpu_type
        assert result1.cores == new_cores
        assert result1.cpuFrequency == new_cpu_frequency
        assert result1.ram == new_ram
        assert result1.networkBandwidth == new_network_bandwidth
        assert result1.gpuType == new_gpu_type
        # assert result1.createdBy == instance_type.createdBy
        # assert result1.modifiedBy == modified
        assert not result1.isDeleted

        resp2 = ExecRequest.send_request('get', instance_type_url + '/' + result.id, None, None)
        result2 = InstanceType(resp2.json()['instanceType'])
        assert result2.name == new_name
        assert result2.nameInProvider == new_name_in_provider
        assert result2.cpuType == new_cpu_type
        assert result2.cores == new_cores
        assert result2.cpuFrequency == new_cpu_frequency
        assert result2.ram == new_ram
        assert result2.networkBandwidth == new_network_bandwidth
        assert result2.gpuType == new_gpu_type
        # assert result2.createdBy == instance_type.createdBy
        # assert result2.modifiedBy == modified
        assert not result2.isDeleted

        resp3 = ExecRequest.send_request('get', instance_type_url, None, None)
        result3 = None
        for temp in resp3.json()['instanceTypes']:
            if InstanceType(temp).id == result.id:
                result3 = InstanceType(temp)
        assert result3 is not None
        assert result3.name == new_name
        assert result3.nameInProvider == new_name_in_provider
        assert result3.cpuType == new_cpu_type
        assert result3.cores == new_cores
        assert result3.cpuFrequency == new_cpu_frequency
        assert result3.ram == new_ram
        assert result3.networkBandwidth == new_network_bandwidth
        assert result3.gpuType == new_gpu_type
        # assert result3.createdBy == instance_type.createdBy
        # assert result3.modifiedBy == modified
        assert not result3.isDeleted
    finally:
        ExecRequest.send_request('delete', instance_type_url + '/' + resp.json()['instanceType']['id'], None, None)
        resp4 = ExecRequest.send_request('get', instance_type_url + '/' + result.id, None, None)
        result4 = InstanceType(resp4.json()['instanceType'])
        assert result4.name == new_name
        assert result4.nameInProvider == new_name_in_provider
        assert result4.cpuType == new_cpu_type
        assert result4.cores == new_cores
        assert result4.cpuFrequency == new_cpu_frequency
        assert result4.ram == new_ram
        assert result4.networkBandwidth == new_network_bandwidth
        assert result4.gpuType == new_gpu_type
        # assert result4.createdBy == instance_type.createdBy
        # assert result4.modifiedBy == modified
        assert result4.isDeleted


# POST   /v1/fleet-manager/images
# PUT    /v1/fleet-manager/images/{id}
# GET    /v1/fleet-manager/images/{id}
# GET    /v1/fleet-manager/images
# DELETE /v1/fleet-manager/images/{id}
def test_image():
    try:
        image_url = Default.image_url
        image = Image()
        resp = ExecRequest.send_request('post', image_url, {'Content-Type': 'application/json'},
                                        {'image': image.object2dict()})
        result = Image(resp.json()['image'])
        assert result.name == image.name
        # assert result.createdBy == image.createdBy
        assert not result.isDeleted

        new_name = Default.random_letters()
        new_os = Default.random_letters()
        new_size = str(Default.random_int(60, 80))
        modified = Default.random_letters()
        result.name = new_name
        result.os = new_os
        result.size = new_size
        result.modifiedBy = modified
        resp1 = ExecRequest.send_request('put', image_url + '/' + result.id, {'Content-Type': 'application/json'},
                                         {'image': result.object2dict()})
        result1 = Image(resp1.json()['image'])
        assert result1.name == new_name
        assert result1.os == new_os
        assert result1.size == new_size
        # assert result1.modifiedBy == modified
        assert not result1.isDeleted

        resp2 = ExecRequest.send_request('get', image_url + '/' + result.id, None, None)
        result2 = Image(resp2.json()['image'])
        assert result2.name == new_name
        assert result2.os == new_os
        assert result2.size == new_size
        # assert result2.createdBy == result.createdBy
        # assert result2.modifiedBy == modified
        assert not result2.isDeleted

        resp3 = ExecRequest.send_request('get', image_url, None, None)
        result3 = None
        for temp in resp3.json()['images']:
            if Image(temp).id == result.id:
                result3 = Image(temp)
        assert result3 is not None
        assert result3.name == new_name
        assert result3.os == new_os
        assert result3.size == new_size
        # assert result3.createdBy == result.createdBy
        # assert result3.modifiedBy == modified
        assert not result3.isDeleted
    finally:
        ExecRequest.send_request('delete', image_url + '/' + resp.json()['image']['id'], None, None)
        resp4 = ExecRequest.send_request('get', image_url + '/' + result.id, None, None)
        result4 = Image(resp4.json()['image'])
        assert result4.name == new_name
        assert result4.os == new_os
        assert result4.size == new_size
        # assert result4.createdBy == result.createdBy
        # assert result4.modifiedBy == modified
        assert result4.isDeleted


# POST   /v1/fleet-manager/fleets
# PUT    /v1/fleet-manager/fleets/{id}
# GET    /v1/fleet-manager/fleets/{id}
# GET    /v1/fleet-manager/fleets
# GET    /v1/fleet-manager/fleets/{id}/view
# DELETE /v1/fleet-manager/fleets/{id}
def test_fleet():
    try:
        instance_type = object_controller.create_instance_type()
        image = object_controller.create_image()

        fleet_url = Default.fleet_url
        fleet = Fleet()
        fleet.instanceTypeId = instance_type.id
        fleet.imageId = image.id
        resp = ExecRequest.send_request('post', fleet_url, {'Content-Type': 'application/json'},
                                        {'fleet': fleet.object2dict()})
        result = Fleet(resp.json()['fleet'])
        assert result.name == fleet.name
        # assert result.createdBy == fleet.createdBy
        assert not result.isDeleted

        new_name = Default.random_letters()
        instance_type1 = object_controller.create_instance_type()
        image1 = object_controller.create_image()
        new_min_available_instances = 2
        new_max_instances = 3
        modified = Default.random_letters()
        result.name = new_name
        result.instanceTypeId = instance_type1.id
        result.imageId = image1.id
        result.minAvailableInstances = new_min_available_instances
        result.maxInstances = new_max_instances
        result.modifiedBy = modified
        resp1 = ExecRequest.send_request('put', fleet_url + '/' + result.id, {'Content-Type': 'application/json'},
                                         {'fleet': result.object2dict()})
        result1 = Fleet(resp1.json()['fleet'])
        assert result1.name == new_name
        assert result1.instanceTypeId == instance_type1.id
        assert result1.imageId == image1.id
        assert result1.minAvailableInstances == new_min_available_instances
        assert result1.maxInstances == new_max_instances
        # assert result1.modifiedBy == modified
        assert not result1.isDeleted

        resp2 = ExecRequest.send_request('get', fleet_url + '/' + result.id, None, None)
        result2 = Fleet(resp2.json()['fleet'])
        assert result2.name == new_name
        assert result2.instanceTypeId == instance_type1.id
        assert result2.imageId == image1.id
        assert result2.minAvailableInstances == new_min_available_instances
        assert result2.maxInstances == new_max_instances
        # assert result2.modifiedBy == modified
        assert not result2.isDeleted

        resp3 = ExecRequest.send_request('get', fleet_url, None, None)
        result3 = None
        for temp in resp3.json()['fleets']:
            if Fleet(temp).id == result.id:
                result3 = Fleet(temp)
        assert result3 is not None
        assert result3.name == new_name
        assert result3.instanceTypeId == instance_type1.id
        assert result3.imageId == image1.id
        assert result3.minAvailableInstances == new_min_available_instances
        assert result3.maxInstances == new_max_instances
        # assert result3.modifiedBy == modified
        assert not result3.isDeleted

        resp4 = ExecRequest.send_request('get', fleet_url + '/' + result.id + '/view', None, None)
        resp4_fleet_vo_dict = resp4.json()['fleetVo']
        assert resp4_fleet_vo_dict['id'] == result1.id
        assert resp4_fleet_vo_dict['name'] == result1.name
        assert resp4_fleet_vo_dict['minAvailableInstances'] == result1.minAvailableInstances
        assert resp4_fleet_vo_dict['maxInstances'] == result1.maxInstances
        assert resp4_fleet_vo_dict['createdBy'] == result1.createdBy
        assert resp4_fleet_vo_dict['modifiedBy'] == result1.modifiedBy
        resp4_instance_type = InstanceType(resp4.json()['fleetVo']['instanceType'])
        assert resp4_instance_type.id == instance_type1.id
        assert resp4_instance_type.name == instance_type1.name
        assert resp4_instance_type.nameInProvider == instance_type1.nameInProvider
        assert resp4_instance_type.cpuType == instance_type1.cpuType
        assert resp4_instance_type.cores == instance_type1.cores
        assert resp4_instance_type.cpuFrequency == instance_type1.cpuFrequency
        assert resp4_instance_type.ram == instance_type1.ram
        assert resp4_instance_type.networkBandwidth == instance_type1.networkBandwidth
        assert resp4_instance_type.gpuType == instance_type1.gpuType
        # assert resp4_instance_type.createdBy == instance_type1.createdBy
        # assert resp4_instance_type.modifiedBy == instance_type1.modifiedBy
        resp4_image = Image(resp4.json()['fleetVo']['image'])
        assert resp4_image.id == image1.id
        assert resp4_image.name == image1.name
        assert resp4_image.nameInProvider == image1.nameInProvider
        assert resp4_image.os == image1.os
        assert resp4_image.size == image1.size
        # assert resp4_image.createdBy == image1.createdBy
        # assert resp4_image.modifiedBy == image1.modifiedBy
    finally:
        ExecRequest.send_request('delete', fleet_url + '/' + resp.json()['fleet']['id'], None, None)
        resp5 = ExecRequest.send_request('get', fleet_url + '/' + result.id, None, None)
        result5 = Fleet(resp5.json()['fleet'])
        assert result5.name == new_name
        assert result5.instanceTypeId == instance_type1.id
        assert result5.imageId == image1.id
        assert result5.minAvailableInstances == new_min_available_instances
        assert result5.maxInstances == new_max_instances
        # assert result5.modifiedBy == modified
        assert result5.isDeleted
        object_controller.delete_instance_type(instance_type1.id)
        object_controller.delete_instance_type(instance_type.id)
        object_controller.delete_image(image1.id)
        object_controller.delete_image(image.id)


# POST   /v1/fleet-manager/profile
# PUT    /v1/fleet-manager/profile/{profile.id}
# GET    /v1/fleet-manager/{fleetId}/profiles
# DELETE /v1/fleet-manager/profile/{id}
def test_profile():
    try:
        instance_type = object_controller.create_instance_type()
        image = object_controller.create_image()
        fleet = object_controller.create_fleet(instance_type.id, image.id)

        profile_url = Default.profile_url
        profile = Profile(fleet.id)
        resp1 = ExecRequest.send_request('post', profile_url, {'Content-Type': 'application/json'},
                                         {'profile': profile.object2dict()})
        result1 = Profile(resp1.json()['profile'])
        assert result1.name == profile.name
        assert result1.workingDir == profile.workingDir
        assert result1.binaryName == profile.binaryName
        assert result1.binaryVersion == '0'
        assert result1.resourceAge == 0

        new_name = Default.random_letters()
        new_fleet = object_controller.create_fleet(instance_type.id, image.id)
        new_working_dir = Default.random_letters()
        new_binary_name = Default.random_letters()
        new_arguments = Default.random_letters()
        new_binary_location = Default.random_letters()
        new_binary_version = Default.random_int()
        new_port = str(Default.random_int())
        new_log_path = Default.random_letters()
        modified = Default.random_letters()
        result1.name = new_name
        result1.fleetId = new_fleet.id
        result1.workingDir = new_working_dir
        result1.binaryName = new_binary_name
        result1.arguments = new_arguments
        result1.binaryLocation = new_binary_location
        result1.binaryVersion = new_binary_version
        result1.port = new_port
        result1.logPath = new_log_path
        result1.modifiedBy = modified
        resp2 = ExecRequest.send_request('put', profile_url + '/' + result1.id, {'Content-Type': 'application/json'},
                                         {'profile': result1.object2dict()})
        result2 = Profile(resp2.json()['profile'])
        assert result2.name == new_name
        assert result2.fleetId == fleet.id
        assert result2.workingDir == new_working_dir
        assert result2.binaryName == new_binary_name
        assert result2.arguments == new_arguments
        assert result2.binaryLocation == new_binary_location
        assert result2.binaryVersion != new_binary_version
        assert result2.binaryVersion == '1'
        assert result2.port == new_port
        assert result2.logPath == new_log_path
        # assert result2.modifiedBy == modified
        assert result2.resourceAge == 1

        resp3 = ExecRequest.send_request('get', profile_url + '/' + result2.id, None, None)
        result3 = Profile(resp3.json()['profile'])
        assert result3.name == new_name
        assert result3.fleetId == fleet.id
        assert result3.workingDir == new_working_dir
        assert result3.binaryName == new_binary_name
        assert result3.arguments == new_arguments
        assert result3.binaryLocation == new_binary_location
        assert result3.binaryVersion != new_binary_version
        assert result3.binaryVersion == '1'
        assert result3.port == new_port
        assert result3.logPath == new_log_path
        # assert result3.modifiedBy == modified
        assert result3.resourceAge == 1

        new_name1 = Default.random_letters()
        modified1 = Default.random_letters()
        result3.name = new_name1
        result3.modifiedBy = modified1
        resp4 = ExecRequest.send_request('put', profile_url + '/' + result3.id, {'Content-Type': 'application/json'},
                                         {'profile': result3.object2dict()})
        result4 = Profile(resp4.json()['profile'])
        assert result4.name == new_name1
        assert result4.fleetId == fleet.id
        assert result4.workingDir == new_working_dir
        assert result4.binaryName == new_binary_name
        assert result4.arguments == new_arguments
        assert result4.binaryLocation == new_binary_location
        assert result4.binaryVersion != new_binary_version
        assert result4.binaryVersion == '1'
        assert result4.port == new_port
        assert result4.logPath == new_log_path
        # assert result4.modifiedBy == modified1
        assert result4.resourceAge == 2

        resp5 = ExecRequest.send_request('get', Default.endpoint + '/v1/fleet-manager/' + fleet.id + '/profiles',
                                         None, None)
        result5 = Profile(resp5.json()['profiles'][0])
        assert result5.name == new_name1
        assert result5.fleetId == fleet.id
        assert result5.workingDir == new_working_dir
        assert result5.binaryName == new_binary_name
        assert result5.arguments == new_arguments
        assert result5.binaryLocation == new_binary_location
        assert result5.binaryVersion != new_binary_version
        assert result5.binaryVersion == '1'
        assert result5.port == new_port
        assert result5.logPath == new_log_path
        # assert result5.modifiedBy == modified1
        assert result5.resourceAge == 2

        '''ExecRequest.send_request('post', Default.profile_url + '/' + result4.id + '/binary/rollout',
                                 {'Content-Type': 'application/json'},
                                 {'version': '0'})
        ExecRequest.send_request('get', Default.profile_url + '/binary/updates?profileId=' + result4.id, None, None)
        ExecRequest.send_request('put', Default.profile_url + '/' + result4.id + '/binary',
                                 {'Content-Type': 'application/json'},
                                 {'binaryLocation': Default.random_letters(), 'rollout': result4.keepAlive,
                                  'resourceAge': result4.resourceAge})'''
    finally:
        ExecRequest.send_request('delete', profile_url + '/' + resp1.json()['profile']['id'], None, None)
        resp6 = ExecRequest.send_request('get', Default.endpoint + '/v1/fleet-manager/' + fleet.id + '/profiles',
                                         None, None)
        assert len(resp6.json()['profiles']) == 0
        object_controller.delete_fleet(new_fleet.id)
        object_controller.delete_fleet(fleet.id)
        object_controller.delete_image(image.id)
        object_controller.delete_instance_type(instance_type.id)


# POST   /v1/fleet-manager/regions
# PUT    /v1/fleet-manager/regions/{id}
# GET    /v1/fleet-manager/regions/{id}
# GET    /v1/fleet-manager/regions
# DELETE /v1/fleet-manager/regions/{id}
def test_region():
    try:
        url = Default.region_url
        region = Region()
        resp = ExecRequest.send_request('post', url, {'Content-Type': 'application/json'},
                                        {'region': region.object2dict()})
        result = Region(resp.json()['region'])
        assert result.name == region.name
        # assert result.createdBy == region.createdBy
        assert not result.isDeleted

        new_name = Default.random_letters()
        new_name_in_provider = Default.random_letters()
        new_region_config = Default.random_letters()
        modified = Default.random_letters()
        result.name = new_name
        result.nameInProvider = new_name_in_provider
        result.regionConfig = new_region_config
        result.modifiedBy = modified
        resp1 = ExecRequest.send_request('put', url + '/' + result.id, {'Content-Type': 'application/json'},
                                         {'region': result.object2dict()})
        result1 = Region(resp1.json()['region'])
        assert result1.name == new_name
        assert result1.nameInProvider == new_name_in_provider
        assert result1.regionConfig == new_region_config
        # assert result1.modifiedBy == modified
        assert not result1.isDeleted

        resp2 = ExecRequest.send_request('get', url + '/' + result.id, None, None)
        result2 = Region(resp2.json()['region'])
        assert result2.name == new_name
        assert result2.nameInProvider == new_name_in_provider
        assert result2.regionConfig == new_region_config
        # assert result2.modifiedBy == modified
        assert not result2.isDeleted

        resp3 = ExecRequest.send_request('get', url, None, None)
        result3 = None
        for temp in resp3.json()['regions']:
            if Region(temp).id == result.id:
                result3 = Region(temp)
        assert result3.name == new_name
        assert result3.nameInProvider == new_name_in_provider
        assert result3.regionConfig == new_region_config
        # assert result3.modifiedBy == modified
        assert not result3.isDeleted
    finally:
        ExecRequest.send_request('delete', url + '/' + resp.json()['region']['id'], None, None)
        resp4 = ExecRequest.send_request('get', url + '/' + result.id, None, None)
        result4 = Region(resp4.json()['region'])
        assert result4.name == new_name
        assert result4.nameInProvider == new_name_in_provider
        assert result4.regionConfig == new_region_config
        # assert result4.modifiedBy == modified
        assert result4.isDeleted


# POST   /v1/fleet-manager/fleet-regions
# PUT    /v1/fleet-manager/fleet-regions/{fleet_region.id}
# GET    /v1/fleet-manager/fleet-regions/{fleet_region.id}
# GET    /v1/fleet-manager/fleet-regions/{fleet.id}/regions
# DELETE /v1/fleet-manager/fleet-regions/{fleet_region.id}
def test_fleet_region():
    try:
        instance_type = object_controller.create_instance_type()
        image = object_controller.create_image()
        fleet = object_controller.create_fleet(instance_type.id, image.id)
        region = object_controller.create_region()

        fleet_region_url = Default.fleet_region_url
        fleet_region = FleetRegion(fleet.id, region.id)
        resp = ExecRequest.send_request('post', fleet_region_url, {'Content-Type': 'application/json'},
                                        {'fleetRegion': fleet_region.object2dict()})
        result = FleetRegion(resp.json()['fleetRegion'])
        assert result.fleetId == fleet.id
        assert result.regionId == region.id
        assert not result.isDeleted

        fleet1 = object_controller.create_fleet(instance_type.id, image.id)
        region1 = object_controller.create_region()
        new_min_available_instances = Default.random_int(2, 4)
        new_max_instances = Default.random_int(5, 10)
        modified = Default.random_letters()
        result.fleetId = fleet1.id
        result.regionId = region1.id
        result.minAvailableInstances = new_min_available_instances
        result.maxInstances = new_max_instances
        result.modifiedBy = modified
        resp1 = ExecRequest.send_request('put', fleet_region_url + '/' + result.id,
                                         {'Content-Type': 'application/json'},
                                         {'fleetRegion': result.object2dict()})
        result1 = FleetRegion(resp1.json()['fleetRegion'])
        assert result1.fleetId == fleet1.id
        assert result1.regionId == region1.id
        assert result1.minAvailableInstances == new_min_available_instances
        assert result1.maxInstances == new_max_instances
        # assert result1.modifiedBy == modified
        assert not result1.isDeleted

        resp2 = ExecRequest.send_request('get', fleet_region_url + '/' + result.id, None, None)
        result2 = FleetRegion(resp2.json()['fleetRegion'])
        assert result2.fleetId == fleet1.id
        assert result2.regionId == region1.id
        assert result2.minAvailableInstances == new_min_available_instances
        assert result2.maxInstances == new_max_instances
        # assert result2.modifiedBy == modified
        assert not result2.isDeleted

        resp3 = ExecRequest.send_request('get', fleet_region_url + '/' + fleet1.id + '/regions', None, None)
        assert len(resp3.json()['fleetRegionVos']) == 1
        result3 = resp3.json()['fleetRegionVos'][0]
        assert result3['id'] == result.id
        assert result3['fleetId'] == fleet1.id
        assert result3['regionId'] == region1.id
        assert result3['regionName'] == region1.name
        assert result3['regionNameInProvider'] == region1.nameInProvider
        assert result3['minAvailableInstances'] == new_min_available_instances
        assert result3['maxInstances'] == new_max_instances
    finally:
        ExecRequest.send_request('delete', fleet_region_url + '/' + result.id, None, None)
        resp3 = ExecRequest.send_request('get', fleet_region_url + '/' + result.id, None, None)
        result3 = FleetRegion(resp3.json()['fleetRegion'])
        assert result3.isDeleted
        object_controller.delete_region(region1.id)
        object_controller.delete_region(region.id)
        object_controller.delete_fleet(fleet1.id)
        object_controller.delete_fleet(fleet.id)
        object_controller.delete_instance_type(instance_type.id)
        object_controller.delete_image(image.id)


# POST   /v1/fleet-manager/fleet-region-providers
# PUT    /v1/fleet-manager/fleet-region-providers/{fleet_region_provider.id}
# GET    /v1/fleet-manager/fleet-region-providers/{fleet_region_provider.id}
# GET    /v1/fleet-manager/fleet-region-providers?fleetId={fleet.id}
# DELETE /v1/fleet-manager/fleet-region-providers/{fleet_region_provider.id}
def test_fleet_region_provider():
    try:
        instance_type = object_controller.create_instance_type()
        image = object_controller.create_image()
        fleet = object_controller.create_fleet(instance_type.id, image.id)
        region = object_controller.create_region()
        fleet_region = object_controller.create_fleet_region(fleet.id, region.id)

        fleet_region_provider_url = Default.fleet_region_provider_url
        fleet_region_provider = FleetRegionProvider(fleet.id, region.id)
        resp = ExecRequest.send_request('post', fleet_region_provider_url, {'Content-Type': 'application/json'},
                                        {'fleetRegionProvider': fleet_region_provider.object2dict()})
        result = FleetRegionProvider(resp.json()['fleetRegionProvider'])
        assert result.name == fleet_region_provider.name
        assert result.fleetId == fleet.id
        assert result.regionId == region.id
        assert result.providerType == fleet_region_provider.providerType
        assert result.providerConfig == fleet_region_provider.providerConfig
        # assert result.createdBy == fleet_region_provider.createdBy
        assert result.resourceAge == 0

        new_name = Default.random_letters()
        new_provider_type = Default.random_letters()
        new_provider_config = Default.random_letters()
        modified = Default.random_letters()
        result.name = new_name
        result.providerType = new_provider_type
        result.providerConfig = new_provider_config
        result.modifiedBy = modified
        resp1 = ExecRequest.send_request('put', fleet_region_provider_url + '/' + str(result.id),
                                         {'Content-Type': 'application/json'},
                                         {'fleetRegionProvider': result.object2dict()})
        result1 = FleetRegionProvider(resp1.json()['fleetRegionProvider'])
        assert result1.name == new_name
        assert result1.providerType == new_provider_type
        assert result1.providerConfig == new_provider_config
        # assert result1.createdBy == result.createdBy
        # assert result1.modifiedBy == modified
        assert result1.resourceAge == 1

        resp2 = ExecRequest.send_request('get', fleet_region_provider_url + '/' + str(result.id), None, None)
        result2 = FleetRegionProvider(resp2.json()['fleetRegionProvider'])
        assert result2.name == new_name
        assert result2.providerType == new_provider_type
        assert result2.providerConfig == new_provider_config
        # assert result2.createdBy == result.createdBy
        # assert result2.modifiedBy == modified
        assert result2.resourceAge == 1

        resp3 = ExecRequest.send_request('get', fleet_region_provider_url + '?fleetId=' + fleet.id, None, None)
        result3 = None
        for temp in resp3.json()['fleetRegionProviders']:
            if FleetRegionProvider(temp).id == result.id:
                result3 = FleetRegionProvider(temp)
        assert result3.name == new_name
        assert result3.providerType == new_provider_type
        assert result3.providerConfig == new_provider_config
        # assert result3.createdBy == result.createdBy
        # assert result3.modifiedBy == modified
        assert result3.resourceAge == 1
    finally:
        ExecRequest.send_request('delete', fleet_region_provider_url + '/' + str(result.id), None, None)
        resp4 = ExecRequest.send_request('get', fleet_region_provider_url + '?fleetId=' + fleet.id, None, None)
        assert len(resp4.json()['fleetRegionProviders']) == 0
        object_controller.delete_fleet_region(fleet_region.id)
        object_controller.delete_region(region.id)
        object_controller.delete_fleet(fleet.id)
        object_controller.delete_image(image.id)
        object_controller.delete_instance_type(instance_type.id)


def test_fleet_log_collector_config():
    pytest.skip(msg='fleet_log_collector_config is deprecated.')
    try:
        fleet_log_collector_config_url = Default.endpoint + '/v1/fleet-manager/fleet-logcollector-config'
        fleet_log_collector_config = FleetLogCollectorConfig()
        resp = ExecRequest.send_request('post', fleet_log_collector_config_url, {'Content-Type': 'application/json'},
                                        {'fleetLogCollectorConfig': fleet_log_collector_config.object2dict()})
        result = FleetLogCollectorConfig(resp.json()['fleetLogCollectorConfig'])
    finally:
        ExecRequest.send_request('delete', fleet_log_collector_config_url + '/' + result.id, None, None)

# TO TEST LIST
# POST /v1/fleet-manager/fleets:search
# GET  /v1/fleet-manager/image-region-instancetype
# GET  /v1/fleet-manager/profile/binary/updates
# GET  /v1/fleet-manager/profile/binary/updates/{id}
# PUT  /v1/fleet-manager/profile/{profileId}/binary
# POST /v1/fleet-manager/profile/{profileId}/binary/rollout
# POST /v1/fleet-manager/fleet-regions:change
