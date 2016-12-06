# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import requests
from openstack_dashboard.dashboards.vault.conf import VAULT_DM_REST_URL
import logging

LOG = logging.getLogger(__name__)

class User:
    def __init__(self, id, user_name, tenant_mppdb_name):
        self.id = id
        self.user_name = user_name
        self.tenant_mppdb_name = tenant_mppdb_name


def getUsers(self):
    tenant_name = self.request.user.username
    response_tenant = requests.get(VAULT_DM_REST_URL + '/v1.0/tenants/' + tenant_name)
    for tenant in response_tenant.json()['tenant']:
        tenant_id = tenant['tenant_id']

    response = requests.get(VAULT_DM_REST_URL + '/v1.0/tenants/' + tenant_id + '/users')
    response_users = response.json()['users']
    if response_users == []:
        return []
    else:
        users = []
        for user in response_users:
            response_tenant_mppdb = requests.get(VAULT_DM_REST_URL + '/v1.0/tenantmppdbs/' + str(user['tenant_mppdb_id']))
            for tenant_mppdb in response_tenant_mppdb.json()['tenant_mppdb']:
                users.append(User(id=user['user_id'], user_name=user['user_name'],
                                  tenant_mppdb_name=tenant_mppdb['tenant_mppdb_name']))
        return users

def add_user(user_name, password, tenant_id, tenant_mppdb_id):
    response = requests.post(VAULT_DM_REST_URL + '/v1.0/tenants/' + tenant_id + '/users',
                             data={'user_name': user_name, 'password': password, 'tenant_mppdb_id': tenant_mppdb_id})
    if(response.status_code != 200):
        raise Exception("Can't create database user")

def deleteUser(self, request, id):
    try:
        LOG.warn(VAULT_DM_REST_URL + '/v1.0/users/' + id)
        response = requests.delete(VAULT_DM_REST_URL + '/v1.0/users/' + id)
    except:
        LOG.error("Cannot Delete User")
        # print "Exception inside utils.deleteUser"
        # print traceback.format_exc()
        # exceptions.handle(self.request, _('Unable to delete user'))
        return False
