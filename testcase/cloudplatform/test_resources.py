import pytest
import datahelper.cloudplatform as cloud_platform_helper
import common.utility as util

automation_org_admin, automation_org_dev = util.get_pre_configured_org()
error_messages = {
    'resource_name_required': 'name为必填字段',
    'resource_type_incorrect': '资源类型错误',
    'resource_spec_not_existed': 'resource spec不存在',
    'resource_insufficient': '余量不足',
    'total_size_not_correct': 'total为必填字段',
    'resource_description_required': 'description为必填字段',
}
success_message = 'success'
fail_message = 'fail'


class TestResources:

    @staticmethod
    def admin_login():
        # user login and get cookies
        user_name, user_pw = util.get_admin_user_name_password()
        public_key = cloud_platform_helper.get_password_public_key()
        user_encrypt_pw = util.get_encrypt_password(public_key, user_pw)
        # get test verify code
        cookies = cloud_platform_helper.user_get_verify_code(None)
        verify_code_response = cloud_platform_helper.user_get_test_verify_code(cookies)
        verify_code = verify_code_response.json()['body']
        cookies = cloud_platform_helper.user_login(user_name, user_encrypt_pw, verify_code, cookies)
        return cookies, user_name

    @staticmethod
    def org_admin_login():
        # user login and get cookies
        user_name, user_pw = util.get_org_admin_user_name_password()
        public_key = cloud_platform_helper.get_password_public_key()
        user_encrypt_pw = util.get_encrypt_password(public_key, user_pw)
        # get test verify code
        cookies = cloud_platform_helper.user_get_verify_code(None)
        verify_code_response = cloud_platform_helper.user_get_test_verify_code(cookies)
        verify_code = verify_code_response.json()['body']
        cookies = cloud_platform_helper.user_login(user_name, user_encrypt_pw, verify_code, cookies)
        return cookies, user_name

    @staticmethod
    def get_auto_org_dev_id(cookies, user_name):
        search_user_query = {
            'account': user_name
        }
        users = cloud_platform_helper.search_users(search_user_query, 1, 10, cookies)
        assert len(users['list']) == 1
        user = users['list'][0]
        orgs = user['orgRole']
        org_name, org_id = None, None
        for org in orgs:
            if org['orgName'] == util.get_automation_org_dev():
                org_name = org['orgName']
                org_id = org['orgId']
                break
        assert org_name is not None and org_id is not None
        return org_id

    # MaxZhang: Resource Create 相关的先注释掉

    # @pytest.mark.bvt
    # def test_admin_create_resource(self):
    #     cookies = None
    #     try:
    #         # user login and get cookies
    #         user_name, user_pw = util.get_admin_user_name_password()
    #         public_key = cloud_platform_helper.get_password_public_key()
    #         user_encrypt_pw = util.get_encrypt_password(public_key, user_pw)
    #
    #         # get test verify code
    #         cookies = cloud_platform_helper.user_get_verify_code(None)
    #         verify_code_response = cloud_platform_helper.user_get_test_verify_code(cookies)
    #         verify_code = verify_code_response.json()['body']
    #
    #         cookies = cloud_platform_helper.user_login(user_name, user_encrypt_pw, verify_code, cookies)
    #
    #         # create resource
    #         # get resource spec firstly
    #         resource_spec = cloud_platform_helper.admin_get_resource_spec(cookies)
    #         resource_spec_id = resource_spec[0]['id']
    #         resource_name = 'test_' + util.random_str(10)
    #         # 资源类型 1：定量；2：弹性
    #         resource_type = '1'
    #         total_size = util.random_int(1, 2)
    #         resource_description = util.random_str(20)
    #
    #         req_body = {
    #             'name': resource_name,
    #             'type': int(resource_type),
    #             'specId': resource_spec_id,
    #             'total': total_size,
    #             'description': resource_description
    #         }
    #         resource_created = cloud_platform_helper.admin_add_resources(req_body, cookies)
    #         assert success_message in resource_created['message']
    #
    #         # search the newly-created resource by name
    #         resource_created = cloud_platform_helper.admin_search_resources(resource_name, resource_type, 0, 0, cookies)
    #         assert resource_created['total'] == 1
    #         resource_list = resource_created['list']
    #         assert len(resource_list) == 1
    #         assert resource_list[0]['name'] == resource_name
    #         assert int(resource_list[0]['type']) == int(resource_type)
    #         assert resource_list[0]['description'] == resource_description
    #         assert resource_list[0]['total'] == total_size
    #
    #     finally:
    #         cloud_platform_helper.user_logout(cookies)

    # @pytest.mark.daily
    # def test_admin_create_resource_invalid_data(self):
    #     cookies = None
    #     try:
    #         # user login and get cookies
    #         user_name, user_pw = util.get_admin_user_name_password()
    #         public_key = cloud_platform_helper.get_password_public_key()
    #         user_encrypt_pw = util.get_encrypt_password(public_key, user_pw)
    #
    #         cookies = cloud_platform_helper.user_get_verify_code(None)
    #         verify_code_response = cloud_platform_helper.user_get_test_verify_code(cookies)
    #         verify_code = verify_code_response.json()['body']
    #
    #         cookies = cloud_platform_helper.user_login(user_name, user_encrypt_pw, verify_code, cookies)
    #
    #         # create resource
    #         # get resource spec firstly
    #         resource_spec = cloud_platform_helper.admin_get_resource_spec(cookies)
    #         resource_spec_id = resource_spec[0]['id']
    #         resource_name = 'test_' + util.random_str(10)
    #         # 资源类型 1：定量；2：弹性
    #         resource_type = '1'
    #         total_size = util.random_int(1, 5)
    #         resource_description = util.random_str(20)
    #
    #         # resource_name is null
    #         resource_name = ''
    #         req_body = {
    #             'name': resource_name,
    #             'type': int(resource_type),
    #             'specId': resource_spec_id,
    #             'total': total_size,
    #             'description': resource_description
    #         }
    #         resource_created = cloud_platform_helper.admin_add_resources(req_body, cookies)
    #         assert error_messages['resource_name_required'] in resource_created['message']
    #
    #         # resource type is incorrect
    #         resource_name = 'test_' + util.random_str(10)
    #         resource_type = 'invalid_type'
    #         req_body = {
    #             'name': resource_name,
    #             'type': resource_type,
    #             'specId': resource_spec_id,
    #             'total': total_size,
    #             'description': resource_description
    #         }
    #         resource_created = cloud_platform_helper.admin_add_resources(req_body, cookies)
    #         # MaxZhang
    #         # 此处返回为 {'code': '00501',
    #         # 'message': 'json: cannot unmarshal string into Go struct field Resource.type of type model.ResType',
    #         # 'body': None}
    #         # 没有约定好此类错误时返回的字段
    #         # assert error_messages['resource_type_incorrect'] in resource_created['message']
    #
    #         # spec id is incorrect
    #         resource_name = 'test_' + util.random_str(10)
    #         resource_type = '1'
    #         resource_spec_id = 'invalid spec id'
    #         req_body = {
    #             'name': resource_name,
    #             'type': int(resource_type),
    #             'specId': resource_spec_id,
    #             'total': total_size,
    #             'description': resource_description
    #         }
    #         resource_created = cloud_platform_helper.admin_add_resources(req_body, cookies)
    #
    #         # MaxZhang
    #         # 所返回的错误message为'所选资源规格数量不足'
    #         # 没有约定好此类错误时返回的字段
    #         # assert error_messages['resource_spec_not_existed'] in resource_created['message']
    #
    #         # total size is not correct
    #         resource_name = 'test_' + util.random_str(10)
    #         resource_type = '1'
    #         resource_spec_id = resource_spec[0]['id']
    #         total_size = 0
    #         req_body = {
    #             'name': resource_name,
    #             'type': int(resource_type),
    #             'specId': resource_spec_id,
    #             'total': total_size,
    #             'description': resource_description
    #         }
    #         resource_created = cloud_platform_helper.admin_add_resources(req_body, cookies)
    #         assert error_messages['total_size_not_correct'] in resource_created['message']
    #
    #         # description is null
    #         resource_name = 'test_' + util.random_str(10)
    #         resource_type = '1'
    #         resource_spec_id = resource_spec[0]['id']
    #         total_size = util.random_int(1, 5)
    #         resource_description = ''
    #         req_body = {
    #             'name': resource_name,
    #             'type': int(resource_type),
    #             'specId': resource_spec_id,
    #             'total': total_size,
    #             'description': resource_description
    #         }
    #         resource_created = cloud_platform_helper.admin_add_resources(req_body, cookies)
    #         assert error_messages['resource_description_required'] in resource_created['message']
    #     finally:
    #         cloud_platform_helper.user_logout(cookies)

    # @pytest.mark.daily
    # def test_admin_update_resource(self):
    #     # user login and get cookies
    #     user_name, user_pw = util.get_admin_user_name_password()
    #     public_key = cloud_platform_helper.get_password_public_key()
    #     user_encrypt_pw = util.get_encrypt_password(public_key, user_pw)
    #
    #     # get test verify code
    #     cookies = cloud_platform_helper.user_get_verify_code(None)
    #     verify_code_response = cloud_platform_helper.user_get_test_verify_code(cookies)
    #     verify_code = verify_code_response.json()['body']
    #
    #     cookies = cloud_platform_helper.user_login(user_name, user_encrypt_pw, verify_code, cookies)
    #
    #     # create resource
    #     # get resource spec firstly
    #     resource_spec = cloud_platform_helper.admin_get_resource_spec(cookies)
    #     resource_spec_id = resource_spec[0]['id']
    #     resource_name = 'test_' + util.random_str(10)
    #     # 资源类型 1：定量；2：弹性
    #     resource_type = '1'
    #     total_size = util.random_int(1, 5)
    #     resource_description = util.random_str(20)
    #
    #     req_body = {
    #         'name': resource_name,
    #         'type': int(resource_type),
    #         'specId': resource_spec_id,
    #         'total': total_size,
    #         'description': resource_description
    #     }
    #     resource_created = cloud_platform_helper.admin_add_resources(req_body, cookies)
    #     assert success_message in resource_created['message']
    #
    #     # search the newly-created resource by name
    #     resource_created = cloud_platform_helper.admin_search_resources(resource_name, resource_type, 0, 0, cookies)
    #     assert resource_created['total'] == 1
    #     resource_list = resource_created['list']
    #     assert len(resource_list) == 1
    #     assert resource_list[0]['name'] == resource_name
    #     assert int(resource_list[0]['type']) == int(resource_type)
    #     assert resource_list[0]['description'] == resource_description
    #     assert resource_list[0]['total'] == total_size
    #     resource_id = resource_list[0]['id']
    #
    #     # update the resource
    #     resource_name_update = 'test_' + util.random_str(10)
    #     # 资源类型 1：定量；2：弹性
    #     resource_type_update = '2'
    #     total_size_update = util.random_int(1, 5)
    #     resource_description_update = util.random_str(20)
    #
    #     req_body = {
    #         'name': resource_name_update,
    #         'type': int(resource_type_update),
    #         'specId': resource_spec_id,
    #         'total': total_size_update,
    #         'description': resource_description_update
    #     }
    #     resource_created = cloud_platform_helper.admin_update_resource(resource_id, req_body, cookies)
    #     assert success_message in resource_created['message']
    #
    #     # search the newly-created resource by name
    #     resource_created = cloud_platform_helper.admin_get_resource_by_id(resource_id, cookies)
    #     assert resource_created['name'] == resource_name_update
    #     assert int(resource_created['type']) == int(resource_type_update)
    #     assert resource_created['description'] == resource_description_update
    #     assert resource_created['total'] == total_size_update
    #
    #     cloud_platform_helper.user_logout(cookies)

    # @pytest.mark.daily
    # def test_admin_update_resource_invalid_data(self):
    #     # user login and get cookies
    #     user_name, user_pw = util.get_admin_user_name_password()
    #     public_key = cloud_platform_helper.get_password_public_key()
    #     user_encrypt_pw = util.get_encrypt_password(public_key, user_pw)
    #
    #     # get test verify code
    #     cookies = cloud_platform_helper.user_get_verify_code(None)
    #     verify_code_response = cloud_platform_helper.user_get_test_verify_code(cookies)
    #     verify_code = verify_code_response.json()['body']
    #
    #     cookies = cloud_platform_helper.user_login(user_name, user_encrypt_pw, verify_code, cookies)
    #
    #     # create resource
    #     # get resource spec firstly
    #     resource_spec = cloud_platform_helper.admin_get_resource_spec(cookies)
    #     resource_spec_id = resource_spec[0]['id']
    #     resource_name = 'test_' + util.random_str(10)
    #     # 资源类型 1：定量；2：弹性
    #     resource_type = '1'
    #     total_size = util.random_int(1, 5)
    #     resource_description = util.random_str(20)
    #
    #     req_body = {
    #         'name': resource_name,
    #         'type': int(resource_type),
    #         'specId': resource_spec_id,
    #         'total': total_size,
    #         'description': resource_description
    #     }
    #     resource_created = cloud_platform_helper.admin_add_resources(req_body, cookies)
    #     assert success_message in resource_created['message']
    #
    #     # search the newly-created resource by name
    #     resource_created = cloud_platform_helper.admin_search_resources(resource_name, resource_type, 0, 0, cookies)
    #     assert resource_created['total'] == 1
    #     resource_list = resource_created['list']
    #     assert len(resource_list) == 1
    #     assert resource_list[0]['name'] == resource_name
    #     assert int(resource_list[0]['type']) == int(resource_type)
    #     assert resource_list[0]['description'] == resource_description
    #     assert resource_list[0]['total'] == total_size
    #     resource_id = resource_list[0]['id']
    #
    #     # update the resource
    #     # resource_name is null
    #     resource_name = ''
    #     req_body = {
    #         'name': resource_name,
    #         'type': int(resource_type),
    #         'specId': resource_spec_id,
    #         'total': total_size,
    #         'description': resource_description
    #     }
    #     resource_created = cloud_platform_helper.admin_add_resources(req_body, cookies)
    #     assert error_messages['resource_name_required'] in resource_created['message']
    #
    #     # resource type is incorrect
    #     resource_name = 'test_' + util.random_str(10)
    #     resource_type = 'invalid_type'
    #     req_body = {
    #         'name': resource_name,
    #         'type': resource_type,
    #         'specId': resource_spec_id,
    #         'total': total_size,
    #         'description': resource_description
    #     }
    #     resource_created = cloud_platform_helper.admin_add_resources(req_body, cookies)
    #     # MaxZhang: 未约定好返回信息
    #     # assert error_messages['resource_type_incorrect'] in resource_created['message']
    #
    #     # spec id is incorrect
    #     resource_name = 'test_' + util.random_str(10)
    #     resource_type = '1'
    #     resource_spec_id = 'invalid spec id'
    #     req_body = {
    #         'name': resource_name,
    #         'type': int(resource_type),
    #         'specId': resource_spec_id,
    #         'total': total_size,
    #         'description': resource_description
    #     }
    #     resource_created = cloud_platform_helper.admin_add_resources(req_body, cookies)
    #     # MaxZhang
    #     # 未约定好错误信息
    #     # assert error_messages['resource_spec_not_existed'] in resource_created['message']
    #
    #     # total size is not correct
    #     resource_name = 'test_' + util.random_str(10)
    #     resource_type = '1'
    #     resource_spec_id = resource_spec[0]['id']
    #     total_size = 0
    #     req_body = {
    #         'name': resource_name,
    #         'type': int(resource_type),
    #         'specId': resource_spec_id,
    #         'total': total_size,
    #         'description': resource_description
    #     }
    #     resource_created = cloud_platform_helper.admin_add_resources(req_body, cookies)
    #     assert error_messages['total_size_not_correct'] in resource_created['message']
    #
    #     # description is null
    #     resource_name = 'test_' + util.random_str(10)
    #     resource_type = '1'
    #     resource_spec_id = resource_spec[0]['id']
    #     total_size = util.random_int(1, 5)
    #     resource_description = ''
    #     req_body = {
    #         'name': resource_name,
    #         'type': int(resource_type),
    #         'specId': resource_spec_id,
    #         'total': total_size,
    #         'description': resource_description
    #     }
    #     resource_created = cloud_platform_helper.admin_add_resources(req_body, cookies)
    #     assert error_messages['resource_description_required'] in resource_created['message']
    #
    #     cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_admin_get_resource_by_id(self):
        cookies = None
        try:
            cookies, username = self.admin_login()

            # pre_created_test_resource
            resource = cloud_platform_helper.get_pre_created_test_resource(cookies)
            resource_name = resource['name']
            resource_type = resource['type']
            total_size = resource['total']
            resource_description = resource['description']

            # search the resource by name
            resource_created = cloud_platform_helper.admin_search_resources(resource_name, resource_type, 0, 0, cookies)
            assert resource_created['total'] == 1
            resource_list = resource_created['list']
            assert len(resource_list) == 1
            assert resource_list[0]['name'] == resource_name
            assert int(resource_list[0]['type']) == int(resource_type)
            assert resource_list[0]['description'] == resource_description
            assert resource_list[0]['total'] == total_size
            resource_id = resource_list[0]['id']

            # get the resource by id
            resource_created = cloud_platform_helper.admin_get_resource_by_id(resource_id, cookies)
            assert resource_created['name'] == resource_name
            assert int(resource_created['type']) == int(resource_type)
            assert resource_created['description'] == resource_description
            assert resource_created['total'] == total_size

            # get the resource by invalid id
            resource_created = cloud_platform_helper.admin_get_resource_by_id('invalid_id', cookies)
            # MaxZhang:
            # 造成了InternalServerError没处理
            assert fail_message in resource_created['message']
        finally:
            cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_admin_search_resources(self):
        cookies = None
        try:
            cookies, username = self.admin_login()

            # pre_created_test_resource
            resource = cloud_platform_helper.get_pre_created_test_resource(cookies)
            resource_name = resource['name']
            resource_type = resource['type']
            total_size = resource['total']
            resource_description = resource['description']

            # search the newly-created resource by name
            resource_created = cloud_platform_helper.admin_search_resources(resource_name, resource_type, 0, 0, cookies)
            assert resource_created['total'] == 1
            resource_list = resource_created['list']
            assert len(resource_list) == 1
            assert resource_list[0]['name'] == resource_name
            assert int(resource_list[0]['type']) == int(resource_type)
            assert resource_list[0]['description'] == resource_description
            assert resource_list[0]['total'] == total_size

            # no search query
            resource_created = cloud_platform_helper.admin_search_resources(None, None, 0, 0, cookies)
            assert resource_created['total'] >= 1
        finally:
            cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_admin_update_org_resource(self):
        org_id, cookies = None, None
        try:
            cookies, username = self.admin_login()

            # add an organization
            org_name = 'test_' + util.random_str(10)
            org_description = util.random_str(20)
            cloud_platform_helper.create_org(org_name, org_description, cookies)

            # search the organization by name
            orgs_return = cloud_platform_helper.search_org(org_name, 0, 0, cookies)
            assert orgs_return['total'] == 1
            org_list = orgs_return['list']
            org_id = org_list[0]['id']

            # pre_created_test_resource
            resource = cloud_platform_helper.get_pre_created_test_resource(cookies)
            resource_name = resource['name']
            resource_type = resource['type']
            total_size = resource['total']
            resource_description = resource['description']

            # search the newly-created resource by name
            resource_created = cloud_platform_helper.admin_search_resources(resource_name, resource_type, 0, 0, cookies)
            assert resource_created['total'] == 1
            resource_list = resource_created['list']
            assert len(resource_list) == 1
            assert resource_list[0]['name'] == resource_name
            assert int(resource_list[0]['type']) == int(resource_type)
            assert resource_list[0]['description'] == resource_description
            assert resource_list[0]['total'] == total_size
            resource_id = resource_list[0]['id']

            req_body = {
                "quotaRes": [
                    {
                        "resourceId": resource_id,
                        "name": resource_name,
                        "capacity": 1
                    }
                ]
            }

            add_org_resource = cloud_platform_helper.admin_update_organization_resource(org_id, req_body, cookies)
            assert success_message in add_org_resource['message']
        finally:
            if org_id:
                # delete the org
                cloud_platform_helper.delete_org_by_id(org_id, cookies)
            cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_admin_get_org_resource_by_id(self):
        org_id, cookies = None, None
        try:
            cookies, username = self.admin_login()

            # add an organization
            org_name = 'test_' + util.random_str(10)
            org_description = util.random_str(20)
            cloud_platform_helper.create_org(org_name, org_description, cookies)

            # search the organization by name
            orgs_return = cloud_platform_helper.search_org(org_name, 0, 0, cookies)
            assert orgs_return['total'] == 1
            org_list = orgs_return['list']
            org_id = org_list[0]['id']

            # pre_created_test_resource
            resource = cloud_platform_helper.get_pre_created_test_resource(cookies)
            resource_name = resource['name']
            resource_type = resource['type']
            total_size = resource['total']
            resource_description = resource['description']

            # search the newly-created resource by name
            resource_created = cloud_platform_helper.admin_search_resources(resource_name, resource_type, 0, 0, cookies)
            assert resource_created['total'] == 1
            resource_list = resource_created['list']
            assert len(resource_list) == 1
            assert resource_list[0]['name'] == resource_name
            assert int(resource_list[0]['type']) == int(resource_type)
            assert resource_list[0]['description'] == resource_description
            assert resource_list[0]['total'] == total_size
            resource_id = resource_list[0]['id']

            req_body = {
                "quotaRes": [
                    {
                        "resourceId": resource_id,
                        "name": resource_name,
                        "capacity": 1
                    }
                ]
            }

            add_org_resource = cloud_platform_helper.admin_update_organization_resource(org_id, req_body, cookies)
            assert success_message in add_org_resource['message']

            org_resource = cloud_platform_helper.admin_get_organization_resource_by_id(org_id, cookies)
            assert success_message in org_resource['message']

            # invalid org id
            org_resource = cloud_platform_helper.admin_get_organization_resource_by_id('invalid_id', cookies)
            # MaxZhang
            # 造成了InternalServerError没处理
            assert fail_message in org_resource['message']
        finally:
            cloud_platform_helper.delete_org_by_id(org_id, cookies)
            cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_admin_search_org_resources(self):
        org_id, cookies = None, None
        try:
            cookies, username = self.admin_login()

            # add an organization
            org_name = 'test_' + util.random_str(10)
            org_description = util.random_str(20)
            cloud_platform_helper.create_org(org_name, org_description, cookies)

            # search the organization by name
            orgs_return = cloud_platform_helper.search_org(org_name, 0, 0, cookies)
            assert orgs_return['total'] == 1
            org_list = orgs_return['list']
            org_id = org_list[0]['id']

            # pre_created_test_resource
            resource = cloud_platform_helper.get_pre_created_test_resource(cookies)
            resource_name = resource['name']
            resource_type = resource['type']
            total_size = resource['total']
            resource_description = resource['description']

            # search the newly-created resource by name
            resource_created = cloud_platform_helper.admin_search_resources(resource_name, resource_type, 0, 0, cookies)
            assert resource_created['total'] == 1
            resource_list = resource_created['list']
            assert len(resource_list) == 1
            assert resource_list[0]['name'] == resource_name
            assert int(resource_list[0]['type']) == int(resource_type)
            assert resource_list[0]['description'] == resource_description
            assert resource_list[0]['total'] == total_size
            resource_id = resource_list[0]['id']

            req_body = {
                "quotaRes": [
                    {
                        "resourceId": resource_id,
                        "name": resource_name,
                        "capacity": 1
                    }
                ]
            }

            add_org_resource = cloud_platform_helper.admin_update_organization_resource(org_id, req_body, cookies)
            assert success_message in add_org_resource['message']

            # search by resource name
            org_resource = cloud_platform_helper.admin_search_organization_resources(org_name, 0, 0, cookies)
            assert len(org_resource['list']) == 1
            org_resource = org_resource['list'][0]
            assert org_resource['name'] == org_name
            assert org_resource['quotaRes'][0]['name'] == resource_name
            assert org_resource['quotaRes'][0]['capacity'] == req_body['quotaRes'][0]['capacity']
        finally:
            if org_id:
                cloud_platform_helper.delete_org_by_id(org_id, cookies)
            cloud_platform_helper.user_logout(cookies)

    # 登录dev admin账户，然后创建resource pool
    @pytest.mark.daily
    def test_org_add_resource_pool(self):
        cookies, pool_display_name, pool_id = None, None, None
        try:
            # 只有admin才可获取资源，因此需要先登录admin
            cookies, username = self.admin_login()

            # pre_created_test_resource
            resource = cloud_platform_helper.get_pre_created_test_resource(cookies)
            resource_name = resource['name']
            resource_type = resource['type']
            total_size = resource['total']
            resource_description = resource['description']
            resource_id = resource['id']
            pool_size = 1

            # 登录组织管理员，以管理resource pool
            cookies, user_name = self.org_admin_login()

            # 创建pool，首先check资源是否充足
            check_response = cloud_platform_helper.org_resource_pool_check(resource_id, pool_size, resource_type,
                                                                           cookies)
            assert success_message in check_response['message']

            # 创建pool
            pool_description = util.random_str(20)
            pool_display_name = "test_pool_" + util.random_str(10)
            add_response = cloud_platform_helper.org_add_resource_pool(pool_description, pool_display_name, resource_id,
                                                                       pool_size, resource_type, cookies)
            assert success_message in add_response['message']
        finally:
            # search pool and delete
            if pool_display_name:
                response = cloud_platform_helper.org_search_resource_pools(pool_display_name, None, 0, 0, cookies)
                assert len(response['list']) == 1
                pool_object = response['list'][0]
                pool_id = pool_object['id']

            if pool_id:
                response = cloud_platform_helper.org_delete_resource_pool_by_id(pool_id, cookies)
                assert success_message in response['message']

            cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_org_resource_pool_check(self):
        cookies = None
        try:
            # 只有admin才可获取资源(resource)，以供后续创建 resource_pool 因此需要先登录admin
            cookies, username = self.admin_login()

            # pre_created_test_resource
            resource = cloud_platform_helper.get_pre_created_test_resource(cookies)
            resource_name = resource['name']
            resource_type = resource['type']
            total_size = resource['total']
            resource_description = resource['description']
            resource_id = resource['id']
            pool_size = 1

            # 登录组织管理员，以管理resource pool
            cookies, user_name = self.org_admin_login()

            # 1. 不合理的 pool_size
            invalid_pool_size = 999999999
            check_response = cloud_platform_helper.org_resource_pool_check(resource_id, invalid_pool_size,
                                                                           resource_type,
                                                                           cookies)
            assert error_messages['resource_insufficient'] in check_response['message']

            # 2. 不合理的 resource_type
            invalid_resource_type = 2023
            check_response2 = cloud_platform_helper.org_resource_pool_check(resource_id, pool_size,
                                                                            invalid_resource_type,
                                                                            cookies)
            assert error_messages['resource_type_incorrect'] in check_response2['message']

            invalid_resource_id = "invalid_resource_id"
            check_response3 = cloud_platform_helper.org_resource_pool_check(invalid_resource_id, pool_size,
                                                                            resource_type,
                                                                            cookies)
            # maxzhang: 此处直接报了InternalServerError，而不是错误信息
            assert check_response3 is not None
            assert fail_message in check_response3['message']
        finally:
            cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_org_add_resource_pool_invalid_data(self):
        cookies, pool_display_name = None, None
        try:
            # 只有admin才可获取资源(resource)，以供后续创建 resource_pool 因此需要先登录admin
            cookies, username = self.admin_login()

            # pre_created_test_resource
            resource = cloud_platform_helper.get_pre_created_test_resource(cookies)
            resource_name = resource['name']
            resource_type = resource['type']
            total_size = resource['total']
            resource_description = resource['description']
            resource_id = resource['id']
            pool_size = 1

            # 登录组织管理员，以管理resource pool
            cookies, user_name = self.org_admin_login()

            # 1. 不合理的 pool_size
            invalid_pool_size = 999999999
            check_response = cloud_platform_helper.org_resource_pool_check(resource_id, invalid_pool_size,
                                                                           resource_type,
                                                                           cookies)
            assert error_messages['resource_insufficient'] in check_response['message']

            pool_description = util.random_str(20)
            pool_display_name = "test_pool_" + util.random_str(10)

            add_response = cloud_platform_helper.org_add_resource_pool(pool_description, pool_display_name, resource_id,
                                                                       invalid_pool_size, resource_type, cookies)
            assert error_messages['resource_insufficient'] in add_response['message']

            # 2. 空白pool_name
            invalid_pool_display_name = ""
            add_response = cloud_platform_helper.org_add_resource_pool(pool_description, invalid_pool_display_name,
                                                                       resource_id, pool_size,
                                                                       resource_type, cookies)
            assert error_messages['resource_name_required'] in add_response['message']

        finally:
            # search pool and delete
            cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_org_delete_resource_pool_by_id(self):
        cookies = None
        try:
            # 只有admin才可获取资源，因此需要先登录admin
            cookies, username = self.admin_login()

            # pre_created_test_resource
            resource = cloud_platform_helper.get_pre_created_test_resource(cookies)
            resource_name = resource['name']
            resource_type = resource['type']
            total_size = resource['total']
            resource_description = resource['description']
            resource_id = resource['id']
            pool_size = 1

            # 登录组织管理员，以管理resource pool
            cookies, user_name = self.org_admin_login()

            # 创建pool，首先check资源是否充足
            check_response = cloud_platform_helper.org_resource_pool_check(resource_id, pool_size, resource_type,
                                                                           cookies)
            assert success_message in check_response['message']

            # 创建pool
            pool_description = util.random_str(20)
            pool_display_name = "test_pool_" + util.random_str(10)
            add_response = cloud_platform_helper.org_add_resource_pool(pool_description, pool_display_name, resource_id,
                                                                       pool_size, resource_type, cookies)
            assert success_message in add_response['message']

            # search and delete
            response = cloud_platform_helper.org_search_resource_pools(pool_display_name, None, 0, 0, cookies)
            assert len(response['list']) == 1
            pool_object = response['list'][0]
            pool_id = pool_object['id']

            response = cloud_platform_helper.org_delete_resource_pool_by_id(pool_id, cookies)
            assert success_message in response['message']

        finally:
            cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_org_update_resource_pool(self):
        pool_id, cookies = None, None
        try:
            # 只有admin才可获取资源，因此需要先登录admin
            cookies, username = self.admin_login()

            # pre_created_test_resource
            resource = cloud_platform_helper.get_pre_created_test_resource(cookies)
            resource_name = resource['name']
            resource_type = resource['type']
            total_size = resource['total']
            resource_description = resource['description']
            resource_id = resource['id']
            pool_size = 1

            # 登录组织管理员，以管理resource pool
            cookies, user_name = self.org_admin_login()

            # 创建pool，首先check资源是否充足
            check_response = cloud_platform_helper.org_resource_pool_check(resource_id, pool_size, resource_type,
                                                                           cookies)
            assert success_message in check_response['message']

            # 创建pool
            pool_description = util.random_str(20)
            pool_display_name = "test_pool_" + util.random_str(10)
            add_response = cloud_platform_helper.org_add_resource_pool(pool_description, pool_display_name, resource_id,
                                                                       pool_size, resource_type, cookies)
            assert success_message in add_response['message']

            # search pool_id
            response = cloud_platform_helper.org_search_resource_pools(pool_display_name, None, 0, 0, cookies)
            assert len(response['list']) == 1
            pool_object = response['list'][0]
            pool_id = pool_object['id']

            # new description
            new_pool_description = "new_" + pool_description
            update_response = cloud_platform_helper.org_update_resource_pool(new_pool_description, pool_display_name,
                                                                             resource_id, pool_size, resource_type,
                                                                             pool_id,
                                                                             cookies)
            assert success_message in update_response['message']
        finally:
            response = cloud_platform_helper.org_delete_resource_pool_by_id(pool_id, cookies)
            assert success_message in response['message']
            cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_org_update_resource_pool_invalid_data(self):
        pool_id, cookies = None, None
        try:
            # 只有admin才可获取资源，因此需要先登录admin
            cookies, username = self.admin_login()

            # pre_created_test_resource
            resource = cloud_platform_helper.get_pre_created_test_resource(cookies)
            resource_name = resource['name']
            resource_type = resource['type']
            total_size = resource['total']
            resource_description = resource['description']
            resource_id = resource['id']
            pool_size = 1

            # 登录组织管理员，以管理resource pool
            cookies, user_name = self.org_admin_login()

            # 创建pool，首先check资源是否充足
            check_response = cloud_platform_helper.org_resource_pool_check(resource_id, pool_size, resource_type,
                                                                           cookies)
            assert success_message in check_response['message']

            # 创建pool
            pool_description = util.random_str(20)
            pool_display_name = "test_pool_" + util.random_str(10)
            add_response = cloud_platform_helper.org_add_resource_pool(pool_description, pool_display_name, resource_id,
                                                                       pool_size, resource_type, cookies)
            assert success_message in add_response['message']

            # search pool_id
            response = cloud_platform_helper.org_search_resource_pools(pool_display_name, None, 0, 0, cookies)
            assert len(response['list']) == 1
            pool_object = response['list'][0]
            pool_id = pool_object['id']

            # new description
            new_name = ""
            update_response = cloud_platform_helper.org_update_resource_pool(pool_description, new_name, resource_id,
                                                                             pool_size, resource_type, pool_id,
                                                                             cookies)
            assert error_messages['resource_name_required'] in update_response['message']
        finally:
            response = cloud_platform_helper.org_delete_resource_pool_by_id(pool_id, cookies)
            assert success_message in response['message']
            cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_org_get_resource_pool_by_id(self):
        pool_id, cookies = None, None
        try:
            # 只有admin才可获取资源，因此需要先登录admin
            cookies, username = self.admin_login()

            # pre_created_test_resource
            resource = cloud_platform_helper.get_pre_created_test_resource(cookies)
            resource_name = resource['name']
            resource_type = resource['type']
            total_size = resource['total']
            resource_description = resource['description']
            resource_id = resource['id']
            pool_size = 1

            # 登录组织管理员，以管理resource pool
            cookies, user_name = self.org_admin_login()

            # 创建pool，首先check资源是否充足
            check_response = cloud_platform_helper.org_resource_pool_check(resource_id, pool_size, resource_type,
                                                                           cookies)
            assert success_message in check_response['message']

            # 创建pool
            pool_description = util.random_str(20)
            pool_display_name = "test_pool_" + util.random_str(10)
            add_response = cloud_platform_helper.org_add_resource_pool(pool_description, pool_display_name, resource_id,
                                                                       pool_size, resource_type, cookies)
            assert success_message in add_response['message']

            # search pool_id
            response = cloud_platform_helper.org_search_resource_pools(pool_display_name, None, 0, 0, cookies)
            assert len(response['list']) == 1
            pool_object = response['list'][0]
            pool_id = pool_object['id']

            get_response = cloud_platform_helper.org_get_resource_pool_by_id(pool_id, cookies)
            assert get_response is not None
            pool_object = get_response['detail']
            assert pool_object['size'] == pool_size
            assert pool_object['displayName'] == pool_display_name
            assert pool_object['resourceId'] == resource_id
        finally:
            response = cloud_platform_helper.org_delete_resource_pool_by_id(pool_id, cookies)
            assert success_message in response['message']
            cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_org_search_resource_pools(self):
        pool_id, cookies = None, None
        try:
            # 只有admin才可获取资源，因此需要先登录admin
            cookies, username = self.admin_login()

            # pre_created_test_resource
            resource = cloud_platform_helper.get_pre_created_test_resource(cookies)
            resource_name = resource['name']
            resource_type = resource['type']
            total_size = resource['total']
            resource_description = resource['description']
            resource_id = resource['id']
            pool_size = 1

            # 登录组织管理员，以管理resource pool
            cookies, user_name = self.org_admin_login()

            # 创建pool，首先check资源是否充足
            check_response = cloud_platform_helper.org_resource_pool_check(resource_id, pool_size, resource_type,
                                                                           cookies)
            assert success_message in check_response['message']

            # 创建pool
            pool_description = util.random_str(20)
            pool_display_name = "test_pool_" + util.random_str(10)
            add_response = cloud_platform_helper.org_add_resource_pool(pool_description, pool_display_name, resource_id,
                                                                       pool_size, resource_type, cookies)
            assert success_message in add_response['message']

            # search pool_id
            response = cloud_platform_helper.org_search_resource_pools(pool_display_name, None, 0, 0, cookies)
            assert len(response['list']) == 1
            pool_object = response['list'][0]
            pool_id = pool_object['id']
            assert pool_object['size'] == pool_size
            assert pool_object['displayName'] == pool_display_name
        finally:
            response = cloud_platform_helper.org_delete_resource_pool_by_id(pool_id, cookies)
            assert success_message in response['message']
            cloud_platform_helper.user_logout(cookies)
