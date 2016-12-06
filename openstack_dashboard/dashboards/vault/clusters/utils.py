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
import traceback
from troveclient.v1 import client

import openstack_dashboard.dashboards.vault.conf
from openstack_dashboard.dashboards.vault.constant import QUERY_ROUTER_URI
from openstack_dashboard.dashboards.vault.conf import VAULT_DM_REST_URL
import logging
from django.utils.translation import ugettext_lazy as _

LOG = logging.getLogger(__name__)

class Flavor:
    def __init__(self, disk, ephemeral, ram, swap, vcpus):
        self.disk = disk
        self.ephemeral = ephemeral
        self.ram = ram
        self.swap = swap
        self.vcpus = vcpus

class Cluster:
    def __init__(self, id, tenant_mppdb_name, request_node_quantity, flavor, status):
        self.id = id
        self.tenant_mppdb_name = tenant_mppdb_name
        self.request_node_quantity = request_node_quantity
        self.flavor = flavor
        self.status = status

    def get_connection_string(self):
        # jdbc:vault://HOST/DATABASE/TENANT_MPPDB_ID
        return "jdbc:vault://%s/db_srvr/%d" % (QUERY_ROUTER_URI, self.id)

    def get_flavor_info(self):
        response_flavor = requests.get(VAULT_DM_REST_URL + '/v1.0/flavor/' + self.flavor)
        flavor = response_flavor.json()['flavor']
        return Flavor(disk=flavor['disk'], ephemeral=flavor['ephemeral'], ram=flavor['ram'], swap=flavor['swap'], vcpus=flavor['vcpus'])

    def get_status(self):
        if(self.status=='ACTIVE'):
            return 'ONLINE'
        else:
            return 'OFFLINE'

def getCluster(id):
    tenantmppdb = requests.get(VAULT_DM_REST_URL + '/v1.0/tenantmppdbs/' + id).json()['tenant_mppdb'][0]
    response_tenant_mppdb = requests.get(VAULT_DM_REST_URL + '/v1.0/tenantmppdbs/' + id)
    trove = client.Client('admin', 'admin', project_id='admin', auth_url=openstack_dashboard.dashboards.vault.conf.AUTH_URL)
    status = None

    for tenant_mppdb in response_tenant_mppdb.json()['tenant_mppdb']:
        response_mppdb = requests.get(
            VAULT_DM_REST_URL + '/v1.0/mppdbs/' + str(tenant_mppdb['tenant_mppdb_group_id']) + '/mppdb')

    for mppdbs in response_mppdb.json()['mppdbs']:
        instance = trove.clusters.get(mppdbs['mppdb_id'])
        status = instance.instances[0]['status']

    return Cluster(id=tenantmppdb['tenant_mppdb_id'], tenant_mppdb_name=tenantmppdb['tenant_mppdb_name'],
                   request_node_quantity=tenantmppdb['request_node_quantity'], flavor=tenantmppdb['flavor'],
                   status=status)


def getClusters(tenant_name):
    response_tenant = requests.get(VAULT_DM_REST_URL + '/v1.0/tenants/' + tenant_name)
    clusters = []

    for tenant in response_tenant.json()['tenant']:
        response_tenantmppdbs = requests.get(VAULT_DM_REST_URL + '/v1.0/tenantmppdbs/' + tenant['tenant_id'] + '/mppdb')
        tenantmppdbs = response_tenantmppdbs.json()['tenantMppdbs']

    for tenantmppdb in tenantmppdbs:
        clusters.append(Cluster(id=tenantmppdb['tenant_mppdb_id'], tenant_mppdb_name=tenantmppdb['tenant_mppdb_name'],
                                request_node_quantity=tenantmppdb['request_node_quantity'], flavor=tenantmppdb['flavor'], status=""))

    return clusters

def get_clusters_by_tenant_id(id):
    clusters = []

    response_tenantmppdbs = requests.get(VAULT_DM_REST_URL + '/v1.0/tenantmppdbs/' + id + '/mppdb')
    tenantmppdbs = response_tenantmppdbs.json()['tenantMppdbs']

    for tenantmppdb in tenantmppdbs:
        clusters.append(Cluster(id=tenantmppdb['tenant_mppdb_id'], tenant_mppdb_name=tenantmppdb['tenant_mppdb_name'],
                                request_node_quantity=tenantmppdb['request_node_quantity'], flavor=tenantmppdb['flavor'], status=""))

    return clusters

def addCluster(request, context):
    node_quantity = context.get('node_quantity')
    tenant_mppdb_name = context.get('tenant_mppdb_name')
    flavor = context.get('flavor')

    tenant_name = request.user.username
    response_tenant = requests.get(VAULT_DM_REST_URL + '/v1.0/tenants/' + tenant_name)

    for tenant in response_tenant.json()['tenant']:
        tenant_id = tenant['tenant_id']

    response = requests.post(VAULT_DM_REST_URL + '/v1.0/tenantmppdbs/' + tenant_id + '/mppdb',
                             data={'request_node_quantity': node_quantity, 'tenant_mppdb_name': tenant_mppdb_name,
                                   'flavor': flavor})


def deleteCluster(request, tenant_mppdb_id):
    try:
        response = requests.delete(VAULT_DM_REST_URL + '/v1.0/tenantmppdbs/' + str(tenant_mppdb_id) + '/mppdb')
    except:
        print "Exception inside utils.deleteMPPDB"
        print traceback.format_exc()
        requests.exceptions.handle(request, _('Unable to delete Parallel Database'))
        return False
