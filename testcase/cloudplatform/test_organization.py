import logging

import pytest
import datahelper.cloudplatform as cloud_platform_helper
import common.utility as util

automation_org_admin, automation_org_dev = util.get_pre_configured_org()
error_messages = {
    'account_required': 'account为必填字段',
    'invalid_email': 'email必须是一个有效的邮箱',
    'user_not_existed': 'user id 不存在',
    'org_name_required': 'org name为必填字段',
    'org_not_existed': 'org id 不存在',
    'relate_type_too_big': 'relatetype必须小于或等于2 ; ',
    'user_not_found': '用户不存在',
}
success_message = 'success'
fail_message = 'fail'


class TestUserOrg:

    @pytest.mark.bvt
    def test_org_add_search(self):
        org_id, cookies = None, None

        try:
            # user login and get cookies
            user_name, user_pw = util.get_admin_user_name_password()
            public_key = cloud_platform_helper.get_password_public_key()
            user_encrypt_pw = util.get_encrypt_password(public_key, user_pw)

            # get test verify code
            cookies = cloud_platform_helper.user_get_verify_code(None)
            verify_code_response = cloud_platform_helper.user_get_test_verify_code(cookies)
            verify_code = verify_code_response.json()['body']

            cookies = cloud_platform_helper.user_login(user_name, user_encrypt_pw, verify_code, cookies)

            # add an organization
            org_name = 'test_' + util.random_str(10)
            org_description = util.random_str(20)
            cloud_platform_helper.create_org(org_name, org_description, cookies)

            # search organizations without any parameters
            cloud_platform_helper.search_org(None, 0, 0, cookies)

            # search the organization by name
            orgs_return = cloud_platform_helper.search_org(org_name, 0, 0, cookies)
            assert orgs_return['total'] == 1

            org_list = orgs_return['list']
            assert len(org_list) == 1
            assert org_list[0]['name'] == org_name
            assert org_list[0]['description'] == org_description

            # get the organization by ID and then search the organization by its id
            org_id = org_list[0]['id']
            org_return = cloud_platform_helper.get_org_by_id(org_id, cookies)
            assert org_return['name'] == org_name
            assert org_return['description'] == org_description

        finally:
            if org_id:
                # delete the org
                cloud_platform_helper.delete_org_by_id(org_id, cookies)

    @pytest.mark.daily
    def test_org_delete_invalid_data(self):
        org_id, cookies = None, None
        try:
            # user login and get cookies
            user_name, user_pw = util.get_admin_user_name_password()
            public_key = cloud_platform_helper.get_password_public_key()
            user_encrypt_pw = util.get_encrypt_password(public_key, user_pw)

            # get test verify code
            cookies = cloud_platform_helper.user_get_verify_code(None)
            verify_code_response = cloud_platform_helper.user_get_test_verify_code(cookies)
            verify_code = verify_code_response.json()['body']

            cookies = cloud_platform_helper.user_login(user_name, user_encrypt_pw, verify_code, cookies)

            # add an organization
            org_name = 'test_' + util.random_str(10)
            org_description = util.random_str(20)
            cloud_platform_helper.create_org(org_name, org_description, cookies)

            # search organizations without any parameters
            cloud_platform_helper.search_org(None, 0, 0, cookies)

            # search the organization by name
            orgs_return = cloud_platform_helper.search_org(org_name, 0, 0, cookies)
            org_id = orgs_return['list'][0]['id']

            # delete with invalid org id
            invalid_org_id = util.random_str(10)
            org_response = cloud_platform_helper.delete_org_by_id(invalid_org_id, cookies)
            # maxzhang:
            # Response body: {'code': '500', 'message': '操作失败，请稍后重试', 'body': None}
            assert error_messages['org_not_existed'] in org_response['message']
        finally:
            if org_id:
                # delete the org
                cloud_platform_helper.delete_org_by_id(org_id, cookies)

    @pytest.mark.daily
    def test_org_update_delete(self):
        # user login and get cookies
        user_name, user_pw = util.get_admin_user_name_password()
        public_key = cloud_platform_helper.get_password_public_key()
        user_encrypt_pw = util.get_encrypt_password(public_key, user_pw)

        # get test verify code
        cookies = cloud_platform_helper.user_get_verify_code(None)
        verify_code_response = cloud_platform_helper.user_get_test_verify_code(cookies)
        verify_code = verify_code_response.json()['body']

        cookies = cloud_platform_helper.user_login(user_name, user_encrypt_pw, verify_code, cookies)

        # add an organization
        org_name = 'test_' + util.random_str(10)
        org_description = util.random_str(20)
        cloud_platform_helper.create_org(org_name, org_description, cookies)

        # search the organization by name
        orgs_return = cloud_platform_helper.search_org(org_name, 0, 0, cookies)
        assert orgs_return['total'] == 1
        org_id = orgs_return['list'][0]['id']

        # update the org with the new org name and description
        org_new_name = 'test_' + util.random_str(10)
        org_new_description = util.random_str(20)
        cloud_platform_helper.update_org(org_id, org_new_name, org_new_description, cookies)

        org_return = cloud_platform_helper.get_org_by_id(org_id, cookies)
        assert org_return['name'] == org_new_name
        assert org_return['description'] == org_new_description

        # delete the org
        cloud_platform_helper.delete_org_by_id(org_id, cookies)
        orgs_return = cloud_platform_helper.search_org(org_name, 0, 0, cookies)
        assert orgs_return['total'] == 0
        org_list = orgs_return['list']
        assert org_list is None
        org_return = cloud_platform_helper.get_org_by_id(org_id, cookies)
        assert org_return is None

    @pytest.mark.daily
    def test_org_update_invalid_data(self):
        org_id, cookies = None, None
        try:
            # user login and get cookies
            user_name, user_pw = util.get_admin_user_name_password()
            public_key = cloud_platform_helper.get_password_public_key()
            user_encrypt_pw = util.get_encrypt_password(public_key, user_pw)

            # get test verify code
            cookies = cloud_platform_helper.user_get_verify_code(None)
            verify_code_response = cloud_platform_helper.user_get_test_verify_code(cookies)
            verify_code = verify_code_response.json()['body']

            cookies = cloud_platform_helper.user_login(user_name, user_encrypt_pw, verify_code, cookies)

            # add an organization
            org_name = 'test_' + util.random_str(10)
            org_description = util.random_str(20)
            cloud_platform_helper.create_org(org_name, org_description, cookies)

            # search the organization by name
            orgs_return = cloud_platform_helper.search_org(org_name, 0, 0, cookies)
            assert orgs_return['total'] == 1
            org_id = orgs_return['list'][0]['id']

            # update the org with the new org name and description
            org_new_name = ''
            org_response = cloud_platform_helper.update_org(org_id, org_new_name, org_description, cookies)
            # maxzhang: Response body: {'code': '200', 'message': 'success', 'body': None}
            # 没有检查出来错误
            assert error_messages['org_name_required'] in org_response['message']
        finally:
            if org_id:
                # delete the org
                cloud_platform_helper.delete_org_by_id(org_id, cookies)

    @pytest.mark.daily
    def test_get_org_by_id(self):
        org_id, cookies = None, None
        try:
            # user login and get cookies
            user_name, user_pw = util.get_admin_user_name_password()
            public_key = cloud_platform_helper.get_password_public_key()
            user_encrypt_pw = util.get_encrypt_password(public_key, user_pw)

            # get test verify code
            cookies = cloud_platform_helper.user_get_verify_code(None)
            verify_code_response = cloud_platform_helper.user_get_test_verify_code(cookies)
            verify_code = verify_code_response.json()['body']

            cookies = cloud_platform_helper.user_login(user_name, user_encrypt_pw, verify_code, cookies)

            # add an organization
            org_name = 'test_' + util.random_str(10)
            org_description = util.random_str(20)
            response = cloud_platform_helper.create_org(org_name, org_description, cookies)

            # search the organization by name
            orgs_return = cloud_platform_helper.search_org(org_name, 0, 0, cookies)
            assert orgs_return['total'] == 1
            org_id = orgs_return['list'][0]['id']

            # get org with invalid org id
            invalid_org_id = util.random_str(10)
            org_response = cloud_platform_helper.get_org_by_id(invalid_org_id, cookies)
            assert org_response is None

            # correct org id
            org_return = cloud_platform_helper.get_org_by_id(org_id, cookies)
            assert org_return['name'] == org_name
            assert org_return['description'] == org_description
        finally:
            if org_id:
                # delete the org
                cloud_platform_helper.delete_org_by_id(org_id, cookies)

    @pytest.mark.daily
    def test_org_binding(self):
        user_new_id, cookies, org_id = None, None, None

        try:
            # user login and get cookies
            user_name, user_pw = util.get_admin_user_name_password()
            public_key = cloud_platform_helper.get_password_public_key()
            user_encrypt_pw = util.get_encrypt_password(public_key, user_pw)

            # get test verify code
            cookies = cloud_platform_helper.user_get_verify_code(None)
            verify_code_response = cloud_platform_helper.user_get_test_verify_code(cookies)
            verify_code = verify_code_response.json()['body']

            cookies = cloud_platform_helper.user_login(user_name, user_encrypt_pw, verify_code, cookies)

            # add an organization
            org_name = 'test_' + util.random_str(10)
            org_description = util.random_str(20)
            cloud_platform_helper.create_org(org_name, org_description, cookies)

            # search the organization by name
            orgs_return = cloud_platform_helper.search_org(org_name, 0, 0, cookies)
            assert orgs_return['total'] == 1
            org_id = orgs_return['list'][0]['id']

            # add a user
            username_to_add = 'test_' + util.random_str(10)
            email = util.random_mail()
            # mg: migu用户, inter: 平台用户
            account_type = 'mg'

            cloud_platform_helper.create_user(username_to_add, email, account_type, cookies)

            # search the newly-created user by account name
            user_new = cloud_platform_helper.get_user_by_account(username_to_add, cookies)
            user_new_id = user_new['id']

            # org binding 关联类型；1：关联；2：取消
            relate_type = 1
            org_response = cloud_platform_helper.org_binding(username_to_add, org_id, relate_type, cookies)
            assert success_message in org_response['message']

            relate_type = 2
            org_response = cloud_platform_helper.org_binding(username_to_add, org_id, relate_type, cookies)
            assert success_message in org_response['message']
        finally:
            if user_new_id:
                cloud_platform_helper.delete_user_by_id(user_new_id, cookies)
            if org_id:
                cloud_platform_helper.delete_org_by_id(org_id, cookies)

    @pytest.mark.daily
    def test_org_binding_invalid_data(self):
        user_new_id, cookies, org_id = None, None, None
        try:
            # user login and get cookies
            user_name, user_pw = util.get_admin_user_name_password()
            public_key = cloud_platform_helper.get_password_public_key()
            user_encrypt_pw = util.get_encrypt_password(public_key, user_pw)

            # get test verify code
            cookies = cloud_platform_helper.user_get_verify_code(None)
            verify_code_response = cloud_platform_helper.user_get_test_verify_code(cookies)
            verify_code = verify_code_response.json()['body']

            cookies = cloud_platform_helper.user_login(user_name, user_encrypt_pw, verify_code, cookies)

            # add an organization
            org_name = 'test_' + util.random_str(10)
            org_description = util.random_str(20)
            cloud_platform_helper.create_org(org_name, org_description, cookies)

            # search the organization by name
            orgs_return = cloud_platform_helper.search_org(org_name, 0, 0, cookies)
            assert orgs_return['total'] == 1
            org_id = orgs_return['list'][0]['id']

            # add a user
            username_to_add = 'test_' + util.random_str(10)
            email = util.random_mail()
            # mg: migu用户, inter: 平台用户
            account_type = 'mg'

            cloud_platform_helper.create_user(username_to_add, email, account_type, cookies)

            # search the newly-created user by account name
            user_new = cloud_platform_helper.get_user_by_account(username_to_add, cookies)
            user_new_id = user_new['id']

            # org binding 关联类型；1：关联；2：取消
            relate_type = 5
            org_response = cloud_platform_helper.org_binding(username_to_add, org_id, relate_type, cookies)
            assert error_messages['relate_type_too_big'] in org_response['message']

            # relate_type = 2
            # org_response = cloud_platform_helper.org_binding(username_to_add, org_id, relate_type, cookies)
            # assert fail_message in org_response['message']

            relate_type = 1
            invalid_user = util.random_str(10)
            org_response = cloud_platform_helper.org_binding(invalid_user, org_id, relate_type, cookies)
            assert error_messages['user_not_found'] in org_response['message']

            invalid_org_id = util.random_str(10)
            org_response = cloud_platform_helper.org_binding(username_to_add, invalid_org_id, relate_type, cookies)
            # maxzhang
            # 直接返回了 {'code': 'InternalServerError', 'message': 'Wrap non AppError', 'body': None}
            assert fail_message in org_response['message']
        finally:
            # delete the user and the org
            if user_new_id:
                cloud_platform_helper.delete_user_by_id(user_new_id, cookies)
            if org_id:
                cloud_platform_helper.delete_org_by_id(org_id, cookies)

    # use it for clean up test added orgs
    @staticmethod
    def cleanup_test_orgs():
        cookies = None
        try:
            # user login and get cookies
            user_name, user_pw = util.get_admin_user_name_password()
            public_key = cloud_platform_helper.get_password_public_key()
            user_encrypt_pw = util.get_encrypt_password(public_key, user_pw)
            # get test verify code
            cookies = cloud_platform_helper.user_get_verify_code(None)
            verify_code_response = cloud_platform_helper.user_get_test_verify_code(cookies)
            verify_code = verify_code_response.json()['body']
            cookies = cloud_platform_helper.user_login(user_name, user_encrypt_pw, verify_code, cookies)

            flag = True
            cnt = 0

            result_list = []

            while flag:
                flag = False
                responses = cloud_platform_helper.search_org("test_", 0, 0, cookies)
                assert responses.get("list") is not None

                for org in responses["list"]:
                    if org['name'].startswith("test_") and len(org['name']) == 15:
                        assert org['name'].startswith("test_") and len(org['name']) == 15
                        assert len(org['description']) == 20
                        assert org['userCount'] == 0
                        assert org['adminAccount'] is None

                        org_id = org['id']
                        logging.info(f"deleted {org_id=} {org['name']=}")
                        result_list.append(f"{org_id=} {org['name']=}")
                        cloud_platform_helper.delete_org_by_id(org_id, cookies)

                        flag = True
                        cnt += 1

            from pprint import pprint
            pprint(result_list)
            logging.info(f"{cnt=}")

        finally:
            if cookies:
                cloud_platform_helper.user_logout(cookies)
