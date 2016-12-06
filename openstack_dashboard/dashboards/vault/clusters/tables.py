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

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from horizon import tables



from django.utils.translation import pgettext_lazy
from troveclient.v1 import client

import openstack_dashboard.dashboards.vault.conf
from openstack_dashboard.dashboards.vault.clusters import utils
from openstack_dashboard.dashboards.vault.conf import VAULT_DM_REST_URL
import requests

class ClusterFilterAction(tables.FilterAction):
    name = "clusterfilter"

class AddTableData(tables.LinkAction):
    name = "add"
    verbose_name = _("Request Parallel Database")
    url = "horizon:vault:clusters:add"
    classes = ("btn-launch", "ajax-modal")


class DeleteTableData(tables.DeleteAction):
    data_type_singular = _("Parallel Database")
    data_type_plural = _("Clusters")

    def delete(self, request, obj_id):
        utils.deleteCluster(request, obj_id)

class UpdateRow(tables.Row):
    ajax = True

    def get_data(self, request, tenant_mppdb_id):
        cluster = None
        response_tenant_mppdb = requests.get(VAULT_DM_REST_URL + '/v1.0/tenantmppdbs/' + tenant_mppdb_id)
        trove = get_trove_client()

        for tenant_mppdb in response_tenant_mppdb.json()['tenant_mppdb']:
            response_mppdb = requests.get(VAULT_DM_REST_URL + '/v1.0/mppdbs/' + str(tenant_mppdb['tenant_mppdb_group_id']) + '/mppdb')

            for mppdbs in response_mppdb.json()['mppdbs']:
                instance = trove.clusters.get(mppdbs['mppdb_id'])

                cluster = utils.Cluster(id=tenant_mppdb['tenant_mppdb_id'], tenant_mppdb_name=tenant_mppdb['tenant_mppdb_name'], request_node_quantity=tenant_mppdb['request_node_quantity'], flavor="", status=instance.instances[0]['status'])


        return cluster

def get_cluster_link(cluster):
    return reverse("horizon:vault:clusters:detail", args=[cluster.id])


def get_trove_client():
    """Return trove client."""
    trove = client.Client('admin', 'admin', project_id='admin', auth_url=openstack_dashboard.dashboards.vault.conf.AUTH_URL)
    return trove

class ClustersTable(tables.DataTable):

    STATUS_CHOICES = (
        ("ACTIVE", True),
        ("BLOCKED", True),
        ("BUILD", None),
        ("FAILED", False),
        ("REBOOT", None),
        ("RESIZE", None),
        ("BACKUP", None),
        ("SHUTDOWN", False),
        ("ERROR", False),
        ("RESTART_REQUIRED", None),
    )

    STATUS_DISPLAY_CHOICES = (
        ("ACTIVE", pgettext_lazy("Current status of a Database Instance",
                                 u"Active")),
        ("BLOCKED", pgettext_lazy("Current status of a Database Instance",
                                  u"Blocked")),
        ("BUILD", pgettext_lazy("Current status of a Database Instance",
                                u"Building")),
        ("FAILED", pgettext_lazy("Current status of a Database Instance",
                                 u"Failed")),
        ("REBOOT", pgettext_lazy("Current status of a Database Instance",
                                 u"Rebooting")),
        ("RESIZE", pgettext_lazy("Current status of a Database Instance",
                                 u"Resizing")),
        ("BACKUP", pgettext_lazy("Current status of a Database Instance",
                                 u"Backup")),
        ("SHUTDOWN", pgettext_lazy("Current status of a Database Instance",
                                   u"Shutdown")),
        ("ERROR", pgettext_lazy("Current status of a Database Instance",
                                u"Error")),
        ("RESTART_REQUIRED",
         pgettext_lazy("Current status of a Database Instance",
                       u"Restart Required")),
    )

    tenant_mppdb_name = tables.Column('tenant_mppdb_name', verbose_name=_("Tenant Name"), link=get_cluster_link)
    tenant_mppdb_id = tables.Column('id', verbose_name=_("Tenant ID"))
    request_node_quantity = tables.Column('request_node_quantity', verbose_name=_("Node Quantity"))
    status = tables.Column("status",verbose_name=_("Status"),status=True,status_choices=STATUS_CHOICES,display_choices=STATUS_DISPLAY_CHOICES)
    actions = tables.Column('actions', verbose_name=_("Actions"))

    class Meta:
        name = "vault"
        verbose_name = _("Clusters")
        status_columns = ["status"]
        table_actions = (AddTableData, ClusterFilterAction)
        row_actions = (DeleteTableData,)
        row_class = UpdateRow