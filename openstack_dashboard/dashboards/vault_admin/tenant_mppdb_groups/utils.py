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
from openstack_dashboard.dashboards.vault.constant import REPLICATION_FACTOR,SLA_THRESHOLD
from openstack_dashboard.dashboards.vault.conf import VAULT_DM_REST_URL


class TenantMppdbGroup:
    def __init__(self, id, formation_time, node_quantity, group_size, service_level, tenant_mppdb_members, total_request_node_quantity, consolidation_effectiveness, MPPDBs):
        self.id = id
        self.formation_time = formation_time
        self.node_quantity = node_quantity
        self.group_size = group_size
        self.service_level = service_level
        self.tenant_mppdb_members = tenant_mppdb_members
        self.total_request_node_quantity = total_request_node_quantity
        self.MPPDBs = MPPDBs
        self.consolidation_effectiveness = consolidation_effectiveness
        self.sla_ok = False if self.service_level < SLA_THRESHOLD else True



def getTenantMppdbGroups():
    response = requests.get(VAULT_DM_REST_URL + '/v1.0/tenantmppdbgroups')
    tenant_mppdb_groups = []
    for tenant_mppdb_group in response.json()['tenant_mppdb_groups']:
        total_request_node_quantity = 0
        if tenant_mppdb_group['group_size']>0:
            service_level_url = VAULT_DM_REST_URL + '/v1.0/tenantmppdbgroups/' + str(tenant_mppdb_group['tenant_mppdb_group_id']) + '/servicelevel'

            service_level = requests.get(service_level_url).json()['tenant_mppdb_group_service_levels'][-1]['value']

            mppdb_list = []
            tenant_mppdb_members_list = 'Tenant '
            for tenant_mppdb in tenant_mppdb_group['tenant_mppdb_members_list']:
                tenant_mppdb_members_list += tenant_mppdb + ', '

                #Get the request node number of each tenant mppdb member
                tenant_mppdb = tenant_mppdb.replace('#','')
                tenant_mppdb_url = VAULT_DM_REST_URL + '/v1.0/tenantmppdbs/' + str(tenant_mppdb)
                request_node_quantity = requests.get(tenant_mppdb_url).json()['tenant_mppdb'][-1]['request_node_quantity']
                total_request_node_quantity = total_request_node_quantity + request_node_quantity

            tenant_mppdb_members_list = tenant_mppdb_members_list[:-2]

            #Calculating consolidation_effectiveness
            consolidation_effectiveness = (float(total_request_node_quantity) - float(tenant_mppdb_group['node_quantity']) * REPLICATION_FACTOR) / float(total_request_node_quantity) * 100
            if(consolidation_effectiveness<=0):
                consolidation_effectiveness = 0


            for mppdb in tenant_mppdb_group['mppdb_list']:
                mppdb_list.append(str(mppdb))
            tenant_mppdb_groups.append(TenantMppdbGroup(id=tenant_mppdb_group['tenant_mppdb_group_id'],
                                                        formation_time=tenant_mppdb_group['formation_time'],
                                                        node_quantity=tenant_mppdb_group['node_quantity'],
                                                        group_size=tenant_mppdb_group['group_size'],
                                                        service_level='{:.2%}'.format(service_level / float(100)),
                                                        tenant_mppdb_members=tenant_mppdb_members_list,
                                                        total_request_node_quantity=total_request_node_quantity,
                                                        consolidation_effectiveness=consolidation_effectiveness,
                                                        MPPDBs=mppdb_list))
    return tenant_mppdb_groups
