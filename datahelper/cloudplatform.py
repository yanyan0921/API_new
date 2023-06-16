import logging
import re
import time

from rest.cloudplatform.cloudplatform import CloudPlatformService

import common.utility as util

cloud_platform_service = CloudPlatformService()


def dict_ext(d1, d2):
    result = dict(d1)
    result.update(d2)
    return result


# Users
def user_get_verify_code(cookies):
    return cloud_platform_service.user_get_verify_code(cookies)


def user_get_test_verify_code(cookies):
    return cloud_platform_service.user_get_test_verify_code(cookies)


def get_password_public_key():
    return cloud_platform_service.user_get_password_public_key()


def get_dynamic_salt(cookies):
    return cloud_platform_service.get_dynamic_salt(cookies)


def user_login(user_name, user_pw, verify_code, cookies):
    req_body = {
        'account': user_name,
        'password': user_pw,
        'verifyCode': verify_code
    }
    return cloud_platform_service.user_login(req_body, cookies)


def user_login_return_response(user_name, user_pw, verify_code, cookies):
    req_body = {
        'account': user_name,
        'password': user_pw,
        'verifyCode': verify_code
    }
    return cloud_platform_service.user_login_response(req_body, cookies)


def user_logout(cookies):
    return cloud_platform_service.user_logout(cookies)


def create_user(account_name, email, account_type, cookies):
    req_body = {
        'account': account_name,
        'email': email,
        'accountType': account_type
    }
    return cloud_platform_service.create_user(req_body, cookies)


def create_user_with_roles(account_name, email, account_type, org_roles, cookies):
    req_body = {
        'account': account_name,
        'email': email,
        'accountType': account_type
    }

    if org_roles is not None:
        req_body.update({'orgRole': org_roles})

    return cloud_platform_service.create_user(req_body, cookies)


def update_user(user_id, email, account_type, org_roles, status, cookies):
    req_body = {
        'email': email
    }

    if account_type is not None and account_type != '':
        req_body.update({'accountType': account_type})
    if org_roles is not None:
        req_body.update({'orgRole': org_roles})
    if status is not None and status != '':
        req_body.update({'status': status})

    return cloud_platform_service.update_user_info(req_body, user_id, cookies)


def get_user_by_account(account_name, cookies):
    return cloud_platform_service.get_single_user_info_by_account(account_name, cookies)


def get_user_by_user_id(user_id, cookies):
    return cloud_platform_service.get_single_user_info_by_id(user_id, cookies)


# The default page is 1 and default page_size is 10 in dev code. we could just set page = 0 and page_size = 0 in
# our test cases
def search_users(search_user_query, page, page_size, cookies):
    return cloud_platform_service.search_users(search_user_query, page, page_size, cookies)


def user_change_role(user_id, change_role_body, cookies):
    return cloud_platform_service.user_change_role(user_id, change_role_body, cookies)


def user_bind_unity_account(req_body, cookies):
    return cloud_platform_service.user_bind_unity_account(req_body, cookies)


def user_reset_password(user_id, req_body, cookies):
    return cloud_platform_service.user_reset_password(user_id, req_body, cookies)


def send_user_reset_password_email(account_email, cookies):
    req_body = {
        'account': account_email
    }
    return cloud_platform_service.user_send_reset_email(req_body, cookies)


def user_reset_password_with_verify_code(req_body, cookies):
    return cloud_platform_service.user_forget_password(req_body, cookies)


def delete_user_by_id(user_id, cookies):
    return cloud_platform_service.delete_user_by_id(user_id, cookies)


# Organizations
def create_org(org_name, org_description, cookies):
    req_body = {
        'name': org_name,
        'description': org_description
    }
    return cloud_platform_service.create_organization(req_body, cookies)


# The default page is 1 and default page_size is 10 in dev code. we could just set page = 0 and page_size = 0 in
# our test cases
def search_org(org_name, page, page_size, cookies):
    return cloud_platform_service.search_organization(org_name, page, page_size, cookies)


def get_org_by_id(org_id, cookies):
    return cloud_platform_service.get_organization_by_id(org_id, cookies)


def update_org(org_id, org_new_name, org_new_description, cookies):
    req_body = {
        'name': org_new_name,
        'description': org_new_description
    }
    return cloud_platform_service.update_organization(org_id, req_body, cookies)


def delete_org_by_id(org_id, cookies):
    return cloud_platform_service.delete_organization_by_id(org_id, cookies)


def user_change_org(user_id, org_id, cookies):
    return cloud_platform_service.user_change_org(user_id, org_id, cookies)


def org_binding(account_name, org_id, relate_type, cookies):
    req_body = {
        'account': account_name,
        'orgId': org_id,
        'relateType': relate_type
    }
    return cloud_platform_service.bind_organization(req_body, cookies)


# Projects
def create_project(org_id, project_name, project_description, cookies):
    req_body = {
        'displayName': project_name,
        'description': project_description
    }
    response = cloud_platform_service.create_project(org_id, req_body, cookies)  # type: dict
    if type(response) is dict and 'body' in response:
        return response['body']
    else:
        return response


def update_project(org_id, project_id, project_name, project_description, cookies):
    req_body = {
        'displayName': project_name,
        'description': project_description
    }
    return cloud_platform_service.update_project(org_id, req_body, project_id, cookies)


def get_project_by_id(org_id, project_id, cookies):
    return cloud_platform_service.get_project_by_id(org_id, project_id, cookies)


def delete_project_by_id(org_id, project_id, cookies):
    return cloud_platform_service.delete_project_by_id(org_id, project_id, cookies)


def search_projects(org_id, project_name, page, page_size, cookies):
    return cloud_platform_service.search_projects(org_id, project_name, page, page_size, cookies)


# package
def get_package_pre_signed_address(org_id, project_id, cookies):
    return cloud_platform_service.get_package_presigned_url(org_id, project_id, cookies)


def upload_package_from_web(api_url, package_file_name, cookies):
    return cloud_platform_service.upload_package_from_web(api_url, package_file_name, cookies)


def save_package_info_after_upload(org_id, project_id, req_body, cookies):
    return cloud_platform_service.save_package_info_after_upload(org_id, project_id, req_body, cookies)


def search_packages(org_id, project_id, package_name, version, package_type, page, page_size, cookies):
    return cloud_platform_service.search_packages(org_id, project_id, package_name, version, package_type,
                                                  page, page_size, cookies)


def get_package_by_id(org_id, package_id, cookies):
    return cloud_platform_service.get_package_by_id(org_id, package_id, cookies)


def delete_package_by_id(org_id, package_id, cookies):
    return cloud_platform_service.delete_package_by_id(org_id, package_id, cookies)


def gen_upload_package_cache(org_id, project_id, file_name, version, cookies):
    return cloud_platform_service.gen_upload_package_cache(org_id, project_id, file_name, version, cookies)


def get_upload_package_cache_part_url(org_id, project_id, cache_id, file_name, part_index, cookies):
    return cloud_platform_service.get_upload_package_cache_part_url(org_id, project_id, cache_id, file_name, part_index,
                                                                    cookies)


def upload_file_part(part_url_response, file_name, cookies):
    return cloud_platform_service.upload_file_part(part_url_response, file_name, cookies)


def complete_upload_package_cache_part(org_id, project_id, cache_id, file_name, part_index, cookies):
    return cloud_platform_service.complete_upload_package_cache_part(org_id, project_id, cache_id, file_name,
                                                                     part_index, cookies)


# 上传文件的整体流程
def upload_file_progress(cookies, org_id, project_id, file_name, version):
    logging.info("start upload_file_progress")

    # upload package file
    gen_cache_response = gen_upload_package_cache(org_id, project_id, file_name, version, cookies)
    gen_cache_response = gen_cache_response['body']
    assert gen_cache_response['cacheId'] is not None and gen_cache_response['cacheId'] != ''
    assert gen_cache_response['orgId'] == org_id
    assert gen_cache_response['projectId'] == project_id

    # 暂时不测试分多片上传，此处仅测一个
    assert gen_cache_response['totalPartCount'] == 1
    cache_id = gen_cache_response['cacheId']
    file_name = file_name
    part_index = 1
    part_url_response = get_upload_package_cache_part_url(org_id, project_id, cache_id, file_name, part_index, cookies)
    part_url_response = part_url_response['body']
    assert part_url_response['url'] is not None and part_url_response['url'] != ''
    assert part_url_response['fData']['bucket'] is not None and part_url_response['fData']['bucket'] != ''
    assert part_url_response['fData']['key'] is not None and part_url_response['fData']['key'] != ''
    assert part_url_response['fData']['policy'] is not None and part_url_response['fData']['policy'] != ''
    upload_response = upload_file_part(part_url_response, file_name, cookies)
    assert upload_response.status_code == 204
    complete_response = complete_upload_package_cache_part(org_id, project_id, cache_id, file_name, part_index, cookies)
    complete_response = complete_response['body']
    assert complete_response['finishUpload'] is True
    assert complete_response['cacheId'] == cache_id

    # 等待游戏包合并
    package_status = ""
    package_id = None
    query_times = 0

    while package_status != "uploaded" and query_times < 10:
        time.sleep(3)
        query_times += 1
        response = search_packages(org_id, project_id, file_name, version, None, 0, 0, cookies)
        package_added = response['list'][0]
        package_status = str(package_added['status'])
        package_id = package_added.get('id')
        logging.info(f"upload_file_progress {query_times=} . package status:" + str(package_added['status']))

    assert package_status == "uploaded"

    logging.info("end upload_file_progress")

    return package_id


def waiting_package_ready(org_id, project_id, pkg_name, version, cookies):
    interval = 10
    logging.info(f"start waiting_package_ready, interval = {interval} seconds")

    package_status = ""
    query_times = 0

    while package_status != "ready" and query_times < 10:
        time.sleep(interval)
        response = search_packages(org_id, project_id, pkg_name, version, None, 0, 0, cookies)
        assert response['total'] == 1
        package = response['list'][0]
        package_status = str(package['status'])
        logging.info(f"waiting_package_ready {query_times=} . package status:" + str(package['status']))
        query_times += 1

    logging.info("end waiting_package_ready")

    if package_status == "ready":
        return True
    return False

def cover_put_url(project_id, cookies):
    response = cloud_platform_service.cover_put_url(project_id, cookies)
    if type(response) is dict and 'body' in response:
        return response['body']
    else:
        return response


def put_image(put_url, image_name, cookies):
    response = cloud_platform_service.put_image(put_url, image_name, cookies)
    return response


def cover_get_url(project_id, cover_key, cookies):
    response = cloud_platform_service.cover_get_url(project_id, cover_key, cookies)
    if type(response) is dict and 'body' in response:
        return response['body']
    else:
        return response


def get_image(url, cookies):
    response = cloud_platform_service.get_image(url, cookies)
    return response


def create_pub_app_cover_image_progress(project_id, cookies):
    response1 = cover_put_url(project_id, cookies)
    assert type(response1) == dict and response1.get('putUrl') is not None
    put_url = response1['putUrl']

    part1 = re.search(r"/app-cover/(.*?)/", put_url).group(1)
    part2 = re.search(r"/app-cover/.*/(.*?)/", put_url).group(1)
    part3 = re.search(r"/app-cover/.*/.*/(.*?)\?", put_url).group(1)
    cover_key = f"{part1}/{part2}/{part3}"

    image_name = "cover.jpeg"
    response2 = put_image(put_url, image_name, cookies)
    assert response2.status_code == 200

    response3 = cover_get_url(project_id, cover_key, cookies)
    assert type(response3) == dict and response3.get('getUrl') is not None
    get_url = response3.get('getUrl')

    response4 = get_image(get_url, cookies)
    assert response4.status_code == 200
    assert response4.headers.get('Content-Type') == 'binary/octet-stream'

    return cover_key


# applications
def create_pub_application(project_id, cover, description, display_name, game_name, cookies):
    req_body = {
        "cover": cover,
        "description": description,
        "displayName": display_name,
        "gameName": game_name
    }
    response = cloud_platform_service.create_pub_application(project_id, req_body, cookies)
    assert response.status_code == 200
    response = response.json()
    return response


def create_dev_application(org_id, project_id, app_name, app_description, package_id, pool_id, cookies):
    req_body = {
        "displayName": app_name,
        "description": app_description,
        "parameters": [],
        "merger": {
            "packageId": package_id,
            "executable": "merger exe",
            "poolId": pool_id,
            "packageName": "server_package_name",
            "parameters": []
        },
        "render": {
            "packageId": package_id,
            "executable": "render exe",
            "poolId": pool_id,
            "packageName": "merger_package_name",
            "parameters": []
        },
        "renderMode": 1,
        "enableRendering": True,
        "enableComputer": False,
        "renderingNodeNumber": 1,
        "computerNodeNumber": 1,
        "clusterRender": {
            "enabled": False,
            "numNodes": 1
        }
    }

    return cloud_platform_service.create_dev_application(org_id, project_id, req_body, cookies)


def update_dev_application(org_id, app_id, app_name, app_description, package_id, pool_id, cookies):
    req_body = {
        "displayName": app_name,
        "description": app_description,
        "parameters": [],
        "merger": {
            "packageId": package_id,
            "executable": "merger",
            "poolId": pool_id,
            "packageName": "server_package_name",
            "parameters": []
        },
        "render": {
            "packageId": package_id,
            "executable": "render exe",
            "poolId": pool_id,
            "packageName": "merger_package_name",
            "parameters": []
        },
        "renderMode": 1,
        "enableRendering": True,
        "enableComputer": False,
        "renderingNodeNumber": 1,
        "computerNodeNumber": 1,
        "clusterRender": {
            "enabled": False,
            "numNodes": 1
        }
    }

    return cloud_platform_service.update_application(org_id, app_id, req_body, cookies)


def delete_dev_application(org_id, app_id, cookies):
    return cloud_platform_service.delete_application(org_id, app_id, cookies)


def search_apps(org_id, project_id, app_name, page, page_size, cookies, env="pub"):
    search_response = cloud_platform_service.search_apps(org_id, project_id, app_name, page, page_size, cookies, env)
    assert search_response.status_code == 200
    response = search_response.json()
    return response


def get_application_by_id(org_id, app_id, cookies):
    return cloud_platform_service.get_application_by_id(org_id, app_id, cookies)


def plan_release(pub_app, release_des, release_version, pkg_id, pool_id, username, cookies):

    req_body = {
        "gameName": pub_app['gameName'],
        "displayName": pub_app['displayName'],
        "description": pub_app['description'],
        "pubDesc": release_des,
        "cover": pub_app['cover'],
        "referredConfigId": "",
        "version": release_version,
        "parameters": [],
        "merger": {
            "packageId": pkg_id,
            "executable": "exe_path",
            "poolId": pool_id,
            "packageName": "",
            "parameters": []
        },
        "enableRendering": False,
        "renderingNodeNumber": 1,
        "enableComputer": False,
        "computerNodeNumber": 1,
        "clusterRender": {
            "enabled": False,
            "numNodes": 1
        },
        "createdTime": pub_app['createdTime'],
        "updatedTime": pub_app['updatedTime'],
        "projectId": pub_app['projectId'],
        "orgId": pub_app['orgId'],
        "id": pub_app['id'],
        "status": "saved",
        "userId": username,
        "appRunStatus": "",
        "belongEnv": "pub",
        "configId": ""
    }

    return cloud_platform_service.plan_release(pub_app['id'], req_body, cookies)


def get_pub_app_releases(pub_app_id, cookies):
    return cloud_platform_service.get_pub_app_releases(pub_app_id, cookies)


def submit_pub_app_release_for_audit(release_id, cookies):
    return cloud_platform_service.submit_pub_app_release_for_audit(release_id, cookies)


def release_app(org_id, app_id, req_body, cookies):
    return cloud_platform_service.release_app(org_id, app_id, req_body, cookies)


def get_release_by_id(org_id, release_id, cookies):
    return cloud_platform_service.get_release_by_id(org_id, release_id, cookies)


def search_releases(org_id, project_id, page, page_size, cookies):
    return cloud_platform_service.search_releases(org_id, project_id, page, page_size, cookies)


def admin_start_audit_release(release_id, cookies):
    return cloud_platform_service.admin_start_audit_release(release_id, cookies)


def admin_pass_audit_release(release_id, cookies):
    return cloud_platform_service.admin_pass_audit_release(release_id, cookies)


def admin_get_reject_options(cookies):
    return cloud_platform_service.admin_get_reject_options(cookies)


def admin_reject_audit_release(release_id, reject_reason_id, reject_text, cookies):
    reject_body = {
        "rejectedReasonId": reject_reason_id,
        "rejectedRemark": reject_text
    }
    return cloud_platform_service.admin_reject_release(release_id, reject_body, cookies)

# def admin_audit_app(app_id, req_body, cookies):
#     return cloud_platform_service.admin_audit_app(app_id, req_body, cookies)


def admin_search_apps(app_name, status_list, page, page_size, cookies):
    return cloud_platform_service.admin_search_apps(app_name, status_list, page, page_size, cookies)


# running app
def search_running_apps(org_id, project_id, app_name, page, page_size, cookies):
    return cloud_platform_service.search_running_apps(org_id, project_id, app_name, page, page_size, cookies)


def get_running_app_by_id(org_id, run_id, cookies):
    return cloud_platform_service.get_running_app_by_id(org_id, run_id, cookies)


def get_running_app_log_by_id(org_id, uuid, cookies):
    return cloud_platform_service.get_running_app_log_by_id(org_id, uuid, cookies)


def get_running_app_log_download_address(org_id, uuid, filename, cookies):
    return cloud_platform_service.get_running_app_log_download_address(org_id, uuid, filename, cookies)


def start_game_server(req_body, cookies):
    return cloud_platform_service.start_game_server(req_body, cookies)


# resources
def admin_add_resources(req_body, cookies):
    logging.info("Do not add resources for now")
    return cloud_platform_service.admin_add_resources(req_body, cookies)


def get_pre_created_test_resource(cookies):
    resource_name, resource_type, spce_id = util.get_pre_created_resource()
    response = cloud_platform_service.admin_search_resources(resource_name, resource_type, 0, 0, cookies)
    assert type(response) is dict
    assert response.get("total") == 1
    assert len(response.get("list")) == 1
    resource = response.get("list")[0]

    resource['spec_id'] = spce_id
    return resource


def admin_get_resource_spec(cookies):
    return cloud_platform_service.admin_get_resource_spec(cookies)


def admin_get_resource_by_id(resource_id, cookies):
    return cloud_platform_service.admin_get_resource_by_id(resource_id, cookies)


def admin_search_resources(resource_name, resource_type, page, page_size, cookies):
    return cloud_platform_service.admin_search_resources(resource_name, resource_type, page, page_size, cookies)


def admin_update_resource(resource_id, req_body, cookies):
    return cloud_platform_service.admin_update_resource(resource_id, req_body, cookies)


def admin_update_organization_resource(org_id, req_body, cookies):
    return cloud_platform_service.admin_update_organization_resource(org_id, req_body, cookies)


def admin_search_organization_resources(org_name, page, page_size, cookies):
    return cloud_platform_service.admin_search_organization_resources(org_name, page, page_size, cookies)


def admin_get_organization_resource_by_id(org_id, cookies):
    return cloud_platform_service.admin_get_organization_resource_by_id(org_id, cookies)


def org_add_resource_pool(description, display_name, resource_id, size, type, cookies):
    req_body = {
        "displayName": display_name,
        "type": type,
        "size": size,
        "resId": resource_id,
        "description": description
    }

    return cloud_platform_service.org_add_resource_pool(req_body, cookies)


def org_update_resource_pool(description, display_name, resource_id, size, type, pool_id, cookies):
    req_body = {
        "displayName": display_name,
        "type": type,
        "size": size,
        "resId": resource_id,
        "description": description
    }
    return cloud_platform_service.org_update_resource_pool(req_body, pool_id, cookies)


def org_get_resource_pool_by_id(pool_id, cookies):
    return cloud_platform_service.org_get_resource_pool_by_id(pool_id, cookies)


def org_delete_resource_pool_by_id(pool_id, cookies):
    return cloud_platform_service.org_delete_resource_pool_by_id(pool_id, cookies)


def org_search_resource_pools(pool_name, pool_type, page, page_size, cookies):
    return cloud_platform_service.org_search_resource_pools(pool_name, pool_type, page, page_size, cookies)


def org_resource_pool_check(resource_id, size, type, cookies):
    req_body = {
        "poolId": "",
        "resId": resource_id,
        "size": size,
        "type": type
    }

    return cloud_platform_service.org_resource_pool_check(req_body, cookies)


def get_org_pool_select(cookies):
    return cloud_platform_service.get_org_pool_select(cookies)
