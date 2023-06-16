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
    'invalid_user_name_or_password': '用户名或者密码错误',
    'failed_to_add_user': '添加用户失败，请重试',
    'failed_to_update_user': '添加用户失败，请重试',
    'duplicate_user_name': '用户名已存在',
    'invalid_operation': '操作失败，请稍后重试',
    'invalid_arg': '请求参数错误',
}
success_message = 'success'
fail_message = 'fail'


class TestUser:

    @pytest.mark.bvt
    def test_user_login_logout(self):
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
            assert cookies is not None
        finally:
            # logout
            cloud_platform_helper.user_logout(cookies)

    @pytest.mark.bvt
    def test_user_login_with_wrong_info(self):
        # user login and get cookies
        user_name, user_pw = util.get_admin_user_name_password()

        public_key = cloud_platform_helper.get_password_public_key()
        user_encrypt_pw = util.get_encrypt_password(public_key, user_pw)
        invalid_account = util.random_str(10)
        # get test verify code
        cookies = cloud_platform_helper.user_get_verify_code(None)
        verify_code_response = cloud_platform_helper.user_get_test_verify_code(cookies)
        verify_code = verify_code_response.json()['body']

        user_response = cloud_platform_helper.user_login_return_response(invalid_account, user_encrypt_pw,
                                                                         verify_code, cookies)
        assert error_messages['invalid_user_name_or_password'] in user_response['message']

        invalid_password = util.random_str(10)
        invalid_password = util.get_encrypt_password(public_key, invalid_password)
        user_response = cloud_platform_helper.user_login_return_response(user_name, invalid_password,
                                                                         verify_code, cookies)
        assert error_messages['invalid_user_name_or_password'] in user_response['message']

    @pytest.mark.bvt
    def test_user_create_migu(self):
        user_new_id = ''
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

            username_to_add = 'test_' + util.random_str(10)
            email = util.random_mail()
            # mg: migu用户, inter: 平台用户
            account_type = 'mg'

            cloud_platform_helper.create_user(username_to_add, email, account_type, cookies)

            # search the newly-created user by account name
            user_new = cloud_platform_helper.get_user_by_account(username_to_add, cookies)
            assert user_new is not None
            assert user_new['account'] == username_to_add
            assert user_new['email'] == email
            assert user_new['status'] == 1
            assert user_new['accountType'] == account_type
            user_new_id = user_new['id']
        finally:
            if user_new_id != '':
                # delete the user
                cloud_platform_helper.delete_user_by_id(user_new_id, cookies)
            cloud_platform_helper.user_logout(cookies)

    @pytest.mark.bvt
    def test_user_create_platform(self):
        user_new_id = ''
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

            # get org
            org_admin = cloud_platform_helper.search_org(automation_org_admin, 0, 0, cookies)
            assert org_admin is not None
            org_id = org_admin['list'][0]['id']

            # add org role : dev
            org_role = 'dev'
            org_roles = {
                org_id: org_role
            }

            username_to_add = 'test_' + util.random_str(10)
            email = util.random_mail()
            # mg: migu用户, inter: 平台用户
            account_type = 'inter'

            cloud_platform_helper.create_user_with_roles(username_to_add, email, account_type, org_roles, cookies)

            # search the newly-created user by account name
            user_new = cloud_platform_helper.get_user_by_account(username_to_add, cookies)
            assert user_new is not None
            assert user_new['account'] == username_to_add
            assert user_new['email'] == email
            assert user_new['status'] == 1
            assert user_new['accountType'] == account_type
            user_new_id = user_new['id']

            org_role_get = user_new['orgRole'][0]
            assert automation_org_admin == org_role_get['orgName']
            assert org_role == org_role_get['role']

        finally:
            if user_new_id != '':
                # delete the user
                cloud_platform_helper.delete_user_by_id(user_new_id, cookies)
            cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_user_create_invalid_data(self):
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

            # invalid name
            invalid_name = ''
            email = util.random_mail()
            # mg: migu用户, inter: 平台用户
            account_type = 'mg'

            user_response = cloud_platform_helper.create_user(invalid_name, email, account_type, cookies)
            assert error_messages['account_required'] in user_response['message']

            # invalid email
            valid_name = 'test_' + util.random_str(10)
            invalid_email = util.random_str(10)

            # mg: migu用户, inter: 平台用户
            account_type = 'inter'
            user_response = cloud_platform_helper.create_user(valid_name, invalid_email, account_type, cookies)
            assert error_messages['invalid_email'] in user_response['message']

            # create user with invalid org id and role
            invalid_org_id = util.random_str(10)
            invalid_org_role = util.random_str(5)
            org_roles = {
                invalid_org_id: invalid_org_role
            }
            user_response = cloud_platform_helper.create_user_with_roles(valid_name, email, account_type, org_roles,
                                                                         cookies)
            assert error_messages['failed_to_add_user'] in user_response['message']

            # create user with invalid org id but valid role
            org_roles = {
                invalid_org_id: 'dev'
            }
            user_response = cloud_platform_helper.create_user_with_roles(valid_name, email, account_type, org_roles,
                                                                         cookies)
            assert error_messages['failed_to_add_user'] in user_response['message']

            # todo: https://jira.internal.unity.cn/browse/MUP-258
            # create user with valid org id but invalid role
            org_admin = cloud_platform_helper.search_org(automation_org_admin, 0, 0, cookies)
            assert org_admin is not None
            org_id = org_admin['list'][0]['id']

            invalid_org_role = util.random_str(5)
            org_roles = {
                org_id: invalid_org_role
            }
            # MaxZhang: 这里错误返回了success，即便传入的为invalid_org_role
            # user_response = cloud_platform_helper.create_user_with_roles(valid_name, email, account_type, org_roles,
            #                                                              cookies)
            # assert error_messages['failed_to_add_user'] in user_response['message']
        finally:
            cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_delete_not_existed_user(self):
        # user login and get cookies
        user_name, user_pw = util.get_admin_user_name_password()
        public_key = cloud_platform_helper.get_password_public_key()
        user_encrypt_pw = util.get_encrypt_password(public_key, user_pw)
        # get test verify code
        cookies = cloud_platform_helper.user_get_verify_code(None)
        verify_code_response = cloud_platform_helper.user_get_test_verify_code(cookies)
        verify_code = verify_code_response.json()['body']

        cookies = cloud_platform_helper.user_login(user_name, user_encrypt_pw, verify_code, cookies)

        # todo: need to check the error message with dev
        # maxzhang :  这里直接返回了500  {'code': '500', 'message': '操作失败，请稍后重试', 'body': None}
        # delete not-existed user
        invalid_user_id = util.random_str(10)
        user_response = cloud_platform_helper.delete_user_by_id(invalid_user_id, cookies)
        assert error_messages['user_not_existed'] in user_response['message']

        cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_user_update(self):
        user_new_id = ''
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

            # get org
            org_admin = cloud_platform_helper.search_org(automation_org_admin, 0, 0, cookies)
            assert org_admin is not None
            org_id = org_admin['list'][0]['id']

            username_to_add = 'test_' + util.random_str(10)
            email_to_add = util.random_mail()
            # mg: migu用户, inter: 平台用户
            account_type = 'inter'

            cloud_platform_helper.create_user(username_to_add, email_to_add, account_type, cookies)

            # search the newly-created user by account name
            user_new = cloud_platform_helper.get_user_by_account(username_to_add, cookies)
            assert user_new is not None
            assert user_new['account'] == username_to_add
            assert user_new['email'] == email_to_add
            assert user_new['status'] == 1
            assert user_new['accountType'] == account_type
            user_new_id = user_new['id']

            # change user info
            email_to_change = util.random_mail()
            account_type = 'mg'

            cloud_platform_helper.update_user(user_new_id, email_to_change, account_type, None, None, cookies)
            user_new = cloud_platform_helper.get_user_by_account(username_to_add, cookies)
            assert user_new is not None
            assert user_new['account'] == username_to_add
            assert user_new['email'] == email_to_change
            assert user_new['status'] == 1
            assert user_new['accountType'] == account_type

            # add org role : dev
            org_role = 'dev'
            org_roles = {
                org_id: org_role
            }

            cloud_platform_helper.update_user(user_new_id, email_to_change, account_type, org_roles, None, cookies)
            user_new = cloud_platform_helper.get_user_by_account(username_to_add, cookies)
            org_role_get = user_new['orgRole'][0]
            assert automation_org_admin == org_role_get['orgName']
            assert org_role == org_role_get['role']

        finally:
            if user_new_id != '':
                # delete the user
                cloud_platform_helper.delete_user_by_id(user_new_id, cookies)
            cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_user_update_invalid_data(self):
        user_new_id = ''
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

            # get org
            org_admin = cloud_platform_helper.search_org(automation_org_admin, 0, 0, cookies)
            assert org_admin is not None
            org_id = org_admin['list'][0]['id']

            username_to_add = 'test_' + util.random_str(10)
            email_to_add = util.random_mail()
            # mg: migu用户, inter: 平台用户
            account_type = 'inter'

            cloud_platform_helper.create_user(username_to_add, email_to_add, account_type, cookies)

            # search the newly-created user by account name
            user_new = cloud_platform_helper.get_user_by_account(username_to_add, cookies)
            assert user_new is not None
            assert user_new['account'] == username_to_add
            assert user_new['email'] == email_to_add
            assert user_new['status'] == 1
            assert user_new['accountType'] == account_type
            user_new_id = user_new['id']

            # change user info
            invalid_email = util.random_str(10)

            user_response = cloud_platform_helper.update_user(user_new_id, invalid_email, None, None, None, cookies)
            assert error_messages['invalid_email'] in user_response['message']

            # change to invalid account type
            # todo: need to discuss with dev, to let them add such restrictions
            # invalid account type
            # mg: migu用户, inter: 平台用户
            account_type = '1'
            new_email = util.random_mail()
            user_response = cloud_platform_helper.update_user(user_new_id, new_email, account_type, None, None, cookies)


            # change to invalid status
            # todo: need to discuss with dev, to let them add such restrictions
            # invalid account type
            # mg: migu用户, inter: 平台用户
            invalid_status = '100'
            user_response = cloud_platform_helper.update_user(user_new_id, new_email, None, None, invalid_status, cookies)

            # update user with invalid org id and role
            invalid_org_id = util.random_str(10)
            invalid_org_role = util.random_str(5)
            org_roles = {
                invalid_org_id: invalid_org_role
            }
            user_response = cloud_platform_helper.update_user(user_new_id, email_to_add, None, org_roles, None, cookies)
            assert error_messages['invalid_operation'] in user_response['message']

            # create user with invalid org id but valid role
            org_roles = {
                invalid_org_id: 'dev'
            }
            user_response = cloud_platform_helper.update_user(user_new_id, email_to_add, None, org_roles, None, cookies)
            assert error_messages['invalid_operation'] in user_response['message']

            # todo: https://jira.internal.unity.cn/browse/MUP-258
            # update user with valid org id but invalid role
            invalid_org_role = util.random_str(5)
            org_roles = {
                org_id: invalid_org_role
            }
            # TODO maxzhang : 这里错误的返回了success，但是其org_role为无效的
            user_response = cloud_platform_helper.update_user(user_new_id, email_to_add, None, org_roles, None, cookies)
            assert error_messages['invalid_operation'] in user_response['message']
        finally:
            if user_new_id != '':
                # delete the user
                cloud_platform_helper.delete_user_by_id(user_new_id, cookies)
            cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_user_get_by_id(self):
        user_new_id = ''
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

            username_to_add = 'test_' + util.random_str(10)
            email = util.random_mail()
            # mg: migu用户, inter: 平台用户
            account_type = 'inter'

            cloud_platform_helper.create_user(username_to_add, email, account_type, cookies)

            # search the newly-created user by account name
            user_new = cloud_platform_helper.get_user_by_account(username_to_add, cookies)
            assert user_new is not None
            assert user_new['account'] == username_to_add
            assert user_new['email'] == email
            assert user_new['status'] == 1
            assert user_new['accountType'] == account_type
            user_new_id = user_new['id']

            user_response = cloud_platform_helper.get_user_by_user_id(user_new_id, cookies)
            user_new = user_response['body']
            assert user_new is not None
            assert user_new['account'] == username_to_add
            assert user_new['email'] == email
            assert user_new['status'] == 1
            assert user_new['accountType'] == account_type

        finally:
            if user_new_id != '':
                # delete the user
                cloud_platform_helper.delete_user_by_id(user_new_id, cookies)
            cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_user_get_by_invalid_id(self):
        user_new_id = ''
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

            username_to_add = 'test_' + util.random_str(10)
            email = util.random_mail()
            # mg: migu用户, inter: 平台用户
            account_type = 'inter'

            cloud_platform_helper.create_user(username_to_add, email, account_type, cookies)

            # search the newly-created user by account name
            user_new = cloud_platform_helper.get_user_by_account(username_to_add, cookies)
            assert user_new is not None
            user_new_id = user_new['id']

            invalid_user_id = util.random_str(10)
            user_response = cloud_platform_helper.get_user_by_user_id(invalid_user_id, cookies)
            # maxzhang: 应返回user id不存在，但是返回的'Wrap non AppError'，且为InternalServerError
            assert error_messages['user_not_existed'] in user_response['message']

        finally:
            if user_new_id != '':
                # delete the user
                cloud_platform_helper.delete_user_by_id(user_new_id, cookies)
            cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_user_search(self):
        user_new_id = ''
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

            username_to_add = 'test_' + util.random_str(10)
            email = util.random_mail()
            # mg: migu用户, inter: 平台用户
            account_type = 'inter'

            cloud_platform_helper.create_user(username_to_add, email, account_type, cookies)

            # search the newly-created user by account name
            user_new = cloud_platform_helper.get_user_by_account(username_to_add, cookies)
            assert user_new is not None
            assert user_new['account'] == username_to_add
            assert user_new['email'] == email
            assert user_new['status'] == 1
            assert user_new['accountType'] == account_type
            user_new_id = user_new['id']

            # search user
            search_user_query = {'status': '1'}
            users = cloud_platform_helper.search_users(search_user_query, 1, 10, cookies)
            assert users['total'] >= 1
            user_list = users['list']
            assert len(user_list) >= 1

            # search user with account name
            search_user_query = {'account': username_to_add}
            users = cloud_platform_helper.search_users(search_user_query, 1, 10, cookies)
            assert users['total'] == 1
            user_list = users['list']
            assert len(user_list) == 1
            assert user_list[0]['account'] == username_to_add
            assert user_list[0]['email'] == email
            assert user_list[0]['status'] == 1
            assert user_list[0]['accountType'] == account_type

        finally:
            if user_new_id != '':
                # delete the user
                cloud_platform_helper.delete_user_by_id(user_new_id, cookies)
            cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_user_change_role(self):
        user_new_id, cookies = None, None
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

            username_to_add = 'test_' + util.random_str(10)
            email = util.random_mail()
            # mg: migu用户, inter: 平台用户
            account_type = 'inter'

            cloud_platform_helper.create_user(username_to_add, email, account_type, cookies)

            # search the newly-created user by account name
            user_new = cloud_platform_helper.get_user_by_account(username_to_add, cookies)
            assert user_new is not None
            assert user_new['account'] == username_to_add
            assert user_new['email'] == email
            assert user_new['status'] == 1
            assert user_new['accountType'] == account_type
            user_new_id = user_new['id']

            # get org
            org_admin = cloud_platform_helper.search_org(automation_org_admin, 0, 0, cookies)
            assert org_admin is not None
            org_id = org_admin['list'][0]['id']

            # change role
            req_body = {
                'orgId': org_id,
                'role': 'dev'
            }
            cloud_platform_helper.user_change_role(user_new_id, req_body, cookies)

            req_body = {
                'orgId': org_id,
                'role': 'org'
            }
            cloud_platform_helper.user_change_role(user_new_id, req_body, cookies)
        finally:
            if user_new_id is not None:
                # delete the user
                cloud_platform_helper.delete_user_by_id(user_new_id, cookies)
            cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_user_change_role_invalid_data(self):
        user_new_id, cookies = None, None
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

            username_to_add = 'test_' + util.random_str(10)
            email = util.random_mail()
            # mg: migu用户, inter: 平台用户
            account_type = 'inter'

            cloud_platform_helper.create_user(username_to_add, email, account_type, cookies)

            # search the newly-created user by account name
            user_new = cloud_platform_helper.get_user_by_account(username_to_add, cookies)
            assert user_new is not None
            assert user_new['account'] == username_to_add
            assert user_new['email'] == email
            assert user_new['status'] == 1
            assert user_new['accountType'] == account_type
            user_new_id = user_new['id']

            # todo
            # get org
            org_admin = cloud_platform_helper.search_org(automation_org_admin, 0, 0, cookies)
            assert org_admin is not None
            org_id = org_admin['list'][0]['id']

            # invalid data
            invalid_user_id = util.random_str(10)
            req_body = {
                'orgId': org_id,
                'role': 'org'
            }
            user_response = cloud_platform_helper.user_change_role(invalid_user_id, req_body, cookies)
            assert error_messages['invalid_arg'] in user_response['message']

            req_body = {
                'orgId': org_id,
                'role': 'admin'
            }
            user_response = cloud_platform_helper.user_change_role(user_new_id, req_body, cookies)
            assert error_messages['invalid_arg'] in user_response['message']

        finally:
            if user_new_id is not None:
                # delete the user
                cloud_platform_helper.delete_user_by_id(user_new_id, cookies)
            cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_user_bind_unity_account(self):
        user_new_id, cookies = None, None
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

            username_to_add = 'test_' + util.random_str(10)
            email = util.random_mail()
            # mg: migu用户, inter: 平台用户
            account_type = 'inter'

            user_response = cloud_platform_helper.create_user(username_to_add, email, account_type, cookies)

            # search the newly-created user by account name
            user_new = cloud_platform_helper.get_user_by_account(username_to_add, cookies)
            assert user_new is not None
            assert user_new['account'] == username_to_add
            assert user_new['email'] == email
            assert user_new['status'] == 1
            assert user_new['accountType'] == account_type
            user_new_id = user_new['id']

            # account binding
            unity_account = 'jasonfu@unity3d.com'
            req_body = {
                'id': user_new_id,
                'unityAccount': unity_account
            }
            user_response = cloud_platform_helper.user_bind_unity_account(req_body, cookies)
            assert success_message in user_response['message']

        finally:
            if user_new_id is not None:
                # delete the user
                cloud_platform_helper.delete_user_by_id(user_new_id, cookies)
            cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_user_bind_unity_account_invalid_data(self):
        user_new_id, cookies = None, None
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

            username_to_add = 'test_' + util.random_str(10)
            email = util.random_mail()
            # mg: migu用户, inter: 平台用户
            account_type = 'inter'

            response = cloud_platform_helper.create_user(username_to_add, email, account_type, cookies)

            # search the newly-created user by account name
            user_new = cloud_platform_helper.get_user_by_account(username_to_add, cookies)
            assert user_new is not None
            assert user_new['account'] == username_to_add
            assert user_new['email'] == email
            assert user_new['status'] == 1
            assert user_new['accountType'] == account_type
            user_new_id = user_new['id']

            # account binding
            invalid_user_id = util.random_str(12)
            invalid_unity_account = 'jasonfu@uni.com'
            req_body = {
                'id': invalid_user_id,
                'unityAccount': invalid_unity_account
            }
            user_response = cloud_platform_helper.user_bind_unity_account(req_body, cookies)
            # MaxZhang:
            # 返回了 InternalServerError {'code': 'InternalServerError', 'message': 'Wrap non AppError', 'body': None}
            assert success_message in user_response['message']
        finally:
            if user_new_id is not None:
                cloud_platform_helper.delete_user_by_id(user_new_id, cookies)
                cloud_platform_helper.user_logout(cookies)

    @pytest.mark.manual
    def test_user_reset_password(self):
        user_new_id = None
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

            username_to_add = 'test_' + util.random_str(10)
            email = util.random_mail()
            # mg: migu用户, inter: 平台用户
            account_type = 'inter'

            response = cloud_platform_helper.create_user(username_to_add, email, account_type, cookies)

            # search the newly-created user by account name
            user_new = cloud_platform_helper.get_user_by_account(username_to_add, cookies)
            assert user_new is not None
            assert user_new['account'] == username_to_add
            assert user_new['email'] == email
            assert user_new['status'] == 1
            assert user_new['accountType'] == account_type
            user_new_id = user_new['id']

            # account reset password
            old_password = util.random_str(10)
            old_password_encrypt = util.get_encrypt_password(public_key, old_password)
            new_password = util.random_str(10)
            new_password_encrypt = util.get_encrypt_password(public_key, new_password)

            req_body = {
                'oldPassword': old_password_encrypt,
                'newPassword': new_password_encrypt
            }
            # maxzhang: 密码相关改为manual
            user_response = cloud_platform_helper.user_reset_password(user_new_id, req_body, cookies)
            assert success_message in user_response['message']

        finally:
            print("deleting...")
            cloud_platform_helper.delete_user_by_id(user_new_id, cookies)
            cloud_platform_helper.user_logout(cookies)

    @pytest.mark.manual
    def test_user_reset_password_invalid_data(self):
        user_new_id = None
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

            username_to_add = 'test_' + util.random_str(10)
            email = util.random_mail()
            # mg: migu用户, inter: 平台用户
            account_type = 'inter'

            cloud_platform_helper.create_user(username_to_add, email, account_type, cookies)

            # search the newly-created user by account name
            user_new = cloud_platform_helper.get_user_by_account(username_to_add, cookies)
            assert user_new is not None
            assert user_new['account'] == username_to_add
            assert user_new['email'] == email
            assert user_new['status'] == 1
            assert user_new['accountType'] == account_type
            user_new_id = user_new['id']

            # account reset password
            # old password is wrong
            old_password = util.random_str(10)
            old_password_encrypt = util.get_encrypt_password(public_key, old_password)
            new_password = util.random_str(10)
            new_password_encrypt = util.get_encrypt_password(public_key, new_password)

            req_body = {
                'oldPassword': old_password_encrypt,
                'newPassword': new_password_encrypt
            }

            user_response = cloud_platform_helper.user_reset_password(user_new_id, req_body, cookies)
            assert success_message in user_response['message']

            # new password is not strong enough
            old_password = util.random_str(10)
            old_password_encrypt = util.get_encrypt_password(public_key, old_password)
            new_password = '11111111'
            new_password_encrypt = util.get_encrypt_password(public_key, new_password)

            req_body = {
                'oldPassword': old_password_encrypt,
                'newPassword': new_password_encrypt
            }

            user_response = cloud_platform_helper.user_reset_password(user_new_id, req_body, cookies)
            assert success_message in user_response['message']
        finally:
            cloud_platform_helper.delete_user_by_id(user_new_id, cookies)

            cloud_platform_helper.user_logout(cookies)

    @pytest.mark.manual
    def test_send_reset_password_email_to_user(self):
        user_new_id = None
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


            username_to_add = 'test_' + util.random_str(10)
            email = util.random_mail()
            # mg: migu用户, inter: 平台用户
            account_type = 'inter'

            cloud_platform_helper.create_user(username_to_add, email, account_type, cookies)

            # search the newly-created user by account name
            user_new = cloud_platform_helper.get_user_by_account(username_to_add, cookies)
            user_new_id = user_new['id']

            # send email
            user_response = cloud_platform_helper.send_user_reset_password_email(email, cookies)
            print(f"{user_response.json()=}")
            assert success_message in user_response.json()['message']

        finally:
            cloud_platform_helper.delete_user_by_id(user_new_id, cookies)

            cloud_platform_helper.user_logout(cookies)

    @pytest.mark.manual
    def test_send_reset_password_email_to_user_invalid_data(self):
        # user login and get cookies
        user_name, user_pw = util.get_admin_user_name_password()
        public_key = cloud_platform_helper.get_password_public_key()
        user_encrypt_pw = util.get_encrypt_password(public_key, user_pw)

        # get test verify code
        cookies = cloud_platform_helper.user_get_verify_code(None)
        verify_code_response = cloud_platform_helper.user_get_test_verify_code(cookies)
        verify_code = verify_code_response.json()['body']

        cookies = cloud_platform_helper.user_login(user_name, user_encrypt_pw, verify_code, cookies)

        # change org
        user = cloud_platform_helper.get_user_by_account(user_name, cookies)
        user_id = user['id']

        platform_admin_org = cloud_platform_helper.search_org(automation_org_admin, 0, 0, cookies)
        assert platform_admin_org is not None
        org_id = platform_admin_org['list'][0]['id']

        cloud_platform_helper.user_change_org(user_id, org_id, cookies)

        username_to_add = 'test_' + util.random_str(10)
        email = util.random_mail()
        # mg: migu用户, inter: 平台用户
        account_type = 'inter'

        cloud_platform_helper.create_user(username_to_add, email, account_type, cookies)

        # search the newly-created user by account name
        user_new = cloud_platform_helper.get_user_by_account(username_to_add, cookies)
        user_new_id = user_new['id']

        # send email
        invalid_email = util.random_str(10)
        user_response = cloud_platform_helper.send_user_reset_password_email(invalid_email, cookies)
        assert error_messages['invalid_email'] in user_response['message']

        cloud_platform_helper.delete_user_by_id(user_new_id, cookies)

        cloud_platform_helper.user_logout(cookies)

    @pytest.mark.manual
    def test_reset_password_after_forgotten(self):
        user_new_id, cookies = None, None
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

            username_to_add = 'test_' + util.random_str(10)
            email = util.random_mail()
            # mg: migu用户, inter: 平台用户
            account_type = 'inter'

            cloud_platform_helper.create_user(username_to_add, email, account_type, cookies)

            # search the newly-created user by account name
            user_new = cloud_platform_helper.get_user_by_account(username_to_add, cookies)
            user_new_id = user_new['id']

            # send email
            user_response = cloud_platform_helper.send_user_reset_password_email(email, cookies)
            assert success_message in user_response['message']

            # reset password according to email verify code
            verify_code = user_response['verifyCode']
            new_password = util.random_str(10)
            new_password_encrypt = util.get_encrypt_password(public_key, new_password)

            req_body = {
                'email': email,
                'verifyCode': verify_code,
                'newPassword': new_password_encrypt
            }
            user_response = cloud_platform_helper.user_reset_password_with_verify_code(req_body, cookies)
            user_response = user_response.json()
            assert success_message in user_response['message']

        finally:
            cloud_platform_helper.delete_user_by_id(user_new_id, cookies)
            cloud_platform_helper.user_logout(cookies)

    @pytest.mark.manual
    def test_reset_password_after_forgotten_invalid_data(self):
        # user login and get cookies
        user_name, user_pw = util.get_admin_user_name_password()
        public_key = cloud_platform_helper.get_password_public_key()
        user_encrypt_pw = util.get_encrypt_password(public_key, user_pw)

        # get test verify code
        cookies = cloud_platform_helper.user_get_verify_code(None)
        verify_code_response = cloud_platform_helper.user_get_test_verify_code(cookies)
        verify_code = verify_code_response.json()['body']

        cookies = cloud_platform_helper.user_login(user_name, user_encrypt_pw, verify_code, cookies)

        # change org
        user = cloud_platform_helper.get_user_by_account(user_name, cookies)
        user_id = user['id']

        platform_admin_org = cloud_platform_helper.search_org(automation_org_admin, 0, 0, cookies)
        assert platform_admin_org is not None
        org_id = platform_admin_org['list'][0]['id']

        cloud_platform_helper.user_change_org(user_id, org_id, cookies)

        username_to_add = 'test_' + util.random_str(10)
        email = util.random_mail()
        # mg: migu用户, inter: 平台用户
        account_type = 'inter'

        cloud_platform_helper.create_user(username_to_add, email, account_type, cookies)

        # search the newly-created user by account name
        user_new = cloud_platform_helper.get_user_by_account(username_to_add, cookies)
        user_new_id = user_new['id']

        # send email
        user_response = cloud_platform_helper.send_user_reset_password_email(email, cookies)
        assert success_message in user_response['message']

        # reset password according to email verify code
        invalid_email = util.random_str(10)
        verify_code = user_response['verifyCode']
        new_password = util.random_str(10)
        new_password_encrypt = util.get_encrypt_password(public_key, new_password)

        req_body = {
            'email': invalid_email,
            'verifyCode': verify_code,
            'newPassword': new_password_encrypt
        }
        user_response = cloud_platform_helper.user_reset_password_with_verify_code(req_body, cookies)
        assert fail_message in user_response['message']

        cloud_platform_helper.delete_user_by_id(user_new_id, cookies)

        cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_get_verify_code(self):
        cookies = cloud_platform_helper.user_get_verify_code(None)
        verify_code_response = cloud_platform_helper.user_get_test_verify_code(cookies)
        assert verify_code_response.status_code == 200

    @pytest.mark.daily
    def test_get_password_public_key(self):
        public_key = cloud_platform_helper.get_password_public_key()
        assert public_key is not None

    @pytest.mark.daily
    def test_get_dynamic_salt(self):
        dynamic_salt = cloud_platform_helper.get_dynamic_salt(None)
        assert dynamic_salt is not None
