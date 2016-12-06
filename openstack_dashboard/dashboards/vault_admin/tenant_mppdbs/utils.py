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


class TenantMppdb:
    def __init__(self, id, tenant_mppdb_name, tenant_mppdb_group_id, request_node_quantity):
        self.id = id
        self.tenant_mppdb_name = tenant_mppdb_name
        self.tenant_mppdb_group_id = tenant_mppdb_group_id
        self.request_node_quantity = request_node_quantity


def getTenantMppdbs(self):
    response = requests.get(VAULT_DM_REST_URL + '/v1.0/tenantmppdbs')
    tenant_mppdbs = []
    for tenant_mppdb in response.json()['tenant_mppdbs']:
        tenant_mppdbs.append(
            TenantMppdb(id=tenant_mppdb['tenant_mppdb_id'], tenant_mppdb_name=tenant_mppdb['tenant_mppdb_name'],
                        tenant_mppdb_group_id=tenant_mppdb['tenant_mppdb_group_id'],
                        request_node_quantity=tenant_mppdb['request_node_quantity']))
    return tenant_mppdbs
