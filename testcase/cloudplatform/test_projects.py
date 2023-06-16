import logging

import pytest
import datahelper.cloudplatform as cloud_platform_helper
import common.utility as util

import re
import copy

error_messages = {
    'display_name_required': 'displayname为必填字段',
    'project_name_required': 'project name为必填字段',
    'project_not_existed': 'project id 不存在',
    'org_not_existed': 'org id 不存在',
    'package_not_existed': 'package id 不存在',
    'package_not_ready': '游戏包未就绪',
    'invalid_releaser_version': 'version不合法',
    'pool_not_existed': '资源池不存在',
    'release_not_exist': 'App发布不存在',
    'reject_not_exist': '驳回原因不存在',
    'operation_failed': '操作失败，请稍后重试',
}
success_message = 'success'
fail_message = 'fail'


class TestProjects:
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

    def add_resource_pool_for_dev_app(self, admin_cookie):
        # pre_created_test_resource
        resource = cloud_platform_helper.get_pre_created_test_resource(admin_cookie)
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

        return pool_id

    @pytest.mark.bvt
    def test_projects_create(self):
        org_id, cookies, project_id = None, None, None
        try:
            # org admin login
            cookies, user_name = self.org_admin_login()

            # get User OrgId
            org_id = self.get_auto_org_dev_id(cookies, user_name)

            # add a project
            project_name = 'test_project_' + util.random_str(10)
            project_description = util.random_str(20)
            project_created = cloud_platform_helper.create_project(org_id, project_name, project_description, cookies)
            project_id = project_created['id']
            assert project_created['displayName'] == project_name
            assert project_created['description'] == project_description
            assert project_created['orgId'] == org_id
        finally:
            response = cloud_platform_helper.delete_project_by_id(org_id, project_id, cookies)
            assert success_message in response['message']
            cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_projects_create_invalid_data(self):
        org_id, cookies, project_id = None, None, None

        try:
            cookies, user_name = self.org_admin_login()

            # get User OrgId
            org_id = self.get_auto_org_dev_id(cookies, user_name)

            # add a project
            invalid_project_name = ''
            project_description = util.random_str(20)
            project_created = cloud_platform_helper.create_project(org_id, invalid_project_name, project_description,
                                                                   cookies)
            # MaxZhang:
            # 直接报了InternalServerError：
            # {'code': 'InternalServerError', 'message': 'Wrap non AppError', 'body': None}
            assert error_messages['project_name_required'] in project_created['message']
        finally:
            cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_projects_delete(self):
        org_id, cookies, project_id = None, None, None
        try:
            # org admin login
            cookies, user_name = self.org_admin_login()

            # get User OrgId
            org_id = self.get_auto_org_dev_id(cookies, user_name)

            # add a project
            project_name = 'test_project_' + util.random_str(10)
            project_description = util.random_str(20)
            project_created = cloud_platform_helper.create_project(org_id, project_name, project_description, cookies)
            project_id = project_created['id']

            assert project_created['displayName'] == project_name
            assert project_created['description'] == project_description
            assert project_created['orgId'] == org_id

            # Normal delete the created project
            delete_response = cloud_platform_helper.delete_project_by_id(org_id, project_id, cookies)
            assert delete_response['message'] in success_message

            get_response = cloud_platform_helper.get_project_by_id(org_id, project_id, cookies)
            assert get_response['deletedTime'] is not None and get_response['deletedTime'] != ''
        finally:
            if project_id:
                response = cloud_platform_helper.delete_project_by_id(org_id, project_id, cookies)
                assert success_message in response['message']
            cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_projects_delete_invalid(self):
        org_id, cookies, project_id = None, None, None
        try:
            # org admin login
            cookies, user_name = self.org_admin_login()

            # get User OrgId
            org_id = self.get_auto_org_dev_id(cookies, user_name)

            # add a project
            project_name = 'test_project_' + util.random_str(10)
            project_description = util.random_str(20)
            project_created = cloud_platform_helper.create_project(org_id, project_name, project_description, cookies)
            project_id = project_created['id']

            assert project_created['displayName'] == project_name
            assert project_created['description'] == project_description
            assert project_created['orgId'] == org_id

            # delete the project with invalid id
            invalid_project_id = util.random_str(10)
            project_response = cloud_platform_helper.delete_project_by_id(org_id, invalid_project_id, cookies)
            # MaxZhang:
            # 直接返回了 {'code': 'InternalServerError', 'message': 'Wrap non AppError', 'body': None}
            assert error_messages['project_not_existed'] in project_response['message']

            # delete the project with invalid_org_id
            invalid_org_id = util.random_str(10)
            project_response = cloud_platform_helper.delete_project_by_id(invalid_org_id, project_id, cookies)
            # MaxZhang:
            # 返回了 {'code': '403', 'message': '无权访问', 'body': None}
            # 而不是org_not_existed
            assert error_messages['org_not_existed'] in project_response['message']
        finally:
            if project_id:
                response = cloud_platform_helper.delete_project_by_id(org_id, project_id, cookies)
                assert success_message in response['message']
            cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_projects_update(self):
        org_id, project_id, cookies = None, None, None
        try:
            # org admin login
            cookies, user_name = self.org_admin_login()

            # get User OrgId
            org_id = self.get_auto_org_dev_id(cookies, user_name)

            # add a project
            project_name = 'test_project_' + util.random_str(10)
            project_description = util.random_str(20)
            project_created = cloud_platform_helper.create_project(org_id, project_name, project_description, cookies)
            assert project_created['displayName'] == project_name
            assert project_created['description'] == project_description
            assert project_created['orgId'] == org_id
            project_id = project_created['id']

            # update the project name and description
            new_project_name = 'test_project_' + util.random_str(10)
            new_project_description = util.random_str(10)
            project_updated = cloud_platform_helper.update_project(org_id, project_id, new_project_name,
                                                                   new_project_description, cookies)
            project_updated = project_updated['body']
            assert project_updated['displayName'] == new_project_name
            assert project_updated['description'] == new_project_description
        finally:
            if project_id:
                # delete the created org and the project
                response = cloud_platform_helper.delete_project_by_id(org_id, project_id, cookies)
                assert success_message in response['message']
            cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_projects_update_invalid_data(self):
        org_id, project_id, cookies = None, None, None
        try:
            # org admin login
            cookies, user_name = self.org_admin_login()

            # get User OrgId
            org_id = self.get_auto_org_dev_id(cookies, user_name)

            # add a project
            project_name = 'test_project_' + util.random_str(10)
            project_description = util.random_str(20)
            project_created = cloud_platform_helper.create_project(org_id, project_name, project_description, cookies)

            assert project_created['displayName'] == project_name
            assert project_created['description'] == project_description
            assert project_created['orgId'] == org_id
            project_id = project_created['id']

            # update the project name and description
            new_project_name = ''
            new_project_description = util.random_str(10)
            project_updated = cloud_platform_helper.update_project(org_id, project_id, new_project_name,
                                                                   new_project_description, cookies)

            # MaxZhang
            # 直接返回了 {'code': 'InternalServerError', 'message': 'Wrap non AppError', 'body': None}
            assert error_messages['project_name_required'] in project_updated['message']

            project_created = cloud_platform_helper.get_project_by_id(org_id, project_id, cookies)
            assert project_created['displayName'] == project_name
            assert project_created['description'] == project_description
        finally:
            if project_id:
                # delete the created org and the project
                response = cloud_platform_helper.delete_project_by_id(org_id, project_id, cookies)
                assert success_message in response['message']
            cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_get_single_project(self):
        org_id, project_id, cookies = None, None, None
        try:
            # org admin login
            cookies, user_name = self.org_admin_login()

            # get User OrgId
            org_id = self.get_auto_org_dev_id(cookies, user_name)

            # add a project
            project_name = 'test_project_' + util.random_str(10)
            project_description = util.random_str(20)
            project_created = cloud_platform_helper.create_project(org_id, project_name, project_description, cookies)
            assert project_created['displayName'] == project_name
            assert project_created['description'] == project_description
            assert project_created['orgId'] == org_id
            project_id = project_created['id']

            project_get = cloud_platform_helper.get_project_by_id(org_id, project_id, cookies)
            assert project_get['displayName'] == project_name
            assert project_get['description'] == project_description
            assert project_get['orgId'] == org_id

            # Get with invalid_project_id
            invalid_project_id = util.random_str(10)
            project_response = cloud_platform_helper.get_project_by_id(org_id, invalid_project_id, cookies)
            # MaxZhang
            # 直接返回了：{"code":"InternalServerError","message":"Wrap non AppError","body":null}
            assert error_messages['project_not_existed'] in project_response['message']

            # Get with invalid_org_id
            invalid_org_id = util.random_str(10)
            project_response = cloud_platform_helper.get_project_by_id(invalid_org_id, project_created['id'], cookies)
            # MaxZhang
            # 直接返回了：b'{"code":"403","message":"\xe6\x97\xa0\xe6\x9d\x83\xe8\xae\xbf\xe9\x97\xae","body":null}'
            assert error_messages['org_not_existed'] in project_response['message']
        finally:
            # delete the project
            response = cloud_platform_helper.delete_project_by_id(org_id, project_id, cookies)
            assert success_message in response['message']
            cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_search_projects(self):
        org_id, project_id, cookies = None, None, None
        try:
            # org admin login
            cookies, user_name = self.org_admin_login()

            # get User OrgId
            org_id = self.get_auto_org_dev_id(cookies, user_name)

            # add a project
            project_name = 'test_project_' + util.random_str(10)
            project_description = util.random_str(20)
            project_created = cloud_platform_helper.create_project(org_id, project_name, project_description, cookies)
            assert project_created['displayName'] == project_name
            assert project_created['description'] == project_description
            assert project_created['orgId'] == org_id
            project_id = project_created['id']

            # search all the projects
            projects = cloud_platform_helper.search_projects(org_id, None, 0, 0, cookies)
            assert projects['total'] > 0
            project_list = projects['list']
            assert len(project_list) > 0
            assert project_list[0]['displayName'] == project_name
            assert project_list[0]['description'] == project_description
            assert project_list[0]['orgId'] == org_id

            # search projects with project name
            projects = cloud_platform_helper.search_projects(org_id, project_name, 0, 0, cookies)
            assert projects['total'] == 1
            project_list = projects['list']
            assert len(project_list) == 1
            assert project_list[0]['displayName'] == project_name
            assert project_list[0]['description'] == project_description
            assert project_list[0]['orgId'] == org_id

        finally:
            # delete the created org and the project
            response = cloud_platform_helper.delete_project_by_id(org_id, project_id, cookies)
            assert success_message in response['message']
            cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_upload_package_new(self):
        org_id, project_id, package_id, cookies = None, None, None, None
        try:
            # org admin login
            cookies, user_name = self.org_admin_login()

            # get User OrgId
            org_id = self.get_auto_org_dev_id(cookies, user_name)

            # add a project
            project_name = 'test_project_' + util.random_str(10)
            project_description = util.random_str(20)
            project_created = cloud_platform_helper.create_project(org_id, project_name, project_description, cookies)
            assert project_created['displayName'] == project_name
            assert project_created['description'] == project_description
            assert project_created['orgId'] == org_id
            project_id = project_created['id']

            # 上传文件流程函数
            file_name = 'server.zip'
            version = "0.0.1"
            package_id = cloud_platform_helper.upload_file_progress(cookies, org_id, project_id, file_name, version)
            assert package_id is not None
        finally:
            if package_id:
                # delete the project
                cloud_platform_helper.delete_package_by_id(org_id, package_id, cookies)
            response = cloud_platform_helper.delete_project_by_id(org_id, project_id, cookies)
            assert success_message in response['message']
            cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_delete_package(self):
        org_id, project_id, cookies, package_id = None, None, None, None
        try:
            # org admin login
            cookies, user_name = self.org_admin_login()

            # get User OrgId
            org_id = self.get_auto_org_dev_id(cookies, user_name)

            # add a project
            project_name = 'test_project_' + util.random_str(10)
            project_description = util.random_str(20)
            project_created = cloud_platform_helper.create_project(org_id, project_name, project_description, cookies)
            assert project_created['displayName'] == project_name
            assert project_created['description'] == project_description
            assert project_created['orgId'] == org_id
            project_id = project_created['id']

            # 上传文件流程函数
            file_name = 'server.zip'
            version = "0.0.1"
            package_id = cloud_platform_helper.upload_file_progress(cookies, org_id, project_id, file_name, version)

            # delete the package
            package_response = cloud_platform_helper.delete_package_by_id(org_id, package_id, cookies)
            assert success_message in package_response['message']

            # delete the package with invalid id
            invalid_package_id = util.random_str(10)
            package_response = cloud_platform_helper.delete_package_by_id(org_id, invalid_package_id, cookies)
            # MaxZhang
            # 这里直接报了 {'code': 'InternalServerError', 'message': 'Wrap non AppError', 'body': None}
            assert error_messages['package_not_existed'] in package_response['message']
        finally:
            if package_id:
                # delete the created org and the project
                cloud_platform_helper.delete_package_by_id(org_id, package_id, cookies)
            response = cloud_platform_helper.delete_project_by_id(org_id, project_id, cookies)
            assert success_message in response['message']
            cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_get_package_by_id(self):
        org_id, package_id, cookies, project_id = None, None, None, None
        try:
            # org admin login
            cookies, user_name = self.org_admin_login()

            # get User OrgId
            org_id = self.get_auto_org_dev_id(cookies, user_name)

            # add a project
            project_name = 'test_project_' + util.random_str(10)
            project_description = util.random_str(20)
            project_created = cloud_platform_helper.create_project(org_id, project_name, project_description, cookies)
            assert project_created['displayName'] == project_name
            assert project_created['description'] == project_description
            assert project_created['orgId'] == org_id
            project_id = project_created['id']

            # 上传文件流程函数
            file_name = 'server.zip'
            version = "0.0.1"
            package_id = cloud_platform_helper.upload_file_progress(cookies, org_id, project_id, file_name, version)

            # get the package with invalid id
            invalid_package_id = util.random_str(10)
            package_response = cloud_platform_helper.get_package_by_id(org_id, invalid_package_id, cookies)
            # MaxZhang:
            # 直接返回了{'code': 'InternalServerError', 'message': 'Wrap non AppError', 'body': None}
            assert error_messages['package_not_existed'] in package_response['message']

            invalid_org_id = util.random_str(10)
            package_response = cloud_platform_helper.get_package_by_id(invalid_org_id, package_id, cookies)
            # MaxZhang:
            # 直接返回了 {'code': '403', 'message': '无权访问', 'body': None}
            assert error_messages['org_not_existed'] in package_response['message']

            # get the package
            package_response = cloud_platform_helper.get_package_by_id(org_id, package_id, cookies)
            assert success_message in package_response['message']
            package_response['body']['displayName'] = file_name
        finally:
            # delete the created org and the project
            cloud_platform_helper.delete_package_by_id(org_id, package_id, cookies)
            response = cloud_platform_helper.delete_project_by_id(org_id, project_id, cookies)
            assert success_message in response['message']
            cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_search_packages(self):
        org_id, package_id, cookies, project_id = None, None, None, None
        try:
            # org admin login
            cookies, user_name = self.org_admin_login()

            # get User OrgId
            org_id = self.get_auto_org_dev_id(cookies, user_name)

            # add a project
            project_name = 'test_project_' + util.random_str(10)
            project_description = util.random_str(20)
            project_created = cloud_platform_helper.create_project(org_id, project_name, project_description, cookies)
            assert project_created['displayName'] == project_name
            assert project_created['description'] == project_description
            assert project_created['orgId'] == org_id
            project_id = project_created['id']

            # 上传文件流程函数
            file_name = 'server.zip'
            version = "0.0.1"
            package_id = cloud_platform_helper.upload_file_progress(cookies, org_id, project_id, file_name, version)

            # search all the packages
            package_response = cloud_platform_helper.search_packages(org_id, project_id, None, None,
                                                                     None, 0, 0, cookies)
            assert package_response['total'] == 1

            package_list = package_response['list']
            assert len(package_list) == 1
            assert package_list[0]['displayName'] == file_name

            # search the package with name
            package_response = cloud_platform_helper.search_packages(org_id, project_id, file_name, version,
                                                                     None, 0, 0, cookies)
            assert package_response['total'] == 1

            package_list = package_response['list']
            assert len(package_list) == 1
            assert package_list[0]['displayName'] == file_name

            # search with invalid name and type
            package_response = cloud_platform_helper.search_packages(org_id, project_id, 'invalid_name', None,
                                                                     'invalid_type', 0, 0, cookies)
            assert package_response['total'] == 0
        finally:
            # delete the project
            response = cloud_platform_helper.delete_project_by_id(org_id, project_id, cookies)
            assert success_message in response['message']
            cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_create_dev_application(self):
        org_id, project_id, pool_id, package_id, dev_app_id, cookies = None, None, None, None, None, None
        try:
            # 创建resource pool资源
            # 只有admin才可获取资源，因此先登录admin
            cookies, username = self.admin_login()
            pool_id = self.add_resource_pool_for_dev_app(cookies)

            # org admin login
            cookies, user_name = self.org_admin_login()

            # get User OrgId
            org_id = self.get_auto_org_dev_id(cookies, user_name)

            # add a project
            project_name = 'test_project_' + util.random_str(10)
            project_description = util.random_str(20)
            project_created = cloud_platform_helper.create_project(org_id, project_name, project_description, cookies)
            assert project_created['displayName'] == project_name
            assert project_created['description'] == project_description
            assert project_created['orgId'] == org_id
            project_id = project_created['id']

            # 上传游戏包
            file_name = 'server.zip'
            version = "0.0.1"
            package_id = cloud_platform_helper.upload_file_progress(cookies, org_id, project_id, file_name, version)
            assert package_id is not None

            # add an dev app
            dev_app_name = "dev_app_" + util.random_str(10)
            dev_app_description = "dev_app_" + util.random_str(20)

            dev_app_response = cloud_platform_helper.create_dev_application(org_id, project_id, dev_app_name,
                                                                            dev_app_description, package_id, pool_id,
                                                                            cookies)
            assert success_message in dev_app_response['message']
            dev_app = dev_app_response['body']
            dev_app_id = dev_app['id']

        finally:
            project_response = cloud_platform_helper.delete_project_by_id(org_id, project_id, cookies)
            pool_response = cloud_platform_helper.org_delete_resource_pool_by_id(pool_id, cookies)
            cloud_platform_helper.user_logout(cookies)

            assert success_message in pool_response['message']
            assert success_message in project_response['message']


    @pytest.mark.daily
    def test_create_dev_application_invalid_data(self):
        org_id, project_id, pool_id, package_id, cookies = None, None, None, None, None
        try:
            # 创建resource pool资源
            # 只有admin才可获取资源，因此先登录admin
            cookies, username = self.admin_login()
            pool_id = self.add_resource_pool_for_dev_app(cookies)

            # org admin login
            cookies, user_name = self.org_admin_login()

            # get User OrgId
            org_id = self.get_auto_org_dev_id(cookies, user_name)

            # add a project
            project_name = 'test_project_' + util.random_str(10)
            project_description = util.random_str(20)
            project_created = cloud_platform_helper.create_project(org_id, project_name, project_description, cookies)
            assert project_created['displayName'] == project_name
            assert project_created['description'] == project_description
            assert project_created['orgId'] == org_id
            project_id = project_created['id']

            # 上传游戏包
            file_name = 'server.zip'
            version = "0.0.1"
            package_id = cloud_platform_helper.upload_file_progress(cookies, org_id, project_id, file_name, version)
            assert package_id is not None

            # add an dev app
            dev_app_name = "dev_app_" + util.random_str(10)
            dev_app_description = "dev_app_" + util.random_str(20)

            # invalid_dev_app_name
            invalid_dev_app_name = ""
            dev_app_response1 = cloud_platform_helper.create_dev_application(org_id, project_id, invalid_dev_app_name,
                                                                             dev_app_description, package_id, pool_id,
                                                                             cookies)
            assert error_messages['display_name_required'] in dev_app_response1['message']

            invalid_package_id = "invalid_package_id"
            dev_app_response2 = cloud_platform_helper.create_dev_application(org_id, project_id, dev_app_name,
                                                                             dev_app_description, invalid_package_id,
                                                                             pool_id, cookies)
            # MaxZhang：
            # {'code': 'InternalServerError', 'message': 'Wrap non AppError', 'body': None}
            assert fail_message in dev_app_response2['message']

            invalid_pool_id = "invalid_pool_id"
            dev_app_response3 = cloud_platform_helper.create_dev_application(org_id, project_id, dev_app_name,
                                                                             dev_app_description, package_id,
                                                                             invalid_pool_id, cookies)
            # MaxZhang：
            # {'code': 'InternalServerError', 'message': 'Wrap non AppError', 'body': None}
            assert fail_message in dev_app_response3['message']
        finally:
            project_response = cloud_platform_helper.delete_project_by_id(org_id, project_id, cookies)
            pool_response = cloud_platform_helper.org_delete_resource_pool_by_id(pool_id, cookies)
            cloud_platform_helper.user_logout(cookies)

            assert success_message in pool_response['message']
            assert success_message in project_response['message']

    @pytest.mark.daily
    def test_update_dev_application(self):
        org_id, project_id, pool_id, package_id, dev_app_id, cookies = None, None, None, None, None, None
        try:
            # 创建resource pool资源
            # 只有admin才可获取资源，因此先登录admin
            cookies, username = self.admin_login()
            pool_id = self.add_resource_pool_for_dev_app(cookies)

            # org admin login
            cookies, user_name = self.org_admin_login()

            # get User OrgId
            org_id = self.get_auto_org_dev_id(cookies, user_name)

            # add a project
            project_name = 'test_project_' + util.random_str(10)
            project_description = util.random_str(20)
            project_created = cloud_platform_helper.create_project(org_id, project_name, project_description, cookies)
            assert project_created['displayName'] == project_name
            assert project_created['description'] == project_description
            assert project_created['orgId'] == org_id
            project_id = project_created['id']

            # 上传游戏包
            file_name = 'server.zip'
            version = "0.0.1"
            package_id = cloud_platform_helper.upload_file_progress(cookies, org_id, project_id, file_name, version)
            assert package_id is not None

            # add an dev app
            dev_app_name = "dev_app_" + util.random_str(10)
            dev_app_description = "dev_app_" + util.random_str(20)

            dev_app_response = cloud_platform_helper.create_dev_application(org_id, project_id, dev_app_name,
                                                                            dev_app_description, package_id, pool_id,
                                                                            cookies)
            assert success_message in dev_app_response['message']
            dev_app = dev_app_response['body']
            dev_app_id = dev_app['id']

            new_dev_app_description = "new_description" + dev_app_description

            update_app_response = cloud_platform_helper.update_dev_application(org_id, dev_app_id, dev_app_name,
                                                                               new_dev_app_description, package_id,
                                                                               pool_id, cookies)
            assert success_message in update_app_response['message']
            assert update_app_response['body']['description'] == new_dev_app_description
        finally:
            project_response = cloud_platform_helper.delete_project_by_id(org_id, project_id, cookies)
            pool_response = cloud_platform_helper.org_delete_resource_pool_by_id(pool_id, cookies)
            cloud_platform_helper.user_logout(cookies)

            assert success_message in pool_response['message']
            assert success_message in project_response['message']

    @pytest.mark.daily
    def test_update_dev_application_invalid_data(self):
        org_id, project_id, pool_id, package_id, dev_app_id, cookies = None, None, None, None, None, None
        try:
            # 创建resource pool资源
            # 只有admin才可获取资源，因此先登录admin
            cookies, username = self.admin_login()
            pool_id = self.add_resource_pool_for_dev_app(cookies)

            # org admin login
            cookies, user_name = self.org_admin_login()

            # get User OrgId
            org_id = self.get_auto_org_dev_id(cookies, user_name)

            # add a project
            project_name = 'test_project_' + util.random_str(10)
            project_description = util.random_str(20)
            project_created = cloud_platform_helper.create_project(org_id, project_name, project_description, cookies)
            assert project_created['displayName'] == project_name
            assert project_created['description'] == project_description
            assert project_created['orgId'] == org_id
            project_id = project_created['id']

            # 上传游戏包
            file_name = 'server.zip'
            version = "0.0.1"
            package_id = cloud_platform_helper.upload_file_progress(cookies, org_id, project_id, file_name, version)
            assert package_id is not None

            # add an dev app
            dev_app_name = "dev_app_" + util.random_str(10)
            dev_app_description = "dev_app_" + util.random_str(20)

            dev_app_response = cloud_platform_helper.create_dev_application(org_id, project_id, dev_app_name,
                                                                            dev_app_description, package_id, pool_id,
                                                                            cookies)
            assert success_message in dev_app_response['message']
            dev_app = dev_app_response['body']
            dev_app_id = dev_app['id']

            invalid_dev_app_name = ""
            update_app_response = cloud_platform_helper.update_dev_application(org_id, dev_app_id, invalid_dev_app_name,
                                                                               dev_app_description, package_id,
                                                                               pool_id, cookies)
            assert error_messages['display_name_required'] in update_app_response['message']

        finally:
            project_response = cloud_platform_helper.delete_project_by_id(org_id, project_id, cookies)
            pool_response = cloud_platform_helper.org_delete_resource_pool_by_id(pool_id, cookies)
            cloud_platform_helper.user_logout(cookies)

            assert success_message in pool_response['message']
            assert success_message in project_response['message']

    @pytest.mark.daily
    def test_search_dev_application(self):
        org_id, project_id, pool_id, package_id, dev_app_id, cookies = None, None, None, None, None, None
        try:
            # 创建resource pool资源
            # 只有admin才可获取资源，因此先登录admin
            cookies, username = self.admin_login()
            pool_id = self.add_resource_pool_for_dev_app(cookies)

            # org admin login
            cookies, user_name = self.org_admin_login()

            # get User OrgId
            org_id = self.get_auto_org_dev_id(cookies, user_name)

            # add a project
            project_name = 'test_project_' + util.random_str(10)
            project_description = util.random_str(20)
            project_created = cloud_platform_helper.create_project(org_id, project_name, project_description, cookies)
            assert project_created['displayName'] == project_name
            assert project_created['description'] == project_description
            assert project_created['orgId'] == org_id
            project_id = project_created['id']

            # 上传游戏包
            file_name = 'server.zip'
            version = "0.0.1"
            package_id = cloud_platform_helper.upload_file_progress(cookies, org_id, project_id, file_name, version)
            assert package_id is not None

            # add an dev app
            dev_app_name = "dev_app_" + util.random_str(10)
            dev_app_description = "dev_app_" + util.random_str(20)

            dev_app_response = cloud_platform_helper.create_dev_application(org_id, project_id, dev_app_name,
                                                                            dev_app_description, package_id, pool_id,
                                                                            cookies)
            assert success_message in dev_app_response['message']
            dev_app = dev_app_response['body']
            dev_app_id = dev_app['id']

            search_response = cloud_platform_helper.search_apps(org_id, project_id, dev_app_name, 0, 0, cookies,
                                                                env="dev")
            assert success_message in search_response['message']
            assert len(search_response['body']['list']) == 1
            dev_app_searched = search_response['body']['list'][0]

            assert dev_app_searched['id'] == dev_app_id
            assert dev_app_searched['displayName'] == dev_app_name

        finally:
            project_response = cloud_platform_helper.delete_project_by_id(org_id, project_id, cookies)
            pool_response = cloud_platform_helper.org_delete_resource_pool_by_id(pool_id, cookies)
            cloud_platform_helper.user_logout(cookies)

            assert success_message in pool_response['message']
            assert success_message in project_response['message']

    @pytest.mark.daily
    def test_delete_dev_application_by_id(self):
        org_id, project_id, pool_id, package_id, dev_app_id, cookies = None, None, None, None, None, None
        try:
            # 创建resource pool资源
            # 只有admin才可获取资源，因此先登录admin
            cookies, username = self.admin_login()
            pool_id = self.add_resource_pool_for_dev_app(cookies)

            # org admin login
            cookies, user_name = self.org_admin_login()

            # get User OrgId
            org_id = self.get_auto_org_dev_id(cookies, user_name)

            # add a project
            project_name = 'test_project_' + util.random_str(10)
            project_description = util.random_str(20)
            project_created = cloud_platform_helper.create_project(org_id, project_name, project_description, cookies)
            assert project_created['displayName'] == project_name
            assert project_created['description'] == project_description
            assert project_created['orgId'] == org_id
            project_id = project_created['id']

            # 上传游戏包
            file_name = 'server.zip'
            version = "0.0.1"
            package_id = cloud_platform_helper.upload_file_progress(cookies, org_id, project_id, file_name, version)
            assert package_id is not None

            # add an dev app
            dev_app_name = "dev_app_" + util.random_str(10)
            dev_app_description = "dev_app_" + util.random_str(20)

            dev_app_response = cloud_platform_helper.create_dev_application(org_id, project_id, dev_app_name,
                                                                            dev_app_description, package_id, pool_id,
                                                                            cookies)
            assert success_message in dev_app_response['message']
            dev_app = dev_app_response['body']
            dev_app_id = dev_app['id']

            delete_response = cloud_platform_helper.delete_dev_application(org_id, dev_app_id, cookies)
            assert success_message in delete_response['message']
        finally:
            project_response = cloud_platform_helper.delete_project_by_id(org_id, project_id, cookies)
            pool_response = cloud_platform_helper.org_delete_resource_pool_by_id(pool_id, cookies)
            cloud_platform_helper.user_logout(cookies)

            assert success_message in pool_response['message']
            assert success_message in project_response['message']

    # pub applications
    # 用于发布的App
    @pytest.mark.daily
    def test_create_pub_application(self):
        org_id, project_id, cookies = None, None, None
        try:
            cookies, user_name = self.org_admin_login()

            # get User OrgId
            org_id = self.get_auto_org_dev_id(cookies, user_name)

            # add a project
            project_name = 'test_project_' + util.random_str(10)
            project_description = util.random_str(20)
            project_created = cloud_platform_helper.create_project(org_id, project_name, project_description, cookies)
            assert project_created['displayName'] == project_name
            assert project_created['description'] == project_description
            assert project_created['orgId'] == org_id
            project_id = project_created['id']

            cover_key = cloud_platform_helper.create_pub_app_cover_image_progress(project_id, cookies)
            discription = "test_app_description" + util.random_str(10)
            display_name = "test_app_display_name" + util.random_str(10)
            game_name = "test_app_game_name" + util.random_str(10)

            response = cloud_platform_helper.create_pub_application(project_id, cover_key, discription,
                                                                    display_name, game_name, cookies)

            assert response.get('message') is not None and success_message in response.get('message')
        finally:
            # delete the project
            response = cloud_platform_helper.delete_project_by_id(org_id, project_id, cookies)
            assert success_message in response['message']
            cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_create_pub_application_invalid_data(self):
        org_id, project_id, cookies = None, None, None
        try:
            cookies, user_name = self.org_admin_login()

            # get User OrgId
            org_id = self.get_auto_org_dev_id(cookies, user_name)

            # add a project
            project_name = 'test_project_' + util.random_str(10)
            project_description = util.random_str(20)
            project_created = cloud_platform_helper.create_project(org_id, project_name, project_description, cookies)
            assert project_created['displayName'] == project_name
            assert project_created['description'] == project_description
            assert project_created['orgId'] == org_id
            project_id = project_created['id']

            cover_key = cloud_platform_helper.create_pub_app_cover_image_progress(project_id, cookies)
            discription = "test_app_description" + util.random_str(10)
            display_name = ""
            game_name = "test_app_game_name" + util.random_str(10)

            response = cloud_platform_helper.create_pub_application(project_id, cover_key, discription,
                                                                    display_name, game_name, cookies)
            assert response.get('message') is not None and \
                   error_messages['display_name_required'] in response.get('message')

        finally:
            # delete the project
            response = cloud_platform_helper.delete_project_by_id(org_id, project_id, cookies)
            assert success_message in response['message']
            cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_search_pub_applications(self):
        org_id, project_id, cookies = None, None, None
        try:
            cookies, user_name = self.org_admin_login()

            # get User OrgId
            org_id = self.get_auto_org_dev_id(cookies, user_name)

            # add a project
            project_name = 'test_project_' + util.random_str(10)
            project_description = util.random_str(20)
            project_created = cloud_platform_helper.create_project(org_id, project_name, project_description, cookies)
            assert project_created['displayName'] == project_name
            assert project_created['description'] == project_description
            assert project_created['orgId'] == org_id
            project_id = project_created['id']

            # add app
            cover_key = cloud_platform_helper.create_pub_app_cover_image_progress(project_id, cookies)
            discription = "test_app_description" + util.random_str(10)
            display_name = "test_app_display_name" + util.random_str(10)
            game_name = "test_app_game_name" + util.random_str(10)

            response = cloud_platform_helper.create_pub_application(project_id, cover_key, discription,
                                                                    display_name, game_name, cookies)

            assert response.get('message') is not None and success_message in response.get('message')

            # search app success
            search_response = cloud_platform_helper.search_apps(org_id, project_id, display_name, 0, 0, cookies,
                                                                env="pub")
            assert success_message in search_response.get("message")
            assert type(search_response.get("body")) is dict
            assert search_response.get("body").get("total") == 1

            app = search_response.get("body").get("list")[0]
            assert app.get("displayName") == display_name
            assert app.get("description") == discription
            assert app.get("gameName") == game_name
            assert app.get("orgId") == org_id
            assert app.get("projectId") == project_id

            # search invalid
            invalid_display = "invalid_display" + util.random_str(20)
            search_response = cloud_platform_helper.search_apps(org_id, project_id, invalid_display, 0, 0, cookies)
            assert type(search_response.get("body")) is dict
            assert search_response.get("body").get("total") == 0
        finally:
            # delete the created org and the project
            response = cloud_platform_helper.delete_project_by_id(org_id, project_id, cookies)
            assert success_message in response['message']
            cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_release_pub_application(self):
        org_id, project_id, package_id, pool_id, cookies = None, None, None, None, None
        try:
            # 创建resource pool资源
            # 只有admin才可获取resource相关信息，因此先登录admin
            cookies, username = self.admin_login()
            pool_id = self.add_resource_pool_for_dev_app(cookies)

            # 登录org admin
            cookies, user_name = self.org_admin_login()

            # get User OrgId
            org_id = self.get_auto_org_dev_id(cookies, user_name)

            # add a project
            project_name = 'test_project_' + util.random_str(10)
            project_description = util.random_str(20)
            project_created = cloud_platform_helper.create_project(org_id, project_name, project_description, cookies)
            assert project_created['displayName'] == project_name
            assert project_created['description'] == project_description
            assert project_created['orgId'] == org_id
            project_id = project_created['id']

            # 上传游戏包
            file_name = 'server.zip'
            version = "0.0.1"
            package_id = cloud_platform_helper.upload_file_progress(cookies, org_id, project_id, file_name, version)
            assert package_id is not None

            # 增加 dev app 关联游戏包，以使游戏包就绪
            dev_app_name = "dev_app_" + util.random_str(10)
            dev_app_description = "dev_app_" + util.random_str(20)
            dev_app_response = cloud_platform_helper.create_dev_application(org_id, project_id, dev_app_name,
                                                                            dev_app_description, package_id, pool_id,
                                                                            cookies)
            assert success_message in dev_app_response['message']

            # 等待游戏包分发成功
            pkg_ready = cloud_platform_helper.waiting_package_ready(org_id, project_id, file_name, version, cookies)
            assert pkg_ready is True

            # 上传 pub app 封面
            cover_key = cloud_platform_helper.create_pub_app_cover_image_progress(project_id, cookies)
            discription = "test_app_description" + util.random_str(10)
            display_name = "test_app_display_name" + util.random_str(10)
            game_name = "test_app_game_name" + util.random_str(10)

            # 创建pub app
            create_pub_response = cloud_platform_helper.create_pub_application(project_id, cover_key, discription,
                                                                               display_name, game_name, cookies)

            assert create_pub_response.get('message') is not None and success_message in create_pub_response.get(
                'message')

            # search pub app
            search_pub_response = cloud_platform_helper.search_apps(org_id, project_id, display_name, 0, 0, cookies,
                                                                    env="pub")
            assert success_message in search_pub_response.get("message")
            assert type(search_pub_response.get("body")) is dict
            assert search_pub_response.get("body").get("total") == 1
            pub_app = search_pub_response['body']['list'][0]

            # create release
            release_des = "pub app release description " + util.random_str(20)
            release_version = "0.0.1"

            plan_response = cloud_platform_helper.plan_release(pub_app, release_des, release_version, package_id,
                                                               pool_id, username, cookies)
            assert success_message in plan_response['message']

            # search release
            release_search_response = cloud_platform_helper.get_pub_app_releases(pub_app['id'], cookies)
            assert success_message in release_search_response['message']
            assert len(release_search_response['body']['list']) == 1

            release_obj = release_search_response['body']['list'][0]
            assert release_obj['appId'] == pub_app['id']

            # release 提交审核
            submit_response = cloud_platform_helper.submit_pub_app_release_for_audit(release_obj['id'], cookies)
            assert success_message in submit_response['message']

            # 登录admin，审核app release
            cookies, username = self.admin_login()

            # admin 开始审核
            start_audit_response = cloud_platform_helper.admin_start_audit_release(release_obj['id'], cookies)
            assert success_message in start_audit_response['message']

            # admin 通过审核
            pass_audit_response = cloud_platform_helper.admin_pass_audit_release(release_obj['id'], cookies)
            assert success_message in pass_audit_response['message']

            # search release again
            release_search_response2 = cloud_platform_helper.get_pub_app_releases(pub_app['id'], cookies)
            assert success_message in release_search_response2['message']
            assert len(release_search_response2['body']['list']) == 1
            release_obj2 = release_search_response2['body']['list'][0]
            # check release status is passed
            assert release_obj2['status'] == 'passed'
        finally:
            # 登录org admin 以删除org admin创建的资源
            cookies, user_name = self.org_admin_login()
            project_response = cloud_platform_helper.delete_project_by_id(org_id, project_id, cookies)
            pool_response = cloud_platform_helper.org_delete_resource_pool_by_id(pool_id, cookies)
            assert success_message in project_response['message']
            assert success_message in pool_response['message']
            cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_reject_release_pub_application(self):
        org_id, project_id, package_id, pool_id, cookies = None, None, None, None, None
        try:
            # 创建resource pool资源
            # 只有admin才可获取资源，因此先登录admin
            cookies, username = self.admin_login()
            pool_id = self.add_resource_pool_for_dev_app(cookies)

            # 登录org admin
            cookies, user_name = self.org_admin_login()

            # get User OrgId
            org_id = self.get_auto_org_dev_id(cookies, user_name)

            # add a project
            project_name = 'test_project_' + util.random_str(10)
            project_description = util.random_str(20)
            project_created = cloud_platform_helper.create_project(org_id, project_name, project_description, cookies)
            assert project_created['displayName'] == project_name
            assert project_created['description'] == project_description
            assert project_created['orgId'] == org_id
            project_id = project_created['id']

            # 上传游戏包
            file_name = 'server.zip'
            version = "0.0.1"
            package_id = cloud_platform_helper.upload_file_progress(cookies, org_id, project_id, file_name, version)
            assert package_id is not None

            # 增加 dev app 关联游戏包，以使游戏包就绪
            dev_app_name = "dev_app_" + util.random_str(10)
            dev_app_description = "dev_app_" + util.random_str(20)
            dev_app_response = cloud_platform_helper.create_dev_application(org_id, project_id, dev_app_name,
                                                                            dev_app_description, package_id, pool_id,
                                                                            cookies)
            assert success_message in dev_app_response['message']

            # 等待游戏包分发成功
            pkg_ready = cloud_platform_helper.waiting_package_ready(org_id, project_id, file_name, version, cookies)
            assert pkg_ready is True

            # 上传 pub app 封面
            cover_key = cloud_platform_helper.create_pub_app_cover_image_progress(project_id, cookies)
            discription = "test_app_description" + util.random_str(10)
            display_name = "test_app_display_name" + util.random_str(10)
            game_name = "test_app_game_name" + util.random_str(10)

            # 创建pub app
            create_pub_response = cloud_platform_helper.create_pub_application(project_id, cover_key, discription,
                                                                               display_name, game_name, cookies)

            assert create_pub_response.get('message') is not None and success_message in create_pub_response.get(
                'message')

            # search pub app
            search_pub_response = cloud_platform_helper.search_apps(org_id, project_id, display_name, 0, 0, cookies,
                                                                    env="pub")
            assert success_message in search_pub_response.get("message")
            assert type(search_pub_response.get("body")) is dict
            assert search_pub_response.get("body").get("total") == 1
            pub_app = search_pub_response['body']['list'][0]

            # create release
            release_des = "pub app release description " + util.random_str(20)
            release_version = "0.0.1"

            plan_response = cloud_platform_helper.plan_release(pub_app, release_des, release_version, package_id,
                                                               pool_id, username, cookies)
            assert success_message in plan_response['message']

            # search release
            release_search_response = cloud_platform_helper.get_pub_app_releases(pub_app['id'], cookies)
            assert success_message in release_search_response['message']
            assert len(release_search_response['body']['list']) == 1

            release_obj = release_search_response['body']['list'][0]
            assert release_obj['appId'] == pub_app['id']

            # release 提交审核
            submit_response = cloud_platform_helper.submit_pub_app_release_for_audit(release_obj['id'], cookies)
            assert success_message in submit_response['message']

            # 登录admin，审核app release
            cookies, username = self.admin_login()

            # admin 开始审核
            start_audit_response = cloud_platform_helper.admin_start_audit_release(release_obj['id'], cookies)
            assert success_message in start_audit_response['message']

            # 查询驳回原因
            reject_option_response = cloud_platform_helper.admin_get_reject_options(cookies)
            assert len(reject_option_response['body']) > 0

            reject_option = reject_option_response['body'][0]
            reject_reason_id = reject_option['id']
            reject_text = reject_option['name']

            # admin 驳回审核
            rejected_audit_response = cloud_platform_helper.admin_reject_audit_release(release_obj['id'],
                                                                                       reject_reason_id, reject_text,
                                                                                       cookies)
            assert success_message in rejected_audit_response['message']

            # search release again
            release_search_response2 = cloud_platform_helper.get_pub_app_releases(pub_app['id'], cookies)
            assert success_message in release_search_response2['message']
            assert len(release_search_response2['body']['list']) == 1
            release_obj2 = release_search_response2['body']['list'][0]
            # check release status is passed
            assert release_obj2['status'] == 'rejected'
        finally:
            # 登录org admin 以删除org admin创建的资源
            cookies, user_name = self.org_admin_login()

            project_response = cloud_platform_helper.delete_project_by_id(org_id, project_id, cookies)
            pool_response = cloud_platform_helper.org_delete_resource_pool_by_id(pool_id, cookies)
            assert success_message in project_response['message']
            assert success_message in pool_response['message']
            cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_create_release_invalid_data(self):
        org_id, project_id, package_id, pool_id, cookies = None, None, None, None, None
        try:
            # 创建resource pool
            # 只有admin才可获取资源，因此先登录admin
            cookies, username = self.admin_login()
            pool_id = self.add_resource_pool_for_dev_app(cookies)

            # 登录org admin
            cookies, user_name = self.org_admin_login()

            # get User OrgId
            org_id = self.get_auto_org_dev_id(cookies, user_name)

            # add a project
            project_name = 'test_project_' + util.random_str(10)
            project_description = util.random_str(20)
            project_created = cloud_platform_helper.create_project(org_id, project_name, project_description, cookies)
            assert project_created['displayName'] == project_name
            assert project_created['description'] == project_description
            assert project_created['orgId'] == org_id
            project_id = project_created['id']

            # 上传游戏包
            file_name = 'server.zip'
            version = "0.0.1"
            package_id = cloud_platform_helper.upload_file_progress(cookies, org_id, project_id, file_name, version)
            assert package_id is not None

            # 上传 pub app 封面
            cover_key = cloud_platform_helper.create_pub_app_cover_image_progress(project_id, cookies)
            discription = "test_app_description" + util.random_str(10)
            display_name = "test_app_display_name" + util.random_str(10)
            game_name = "test_app_game_name" + util.random_str(10)

            # 创建pub app
            create_pub_response = cloud_platform_helper.create_pub_application(project_id, cover_key, discription,
                                                                               display_name, game_name, cookies)

            assert create_pub_response.get('message') is not None and success_message in create_pub_response.get(
                'message')

            # search pub app
            search_pub_response = cloud_platform_helper.search_apps(org_id, project_id, display_name, 0, 0, cookies,
                                                                    env="pub")
            assert success_message in search_pub_response.get("message")
            assert type(search_pub_response.get("body")) is dict
            assert search_pub_response.get("body").get("total") == 1
            pub_app = search_pub_response['body']['list'][0]

            # invalid test 1: 测试游戏包未就绪
            release_des = "pub app release description " + util.random_str(20)
            release_version = "0.0.1"

            plan_response = cloud_platform_helper.plan_release(pub_app, release_des, release_version, package_id,
                                                               pool_id, username, cookies)
            assert error_messages['package_not_ready'] in plan_response['message']

            # 增加 dev app 关联游戏包，以使游戏包就绪
            dev_app_name = "dev_app_" + util.random_str(10)
            dev_app_description = "dev_app_" + util.random_str(20)
            dev_app_response = cloud_platform_helper.create_dev_application(org_id, project_id, dev_app_name,
                                                                            dev_app_description, package_id, pool_id,
                                                                            cookies)
            assert success_message in dev_app_response['message']

            # 等待游戏包分发成功
            pkg_ready = cloud_platform_helper.waiting_package_ready(org_id, project_id, file_name, version, cookies)
            assert pkg_ready is True

            # invalid test 2: invalid pool_id
            invalid_pool_id = "invalid_pool_id"
            plan_response = cloud_platform_helper.plan_release(pub_app, release_des, release_version, package_id,
                                                               invalid_pool_id, username, cookies)
            # maxzhang: 后端返回{'code': 'InternalServerError', 'message': 'Wrap non AppError', 'body': None}
            assert error_messages['pool_not_existed'] in plan_response['message']

            # invalid test 3: 测试invalid_version
            invalid_version = "0.0.1.invalid_version"

            # maxzhang: 后端未检查，返回success
            plan_response = cloud_platform_helper.plan_release(pub_app, release_des, invalid_version, package_id,
                                                               pool_id, username, cookies)
            assert error_messages['invalid_releaser_version'] in plan_response['message']

        finally:
            # 登录org admin 以删除org admin创建的资源
            cookies, user_name = self.org_admin_login()
            project_response = cloud_platform_helper.delete_project_by_id(org_id, project_id, cookies)
            pool_response = cloud_platform_helper.org_delete_resource_pool_by_id(pool_id, cookies)
            assert success_message in project_response['message']
            assert success_message in pool_response['message']
            cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_submit_audit_release_invalid_data(self):
        org_id, project_id, package_id, pool_id, cookies = None, None, None, None, None
        try:
            # 创建resource pool资源
            # 只有admin才可获取资源，因此先登录admin
            cookies, username = self.admin_login()
            pool_id = self.add_resource_pool_for_dev_app(cookies)

            # 登录org admin
            cookies, user_name = self.org_admin_login()

            # get User OrgId
            org_id = self.get_auto_org_dev_id(cookies, user_name)

            # add a project
            project_name = 'test_project_' + util.random_str(10)
            project_description = util.random_str(20)
            project_created = cloud_platform_helper.create_project(org_id, project_name, project_description, cookies)
            assert project_created['displayName'] == project_name
            assert project_created['description'] == project_description
            assert project_created['orgId'] == org_id
            project_id = project_created['id']

            # 上传游戏包
            file_name = 'server.zip'
            version = "0.0.1"
            package_id = cloud_platform_helper.upload_file_progress(cookies, org_id, project_id, file_name, version)
            assert package_id is not None

            # 增加 dev app 关联游戏包，以使游戏包就绪
            dev_app_name = "dev_app_" + util.random_str(10)
            dev_app_description = "dev_app_" + util.random_str(20)
            dev_app_response = cloud_platform_helper.create_dev_application(org_id, project_id, dev_app_name,
                                                                            dev_app_description, package_id, pool_id,
                                                                            cookies)
            assert success_message in dev_app_response['message']

            # 等待游戏包分发成功
            pkg_ready = cloud_platform_helper.waiting_package_ready(org_id, project_id, file_name, version, cookies)
            assert pkg_ready is True

            # 上传 pub app 封面
            cover_key = cloud_platform_helper.create_pub_app_cover_image_progress(project_id, cookies)
            discription = "test_app_description" + util.random_str(10)
            display_name = "test_app_display_name" + util.random_str(10)
            game_name = "test_app_game_name" + util.random_str(10)

            # 创建pub app
            create_pub_response = cloud_platform_helper.create_pub_application(project_id, cover_key, discription,
                                                                               display_name, game_name, cookies)

            assert create_pub_response.get('message') is not None and success_message in create_pub_response.get(
                'message')

            # search pub app
            search_pub_response = cloud_platform_helper.search_apps(org_id, project_id, display_name, 0, 0, cookies,
                                                                    env="pub")
            assert success_message in search_pub_response.get("message")
            assert type(search_pub_response.get("body")) is dict
            assert search_pub_response.get("body").get("total") == 1
            pub_app = search_pub_response['body']['list'][0]

            # create release
            release_des = "pub app release description " + util.random_str(20)
            release_version = "0.0.1"

            plan_response = cloud_platform_helper.plan_release(pub_app, release_des, release_version, package_id,
                                                               pool_id, username, cookies)
            assert success_message in plan_response['message']

            # search release
            release_search_response = cloud_platform_helper.get_pub_app_releases(pub_app['id'], cookies)
            assert success_message in release_search_response['message']
            assert len(release_search_response['body']['list']) == 1

            release_obj = release_search_response['body']['list'][0]
            assert release_obj['appId'] == pub_app['id']

            # invalid test: release 提交invalid release id审核
            invalid_release_id = "invalid_release_id"
            # maxzhang: 后端直接返回了{'code': 'InternalServerError', 'message': 'Wrap non AppError', 'body': None}
            submit_response = cloud_platform_helper.submit_pub_app_release_for_audit(invalid_release_id, cookies)
            assert error_messages['release_not_exist'] in submit_response['message']
        finally:
            # 登录org admin 以删除org admin创建的资源
            cookies, user_name = self.org_admin_login()

            project_response = cloud_platform_helper.delete_project_by_id(org_id, project_id, cookies)
            pool_response = cloud_platform_helper.org_delete_resource_pool_by_id(pool_id, cookies)
            assert success_message in project_response['message']
            assert success_message in pool_response['message']
            cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_reject_release_invalid_reason(self):
        org_id, project_id, package_id, pool_id, dev_app_id, cookies = None, None, None, None, None, None
        try:
            # 创建resource pool资源
            # 只有admin才可获取资源，因此先登录admin
            cookies, username = self.admin_login()
            pool_id = self.add_resource_pool_for_dev_app(cookies)

            # 登录org admin
            cookies, user_name = self.org_admin_login()

            # get User OrgId
            org_id = self.get_auto_org_dev_id(cookies, user_name)

            # add a project
            project_name = 'test_project_' + util.random_str(10)
            project_description = util.random_str(20)
            project_created = cloud_platform_helper.create_project(org_id, project_name, project_description, cookies)
            assert project_created['displayName'] == project_name
            assert project_created['description'] == project_description
            assert project_created['orgId'] == org_id
            project_id = project_created['id']

            # 上传游戏包
            file_name = 'server.zip'
            version = "0.0.1"
            package_id = cloud_platform_helper.upload_file_progress(cookies, org_id, project_id, file_name, version)
            assert package_id is not None

            # 增加 dev app 关联游戏包，以使游戏包就绪
            dev_app_name = "dev_app_" + util.random_str(10)
            dev_app_description = "dev_app_" + util.random_str(20)
            dev_app_response = cloud_platform_helper.create_dev_application(org_id, project_id, dev_app_name,
                                                                            dev_app_description, package_id, pool_id,
                                                                            cookies)
            assert success_message in dev_app_response['message']
            dev_app_id = dev_app_response['body']['id']

            # 等待游戏包分发成功
            pkg_ready = cloud_platform_helper.waiting_package_ready(org_id, project_id, file_name, version, cookies)
            assert pkg_ready is True

            # 上传 pub app 封面
            cover_key = cloud_platform_helper.create_pub_app_cover_image_progress(project_id, cookies)
            discription = "test_app_description" + util.random_str(10)
            display_name = "test_app_display_name" + util.random_str(10)
            game_name = "test_app_game_name" + util.random_str(10)

            # 创建pub app
            create_pub_response = cloud_platform_helper.create_pub_application(project_id, cover_key, discription,
                                                                               display_name, game_name, cookies)

            assert create_pub_response.get('message') is not None and success_message in create_pub_response.get(
                'message')

            # search pub app
            search_pub_response = cloud_platform_helper.search_apps(org_id, project_id, display_name, 0, 0, cookies,
                                                                    env="pub")
            assert success_message in search_pub_response.get("message")
            assert type(search_pub_response.get("body")) is dict
            assert search_pub_response.get("body").get("total") == 1
            pub_app = search_pub_response['body']['list'][0]

            # create release
            release_des = "pub app release description " + util.random_str(20)
            release_version = "0.0.1"

            plan_response = cloud_platform_helper.plan_release(pub_app, release_des, release_version, package_id,
                                                               pool_id, username, cookies)
            assert success_message in plan_response['message']

            # search release
            release_search_response = cloud_platform_helper.get_pub_app_releases(pub_app['id'], cookies)
            assert success_message in release_search_response['message']
            assert len(release_search_response['body']['list']) == 1

            release_obj = release_search_response['body']['list'][0]
            assert release_obj['appId'] == pub_app['id']

            # release 提交审核
            submit_response = cloud_platform_helper.submit_pub_app_release_for_audit(release_obj['id'], cookies)
            assert success_message in submit_response['message']

            # 登录admin，审核app release
            cookies, username = self.admin_login()

            # admin 开始审核
            start_audit_response = cloud_platform_helper.admin_start_audit_release(release_obj['id'], cookies)
            assert success_message in start_audit_response['message']

            invalid_reject_reason_id = "invalid_reason_id"
            reject_text = "just reject!!!"

            # admin 驳回审核
            rejected_audit_response = cloud_platform_helper.admin_reject_audit_release(release_obj['id'],
                                                                                       invalid_reject_reason_id,
                                                                                       reject_text, cookies)
            assert error_messages['operation_failed'] in rejected_audit_response['message']
        finally:
            # 登录org admin 以删除org admin创建的资源
            cookies, user_name = self.org_admin_login()

            delete_dev_response = cloud_platform_helper.delete_dev_application(org_id, dev_app_id, cookies)
            project_response = cloud_platform_helper.delete_project_by_id(org_id, project_id, cookies)

            # maxzhang: BUG
            # release被submit后，如果admin点了开始审核，但是没有进一步通过或驳回的话，
            # 会导致resource_pool无法被删除
            pool_response = cloud_platform_helper.org_delete_resource_pool_by_id(pool_id, cookies)

            assert success_message in delete_dev_response['message']
            assert success_message in project_response['message']
            assert success_message in pool_response['message']
            cloud_platform_helper.user_logout(cookies)
